---
title: "Tech Debt Is a Limited Metaphor"
subtitle: "It breaks down when you look too close"
date: 2025-06-17
slug: tech-debt-is-a-limited-metaphor
tags:
- tech
summary: "Long ago, doing things the fast way instead of the right way was nicknamed “technical debt” in the field of software development. However, analogies have limits."
---

Long ago[^citation-needed], doing things the *fast* way instead of the *right* way was nicknamed "technical debt" in the field of software development.
It's mortgaging the future for the sake of the present, which despite the typically-negative connotations of that framing, is sometimes a good idea.
The value of shipping a new feature or fixing a bug quickly often outweighs the long-term downsides of writing janky code that will be hard to work with later on.

This metaphor is used to an exhausting degree in many tech organizations, and for good reason:
it's very applicable.

Like real financial debt, technical debt results in paying back more than you initially borrowed, but over a longer time.
If you want to buy a house before you've saved up enough cash to afford it, you borrow money from the bank and agree to pay back slightly more over the following years.
With tech, your debt is denominated in time and energy, not in dollars, but the idea is much the same.
You get the asset (the feature, bug fix, or house) sooner than you would have if you paid for it in full.
But you'll spend the following months or years paying interest (expending time understanding confusing code or fixing new bugs).

And just as buying things on credit (like houses) can be the most efficient way to get what you want, building features through debt is often the best way for a business to succeed, since acquisition and retention of customers depends on the speed at which those features are available.

However, analogies have limits.
It seems like common ones end up stretched beyond the level at which they apply.
This has happened with tech debt.

The metaphor above implies that a single entity makes this decision and will bear the full weight of the costs and benefits, as a borrower would in the case of buying a house.
Sure, some borrowers haven't thought carefully enough, but they alone feel the consequences[^consequences].
But it's my experience in software engineering that a lot of disagreements between short-term and long-term focus aren't like this:
they reflect differing incentives, not a pure optimization of business value.

The trouble is that considering these cases as "technical debt" leads to incorrect conclusions, mainly that with enough discussion, everyone will agree on whether certain new tech debt is worth it.
Sometimes this is true; sometimes it isn't.

An easy example is genuine short-termism.
A sales team will have revenue targets, and they can lean on the engineering team to churn out half-baked features.
The net consequences might be clearly negative for the business, but current salespeople aren't necessarily going to be around to see the costs.
And even if they are, humans just have a natural tendency to prioritize the short term, from routine procrastination to our inability to stick with a diet.

The funniest case of this is when engineers themselves incur debt that isn't worth it *without being asked*, simply because it's easier to take shortcuts!
This happens all the time despite the irony that engineers are always the ones complaining about short-termism from other departments.
We're all mortals!

It's just good to keep this in mind when approaching conversations about "tech debt".
Sometimes old debt was incurred for silly reasons and never served a purpose.
Sometimes you'll be tempted to incur new debt even when it's actually bad for the business.
And – cover your ears, engineers – sometimes your ostensibly-pious desire to avoid creating new tech debt is *actually* because it would be unpleasant for you (or future you) in your day-to-day work, not because it's a bad idea for the business.

[^citation-needed]: Citation needed. I have no idea when this started.
[^consequences]: Of course, the bank is impacted by potential default - and in some extreme cases the whole financial system is - but we can ignore that here.