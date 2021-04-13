---
layout: post
date: 2021-04-10
categories:
- python
title: "Apartment Hunting with Python"
preview_image: "/images/apartment_score_distributions.png"
---

I recently crossed the 9-month mark as a Chicago resident.
The time has come for a big decision: renew my lease, or make the move to a new apartment?
<!--more-->

I really like my current home.
Two bedrooms, a back porch, a garage, and more grounded outlets than even a tech nerd like me could want.
It's in Little Italy, which is not a popular choice for Chicago young professionals, but is comfortable and has a decent set of restaurants.
I suspect that a similar unit in a more "hip" neighborhood might be out of my price range.
And my real office (not my extra bedroom, which has been serving in that capacity since I moved here) is a 10-minute bike ride away.
The north side, a potential relocation option, would bring with it a commute at least twice as long.

On the other hand, my primary motivation in moving to a big city was exploration and experience.
I wanted to get to know Chicago, particularly its neighborhoods.
Moving would offer me a change of location, unlocking many new walkable or bikable destinations.
Additionally, none of my friends live near my current apartment; most live in various parts of the northern neighborhoods, while I live due west of the Loop (the downtown area of Chicago).
Seeing most friends requires a 15+ minute drive or 30+ minute train ride.

On the *other* other hand, I've never lived in my neighborhood during "normal" times, so I'm hardly in a position to render a judgment on it.
I've recently discovered some frisbee and basketball groups that meet nearby, and I've been known to play pickup sports 3+ times a week if the option exists.
Finding groups here that I like and that don't require a long commute is a big point in favor of my current home.

As you can see, I'm torn.
There are pros and cons.
Part of the trouble with decisions about moving is the uncertainty: yes, you tend to have a pretty good sense of how much you like your current domestic situation, but it's hard to know how it compares to the great unknown of apartments you *don't* live in.

## Searching for Promising Listings

The easiest way to resolve some of this uncertainty is to systematically investigate apartments listings on a website like Zillow.
Many questions boil down to some variant of "What combination of amenities can I get, in neighborhood X, at price point Y?".
For me, in-unit laundry, a parking spot, and some outdoor space (a deck or patio) are top of the amenity list.

This is a hard problem, admittedly, to build a nice user interface around.
Zillow actually does a pretty good job: you can view what's available in a given neighborhood within a certain price range, and even restrict results to those with certain amenities.

*But* it's not quite the ideal way to understand my apartment options, for a few reasons:

1. There's no easy way to keep track of which properties you've already seen. You can "heart" the ones you like, but units you've ruled out for one reason or another remain in the search results and on the interactive map. And since search result order seems to change, it's almost impossible to conduct a thorough, exhaustive review of all options.

2. It's hard to express your interrelated preferences. Zillow makes it easy to create a blanket filter ("rent must be below x"), but there's no way to define something more nuanced. Maybe I'm willing to pay an extra $200 a month if the apartment has parking -- sure, I can raise my maximum price *and* require the place have parking, but I can't require the latter as a *condition* for the former. With location, it can be even more complicated; yes, I would be willing to consider a place outside of the neighborhood I want, but only if it were perfect in every other way.

3. There's no simple way to export data and save it. You can "save" individual properties, but really Zillow just adds them to a list that you can find later in your browser. This lack of "data portability" is definitely the kind of thing that irks a programmer but no one else.

Fortunately, that same programmer sensibility can help solve all three issues.

## Web Scraping with Python

... is the title of [an excellent O'Reilly book](https://www.amazon.com/Web-Scraping-Python-Collecting-Modern/dp/1491985577) I finished recently.
It's also a solution to some of my frustrations with apartment hunting.
