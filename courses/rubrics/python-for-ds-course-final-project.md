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
table td{
  border-top: 1px solid lightgray;
}
</style>

#### Points Necessary by Team Size
For an individual worker (team of 1), a 100% grade requires 25 earned points.
Every additional team member increases the required points by 4;
for example, a team of 3 total members has 2 extra participants, and so must earn 33 (=25 + 2\*4) points for a 100% grade.

Team Size    | Pts for 100%             | ... for 90% | ... for 80%
-------------|--------------------------|-------------|-------------
1            | 25                       | 22.5        | 20
2            | 29                       | 26.5        | 23.5
3            | 33                       | 30          | 26.5
4            | 37                       | 33.5        | 30

<br>

#### Earning Points

##### Data Acquisition

Points | Task
-------|-----
**2** | Acquire a dataset from the internet
**1** | For **each** dataset acquired and used beyond the first (max 3 additional)
**2** | Create a dataset yourself to work with other data you found online; e.g. a mapping of state abbreviations to state names.

##### Data Wrangling

Points | Task
-------|-----
**4** | Use at least one join
**3** | Melt and/or reshape your data

##### Modeling

Points | Task
-------|-----
**1** | For **every** linear model trained and used in your project
**2** | For **every** nonlinear model trained and used in your project
**0.5**| For **every** statistical metric (mean, median, mode) included in your final deliverable(s)
**2** | For **each** plot included in your final deliverable(s)

##### Meta

Points | Task
-------|-----
**10**| Version control your code using a public GitHub repository (easy points -- this makes it infinitely easier for me to grade)
**Up to 5** | Points at the instructor's discretion for particularly impressive projects

##### Stretch Goals (topics not included in the course lectures)

Points | Task
-------|-----
**4** | Pull data from a web-based API
**6** | Scrape data from a website
**3** | Create a web dashboard using [Dash](https://dash.plot.ly)
**5** | Train and use a neural network
