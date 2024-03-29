---
layout: post
date: 2022-05-10
tags:
- python
title: "Is PyScript a Big Deal?"
slug: pyscript
thumbnail-img: "https://pyscript.net/assets/images/pyscript-sticker-black.svg"
excerpt: "I went to PyCon a few weeks ago and while there, saw Peter Wang's keynote on a new project called PyScript. I think that's going to have a significant impact on the Python world, though maybe not in the way you'd first expect."
---

I went to PyCon a few weeks ago and while there, saw Peter Wang's keynote on a new project called [PyScript](https://pyscript.net).
PyScript is, essentially, a set of tools for running Python code in the browser – potentially even user-submitted code.
I think that's going to have a significant impact on the Python world, though maybe not in the way you'd first expect.

<!-- more -->

## Some Background

For years now, various groups have been working on finding a way to "run" Python in the browser.
The most successful effort I'm aware of is [Pyodide](https://pyodide.org/en/stable/), a version of the Python interpreter compiled to WebAssembly.

WebAssembly -- often abbreviated *wasm*, pronounced like WAH-zuhm -- is a set of low-level instructions  supported by all major browsers.
The name "WebAssembly" is a reference to traditional assembly code, which is a set of "instructions" that are executable on a given computer architecture (likely Intel x86 or ARM on the device you're reading this with).
Different CPU manufacturers support different instructions, so assembly code is specific to a particular platform.
You might be familiar with compilers for languages like C and Java, which are basically tools to convert code you've written into assembly (and sometimes past assembly, to machine code, but that's a different topic).

Native compilers have a hard job in that they need to generate the appropriate assembly code for whatever platform they're on.
That platform-dependence also means that the resulting executable file isn't portable to other devices with different architectures.
If you were to compile a C program on an M1 ARM Mac, you couldn't copy and run it on an Intel machine.

In contrast to traditional assembly code, WebAssembly is extremely portable: it can run on any computer with a browser that supports the standard, which at this point is basically everywhere (as far as I know).
And since WebAssembly instructions can run anywhere, if you have a reliable way to convert some *other* code into wasm, you can now run that code anywhere as well.
In the case of Pyodide, the Python program itself has been rewritten (well, compiled to) WebAssembly – giving us the ability to run Python in the browser on any device[^1].

PyScript looks to be a set of components atop Pyodide that make it simple to embed Python code within HTML, the source of web pages.
Using these tools, a developer could write Python as part of a website and have it execute on the viewers' computers.
Better still, users could themselves run code as part of the website, but it would run entirely on their own machine – making it snappy, and relieving developers from the need to provide server resources for every user.
If you've ever used Jupyter Notebooks/Lab, you could imagine something similar except that there is no background "server", which you may currently have to spin up manually or see launch in a console in the background when you open Jupyter.
Instead, all the code would be running in your browser itself.

## Why Can't We Run Python Everywhere Without a Special Framework?

You might, correctly, think that we've already basically solved the problem of getting Python and similar languages running on all platforms.
You can download Python for Mac, for Windows, for both ARM and Intel.
There are iOS apps for writing Python on mobile ([Pythonista](https://omz-software.com/pythonista/index.html), [Pyto](https://pyto.app)) and presumably some for Android as well though I'm less familiar with that platform.
Other popular languages offer a similar level of portability.

But in all the traditional ways we run Python, we have to install the Python program itself first.
On mobile that's done with apps, but on desktop you still need to download Python via a package manager, with Anaconda, through pyenv, or from the Python website.
And that's an issue because you can never assume other people will have Python installed, and you certainly can't expect them to have a particular version and collection of libraries.
Even in past workplaces I've had problems sharing simple Python scripts because others didn't have a way to run them.

This is where browser-based Python comes in.
We can rely on *everyone* having the tools to run Python code if it's executed this way, and that unlocks a lot of possibilities.
One that I mentioned above is a version of Jupyter that doesn't require any kind of background Python process.
This actually exists, in the [JupyterLite](https://jupyterlite.readthedocs.io/en/latest/) project.
JupyterLite was built on Pyodide directly, not PyScript, proving that this sort of thing was possible already.
But PyScript is a step closer to making it *easy*, not just possible.

## What Else Is This Good For?

JupyterLite is a great idea.
In Python classes I teach, I don't want beginners to have to figure out the whole Python installation process on their own, so I typically recommend they use [Binder](https://mybinder.org), a hosted Jupyter notebook solution.
But this has serious downsides, like the latency (which sometimes causes autocomplete to fail) and the ephemerality of the session (which means students lose their work unexpectedly when the session shuts down).
I'm considering switching to JupyterLite, since it still doesn't require any installation, but would be responsive and permanent.

But there are other places we could use Python in the browser.
One that I've been thinking about recently is in "live" slideshows.
I maintain a [small library](https://premark.readthedocs.io/en/latest/) for building HTML slideshows out of markdown files, mostly for my use in teaching courses.
I'd love to embed executable code in the slides for students to run themselves, but I don't want to set up some kind of Python server in the cloud to run that code for them.
I'm hoping to add PyScript integration once it's more mature (see my thoughts in the next section) to make this vision possible.

In general, teaching applications are very promising.
Teachers generally don't have huge budgets or the time to set up remote Python executors in a data center, but for most classes, the resources available on each student's laptop should be more than enough to run the relevant code.
Bringing that code execution *to* the student without requiring an elaborate setup process first should enable educators to build a more hands-on curriculum, and that benefits everyone.

In his conference talk, Peter Wang also brought up PyScript's potential applications in machine learning.
ML as a field focuses a lot on "reproducibility", the idea that I should be able to recreate your model or analysis on my own computer.
Right now, containers seem to be the favored solution to that problem, as they guarantee much stronger consistency of platform, software, and libraries across devices.
However, they're complex to learn and slow to work with, relative to just running code natively.

Will Python in the browser represent an improvement in this area?
Honestly I'm not so sure.
It's possible that confining Python to the browser's execution engine will add limitations that might be a problem for serious ML projects.
For example, does PyScript have access to the GPU – a requirement for most deep learning workflows?
But more importantly, if Docker (or a competing option) gets easier and/or faster, I think that containers would remain the preferred solution.
They have a big head start, and they offer more flexibility in customizing the operating system-level package dependencies that you might want for your modeling work.
That said, having a simpler solution wouldn't hurt and might be so much nicer that it wins out anyway.


## My Time with PyScript

I spent a couple of hours toying with PyScript last weekend.
It's much more raw than I'd expected.
That's no slight to the project maintainers; they've left warnings all over the place about how very beta this whole thing is.
But I was disappointed when I found some consistent bugs and discovered that the existing components offer limited customizability (for example, I couldn't find a way to automatically clear previous output upon rerunning a chunk of code).

I don't think I'll be able to incorporate PyScript into my slide-generator for a while yet, which is a disappointing since I had a fun use case in mind.
Still, it's exciting, and if I really put my mind to it (and accepted writing a lot of CSS and JavaScript to smooth over the rough edges), I could probably get things working with the current version.
We're not in the era of PyScript just yet but we're rounding the corner and starting to see the promise.

[^1]: With some limitations – browsers have lots and lots of rules about security that limit your access to files, etc, on the local computer.
