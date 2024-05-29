---
title: "Building a Locally-hosted Todo App"
subtitle: "A practical tool using a practical tech stack"
slug: building-a-todo-app
layout: post
date: 2024-04-06
tags:
- content
- now-and-here
summary: "My life is held together with the Todoist app ... but it's just not a good fit for work in the corporate world. And that led me to a practical side project."
---

My life is held together with the [Todoist](https://todoist.com) app:
every task I need to do, from watering my plants tomorrow to renewing my passport in five years, is there.
I've been using it for almost eight years now and have completed 14,241 tasks in that time – almost five a day.
As life has gotten busier, I've become more and more diligent about tracking absolutely everything.

I'm very loyal to Todoist and have few complaints, but it's just not a good fit for work in the corporate world.
Not in terms of features - it would still be more than adequate for personal task management - but because big companies don't like you storing "sensitive" data in a cloud service.
Todoist, like almost every popular task manager, stores your task data on remote servers.
Keeping the data on a server ensures durability and allows for syncing across multiple devices, but also constitutes data exfiltration from the perspective of a corporate bureaucracy.

And that led me to a practical side project[^practical-side-project]: a locally-hosted task manager that supports the most important features of Todoist.
For the last month I've been incrementally building out a little application called *Now and Here*[^now-and-here-name].

What follows is some discussion of how I architected and built it.

If you want to check out *Now and Here* yourself, see the [GitHub repo](https://github.com/eswan18/now-and-here).
You can also install it on your own system if you have pipx, using `pipx install git+https://github.com/eswan18/now-and-here`.
It's pretty lightly-documented at the moment but I plan to improve that.

## Initial Decisions

Implementation language was the easiest decision.
I know Python inside and out, especially application development and packaging, and it's a great ecosystem for building things quickly.
It was the clear choice.

Things got trickier after that.
I wanted to get something working quickly but also envisioned the possibility of using this application for years.
That led me to prioritize a strictly-decoupled architecture, so that I could scrap and rebuild pieces of the app in isolation as needed after first building "minimum viable product"
Get a working prototype out the door, then iteratively replace the pieces.

There were basically two components to build: the user interface and the data store[^2-components].

## Data Store

Many of my past projects have been sunk by the burden of complex architecture that I didn't really need when getting started.
Knowing my tendencies toward overengineering, I made very different decisions in this case.

For a data store, I needed something stored locally, and I didn't want to run any kind of background process like a database application – that would have made installation difficult for users.
Thus, SQLite seemed like a great choice: it's basically a file on disk that can be treated like a relational database, and I've heard of it performing well for most simple uses cases.

On the other hand, a relational database and its enforcement of strict tabular schemas would make iteration slow.
I'd have to use a SQL migration tool like Alembic and update the database itself every time I wanted to add, rename, or retype a column.
I expected to be doing this often especially at the beginning.

So I chose a path that a younger me would have laughed at: making SQLite into a document database.
I just smushed all the data for each task/project into a json column.
I first did a little bit of research into nonrelational SQLite alternatives but found nothing except some people mentioning that they'd tried this json-in-SQLite approach and it had worked perfectly well.

So in the spirit of pragmatism, I went with it.
Using pydantic, it's easy to convert tasks and projects into JSON and back again within the application.
And as I've updated the fields on these models, I've never had to change any table definitions in the database[^update-models].

To make data stores easy to switch in and out, I created a [`Datastore`](https://github.com/eswan18/now-and-here/blob/f670cadd79ec2a2dc7906bafc84ec1c6c6bfce69/now_and_here/datastore/datastore.py) interface class in Python.
One concrete implementation of this class is the [`UnstructuredSQLiteStore`](https://github.com/eswan18/now-and-here/blob/f670cadd79ec2a2dc7906bafc84ec1c6c6bfce69/now_and_here/datastore/sqlite_store/unstructed_sqlite_store.py), but if I choose to use a new data store, I can just build a new class around it as long as I implement the expected methods: things like `save_task`, `checkoff_task`, `get_tasks`.

It all sounds disconcertingly similar to Java design patterns, but the nice thing about Python is that it's not Java.

One less-than-ideal aspect of this architecture is that it's not clearly separated from [application models](https://github.com/eswan18/now-and-here/tree/f670cadd79ec2a2dc7906bafc84ec1c6c6bfce69/now_and_here/models) and the logic that lives with them.
For example, when a user checks off a task, the code has to check if the task has a repeat interval – and if so, it needs to figure out the next instance of the task and create it.
Some of that code lives with the models, but it has to be invoked from either the data store or the front end, and I thought it was ultimately cleaner to do it from the data store.

## User Interface

To start, a command line interface seemed like the right way to interact with the app.
I could build out commands incrementally and spend minimal time designing a UI.
A decent CLI could support every relevant action, though it would probably be an awkward way to view and update tasks – a fine tradeoff for the MVP.

I've used [Click](https://click.palletsprojects.com/en/8.1.x/) in the past to build CLIs, but after some research, I decided to use [Typer](https://typer.tiangolo.com) this time.
It's a bit more modern, taking advantage of type hints to automatically annotate and validate inputs where it can.

Building out the CLI was pretty straightforward.
I settled on a syntax of `nh <noun> <verb>`, so listing tasks is done with `nh task list` and deleting a project is `nh project delete <project-id>`.
This format has the advantage of mapping very nicely to the application models and data store layer – almost every data store method corresponds one-to-one with a CLI command (e.g. `list_tasks()` is `nh task list`).
And with this format, the model name (`task`, `project`) is the first subcommand, so the [code file](https://github.com/eswan18/now-and-here/blob/f670cadd79ec2a2dc7906bafc84ec1c6c6bfce69/now_and_here/cli_app/task.py) for the `nh task` subcommand holds all the code related to the `Task` model.

A more sentence-like grammar like `nh add task` would have been nice for users, but would have forced me to break up model code across every subcommand (`nh add`, `nh delete`, `nh update`, etc. would each own behavior related to the `Task` model).
For the CLI – an interface necessarily meant for technical users – I prioritized code organization over small readability advantages.

## Iterating

I've already started to build a new UI, a basic web interface.
It's been interesting to figure out how to bundle a web application into a Python package, particularly because I want to be able to use modern web tools like [Tailwind CSS](https://tailwindcss.com).
That's a big topic and better suited to a different post.

What I want to mention here about building a fresh UI is that it's validated my decoupled architecture approach.
Tying the web interface into the data store has been pretty seamless and required almost no duplicated code.
Good design pays off!

[^practical-side-project]: This is almost without question the *most* practical side project I've done, by virtue of having any practical value at all.
[^now-and-here-name]: Hopefully the wordplay is obvious, but to explain: I wanted a memorable phrase that was also unusual enough that it hadn't been taken on registries like the Python package index, which was doable by inverting an existing common phrase. "Here" is a reference to the app being locally-hosted, and "now" is a (stretched) allusion to task management (things due right now). An unexpected advantage is that `nh` – the invocation of the command line interface – is a very comfortable two-letter combination to type.
[^2-components]: Of course, there's backend logic as well (how to handle repeating tasks, for instance) but surprisingly there isn't too much of this (yet) and I felt comfortable building it into the application's datastore code.
[^update-models]: Though unfortunately, I've sometimes had to manually fix records in the database to conform to the application's new expectations. For example, when I changed the format of how task's parent projects were stored, I had to fix all the now-malformed entries as they were causing the app to crash at runtime. You can take schema enforcement out of the database but you can't avoid schema enforcement at some level, since your application can't perform any useful business logic without some assumptions as to the shape and type of the data. That's a very interesting lesson that I first encountered in [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) and has stuck with me.
