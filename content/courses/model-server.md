---
title: Building a Model Prediction Server
summary: In predictive modeling, training a model is only half the battle; predictions typically need to be “served” to other systems in production via an API or similar interface. We'll build that model server together.
courseType: Workshop
category: Python
---

## Overview

In predictive modeling, training a model is only half the battle; predictions typically need to be “served” to other systems in production via an API or similar interface.

In this tutorial, students start with a trained scikit-learn model and build a working FastAPI application to deliver its predictions in realtime. No prior experience with API development is expected.

## Details

### Format

This tutorial is highly interactive.
It runs over about 3 hours, and half of that time is for students to work independently.
During that time, I'll walk around the room, answer questions, and help debug code.

I delivered [this tutorial at PyCon 2023](https://us.pycon.org/2023/schedule/presentation/79/), and you can see a recording of the lecture portions [here](https://www.youtube.com/watch?v=HHjsqcavdQs&t=2257s).

### Audience and Goals

This tutorial is for Python users who come from a data science background and want to learn how to deploy a model for use in production.
No familiarity with web or API development is expected.

Students will leave with the skills to build a simple API to serve predictions from an underlying machine learning model.

### Schedule

Over three hours of total time, we'll go through the following agenda.

- Intro, About Me, & Agenda (10 minutes)
- Setting up your project workspace (30 minutes)
- Creating a “hello world” FastAPI app (30 minutes)
- Pydantic models and payloads (40 minutes)
- Connecting our model to the API (40 minutes)

This format gives 30 minutes of buffer time in case we run long, have tech problems, or just want to talk about more topics at the end.