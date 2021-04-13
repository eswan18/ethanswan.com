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

## Turning to Zillow

The easiest way to resolve some of this uncertainty is to systematically investigate apartments listings on a website like Zillow.
Many questions boil down to some variant of "What combination of amenities can I get, in neighborhood X, at price point Y?".
For me, air conditioning, in-unit laundry, a parking spot, and some outdoor space (a deck or patio) are at the top of the amenity list.
I want to know which of those I can get in an apartment within my budget, in each of the neighborhoods I'm considering.
And -- importantly -- the apartments *also* have to meet a general standard of quality and attractiveness that I'm never going to be able to define in a search query.

This is admittedly a hard problem to build a nice user interface around.
Zillow actually does a pretty good job: you can add filters to results using criteria like price range, neighborhood or geographic boundary, or set of amenities.

*But* it's not quite the ideal way to understand my apartment options, for a few reasons:

1. There's no easy way to keep track of which properties you've already seen. You can "heart" the ones you like, but units you've ruled out for one reason or another remain in the search results and on the interactive map. And since search result order seems to change, it's almost impossible to conduct a thorough, exhaustive review of all options.

2. It's hard to express your interrelated preferences. Zillow makes it easy to create a blanket filter ("rent must be below x"), but there's no way to define something more nuanced. Maybe I'm willing to pay an extra $200 a month if the apartment has parking -- sure, I can raise my maximum price *and* require the place have parking, but I can't require the latter as a *condition* for the former. With location, it can be even more complicated; yes, I would be willing to consider a place outside of the neighborhood I want, but only if it were perfect in every other way.

3. While it's not exactly a problem with the interface, the lack of a simple way to export data and save it means that you can't just build your own spreadsheet of apartments -- which would be a good answer to the first two issues. Maybe this lack of "data portability" is something that would irk only a programmer, but it's frustrating.

Fortunately, a dose of that same programmer sensibility can help solve all three issues.

## Web Scraping with Python

... is the title of [an excellent O'Reilly book](https://www.amazon.com/Web-Scraping-Python-Collecting-Modern/dp/1491985577) I finished recently.
It's also a solution to some of my frustrations with the Zillow website.

And if you came here looking for a technical article about Python, I promise you've found it at last.

Using the [requests](http://docs.python-requests.org) library, it's not hard to interact with the Zillow website (or most other sites) from Python.
The simplest way to do this is to send a "Get" request to `www.zillow.com` and save the content of its response.

```python
>>> import requests

>>> response = requests.get('https://www.zillow.com')
>>> page_content = response.content
```

Unfortunately, printing the response's content yields just a lot of HTML, which most humans aren't going to be able to understand very well.
And that's where the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library comes in -- it helps you parse HTML by searching for certain tags or attributes.

```python
>>> from bs4 import BeautifulSoup

>>> soup = BeautifulSoup(response.content, 'html.parser')
```

The resulting `soup` object supports a `.find` method that makes it fairly straightforward to look for certain things in the HTML code.
For example, this code prints out the first image on the page.

```python
>>> soup.find('img')
```
```
<img alt="Zillow" height="14" src="https://www.zillowstatic.com/static/logos/logo-65x14.png" width="65"/>
```

Of course, figuring out what elements of the page you want, and extracting information from those bits can be tricky.
And we don't even know what page we want to pull from yet!
Certainly the Zillow home page isn't going to automatically show Chicago apartments with in-unit laundry.
Finding the right URL (which we sometimes call an "endpoint") and determining how to parse it is 90% of the work, at least.

## Design and Planning

Before jumping right in, let's think about how things are going to need to be structured.
a) the components you need to build
b) how the components fit together

I'd be lying if I said I always spent enough time planning, but at least in this case I gave it some thought.

