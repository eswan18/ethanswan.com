---
title: "Implementing Semantic Search"
subtitle: "Easier than it sounds"
slug: semantic-search
layout: post
date: 2024-06-03
tags:
- now-and-here
summary: "Sometimes when you're searching for a digital record, you don't remember the precise wording of the original entry.... Semantic search attempts to compare the meanings of words and phrases instead of the characters."
---

Sometimes when you're searching for some text, you don't know or remember the precise wording of what you're looking for.

I might be searching in my task manager for the "Take out the trash" task.
But I type "garbage" instead of "trash", having forgotten the original verbiage.

In *lexical* (traditional) search algorithms, the words of the query are compared directly against the words of the records.
Searches for "take" or "trash" would match my task, as would phrases like "take out", "the trash", etc.
But searching for "garbage" would turn up nothing.

Lexical search can go a long way, especially with some simple refinements: making everything lowercase, normalizing characters[^diacritics], and stripping off suffixes[^stemming].
Another improvement is using a technique like [edit distance](https://en.wikipedia.org/wiki/Edit_distance#:~:text=In%20computational%20linguistics%20and%20computer,one%20string%20into%20the%20other.) to compute the similarity between terms, so that close-enough records will be found even if they're not a perfect match to the query (so a misspelling like "orangatan" would still be similar enough to "orangutan" because it differs by just one character).

Ultimately, though, lexical search relies on similarities present in the text itself, without any regard for the meaning of that text.

## Semantic Search

Semantic search is a more modern approach that attempts to compare the *meanings* of words and phrases instead of the characters.
Modern semantic search is largely built on *embeddings*, conversions of chunks of text into fixed-length lists of numbers.
The general term for these fixed-length lists is *vectors*; and embeddings are vectors derived from the semantic meaning of some text.

Embeddings sound complex, and to be fair the process of building them is pretty mathy, but actual embeddings vectors are very simple.
The specific values and length of the vectors are determined by which embeddings model you use, but below is a valid embedding[^valid-embedding].

```
[0.43 1.4 -0.33 -3.19]
```

A model would spit out a vector like this in response to any word or phrase it was given.
Maybe we fed it "take out the garbage" as input, and it responded with this embedding.

The values would be different for each word or phrase, but *semantically similar* bits of text will produce vectors with similar values in them.

```
take out the garbage -> [0.43 1.4 -0.33 -3.19]
take out the trash -> [0.41 0.81 -0.35 -3.05]
buy groceries -> [-0.11 0.53 -0.39 1.78]
hang up painting -> [-0.41 -0.18 1.83 0.03]
```

If we plot these embeddings in two dimensions[^plot-pca], we can see that the "take out the garbage" embedding is extremely similar to the "take out the trash" embedding.
But the vectors generated for our unrelated tasks are quite different.

{{< images/image src="2d_embeddings.png" alt="2D Embeddings" class="" caption="Our embeddings in a 2D space" >}}

So that's embeddings: numerical representations of the meaning ("semantics") of text.
They're not only useful for search but are also the foundation of large language models.

## Implementing Semantic Search

Once you have a way to turn text into embeddings, it's not much of a leap to figure out how to use them for search.
The basic idea is:

1. Compute embeddings for all the records in your data
2. Compute an embedding for the user's search query
3. Find the embeddings in your data that are most similar to the query embedding
4. Return the corresponding records for those embeddings

In practice, though, a search tool that works this way will be very slow.
Computing embeddings for every record in your data takes time, and potentially a *lot* of time if your data is large.
Ideally the embeddings would be precomputed so we could skip that at query time.

This is easy enough: every time a new record is created, generate an embedding and save it.
Then when records are deleted or updated, just delete/update the corresponding embedding.

Each query will still need to be converted to an embedding on-the-fly, but generating a single embedding is pretty fast.
Then the query embedding can be compared against all the precomputed embeddings in the database, and the most similar records retrieved.

## Nitty-gritty Details

I [added semantic search to my task manager project](https://github.com/eswan18/now-and-here/pull/16) over the weekend, and was surprised at how manageable a feature it was.
Below are some reflections on specific decisions I made.

### Vector Database

My app runs entirely locally and (as of now) doesn't require any kind of background process.
It's entirely contained in a CLI app.
That's been possible because I use sqlite, which runs as a library (without any daemon process) and stores its data in a file.

I wanted to keep it this way and avoid running a standalone database.
That meant storing my vectors in sqlite instead of a dedicated vector database like Pinecone.

However, there's a reason people prefer vector databases: working with vectors requires some functionality that most databases don't have, like highly-optimized vector similarity computation.
Embeddings contain hundreds or thousands of elements, so distance computation will be extremely slow if it's not implemented in the database or a low-level extension.

I was thrilled to discover [sqlite-vss](https://github.com/asg017/sqlite-vss), a vector search extension for sqlite that is even installable as a Python package!
Its features are limited, but it suits my purposes just fine.
The real test will come when I have more tasks and search performance starts to matter more.

A note for posterity: sqlite-vss is a great option, but the author has actually stopped maintaining it and put his effort toward a replacement extension called [sqlite-vec](https://github.com/asg017/sqlite-vec).
It's not ready yet (nor installable as a Python package yet), but if you try to build your own semantic search in the future I would recommend looking there first.

### Generating Embeddings

The selection of open source embeddings models is huge.
Superior models have a few qualities:
1. They understand how the context around a word influences its semantics. For example, *flute* is related to *clarinet* in one way: as musical instruments.
*Flute* is also related to *champagne*, though in a very different way.
Importantly, *clarinet* and *champagne* aren't themselves similar, even though they're both related to *flute*.
For our search use case, this matters: a query for *clarinet* should score well against a task like *practice the flute*.
But a query for *champagne* shouldn't.
2. They have enough fidelity to disambiguate similar words that are slightly different. Many synonyms carry subtly different connotations, such as "boss" and "manager". If a model is forced to condense semantics too much, or doesn't "understand" words well enough, it won't be able to tease this apart.
For my use case, this isn't as important, but it matters a lot for large language models.
Imagine if ChatGPT gave you the advice: "Don't let anyone manager you around."
Synonyms are rarely interchangeable in *all* situations.

All that to say: better embeddings models really are better.
Unfortunately, better models tend to have three major drawbacks:
- **The model file is much larger**, sometimes many gigabytes. App users will need to download the model locally, and minutes-long downloads are something I'd like to avoid.
- **The created embeddings are higher-dimensionality** (larger), making them more expensive to store and slower to query against.
- **Creating embeddings is slower**, which matters a lot if we want to rapidly create an embedding on-the-fly for user queries.

I did a little research on small, fast, and reasonably-good embeddings models and found some good advice.
But in the end I avoided all of them because of issues with models stored on the premier online model registry ([Hugging Face](https://huggingface.co)).

Pulling a model from Hugging Face and incorporating it into a project is a surprisingly clunky process[^clunky-huggingface].
Model files are buried in collections of code files, and they can't be run without installing a huge set of Python dependencies including things like numpy and pytorch that are slow to download.

I stumbled upon an alternative solution, [fastembed](https://github.com/qdrant/fastembed), described as "Fast, Accurate, Lightweight Python library to make State of the Art Embedding".
The docs were a little out-of-date, but I got it working and it's exactly what I need.
The best thing is that it can be installed as a Python package, just like sqlite-vec.
Being able to manage these dependencies through my package manager (Poetry) kept complexity from spiraling out of control with this addition, I feared might happen with this feature.

## The Code

You can poke around with [Now and Here](https://github.com/eswan18/now-and-here) or look specifically at the [pull request](https://github.com/eswan18/now-and-here/pull/16) where I implemented this.

{{< images/image src="nh-search.gif" alt="Now and Here Search" class="w-full sm:max-w-none" caption="Semantic Search in Now and Here" >}}

[^diacritics]: ... to remove diacritics or standardize characters than can be represented in multiple forms, which is common in Unicode.
[^stemming]: This is called "stemming" and can help with converting plural words to their singular form so that a search for "penguins" will still match "penguin". The related process of using a mapping of words to their base form (e.g. "better" -> "good") is called lemmatization, though I'm not sure how common it is in search algorithms.
[^valid-embedding]: It's *valid*, yeah, but I just made it up. Practical embeddings models create vectors of hundreds or thousands of values, which would not be useful for an example. Still, there's nothing wrong with a low-dimensional embedding; it's just lower fidelity.
[^plot-pca]: I used [principal component analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) to reduce these 4D vectors down to 2D so they'd be interpretable on a 2D graph.
[^clunky-huggingface]: This was a big surprise to me. Everything I read about language models points you to use models from Huggingface, but then actually downloading and implementing those models requires jumping through hoops. I think HF intends that you use the models via their Python library, but that means installing a bunch of enormous dependencies, and I don't want to embed anything extra in an application that really just needs a single model. The whole workflow seems to be designed for Jupyter Notebooks users and not application developers, perhaps understandably.