---
title: "Tech for Teaching"
slug: slides-with-jupyter
layout: post
date: 2023-04-21
tags:
- teaching
---

I taught a tutorial at PyCon a few days ago.
It went well, but what I want to discuss are some technical things I did that went well and (I think) made the presentation easier for students to follow.
 <!--more--> 
An overview:
- Create a repository with separate folders for the code that should be finished after each section of the talk.
- Produce diffs of those incremental versions and put them somewhere that attendees can reference
- Build slides with Jupyter and add custom styling by embedding a CSS file in the Reveal template
    - This was tricky enough that I'll punt it to a future blog post
    - Add custom styling by embedding a CSS file in the Reveal template
        - Add empty divs with special classes and use the next-sibling selector to style the next element
- Use GitHub Actions to build and host the slides online