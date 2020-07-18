---
layout: post
date: 2020-03-01
categories:
- technology
title: State of the Tools 2020
preview_image: ""
---

I spend a lot of time on meta-productivity: thinking about how to get work done better and faster.
The majority of that thinking is around technology and specifically the tech tools I use.
Maybe thinking about my workflow has returns large enough to offset the time it consumes in my life, but frankly it doesn't matter too much to me since life optimization is as much a hobby as an objective.
<!--more-->

2019 was a pretty good year. I picked up quite a few new tools, but not so quickly or so often that I didn't comfortable with the ones I cared about.
Below is a fairly comprehensive list of the tech I use regularly.
I hope to make *State of the Tools* an annual tradition, if for no other reason than to give my future self a record to look back on in future years.

This first post is just hardware.
I'll publish another (longer) post on software in the near future.

- **iPhone Xs Max** – The obvious first item in this list.
Screen time tells me I use it about 2 hours a day on average, a number which (I often say to my [Walden Ponding](https://breakingsmart.substack.com/p/against-waldenponding) friends, winkingly) should really be higher.
I love the big screen, and for a long time my only complaint was the difficulty of typing with one hand -- an issue largely obviated by the introduction of swipe-typing in iOS 13.
As I understand it, the biggeset improvements in last year's iPhone (the 11) came in battery life and the camera; my battery remains very good -- probably related to how much more battery space can go in a Max phone -- and frankly I can no longer see differences (or care about them) in camera quality at this point in phone camera technology.
<br><br>
- **16" MacBook Pro, late 2016** – I bought the touchbar MacBook Pro just a month or two after its release.
I've experienced most of the common annoyances: the touchbar is basically useless, made worse by the loss of a physical escape key; the keyboard feels not so much bad as just weird, which makes it very hard to switch between the laptop and normal external keyboards (which I use often); the lack of USB-A and HDMI ports is regularly frustrating and has probably resulted in me spending $100 in dongles.
So it has some problems.
But despite all that, this machine has been a workhorse and endured a huge amount of abuse -- it comes with me everywhere, gets bounced around in my backpack, and serves as a testing-ground for all kinds of software tools I want to try out.
It's not noticeably worse in any way than the day I bought it, which was over 3 years ago.
The introduction of Sidecar, the tool for using an iPad as an external display, has made me like my Mac all the more.
I'll upgrade the at the next major Mac update, but more out of curiousity than necessity.
<br><br>
- **iPad Pro, early 2018** – I have the last iPad Pro without USB-C, meaning it still has bezels and Touch ID.
It's much less integral to my life than my iPhone or Mac, but I've still loved having it.
I use it mainly for reading and videos, which seems to be largely the consensus around what iPads are good for.
But, as mentioned above, Sidecar has led to me taking my iPad everywhere over the last few months.
I'm dying to upgrade to a new iPad Pro, for the larger screen, Face ID, and better Apple Pencil, but am waiting for Apple's rumored Spring event and the likely iPad Pro update with it.
<br><br>
- **Desktop Ubuntu Workstation, with Windows Dualbooted** – Back in early 2018, I embarked on the somewhat scary challenge of building a desktop PC.
It was fun and I learned a lot -- but honestly this computer is much more of a toy than a necessity.
I like using Ubuntu occasionally to force myself not to get too dependent on MacOS, as it still has a Unix-like command line and filesystem hierarchy.
I use Windows mainly for the occasional video gaming, but as a teacher it's nice to be able to test out certain workflows on the same operating system that most students have, so I have spent many hours trying to get Python and adjacent tools working properly on Windows.
Needless to say, this has not endeared that OS to me.
<br><br>
- **AirPods Pro** – Ridiculously good. Really.
I was a diehard fan of the original Airpods, which achieved an impossible level of unnoticeability -- at least once a day, I'd put my hands to my ears to determine whether I was wearing them.
Unfortunately the Pros aren't quite so perfect in this regard, but they've improved in every other aspect.
The sound quality is great, the noise cancelling almost unbelievable for the form factor, and the comfort still excellent.
These have become nearly as indispensable as my phone.
<br><br>
- **Lots of Raspberry Pis** – Where would I be without Raspberry Pis?
I have one original Pi, four Pi 3s, one Pi 4, two Pi Zeros, and a tinkerboard.
Mostly the Pis are great for temporary projects: set it up, try to build something, and wipe and repeat when things go wrong.
They've been great for learning about networking, web apps, and administering Linux.
One Pi 3 is running [RetroPie](https://retropie.org.uk), a very cool retro video game emulator that was very straightforward to set up, and another is running [Autodoist](https://github.com/eswan18/autodoist_d), a daemon Python program I set up to automatically manage some aspects of my to-do list.

<hr>

## Software/Services

##### Life Organization
- **Todoist** – The cornerstone of my life.
I started using Todoist for all my task-tracking in 2018, and honestly I can't imagine how I got things done before that.
Every thing I need to do lives in Todoist.
I really appreciate the simplicity of the interface, but occasionally that simplicity frustrates me -- the ability to handling recurring tasks and when tasks become visible isn't great.
But what has kept me with Todoist is their [API](https://developer.todoist.com/sync/v8/), which supports pretty much anything you can do from the app.
Even better, there is a fantastically elegant third-party Python library wrapper for the API called [PyTodoist](https://github.com/Garee/pytodoist).
Using PyTodoist, I built a Python daemon that manages some aspects of my Todoist tasks that the app doesn't support natively ([Autodoist](https://github.com/eswan18/autodoist_d)).
As an added benefit, Todoist is available on all platforms, so it actually reduces my Apple platform lock-in.
- **Fantastical** – Until just a few months ago, I used Apple Calendar for most of my calendar-keeping.
Apple's app is actually pretty good and probably fine for most people.
But Fantastical brings a lot of nice touches, including different ways of displaying a calendar that I find really nice.
The best feature is something called *calendar sets*, which allows you to save combinations of calendars (e.g. work and chores) as a "set" -- and then toggle which set is visiible at any given time.
This is excellent for managing work vs home calendars; I usually display just one at a time, but occasionally I need to see everything all at once and easily toggle into that view.
- **Apple Notes** – Apple Notes might be the software about which I'm most conflicted.
It's a very nice interface: simple, aesthetically pleasing, and easily searchable.
But the platform lock-in is huge -- I've searched for ways to export my notes and none meet my needs.
I've tried to use a Google account as the underlying notes store (instead of my iCloud account), but this limits the features available in your notes.
In the end, I've basically resigned myself to lock-in with Notes, but I wish I could have a contingency plan in case the time ever comes that I want to switch from Apple platforms.
- **Apple Mail** – I 
- **Outlook** – 
- **Strides**
- **Lastpass**

##### Fitness
- **MapMyFitness**
- **Gymaholic**

##### Media
- **Overcast**
- **Spotify**
- **O'Reilly**
- **Feedly**
- **Instapaper**

##### General Utilities
- **Alfred** – Used to use launchbar but it felt clunky and required purchase to do the things that I can do for free with Alfred.
- **Spectacle**

##### Programming
- **iTerm**
- **Vim**
- **Python**

##### Storage and Filesharing
- **Backblaze** – backups
- **Dropbox** – teaching
- **Google Drive** – podcast

##### Other
- **Paprika**

## Honorable Mention
- **iStat Menus** - 
- **Mullvad VPN** - 
- **Drafts** – I'm still figuring out how Drafts fits into my workflow. I sketched the outline of this post there, but did all the actual writing right in my terminal. Not having Vim keybindings remains a near-dealbreaker.
- **Clipy**
- **Due** – for nightly reminders to get ready for bed
- **Eufy Life** – for smart scale
- **Slack** – for a few groups with specific purposes
- **Both Apple and Google Maps** – I waffle. Google Maps is bettter but Apple Maps has integration with the Apple Watch.
- **VSCode** – A tolerable Vim substitute when I need a visual feature, like markdown rendering.
- **Git** – Git is so obvious and standard that it's not really a "choice", so while I use it daily it stays in Honorable Mention.
- **Docker** - I don't use Docker as much as Git, but it occasionally solves a hard problem very quickly. Like Git, it's pretty much the standard tool for what it does.
