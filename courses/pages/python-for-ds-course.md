---
layout: page
title: Python for Data Science Course
---

A 7-week, 2-credit hour course focused on using Python for data science.
Topics include data wrangling, interaction with data sources, visualization, running scripts, the Python ecosystem, functions, and modeling.

If you are looking for information on the associated bootcamp, click [here](/courses/pages/python-for-ds-bootcamp).

### Links
[Lecture Slides](https://www.dropbox.com/sh/5hwwqbfx3fep4z5/AADMJTxKB0_ZmSBnt8s8GDaOa?dl=0) | [Labs](https://github.com/uc-python/python-for-ds-course/tree/spring-2020/lab_notebooks) | [Lab Solutions](https://github.com/uc-python/python-for-ds-course/tree/spring-2020/lab_solutions)

### Page Contents<br>
[Objectives](#primary-objectives)<br>
[Pre-work](#pre-work)<br>
[Agenda](#course-agenda)<br>
[Grading](#course-grading)<br>
[Final Project](#course-project)<br>

### Primary Objectives
1. Expose students to the Python data science ecosystem's libraries, capabilities, and vocabulary.
2. Build students' proficiency in the core data wrangling skills: importing data, reshaping data, transforming data, and exporting data.
3. Develop students' ability to use Python within both interactive (Jupyter, REPL) and non-interactive (scripts) environments.
4. Explore various methods of producing output in Python: plotting, exporting various data formats, converting notebooks to static files as deliverables, and writing to a SQL database.
5. Expose students to modeling via scikit-learn and discuss the fundamentals of building models in Python.
6. Teach students how and when to teach themselves, through a discussion of widely-available Python resources.

### Pre-work
I try to limit pre-work as much as possible, but having Python, Jupyter, and the relevant packages installed is an unavoidable necessity.
Below are instructions to do so via Anaconda (a popular Python distribution):
1. Visit the [Anaconda download page](https://www.anaconda.com/distribution/).
2. Click the "Download" button for Python 3.7 - this will begin to download the Anaconda installer.
3. Open the installer when the download completes, and then follow the prompts. If you are prompted about installing PyCharm, elect not to do so.
4. Once installed, open the Anaconda Navigator and launch a Jupyter Notebook to ensure it works.
5. Follow the package installation instructions to ensure the following packages are installed:
  - pandas
  - seaborn
  - altair
  - scikit-learn
  - requests
  - tensorflow
  - keras
  - gensim

I would also suggest, but not mandate, reading [the preface](https://jakevdp.github.io/PythonDataScienceHandbook/00.00-preface.html) and [Chapter 1](https://jakevdp.github.io/PythonDataScienceHandbook/01.00-ipython-beyond-normal-python.html) of the Python Data Science Handbook for an overview of data science and to gain familiarity with the Python environment and Jupyter notebooks.

### Course Agenda
Class sessions will be structured as 110 minutes of lecture, a 10-minute break, and 110 minutes of lab.
Additional breaks will be given if time permits.

##### Session 1: Refresher on Python and DataFrames; Importing and Exporting; Joining
- *Supplemental Reading*: [The Python Data Science Handbook, starting at the beginning of Chapter 3 up to and including the "Pivot Tables" section](https://jakevdp.github.io/PythonDataScienceHandbook/03.00-introduction-to-pandas.html)
- *Lab*: Lab 01, Lab 02
- *Project Work*: None
- *Due*: None

##### Session 2: *Abbreviated Due to Switching to Remote* -- Introduction of Final Project
- *Supplemental Reading*: None
- *Lab*: None
- *Project Work*: Look over the [project rubric](/courses/rubrics/python-for-ds-course-final-project). Decide on a topic/dataset. Choose a partner if you want one.
- *Due*: Last week's lab.

##### Session 3: Grouping and Reshaping; Control Flow; Functions
- *Supplemental Reading*:
  - Conditionals: [How to Think Like a Computer Scientist, Sections 5.1-5.8](http://openbookproject.net/thinkcs/python/english3e/conditionals.html)
  - Iteration: [How to Think Like a Computer Scientist, Sections 7.1-7.4](http://openbookproject.net/thinkcs/python/english3e/iteration.html)
  - Functions: [How to Think Like a Computer Scientist, Chapter 4](http://openbookproject.net/thinkcs/python/english3e/functions.html)
- *Lab*: Lab 04, Lab 05, Lab 06, Lab 07, Lab 08
- *Project Work*: Pull your data. Push your project code so far to GitHub.
- *Due*: None

##### Session 4: Applying Functions to Data; Version Control with Git and GitHub; Visualization with Matplotlib, Seaborn, and Altair
- *Supplemental Reading*: 
  - Version Control: [Atlassian's Explanation of Version Control](https://www.atlassian.com/git/tutorials/what-is-version-control)
  - Git: [The "Version Control with Git" section of Atlassian's Explanation of Git](https://www.atlassian.com/git/tutorials/what-is-git#version-control-with-git)
  - Visualization with Matplotlib and Seaborn: [The Python Data Science Handbook, Chapter 4](https://jakevdp.github.io/PythonDataScienceHandbook/04.00-introduction-to-matplotlib.html)
- *Lab*: Lab 09, Lab 10
- *Project Work*: Clean your data. Commit and push that code. Send Ethan your GitHub repo with code that imports your data.
- *Due*: Last week's lab.

##### Session 5: Classical Modeling and Feature Engineering; Deep Learning and NLP Tools (High-level)
- *Supplemental Reading*: [The Python Data Science Handbook, Chapter 5](https://jakevdp.github.io/PythonDataScienceHandbook/05.00-machine-learning.html)
- *Lab*: Lab 11
- *Project Work*: Start your modeling process.
- *Due*: Last week's lab. **Project Check-in**.

##### Session 6: Topics I Wish We Had More Time for
Conda, Python Package Ecosystem, Spark, Requests & APIs, Docker, Cloud Computing

- *Supplemental Reading*: None
- *Lab*: None -- work on your project
- *Project Work*: Finish your project!
- *Due*: Last week's lab.

##### Session 7: Final Exam; Student-suggested Topics
No one will pay attention if I teach before the final, so we'll reserve the first two hours of class for the test and then the remaining time for Q&A and fun topics.
- *Due*: **Final Project (due the Sunday before class)**


### Course Grading
- **30%** Assignments -- *completion-based, 5% each*
- **15%** Final Exam
- **5%** Course Project Check-in -- *have code in a GitHub repo that imports your data, due at the beginning of session 5*
- **50%** Course Project -- *see below*

### Course Project
The final project requires students to **apply the data science skills covered in the course (and optionally, beyond what's covered) to real datasets.**

A total of 55% of the course grade is related to the final project.
The project must include data wrangling and the creation of a deliverable to explain the findings.
Students may complete the project alone or in teams of two;
however, groups of two will need to earn more points to score the same grade as an individual (more details in [rubric](/courses/rubrics/python-for-ds-course-final-project)).

##### Data
Teams must use at least two datasets in their project.
The data used is at each team's discretion, but I highly recommend selecting data from a domain in which your team has interest and/or expertise, as domain knowledge is an important aspect of using data science in industry -- and it will make the project more enjoyable.

Some suggested data sets:
- World economic data, such as [this](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?view=chart).
- Something from the FiveThirtyEight [website data](https://data.fivethirtyeight.com) or [GitHub repo](https://github.com/fivethirtyeight/data).
- Anything else you can find on the internet, within reasonable ethical boundaries. It's straightforward to find [CSVs of baby names over time](https://github.com/hadley/data-baby-names/blob/master/baby-names.csv) or an [API to fetch NBA data](https://github.com/swar/nba_api). You could even scrape a website using Python (see packages like [Scrapy](https://scrapy.org) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)). Acquiring the data via an API or scraping will net you extra points, as those are beyond the scope of what we discussed in this course.

##### Grading Details
The first project-related grade is the Check-in, due for Session 5. You must show that you have a GitHub repo with code in it that imports your data and does some data wrangling -- joining, filtering, cleaning, etc.
This is worth 5% of your course grade, so take advantage of the easy points.

The other 50 percentage points come from your final submission, and are graded via the [rubric](/courses/rubrics/python-for-ds-course-final-project).
This rubric for a great deal of flexibility on your side.
Points are earned by completing tasks from the list, with different tasks worth various point values based primarily on two things:
the difficulty and how integral the task is to the data science workflow.
Larger teams are expected to earn more points for an equivalent grade.
