---
title: "Agentic Coding in 2025"
date: 2025-12-24
slug: agentic-coding-in-2025
tags:
- ai
summary: "2025 was the year of agentic coding for me. Perhaps the first of many. I tried out Claude Code in June and then subscribed to Cursor soon after. Since then, I've been using both frequently. I've got some thoughts."
---

2025 was the year of agentic coding for me. Perhaps the first of many. I tried out Claude Code in June and then subscribed to Cursor soon after. Since then, I've been using both frequently[^cursor].

I've got some thoughts.


## The State of the Tools

I've written [before](/feed/2025/07/19/this-week-claude-code/) about my early highs and lows (mostly highs though) with agentic coding tools. The agents have improved dramatically even in just six months: they usually interrogate complex codebases quickly and correctly, understand the right way to build/run projects, and test code when appropriate. They do much of this without being explicitly asked, much like a competent software developer would figure out how and when to do these tasks from documentation and knowing the conventions of the language.

There are still some notable weaknesses, but it can take a while to notice them. To me, the biggest ones a) lack of proactive refactoring and b) lack of "vision".

When I say agents aren't proactive, this is what I mean: they seem to be trained to make the smallest possible change to your code while still adhering to the basic standards of your codebase.
It's a good instinct; competent human developers also avoid massive, rippling changes.
But sometimes it's better to take a step back and simplify the code structure rather than just adding in a new module.
Yes, it's a judgment call, but this needs to be done at least *sometimes* or your code will become a disorganized pile of branching paths.
My experience is that right now, agents rarely spot these opportunities for simplification.

The lack of vision is closely related. Good code tends to follow a clear vision, with the "joints" (boundaries between disparate areas of the code) occurring at natural places such that it's possible to reason about the pieces independently. Bad code isn't like this: different people added different things at different times, and didn't have a clear sense of where those things fit relative to the core structure of the code.

Most code starts out good, with a design that encourages norms like "all REST resource definitions go in this folder".
Maybe it defines a set of common utilities that all new endpoints should use for authorization.
But over time this knowledge is lost.
New devs don't understand the vision and make their changes in ways that break the norms or duplicate functionality that already exists elsewhere.
Agents make these same mistakes, *unless* you tell them the vision in your prompts.
Increasingly, they can also figure out the vision if you specifically instruct them to look for it.
But without any direction, they will frequently fail to adhere to the spirit of the application's design.

It's no accident that both of these weaknesses are fundamentally a lack of context: either about the broader code or about the design.
AI isn't omnipotent.

But I suspect we'll find ways to mitigate them over time.
I'll talk more about that in a later section.

## Adoption

These tools are already moving beyond early adopters to regular software developers.
My colleagues and friends are using them to varying degrees, some having just barely experimented and a few every bit as deep as me.

So adoption is one spectrum.
Another is *skepticism*: how much you trust the tools to produce good work.
Together, these two axes help describe how different devs relate to the new agentic tools.

Most people I know fall into one of these buckets:
- **Vibecoders**: High adoption, low skepticism.
They love agentic tools and are constantly finding new ways to use them, but sometimes without consideration of how well-suited they are to the task.
Some devs are only vibecoders for a short time, right after esperiencing the high of some early successes, and then mellow out as they see the limitations.
Others are just very trusting, or (occasionally) so junior/unskilled that they aren't capable of understanding the ways that models go wrong.
- **Sweet spot**: High adoption, medium/high skepticism. They've found a lot of uses for agentic tools and employ them for many tasks, but avoid them in certain specific cases. They think that some things (e.g. reimplementing a common pattern) with AI barely even requires a human's lookover, but bespoke solutions in complex systems still need painstaking PR reviews. This is the bucket I place myself in.
- **Dubious**: Low/medium adoption, high skepticism. They've seen high-profile (and sometimes even publicized) mistakes from AI agents and think they're too risky to trust without great oversight for almost anything, and with that much extra effort the agents just aren't worthwhile. Still, many of these people are being pushed by their employer to use the tools, so they do... a little bit.
- **Artisans**: Low adoption, low/medium skepticism: They're not as troubled by AI errors as by the prospect of letting go of the craft of software development[^sympathy]. They don't like that it's much more challenging to understand codebases if you never actually write any of the code in them. Sometimes they've used AI to add a few features, and along the way they found they encountered the refactoring and vision problems discussed above, and they hate the prospect of letting all their code become spaghetti.

I understand where all these people are coming from, but market pressures are going to rapidly force everyone toward the sweet spot or full-on vibecoding[^vibecoding].
Other forces will push us toward higher adoption too: the tools will keep improving and new generations will be more capable with them.

What organizations need to avoid is a holy war.
Skeptics need to take this seriously as a disruptive technology, but enthusiasts also need to be patient.
As an enthusiast myself, I feel that the skeptics' critiques are often things you could say just as well about human developers: sloppy, mistake-prone, unaware of the bigger picture.
But agents do have flaws and sometimes fail in unexpected ways, so a little wariness is wise.

## 2026 and Beyond

**Being a software developer is even more about high-level design and goals**.
As we discussed above, agents need to be guided in refactoring and adhering to the project vision.
From my experience, the single most valuable skill you need for agentic development is a clear sense of *should*.
Agents are good at knowing how to do something, but not what ought be done.
The human has to decide that the system *should* use these frameworks, communicate with this standard, keep these things in this location, test these specific aspects, etc.

Increasingly, I think every good developer will be an engineering lead -- for a team of AI agents. You set expectations for them, check in periodically, and review their output.

**Prefer the most common languages and frameworks.**
This was always wise, but it's even more true with AI coding.
LLMs are much better at generating good code if that code looks like some existing code on the internet, and the chances of that are better if you stick to the standards.
But by naming this explicitly as a goal, agents themselves can adhere to it, and that should give you confidence to trust them with more decisions.

**Use static analysis aggressively.**
This too has always been good advice.
However, a complicated suite of static analysis tools can be annoying for developers.
Some developers will never even figure out how to use all of it, and they'll just push their code and see if it fails in CI.

But if you describe the quality checks in the repository Readme, an AI agent can execute them faithfully, and rapidly catch its own mistakes before going down rabbit holes.

**And last, you can't just stop thinking.**
Sometimes it really feels like you can, because you're watching hundreds of lines of working code appear on screen.
But that's an illusion, because you still need to be actively engaged with the system as a whole.

Once you lose your grasp on how the code works, you become much less able to make changes without degrading it.
I've several times had to roll back thousands of lines of agent-generated code when I realized I didn't understand what had been added in the last few commits.
Resisting the temptation to delegate to the agents completely will likely be the greatest challenge of this era of software development.

[^cursor]: I'm increasingly using more Cursor than Claude Code, though it pains me to say that. I really love how good a terminal interface the CC team has created. But ultimately, I don't feel like I understand its changes as well as I understand those from Cursor, because with Cursor I can see the entire surrounding context of the new lines, not just a snippet that fits in my terminal. Still, as an active holder of subscriptions to both, I hope Claude Code finds a way to win me back eventually!
[^sympathy]: Honestly, I completely sympathize. I sometimes have to remind myself that the job of a developer is to produce useful software quickly, not beautifully-crafted designs of code-art. Because being a craftsman is satisfying.
[^vibecoding]: At least with the capabilities of current LLMs, I don't think pure vibecoding is a good strategy for most organizations. But at the same time, if you're a startup with a product idea and almost no budget, the temptation to release a storm of AI agents instead of hiring more software developers will be too great, and I have a hard time even saying it's the wrong strategy
