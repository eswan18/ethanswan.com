---
title: Timezones
subtitle: 24+ Places (and Times) to Lose Your Mind
date: 2022-06-01
---

Probably once a year, I end up back in the same discussion about timezones.
I don't like timezones and apparently I bring that up a lot.

## The Usual Griping

Programmers' hatred for timezones is a bit of a meme.
(I just googled "xkcd timezones" with absolute confidence there would be a comic, and of course [I was right](https://xkcd.com/1883/).) 

Computer systems don't play nice with different times across the world.
If I run a retail website, "weekend" sales should begin Saturday morning and end Sunday evening *your* time, even if it happens to mean that's not the weekend where I am.
But that's not easy because the computer that serves the website probably isn't in your timezone.
In their work, developers often have to interact with systems that are running in a different timezone, meaning they have to remember to add/subtract the right number of hours whenever cross-referencing events that affected both systems (for example, when reading logs).

UTC (Greenwich Mean Time for nerds) helps with this. Sorta.
Most computer systems store everything in UTC and just convert to the local timezone when displaying the time to humans.
Problem solved!
Well no, not really, implementing that logic is actually part of your job as a developer.

Sometimes other developers forget (or don't bother) to add that feature.
Sometimes -- as a user -- you're not sure if you're seeing a "localized" time or a UTC time or the time in the timezone where the website creator lives ... something that happened to me recently when viewing a schedule for a conference I was attending.

There are also ambiguities all over the place.
If an ecommerce customer asks to see all the products they viewed on January 1st, should we determine that based on their current timezone?
Or the timezone they were in when they looked at the products?
What if they were in one timezone for part of January 1st and then another later in the day, and looked at products in both?
Should all of those products be returned?

## Some More Original Gripes

The thing is, if timezones were just a problem for developers, that would be no different from any number of other industry-specific annoyances.
Talk to anyone new about their job for more 20 minutes and they're likely to complain about some frustration you've never heard of before.

But timezones aren't like that!

As the world gets more and more connected, they're increasingly responsible for daily frustrations.
Every time we have to schedule a call with a friend across the country or across the globe and try to remember the hour offset, and whether to add or subtract.
It gets worse if you're traveling and temporarily in a different timezone.
Am I now an extra hour behind my parents' time or closer to it?

A lot of this sounds easy: my West Coast friends are two hours behind, how hard is that?
And yet I've messed it up so often, because hearing and processing times is something we often have to do within the flow of conversation.
I don't think it's just me, either; most people in office jobs are having more remote, cross-timezone meetings.
More importantly, as video calling has gotten better, we can have more communication with people who don't live near us -- and in these situations we don't have the benefit of an Outlook calendar handling our scheduling and normalizing our meetings times.

One instance of localization that makes me laugh is in TV schedules.
"Airing at 9/8 central" is not uncommon to see on commercials.
It's funny because there's no situation where it's clearer that **there's only one absolute time** and localizing it for various audiences just adds complexity.

## They're Not Real

I mean, yes, obviously they're not real.
Unless you're concerned about the effects of relativity, there is no sense in which different people on the earth are experiencing different times.
What they're experiencing is different *sun positions*.

And that's ostensibly why we have timezones.
When the sphere of communication was your town or city, the simplest thing to do was to calibrate clocks based on the noon position of the sun.
It actually made things easier, since you could set your timepiece based only on the sky.
And there were no situations where you needed to coordinate exact times with people outside your town let alone outside what we'd now consider your "time zone".

But this was always just a shortcut.
One town in Alaska could have decided that clocks should show 7:00pm when the sun was at its peak, and that wouldn't have caused any issues as long as everyone in the town synchronized their clocks.
What's important is that everyone involved in scheduling keeps the same time, and for much of human history there was no scheduling beyond your own region.

That shortcut breaks down spectacularly when the whole world is in communication for meetings, social calls, deliveries, watching live events, etc.
The idea that every little community could basically "make up" its own time system is obviously untenable, but we still have 24ish separate chunks of humanity keeping their own personal times for reasons that -- to me -- seem like basically the inertia of history.

## Absolute vs Relative

Let's take a quick detour into physical positions and directions.

If somebody asked me which direction California is from here, I'd probably say West.
I certainly *wouldn't* say left, or right, or down.
Even if I was facing North, and you were facing North, I still wouldn't tell you that California was to our left.
*Go Left, Young Man* -- it just doesn't have the same ring.

In situations where your current position isn't especially relevant, we want to use *absolute* directions rather than relative ones.

However, if we were looking out from a balcony on a street below, I'd almost certainly describe things with left, right, forward, backward.
I wouldn't tell someone their liver was on the North side of their body no matter which direction they were facing at the time.

One notable thing about relative directions is that they're less precise than absolute ones.
We use notation like WNW, but wouldn't say left-forward-left[^1].

You can probably see where I'm going with this.

## A Practical Idea That Will Never Happen

Here's the pitch: express precise moments in time using UTC and only UTC.
What time does the Super Bowl start?
What time should I call you to chat?
What time do you want to meet at the park?

Critics will ask: but how will I understand the context of a given time for the person I'm talking to?
If they told me they got pancakes at 3am UTC, is that breakfast for dinner or breakfast for breakfast?
Is it the start of the day or the end of the day?

This question actually hides an (incorrect) assumption: that times must reflect sun positions.
What they're actually asking is: *how do I know what the sun position was for an event outside my region?*
And the answer is that we already have a complete, if less precise, vocabulary for this:
- noon
- midnight
- sunrise
- sunset
- morning
- afternoon
- evening
- night

Because of how we localize time, we think of "noon" and "12pm" as synonyms.
But they shouldn't be; they just happen to co-occur under the current system.
Noon is the time in the current region when the sun is at its highest point; 12pm is a specific moment in time that exists independent of where the speaker is.

Sun position words are a bit like relative directions, in that they don't usually require as much precision and that they're relative to the speaker.
I can tell people that I fell off my bike on a *morning* bike ride and they'll understand that I was in the first half of my day.

There are very few situations where information about both sun position and precise moment are relevant -- but in those cases, it's still easy to include both a sun position word and a UTC time.
*Want to do a videocall at 8:30? That will be evening for me and I think it's around noon for you.*

Yeah, I'm sure most people hate it.
For example, it feels really unnatural that "8:30 is around noon for you".
I'm not living my life in expectation of the day we all switch to UTC.

That said, in all my arguments about this, I don't think I've ever encountered a really compelling case that the current system is superior to this one in any way but familiarity.
I think the idea that "sun position words" don't need to be as precise as times doesn't seem obvious until you listen to yourself in conversation and notice that most references to time could already be replaced by "late morning", "after midnight", etc., without loss of meaning.

Most people reading have already concluded that I'm an irredeemable moron, so I'll just stir the pot a bit more as I wrap up. Roast me for these takes at your leisure:
1. Analog clocks are a relic that exist purely because of historical limitations of (electro)mechanical technology, and we shouldn't waste the next generation's brainspace on learning to read them.
2. 24-hour time is so clearly superior to looping over the same times twice a day that it doesn't even merit a blog post.

And with that, it's 12:30 UTC -- breakfast time. Gotta go.

[^1]: Some might point out that the *most* absolute system we have for navigating Earth is latitude and longitude. You're correct, it just doesn't fit the metaphor as well so I left it out.
