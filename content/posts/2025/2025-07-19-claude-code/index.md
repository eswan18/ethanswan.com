---
title: "What I've Been Up To: Claude Code"
subtitle: It's pretty fun
date: 2025-07-19
slug: this-week-claude-code
tags:
- ai
# summary: "..."
---

This last week I visited Portland with some friends.
I had some tremendous coffee, good food, and interesting long runs (using some new shoes!).

But the main thing on my mind has been AI coding agents.
I've been using GitHub Copilot since its fairly early days and asking ChatGPT for coding advice/solutions since GPT 3 or 3.5.
But until late last week, I'd never used any of the "agentic" tools: Claude Code, Codex, Gemini CLI, etc.

Much has already been written about the relative merits of these tools, and others have experimented more thoroughly than I have.
I'll just say that Codex seemed to only operate at a surface level, while Claude has vastly exceeded my expectations with its ability to creatively solve problems much as a human would: investigating, proposing a solution, writing some code, testing it in the simplest possible way, and iterating.
I haven't even touched Gemini yet.

Still, I've seen enough to significantly revise my conception of what it is (or will be) to be a programmer.
I'm working in a small but tricky codebase: my [fitness](https://github.com/eswan18/fitness) app that pulls data from Strava and from a static CSV, spins up a backend api, and starts up React app with a dashboard for viewing the data from the api.
And I've implemented several features that I was dreading due to their trickiness (one involves time zones, of course) without really writing any code myself;
Claude has done everything, with my guidance.

Admittedly, I've had to do plenty of steering and correcting.
But it's taken way less time and thinking than it would have for me to do it myself.
And even during that time, I've been reading newsletters while Claude chugs away.

I assume these tools will only get better, or at least not worse.
So the feeling of bouncing between one task (e.g. reading newsletters) and directing my AI agent is probably going to become normal very quickly.

In the cases I've needed to get involved, it's usually some combination of:
- Claude not understanding how to run commands in my environment. E.g. it was trying to run `python` without prefacing it with `uv run`, so it wasn't able to access all the installed packages.
- Claude going down a route that I thought didn't make much sense architecturally. Admittedly that's my opinion, but it seems like Claude tries not to tear apart your whole codebase if possible. Sometimes you need to tell it to be a little more interventionist in order to avoid kludgy hacks, though.
- Claude not testing its work enough. I'm happy to burn more tokens in order to be sure my time zone logic is airtight, and I've told it to check more edge cases. Often, it's found bugs.
- A human being needed to inspect a visual artifact. In my case, my dashboard needs to look good to me, and I've had to steer Claude a lot in order to fix things that register to me as bad.

I haven't tried anything too complicated, but Claude did get seriously hung up on the complexities of time zone logic across a bunch of filters and aggregations.
In fairness, I'd get hung up too.

But for all the direction I've had to give, it's still been far more efficient than doing this myself.
And I suspect that as I get more understanding of where AI agents excel, I'll be able to define these tasks more clearly and get them done more quickly.

At organizations that permit these tools, I fully expect the job of software developer to shift toward something like a combination of architect and tech lead: designing and steering the work, and perhaps very infrequently swooping in to build some challenging corner of the functionality.