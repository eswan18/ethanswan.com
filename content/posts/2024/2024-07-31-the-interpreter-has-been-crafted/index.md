---
title: "The Interpreter Has Been Crafted"
subtitle: "Just two short years later"
date: 2024-07-31
slug: the-interpreter-has-been-crafted
summary: "It took two years, but I finally finished building an interpreter."
---

Back in 2022, [I wrote](http://localhost:1313/feed/2022/06/07/crafting-interpreters/) about my progress through the book *Crafting Interpreters*.
It took two years, but I finally finished building an interpreter.

I'm not great at finishing projects like this.
Life always gets in the way, and I always have new ideas of things I want to work on.
But I got the push I needed by attending a workshop run by [Dave Beazley](http://www.dabeaz.com) in which we worked through the book together, in Rust.

I started picking up Rust in December 2022 through Advent of Code, and then used it again for AoC 2023.
It took some time, but I've embraced the role of guy-who-loves-Rust-and-will-tell-you-about it.
A chance to work on the interpreter book with a group of smart people using a language I like was too good to miss.

During the workshop week, I got only a little further than I had two years before.
Of course, this was a clean start, and the difficulty was higher -- writing Rust code requires a lot more care than writing Python.
This time I understood what I was doing much better than before, having grappled with the material several times at this point.
After the session ended, I finished up the interpreter on my own with some effort.

You can find the code [here](https://github.com/eswan18/loxrs) if you're interested.
I think it's in a working state.

## Slaying Dragons

Finishing the intepreter was a remarkable feeling.

As a new software developer (or anyone who writes code), intepreters are a form of magic.
You can't even begin to ponder them; you're too overwhelmed by the complexity of just getting code that works.

Over time, you start to appreciate the craftsmanship that must go into an application so complex.
Every programmer finds countless bugs in their own code.
But an interpreter needs to be absolutely rock solid in a way that few other applications do, while also executing an extremely tricky task, with infinite possible inputs[^infinite-inputs].

I think most people probably stop there.

But for some, including me, you just keep wondering how it all works.
I felt like I was spending my days standing on the shoulders of compiler developers.
A "tough" problem for me was when I struggled to express an idea clearly in a few lines of Python, but I always assumed that the interpreter would handle everything from there.
When you step back and think about it, the convenience of a high-level language is mind-boggling!

That led me to the next step: diving in.
For months, I read the Python core developer mailing list.
And at that point I started to understand certain pieces, but not how they fit together.
Then I found *Crafting Interpreters* and saw it as a way to learn more.

Without realizing it, I was moving to a new step: creation.
Building is one of the few ways to prove to yourself that you understand an idea.
The book led me to do that.
By doing it in a different language than the book used (Rust for me, Java for the book), I couldn't just copy code; I had to grapple with how and why it works.

Finally finishing the project was very gratifying.
As with so many things, interpreters can initially feel too complex for mere mortals.
But with some diligence, a mortal *can* grok them, and eventually even see them as just another project.
A big project, but ultimately a doable one.

## Epilogue

I didn't finish the whole book[^whole-book].
I finished the first half, in which you build a tree-walk interpreter.
The second half of the book covers a much more performant (and thus, realistic) implementation in C: a stack machine.

I've been reading the second half of the book without following along, and it's fascinating.
But for now, my desire to see through the magic is sated.
Maybe someday I'll have a practical need to build an interpreter, at which point I'll revisit some of these concepts.
For now though, I'll take my new learnings and move on to other projects.


[^infinite-inputs]: This is something about interpreters that I never fully appreciated until recently. The "input space" (all the possible inputs that could be seen) is infinite, and that's staggering. You literally *can't* test every case, or even some approximation of every important case.
[^whole-book]: I know, with all this talk of accomplishment you could be forgiven for assuming I had.