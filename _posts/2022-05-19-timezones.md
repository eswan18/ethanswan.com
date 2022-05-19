---
title: Timezones
subtitle: 24+ Places (and Times) to Lose Your Mind
date: 2022-05-19
---

Probably once a year, I end up back in the same discussion about timezones.
I don't like timezones and based on the frequency of this conversation, apparently I bring that up a lot.

## The Usual Griping

Programmers' hatred for timezones is a bit of a meme at this point (I just googled "xkcd timezones" with absolute confidence there would be a comic, and of course [I was right](https://xkcd.com/1883/)). 
When you think about it, it's not surprising that computer systems don't play nice with different times across the world.
If I build a retail website, the weekend sales should begin Saturday morning and end Sunday evening *your* time, even if it happens to mean that's not the weekend where I am.
As developers know, things get even worse once you're doing development using systems that are in a different timezone.
You read logs to find out what time something broke and eventually realize you've been forgetting to subtract five hours to adjust for the timezone the server is in.

UTC (basically Greenwich Mean Time for nerds) helps with this. Sorta.
Most computer systems store everything in UTC and just convert to the local timezone when displaying the time to humans.
Problem solved!
Well no, not really, because you often need to write that logic to display that time as part of your application, along with logic to handle times submitted by the user.

There are also ambiguities all over the place.
If someone tries to see all the products they viewed on January 1st, should we determine that based on their current timezone?
Or the timezone they were in when they looked at the products?
What if they were in one timezone for part of January 1st and then another later in the day, and looked at products in both?
Should all of those products be returned?

## Some More Original Gripes

The thing is, if timezones were just a problem for developers, that would be no different from any number of other industry-specific annoyances.
If I talk to anyone new about their job for more than 20 minutes, I find out about some kind of routine frustration I'd never considered.

But timezones aren't like that!
They drive all of us crazy in tiny ways.
Every time we have to schedule a call with a friend across the country or across the globe and try to remember the hour offset, and whether to add or subtract.
Checking the sports schedule online and being unsure if the time was localized -- does the game start at 2:30 eastern or 2:30 *my time*?

A lot of this sounds easy: my West Coast friends are two hours behind, how hard is that?
And yet I've messed it up so often, because hearing and processing times is something we do mostly without much mental attention.
I don't think it's just me, either; most people in office jobs are having more remote, cross-timezone meetings.
More importantly, as video calling has gotten better, we can have more communication with people who don't live near us -- and in these situations we don't have the benefit of an Outlook calendar handling our scheduling and normalizing our meetings times.

## They're Not Real

I mean, yes, obviously they're not real.
Unless you're concerned about the effects of relativity, there is no sense in which different people on the earth are experiencing different times.
What they *are* experiencing is different sun positions.

And that's ostensibly why we have timezones.
So that you know (roughly) where the sun was in the sky when I tell you I went for a bike ride at 4pm.
Yeah, that intentionally makes it sound dumb.
But it is dumb.

## Enter Absolute vs Relative

If somebody asked me which direction California is from here, I'd probably say West.
I certainly *wouldn't* say left, or right, or down.
Even if I was facing North, and you were facing North, I still wouldn't tell you that California was left.
Go Left, Young Man -- it just doesn't have the same ring.
In situations where your current position isn't especially relevant, we want to use *absolute* directions rather than relative ones.

However, if we were looking out from a balcony on a street below, I'd almost surely explain things with left, right, forward, backward.
I wouldn't tell someone their liver was on the North side of their body no matter which direction they were facing at the time.

One notable thing about relative directions is that they're less precise than absolute ones.
We use notation like WNW, but wouldn't say left-forward-left.
We also have lines of latitude and longitude, the most absolute measure of location, for which there is no relative counterpart.

As you may have guessed, I think this is very similar to how we should think about times.


