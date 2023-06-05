---
title: "Chips 101 and Nvidia"
slug: chips-101-nvidia
layout: post
date: 2023-05-30
tags: []
summary: "Last week, Nvidia's stock exploded.... The AI arms race has heated up and is even getting the attention of normal people through stock prices (among other news), so I'm sure this won't be the last time I explain GPUs to someone without a computer science degree. I'm using this post as a chance to organize my *Chips 101* talking points."
---

{{< images/image src="chips.png" alt="Dall-E's take on \"chips\"" class="" caption="Dall-E's take on \"chips\"">}}


Last week, Nvidia's stock exploded.
They announced dramatically better earnings than predicted, and quickly became the [fifth most valuable publicly-traded US company](https://en.wikipedia.org/wiki/List_of_public_corporations_by_market_capitalization) (as of May 30).
It's one of the only ones in the top 10 that isn't a household name.

I was talking to a friend who doesn't work in tech about this, and trying to explain what exactly Nvidia does.
That very rapidly become a conversation more about CPUs, GPUs, and deep learning than about details of the particular company.

The AI arms race has heated up and is even getting the attention of normal people through stock prices (among other news), so I'm sure this won't be the last time I explain GPUs to someone without a computer science degree.
I'm using this post as a chance to organize my *Chips 101* talking points.

## What's a "Chip"?

Simple: a tiny piece of silicon [etched with lasers](https://en.wikipedia.org/wiki/Photolithography).

But why do we carve up little bits of silicon?
It's the best way to create a bunch of **logic gates**, the building blocks of computation.
Logic gates are basically circuits that take one or two logical (that is, True or False) inputs and produce an output [^1].
For example, an *OR* gate takes two inputs and returns True if either of them is True.
It's called "OR" because it returns True if the first input is True **or** the second input is True.

```
    Inputs          Result
---------------     ------
True  OR  True  -->  True
True  OR  False -->  True
False OR  True  -->  True
False OR  False -->  False
```

Similarly, there are *AND* gates, which return True only if both inputs are True.
And also *NOT* gates – which turn True into False and vice versa – and more.

Logic gates themselves are composed of one or several [**transistors**](https://en.wikipedia.org/wiki/Transistor), an even smaller electrical device.
We stuff billions of these on a piece of silicon the size of a fingernail.
Apple's entry-level laptops ship with the *M2* processor, which has [20 billion transistors](https://www.notebookcheck.net/Apple-M2-Processor-Benchmarks-and-Specs.632312.0.html).

Roughly speaking, a chip with more transistors can do things faster – and that translates to your computer being faster at browsing the web, opening applications, etc.
Beyond that, the details aren't too important[^2].

## From Logic Gates to Cores

When we build a chip, we end up with a single piece of silicon with an unimaginable number of logic gates[^3].
When we put it in a computer, we call it the **CPU** – the *central processing unit*.
It's the brain of the whole machine.
Practically speaking, you can think of "chip" and "CPU" as synonymous.

A CPU isn't a single brain though;
it tends to have its logic gates split up into multiple sections, each of which works somewhat independently.
We call each section a **core**.

The Apple M2 has eight cores, and that means that it can work on eight tasks at once [^4].
Not all cores on a chip have to be the same, and indeed, the M2 has [four "high performance" cores and four "high efficiency" cores](https://www.anandtech.com/show/17431/apple-announces-m2-soc-apple-silicon-updated-for-2022).

What all CPU cores have in common is that they're specifically tailored to the complicated tasks that computers do often.
We can instruct them to do things like load some data, modify it, and store it again all in one fell swoop.
While designing them this way makes them more complicated, it's a very practical optimization.

## Enter: GPUs

CPUs have worked like this for a very long time.
Back in the 1990s and early 2000s, they had fewer transistors and often only a single core.
But still, that core was optimized to do normal computer-y things – tricky, multi-part tasks.

Then the rise of video games exposed a big weakness in that approach.
Rendering graphics on a screen often involves doing some math to compute what color to show on every single pixel on the screen.
It's relatively simple math, but even on a 640x480 monitor in the 2000s, that would be over 300 million computations.
Say a CPU (executing one task at a time) could solve 1 million computations per second -- it would still take five minutes just to update the image on screen!

And so a different processing model arose: **GPUs**.
GPUs are *graphics processing units*, sometimes called "graphics cards"[^5].
GPUs represent a whole different paradigm from CPUs: instead of combining all those transistors into a few very advanced cores, they group them into hundreds or thousands of simpler cores.

Each of these cores are dramatically less complex than the cores of a CPU.
They can't do as many operations in a single step.
But instead they offer massive **parallelism**, the ability to do multiple tasks at once.
And in video games, the work of rendering each pixel can be done independently, which means that it can be split up across all these cores.
This is a dramatically better solution than CPUs for the problem at hand.

And here Nvidia comes into our story: it was one of the biggest GPU manufacturers and rose to prominence by building graphics cards for gamers.

## GPUs and Deep Learning

For years, PC gamers were the main consumers of GPUs.
With this reliable customer base, manufacturers kept improving the technology, allowing for high-fidelity gaming at higher resolutions (more pixels) and higher frame rates (more frequent re-renders).

But meanwhile, the machine learning community was adopting algorithms that just so happened to be well-suited to running on GPUs.
There were several, but the most relevant model is the **neural network**.

Building a neural network involves a lot of steps, but nothing more mathematically complicated than taking a derivative.
And for certain large neural networks, all the components of the network can be solved independently.
These features made neural nets perform vastly better on GPUs than on CPUs, and suddenly GPUs were coveted not just by gamers but also by professional research scientists and even by large companies like Meta and Google [^6].

Neural networks have come to dominate many domains of machine learning.
As far as I know, most computer vision tasks – like identifying or altering objects in photos and video – are done with [convolutional neural nets](https://en.wikipedia.org/wiki/Convolutional_neural_network).
"Large language models" (ChatGPT and its relatives) are actually [transformers](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)), a type of neural net.
Complex neural networks like these are sometimes called **deep learning**, because they have many layers and are thus "deep" networks.

Over the last decade, large tech companies have become obsessed with deep learning: almost every "artificial intelligence" application is built with huge neural networks, and they need countless GPUs to build those networks.

## Nvidia

Nvidia is one of the oldest GPU manufacturers; as of 2023 they've been in the business for 30 years.
They have a ton of expertise building this in-demand product, and they've also made some wise choices along the way.

As it pertains to deep learning, their best decision was the development and rollout of the [CUDA platform](https://en.wikipedia.org/wiki/CUDA), a programming utility that made it easier for software engineers to train neural networks on their GPUs.
That tool only worked on Nvidia's products, not their competitors', giving them an edge among ML scientists that they've never relinquished.

Some other companies have fabricated chips even more tailored to machine learning, such as Google's [Tensor Processing Units](https://en.wikipedia.org/wiki/Tensor_Processing_Unit), but GPUs remain hugely in-demand for building neural net architectures.
With the explosion in popularity of large language models, all kinds of companies are investing more in "AI".

You're likely to hear a lot more about Nvidia as long as AI remains culturally and economically important.
It has set itself up to be one of the big winners of this era.


[^1]: You might be wondering how exactly we pass True and False into a circuit. The answer: we send a high voltage current for True or a low voltage current for False, and those stand in for "logical values" throughout the whole system.
[^2]: Even if they were, my performance in my sophomore year Logic Design course would disqualify me from explaining them.
[^3]: More technically, we end up with a big piece of silicon called a [die](https://en.wikipedia.org/wiki/Die_(integrated_circuit)), which is then split into multiple identical chips. Interesting but not especially relevant here.
[^4]: Ignoring, for simplicity, the ability to run concurrent tasks on the same core with technologies like [hyperthreading](https://en.wikipedia.org/wiki/Hyper-threading).
[^5]: They're called "cards" because of their shape. Every GPU I've seen has been of similar dimensions to a VCR cassette, making it one of the bulkiest components of a computer. I don't know if the form factor was the same before 2010 but I assume it was.
[^6]: And for a while, also by another group: cryptocurrency miners. Thousands of simple cores is an ideal recipe for solving the puzzles at the center of crypto mining, and so at the height of crypto mania, miners were buying so many cards that manufacturers couldn't keep up. Every store was sold out and the only buying options were secondhand GPUs that were still priced above MSRP. This phenomenon was in full swing when I was building my own PC, and I spent over a year waiting to find a reasonably-priced graphics card for my new computer.