---
title: "The Tool Lifecycle Trap"
subtitle: Investing in speedups that don't become speed bumps
date: 2025-04-23
slug: tool-lifecycle-trap
summary: "Good tools save time and free users from repetitive tasks, but only if they're adopted (primarily) organically...."
---

Across all my jobs, internal tooling has always fascinated me.

In my first job, at 84.51˚, I saw some low-hanging fruit for automation and started developing an internal Python library side-of-desk.
Over the years, that one Python package turned into several. By the time I left, toolbuilding had become my primary role.

Everyone dabbled in DevOps here and there at ReviewTrackers, but I especially loved digging through the code for our deployment pipeline and test environment.
And when I got tired of using curl to interactively test new features in our API layer, I put together a little Python client library.

Capital One’s culture and bureaucracy made experimental side projects difficult, but it introduced me to some genuinely complex internal systems, many of which were mandatory for tasks like deployment and testing.
I spent a lot of time dealing with them and just as much thinking about how I'd have done things differently if I were in charge.

My view is that most of the time, investing in internal tools is a big win.
But not always.

**Good tools save time and free users from repetitive tasks, but only if they're adopted (primarily) organically.**
Mandating their use diminishes the incentive to create good software, leading to poor-quality tools that slow things down and add frustration.

## The Lifecycle

I've seen a natural "tool lifecycle" that companies experience as they grow.

In the startup phase, a company is solving fresh problems every day, and shipping features is paramount for survival.
There's a lot of work to do but not much of it is duplicative.
At this stage, building internal tools just doesn't pencil out as worthwhile.

But as a company matures, developers and data scientists start solving problems that look very similar to ones they've seen before.
There are clear opportunities to manage duplicative work via internal tools.
However, it's hard for leaders to prioritize these because the company is still shipping as fast as possible with a very small team.

Still, smart companies begin to prioritize toolbuilding over less critical feature work at this stage.
Good tools are hugely valuable over the medium- and long-term, often requiring just 2-5 engineers to build and saving 10-100x that headcount as the company grows.
Those developers can measure their success by how many other employees choose to use their tool;
as long as they build something useful, it's an easy sell to internal "customers".

As the organization grows more, it keeps adding and enhancing tools that address repetitive tasks.
Many organizations are then tempted to begin *mandating* the use of certain internal tools.
It makes sense: these tools can be used to enforce standardization across the enterprise, including methodology or regulatory requirements where applicable.

But my experience is that top-down mandates usually come back to bite the companies that use them.

## The Trap

Once tools are made mandatory, the tool development team no longer needs to target user experience:
its "customer base" is guaranteed by internal fiat.
Feature development continues, but with an emphasis on checking boxes rather than building things that users want to use.

**This leads to tools that *technically* work but are confusing, error-prone, underdocumented, and not generalizable to novel use cases[^enterprise-software]**.

Eventually, the hidden costs of these tools cause internal paralysis: building new products is slow and painful because it requires interacting with numerous flaky and difficult tools along the way.
Blame for this slowdown is hard to attribute.
Developers and data scientists complain about the internal tools, but those tools technically meet all the requirements set forth by leadership.
And even if some UX improvements are prioritized for them, it's hard to find a sustainable way to fix the underlying incentives problem, so this will happen again and again.

## Solutions

The key insight is that **user adoption is the most valuable metric** for internal tools, and mandates just remove your ability to track that indicator.

So mandate your standards, not your tools[^interfaces-implementation].

Want to be sure everyone uses a certain methodology?
Require teams *either* go through a thorough internal review *or* use the internal library that encodes the methodology.
If the tool is any good at all, users will opt for it.
But if they don't, that tool must be truly dysfunctional.

Have regulatory rules?
Mandate compliance, and make teams *prove it* unless they use your internal tools that handle compliance for them.
Again, they'll choose to just use the tools unless they're awful.

You can't rely on good product leadership to overcome this problem, although many organizations try to.
With external-facing features, product owners are motivated to understand users so they can drive sales (i.e. adoption) of the product.
But when the product is mandated, as it is in required internal tooling, there's no "ground truth" indicating whether it's any good -- adoption is guaranteed regardless and product owners have no incentive to search for UX issues.

By far the best measure of usefulness is elective adoption of the product.
Other metrics, like survey results, are weak proxies at best.

## One Caveat: Tools that aren't tools

What about project management tools like Jira?
There's no way to make them optional: teams either record their tasks there or don't.
And a lot of teams would prefer not to use them.

But that's because project management systems usually aren't "tools" in the sense I've used the word until now.
The purpose of project management systems, and similar software, is to enable *leadership* to oversee progress throughout the organization.

So yes, you can and probably should mandate them, along with any other systems that are in place for an organizational purpose beyond employee enablement.

[^enterprise-software]: This is reminiscent of enterprise software, where poor user experience despite fulfilling all the technical requirements is almost the norm, as anyone who's used a lot of it can attest.
The underlying issue with enterprise software is that the buyer makes their decision based on some kind of feature list, and the eventual users of the software never have any choice in the matter.
This means that user experience is almost completely absent from consideration when choosing a product -- just as it's usually absent from prioritization decisions when developing mandated internal tools.

[^interfaces-implementation]: This is an echo of the software engineering principle that emphasizes a focus on interfaces over implementation. Mandating the *what* (the specification of what should be delivered) is important, but mandating the *how* (the tools used, or the particulars of the implementation) needlessly limits developers.