---
title: "The Tool Lifecycle Trap"
subtitle: Investing in speedups that don't become speed bumps
date: 2025-04-18
slug: tool-lifecycle-trap
# tags: []
summary: "Good tools save time and free users from repetitive tasks, but only if they're adopted (primarily) organically...."
---

Across all my jobs, internal tooling has always fascinated me.

In my first job, at 84.51˚, I saw some low-hanging fruit for automation and started developing an internal Python library side-of-desk.
Over the years, I switched teams a few times, that one Python package turned into several, and eventually toolbuilding became into my primary role there.

Everyone dabbled in DevOps here and there at ReviewTrackers, but I especially loved digging through the code for our deployment pipeline and test environment.
And when I got tired of using curl to interactively test new features in our API layer, I put together a little Python client library.

Capital One wasn't the kind of place that enabled experimental side projects very well, but it introduced me to some genuinely complex internal systems, many of which were mandatory for tasks like deployment and testing.
I spent a lot of time dealing with them and just as much thinking about how I'd have done things differently if I were in charge.

My view is that most of the time, investing in internal tools is a big win.
But not always.

**Good tools save time and free users from repetitive tasks, but only if they're adopted (primarily) organically.**
Mandating their use diminishes the incentive to create good software, leading to poor-quality tools that slow things down and add frustration.

## The Trap

I see a natural "tool lifecycle" that companies experience as they grow.

In the startup phase, a company is solving fresh problems every day, and shipping features is paramount for survival.
There's a lot of work to do but not much of it is duplicative.
At this stage, building internal tools just doesn't pencil out.

But as a small company matures, developers and data scientists start solving problems that look very similar to ones they've seen before.
There are some opportunities to manage duplicative work via internal tools, but it's hard for leaders to prioritize these, because the company is still shipping as fast as possible with a very small team.
Still, it's at this stage that smart companies begin to prioritize toolbuilding over less critical feature work; the gains are huge over the medium- and long-term.

As it grows, a successful company continues adding and enhancing tools that address repetitive tasks.
But as it adds employees, it expands its focus to also include *processes*: standard internal trainings and documentation.