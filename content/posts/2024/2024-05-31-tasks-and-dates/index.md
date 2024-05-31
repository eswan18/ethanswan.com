---
title: "Tasks and Dates"
subtitle: "There's much more than just due dates"
slug: tasks-and-dates
layout: post
date: 2024-05-31
tags:
- content
- now-and-here
summary: "Tasks. So simple that every online app tutorial uses them as example data. But try to build a practical task management app and you'll quickly discover that there's a lot of complexity to them."
---


Tasks.
So simple that every online app tutorial uses them as example data.

But try to build a practical task management app[^build-a-task-app] and you'll quickly discover that there's a lot of complexity to them.
One particularly surprising part of a task is *dates*.

{{< images/image src="abstract-task.png" alt="abstract task" class="" caption="An absolutely bonkers abstract representation of \"tasks\" from Dall-E" >}}

## The basics

A minimal task might just be a description and a due date.

```rust
struct Task {
    desc: String,
    due_date: Date | None,
}
```

We're gonna run into problems pretty quickly though.

If I need to take out the trash every Thursday, this could only be expressed with a separate task for every week: clearly redundant.
That's a *repeating task* and the task data model should support that.
So we'll add some kind of "repeat interval" to a task[^repeat-interval-implementation].

```rust
struct Task {
    desc: String,
    due_date: Date | None,
    repeat: RepeatInterval | None,
}
```

With this model, we can actually get pretty far.
The most useful filters and sorts (e.g. tasks due today, all tasks ordered by due date, etc.) are possible with this info.

## Start date

One thing that *isn't* possible yet is excluding tasks that aren't ready to be started (for whatever reason).

Take filing taxes as an example.
I can't start my taxes until my banks/brokerages/etc have sent the necessary forms, which is usually around February 15.
When I list out all my tasks, I might not want to see things like this -- since I can't actually do them just yet.

We can address that by storing a "start date" in the task metadata.

```rust
struct Task {
    desc: String,
    due_date: Date | None,
    start_date: Date | None,
    repeat: RepeatInterval | None,
}
```

Simple enough.
But how do repeat intervals interact with start dates?

Taking the trash out to the curb is something that only makes sense to do on the day the trash is picked up, or maybe the night before.

A concrete task for taking out the trash on June 3 might look like this, with a start date of June 2:

```rust
Task {
    desc: "Take out trash",
    due_date: Date("2024-06-03"),
    start_date: Date("2024-06-02"),
    repeat: RepeatInterval::Weekly,
}
```

When I complete this task, the next iteration should be due a week after the current due date: June 10.
And the next start date should be one week after the current start date: June 9.

But simply adding the interval to both due date and start date actually breaks down in some cases, specifically monthly tasks that have a start date in the previous month.


```rust
Task {
    desc: "Pay Rent",
    due_date: Date("2024-07-01"),
    start_date: Date("2024-06-30")
    repeat: RepeatInterval::Monthly,
}
```

With our naive method of adding the repeat interval (here, a month) to both dates, the next iteration of this task would have a start date of July 30 -- *2* days before the due date (August 1) -- because months have different numbers of days.
This is almost certainly not what the user intended.

```rust
Task {
    desc: "Pay Rent",
    due_date: Date("2024-08-01"),
    start_date: Date("2024-07-30")
    repeat: RepeatInterval::Monthly,
}
```

This example illustrates that start dates are better expressed as *relative* to the due date, not as an absolute.

```rust
struct Task {
    desc: String,
    due_date: Date | None,
    start_date: TimeDelta | None,
    repeat: RepeatInterval | None,
}
```

So our Pay Rent task might look like this:

```rust
Task {
    desc: "Pay Rent",
    due_date: Date("2024-07-01"),
    start_date: TimeDelta{days: 1},  // Can be started one day before the due date.
    repeat: RepeatInterval::Monthly,
}
```

This approach still brings some potential weirdness:
updating the due date will cause the start date to change as well, which is a little bit strange particularly for non-repeating tasks.
But it's a solid enough solution.

## Target date

We're not done with dates yet: some people track their *intended* start date[^intended-start-date] for a task as well.

I conducted a "user interview" of a friend and fellow obsessive task-tracker.
She uses her app's start date feature as more of a scheduler;
a start date is when she plans to start working on the task, not when the task becomes doable.

This isn't how I think about tasks at all[^think-about-tasks], so I had to grapple a bit with the idea, but ultimately it's pretty clear that this is an entirely different idea the kind of start dates we covered above.
For clarity, I'll call it "target date".

Target dates are a lot like start dates, and most of the same logic about absolute versus relative applies to them as well.
Hopefully we've learned our lesson from last time, so target dates will also be stored relative to the due date.

```rust
struct Task {
    desc: String,
    due_date: Date | None,
    start_date: TimeDelta | None,
    target_date: TimeDelta | None,
    repeat: RepeatInterval | None,
}
```

At this point we have a data structure that can store pretty much all of the date related data that most people could want in a task.

## Tasks without due dates

Can we support start dates for tasks that don't have a due date with this design?
Nope.

```rust
Task {
    desc: "Update resume",
    due_date: None,
    start_date: // ????
}
```

Start dates are stored as the time delta before the due date, but there is no due date.
Still, this should be possible!
And now we've really made trouble for ourselves.

We have a few options:
1. Create two entirely different data structures, one for a task-with-due-date and another for task-without-due-date. Then we can store absolute dates for the start and target dates on the latter.
2. Make the schema a bit more flexible, such that `start_date` and `target_date` fields can also accommodate absolute dates. Build the logic into the application to handle using relative or absolute dates when each is needed – for tasks with due dates and tasks without due dates, respectively.
3. Switch to always using absolute dates for `start_date` and `target_date`, and build logic into the application to update those values intelligently when the due date is modified.
4. Force all tasks to have a due date.

The first three options require gnarly implementations; the fourth offloads the gnarliness onto the user.

My initial inclination was to go with #4 (sorry, users!), but here's the problem.
If I want a task with no due date but am forced to set one, I'd probably just choose an arbitrary far away date in the future: in a year from now, for example.

If my task has a target date though, it'll be stored relative to the due date – probably a pretty big delta.

```rust
// A task with an arbitrary due date
Task {
    desc: "Update resume",
    due_date: Date("2025-06-01"), // random date far from now
    target_date: TimeDelta(days=358), // 2024-06-08
}
```

And if I move the due date to be sooner, because I realize I need to have my resume finished for some reason, then suddenly my target date is way in the past.

```rust
// A task with an arbitrary due date
Task {
    desc: "Update resume",
    due_date: Date("2024-08-15"), // now much sooner
    target_date: TimeDelta(days=358), // 2023-08-23 -- almost a year ago
}
```

Ultimately, users shouldn't be forced to assign random due dates because it will cause bizarre behavior of other dates on the task when updated.

While all four options have drawbacks, I actually think that #1 is best.
It encodes invariants into the type system (it would in a statically-typed language, anyway), offloading the hard work of validation onto the language's type checker.
It requires a fair bit of extra work in building out the data structure itself though.

In a language with algebraic data types – which is sadly not most practical languages – it could be expressed like this:

```rust
enum TaskDates {
    Due {
        due: Date,
        repeat: RepeatInterval | None,
        start_date: TimeDelta | None,
        target_date: TimeDelta | None,
    },
    NotDue {
        start_date: Date | None,
        target_date: Date | None,
    },
}

struct Task {
    desc: String,
    dates: TaskDates,
}
```

In a language without typed unions (the role of the `Enum` above), it could be done with inheritance but it's less elegant.

```python
class Task:
    desc: str

class DueTask(Task):
    due: Date
    repeat: RepeatInterval | None
    start_date: TimeDelta | None
    target_date: TimeDelta | None

class NotDueTask(Task):
    start_date: Date | None
    target_date: Date | None
```


## An unsatisfying conclusion

I can't see any way to make this simpler; the more I think about it the more complicated it seems.
Representations that are more straightforward in the application and database are more surprising to the user.

While a user can't expect an application to read their mind, it's also not reasonable to offload all this complexity onto them.
So the simplest viable solution - two separate representations for tasks depending on whether they have a due date – is probably the right answer[^right-answer].
Sometimes software design is just inelegant and there's nothing you can do about it.

Tasks. Not such simple data after all.

[^build-a-task-app]: Which [I'm doing](/feed/2024/04/06/building-a-todo-app/)!
[^repeat-interval-implementation]: I'm skipping over a lot of complexity, like: how exactly to represent a repeat interval, how to calculate the next occurrence, and the trickiness of making sure users don't create invalid tasks by assigning a repeat interval but no due date.
[^intended-start-date]: Confusingly, some task managers (and users) also call this "start date". That term admittedly makes sense both for "intended start date" and for "earliest possible start date", and both phrases are long so it's understandable to shorten them. However, "earliest possible start date" is much more cumbersome – and harder to replace with a clear term other than "start date". So that field got to keep the nicer moniker, and I settled on "target date" as the concise expression for intended start date. In my opinion, the best term for this idea is really "do date", as in *when I'm going to do the task* – but I think we can agree that's just too confusing.
[^think-about-tasks]: To me, tasks are an endless pit of things I should do, and I'm usually looking at my full list of tasks (right now that's about 200) sorted by due date, sometimes filtered to things due in the next few weeks. I very rarely schedule a specific time to do a task, and when I do, I'd record that as an event in my calendar app – since it feels like a detail related to my *schedule*, not to anything about the task itself. But admittedly, my system means that I'm always staring down a near-infinite well of todos that *could* be done (because most things don't have a start date), and I can see how that might feel a bit overwhelming to some people. Personally, I'm used to it.
[^right-answer]: For my own project, I haven't decided what direction I'll go. Thinking more carefully about this topic made me realize just how fraught it is. Right now I support due dates and repeat intervals but no other date metadata, and now I'm reluctant to add start dates and target dates because it's going to be a much bigger undertaking than I'd initially anticipated.