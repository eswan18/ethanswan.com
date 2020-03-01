---
layout: page
title: Final Project Rubric
---
### for [Python for Data Science Course](/courses/pages/python-for-ds-course)
<br>
{% comment %}
Super hack! I need to style [only] this particulary table but it's generated from a markdown file. This approach is stylistically terrible for a variety of reasons -- but it works.
{% endcomment %}
<style>
table th {
  font-size: 0.8em;
}
table td {
  border-top: 1px solid lightgray;
  font-size: 0.8em;
}
h5 {
  margin-top: 1em;
}
</style>

#### Points Necessary by Team Size
For an individual worker (team of 1), a 100% grade requires 34 earned points.
For a team of two, a 100% grade requires 42 points.

Team Size    | Pts for 100%             | ... for 90% | ... for 80%
-------------|--------------------------|-------------|-------------
1            | 34                       | 31          | 27.5
2            | 42                       | 38          | 34

<br>

#### Earning Points

##### Data Acquisition

Points | Max | Task
:-----:|:---:|------
**2**  |  2  | Acquire a dataset from the internet
**1**  |  3  | For **each** dataset acquired and used beyond the first
**2**  |  2  | Create a dataset yourself to work with other data you found online; e.g. a mapping of state abbreviations to state names.

##### Data Wrangling

Points | Max | Task
:-----:|:---:|------
**4**  |  4  | Use at least one join
**3**  |  3  | Group by, melt, or reshape your data
**1**  |  2  | `apply` a function to your data.

##### Modeling

Points | Max | Task
:-----:|:---:|------
**2**  |  6  | For each linear model trained and used in your project
**3**  |  9  | For each nonlinear model trained and used in your project
**0.5**|  3  | For each statistical metric (mean, median, mode) included in your final deliverable(s)
**1**  |  6  | For **each** plot included in your final deliverable(s)

##### Meta

   Points  | Max | Task
:---------:|:---:|------
   **6**   |  6  | Version control your code using a public GitHub repository (easy points -- this makes it infinitely easier for me to grade). If you have two team members, **both people must have a commit recorded in the Git history** to get these points.
  **0.5**  |  3  | For each additional Git commit beyond the first.
**Up to 5**|  5  |  Points at the instructor's discretion for particularly impressive projects

##### Stretch Goals (topics not included in the course lectures)

Points | Task
:-----:|-----
 **3** | Pull data from a web-based API (I recommend the [Requests library](https://requests.readthedocs.io/en/master/#))
 **6** | Scrape data from a website using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and/or [Scrapy](https://scrapy.org).
 **7** | Create a web dashboard using [Dash](https://dash.plot.ly).
 **5** | Correctly train and make predictions using a neural network (I recommend [Keras](https://scrapy.org)).
