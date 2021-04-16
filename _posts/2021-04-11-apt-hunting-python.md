---
layout: post
date: 2021-04-10
categories:
- python
title: "Apartment Hunting with Python"
preview_image: "/images/posts/apartment_score_distributions.png"
---

I recently crossed the 9-month mark as a Chicago resident.
The time has come for a big decision: renew my lease, or make the move to a new apartment?
<!--more-->

I really like my current home.
Two bedrooms, a back porch, a garage, and more grounded outlets than even a tech nerd like me could want.
It's in Little Italy, which is not a popular choice for Chicago young professionals, but is comfortable and has a decent set of restaurants.
I suspect that a similar unit in a more "hip" neighborhood might be out of my price range.
And my real office (not my extra bedroom, which has been serving in that capacity since I moved here) is a 10-minute bike ride away.
The north side, home of many of those hip neighborhoods, would bring with it a commute at least twice as long.

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
I'm not going to explain every aspect of the scraper I built; it's a lot of code and makes use of some intermediate-level features of Python itself, like type hints and packaging.
But I'll walk through some of the interesting bits and try to keep the discussion at a level such that newcomers to web scraping should leave with a better understanding of how it works and how to get started.
The only expected knowledge for the reader, from here on out, is basic Python.

And if you want to peruse the code yourself, you can find it [here](https://github.com/eswan18/zillow_scraper).

## The Basics of "Scraping"

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

The resulting `soup` object supports a `.find` method that makes it fairly straightforward to look for certain things in the HTML.
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

## The URL

Scraping websites meant for humans can be a pain, but a bright side is that we can use our human brain to find shortcuts.
Programmatically enter a search on the Zillow homepage seems likely to be hard; we'd have to get the page, parse through it to find the searchbar, enter "Chicago" as our location, locate the amenities checklist (to select things like washer/dryer), and then submit that search.
A lot of effort would go into that.

But, a far more elegant approach is to just conduct the search ourselves and save the URL of the results page.
Then, as long as our search includes any apartment that could possibly meet our criteria, we can collect them all and do our filters later in the process.

My Zillow search returned a URL that looked like this.
```
https://www.zillow.com/chicago-il/rentals/?searchQueryState=%7B%22pagination%22%3A%20%7B%7D%2C%20%22mapBounds%22%3A%20%7B%22west%22%3A%20-88.09607811914063%2C%20%22east%22%3A%20-87.36823388085938%2C%20%22south%22%3A%2041.217142667058575%2C%20%22north%22%3A%2042.444992337648856%7D%2C%20%22regionSelection%22%3A%20%5B%7B%22regionId%22%3A%2017426%2C%20%22regionType%22%3A%206%7D%5D%2C%20%22isMapVisible%22%3A%20false%2C%20%22filterState%22%3A%20%7B%22fsba%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22fsbo%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22nc%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22fore%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22cmsn%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22auc%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22pmf%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22pf%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22fr%22%3A%20%7B%22value%22%3A%20true%7D%2C%20%22ah%22%3A%20%7B%22value%22%3A%20true%7D%2C%20%22mf%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22manu%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22land%22%3A%20%7B%22value%22%3A%20false%7D%2C%20%22beds%22%3A%20%7B%22min%22%3A%202%7D%2C%20%22mp%22%3A%20%7B%22max%22%3A%203000%7D%2C%20%22price%22%3A%20%7B%22max%22%3A%20890941%7D%2C%20%22lau%22%3A%20%7B%22value%22%3A%20true%7D%2C%20%22doz%22%3A%20%7B%22value%22%3A%20%227%22%7D%7D%2C%20%22isListVisible%22%3A%20true%7D
```

Yikes.

However, if you scan that string, you'll see some recognizable words like "mapBounds", "regionID", "value", and "false".
In fact, all of these fall after the `?searchQueryState=` part of the URL.
Mappings like this (`x=y`) after a question mark in a URL are called *parameters*, and typically indicate that the server is customizing the page you receieve based on those values.
So my guess was that my whole search -- price, amenities, location -- was encoded in this string somehow, and passed as "searchQueryState" in this URL.

After some googling, I discovered the `unquote` function in `urllib`...

```python
from urllib.parse import unquote
unquote('https://www.zillow.com/chicago-il/rentals/?searchQueryState=%7B%22pagination%22%3A%20%7B%7D%2C%20%22mapBounds%22%3A%20%7B%22...')
```
```
> 'https://www.zillow.com/chicago-il/rentals//?searchQueryState={"pagination": {}, "mapBounds": {"west": -88.09607811914063, "east": -87.36823388085938, "south": 41.217142667058575, "north": 42.444992337648856}, "regionSelection": [{"regionId": 17426, "regionType": 6}], "isMapVisible": false, "filterState": {"fsba": {"value": false}, "fsbo": {"value": false}, "nc": {"value": false}, "fore": {"value": false}, "cmsn": {"value": false}, "auc": {"value": false}, "pmf": {"value": false}, "pf": {"value": false}, "fr": {"value": true}, "ah": {"value": true}, "mf": {"value": false}, "manu": {"value": false}, "land": {"value": false}, "beds": {"min": 2}, "mp": {"max": 3000}, "price": {"max": 890941}, "lau": {"value": true}, "doz": {"value": "7"}}, "isListVisible": true}'
```

Our URL is actually hiding a nested structure that represents our search query!
That's pretty cool.

Now I don't know exactly what each parameter means in this case, but some are easy: `"doz"` is days on Zillow, which I required to be 7 or fewer.
`"beds": {"min": 2}` indicates that I specified 2+ bedrooms.
The best part is that now we can store the search as part of our Python code and construct the URL on the fly; we could even tweak our search parameters by just updating their value in the Python code.
```python
from urllib.parse import quote as url_quote
import json
import requests

CHI_URL = "https://www.zillow.com/chicago-il/rentals/"
query_state = {
    "pagination": {},
    "mapBounds": {
        "west": -88.09607811914063,
        "east": -87.36823388085938,
        "south": 41.217142667058575,
        "north": 42.444992337648856,
    },
    "regionSelection": [{"regionId": 17426, "regionType": 6}],
    "isMapVisible": False,
    "filterState": {
        "fsba": {"value": False},
        "fsbo": {"value": False},
        "nc": {"value": False},
        "fore": {"value": False},
        "cmsn": {"value": False},
        "auc": {"value": False},
        "pmf": {"value": False},
        "pf": {"value": False},
        "fr": {"value": True},
        "ah": {"value": True},
        "mf": {"value": False},
        "manu": {"value": False},
        "land": {"value": False},
        # Here begin the params I understand: beds, price, laundry, days on Zillow.
        "beds": {"min": 2},
        "mp": {"max": 3000},
        "price": {"max": 890941},
        "lau": {"value": True},
        "doz": {"value": "7"},
    },
    "isListVisible": True,
}
# Turn the dictionary into a URL-safe string.
formatted_q_state = url_quote(json.dumps(query_state))
# Combine that string with the base URL for Chicago apartments on Zillow.
final_url = f"{CHI_URL}/?searchQueryState={formatted_q_state}"

# Fetch the page.
response = requests.get(final_url)
```

The real code is [here](https://github.com/eswan18/zillow_scraper/blob/15f981ab81f65595f6c6a1e21e9eba48272684c3/zillow-scraper/scrape/zillow.py).
It also has to deal with complications like [believable browser headers](https://github.com/eswan18/zillow_scraper/blob/15f981ab81f65595f6c6a1e21e9eba48272684c3/zillow-scraper/scrape/zillow.py#L9-L15), fetching [multiple pages of results](https://github.com/eswan18/zillow_scraper/blob/15f981ab81f65595f6c6a1e21e9eba48272684c3/zillow-scraper/scrape/zillow.py#L57-L58), and [maintaining cookies in a "session"](https://github.com/eswan18/zillow_scraper/blob/15f981ab81f65595f6c6a1e21e9eba48272684c3/zillow-scraper/scrape/__main__.py#L130) across all of those page requests.
But if you're just here for the basics, those are rabbit holes you can easily skip for now.

## Parsing Search Results

So we know the URL that returns the properties we're intersted in, we know how to fetch pages as HTML, and we know (in principle) that we can parse those pages using BeautifulSoup.
How do we actually do it?

Well, the bad news is that there's a lot of tedious clicking around that goes into it.
To start, I typically go to the page in my browser and right click on bits of text that I want my scraper to be able to find.
The "Inspect Element" option brings up the page HTML in a separate pane and highlights what part of that code defines the element in question.
In this case, I focused on parts of the page that contained information on price, rooms (beds/baths), and square footage.

![Inspecting Zillow Elements](/images/posts/zillow-inspect-element.png)

Here, you can see that I've found the HTML code corresponding to the info for the apartment on the right.
```html
<div class="list-card-info">...</div>
```
The `...` indicates that there is more content between the opening and closing `div` tags, but it's omitted here.

As enterprising web scrapers, we're well on our way to getting the info we want.
It's likely that all the search result properties are formatted similarly, so if we search the page for `div` elements that are of class `list-card-info`, we could potentially extract all the text inside and have basic attributes on each apartment.
We could print all the text inside each div with that class, using BeautifulSoup, like so:
```python
for div in page.find("div", class_="list-card-info"):
    print(div.text)
```

The [actual code](https://github.com/eswan18/zillow_scraper/blob/15f981ab81f65595f6c6a1e21e9eba48272684c3/zillow-scraper/scrape/__main__.py#L35-L81) is quite a bit longer; I went deeper than the `list-card-info` and looked for more HTML elements within it, in order to sort out what text was about bedrooms vs price vs square footage (and used some regexes for that purpose as well).
But at a basic level, a lot of scraping is just about finding the element you want and extracting the text inside of it.

## Design and Planning


 ... got request headers from here: https://medium.com/dev-genius/scraping-zillow-with-python-and-beautifulsoup-bbc7e581c218
