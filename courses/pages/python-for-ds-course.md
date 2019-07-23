---
layout: page
title: Python for Data Science
---

A 7-week, 2-credit hour course focused on using Python for data science.
Topics include data wrangling, interaction with data sources, visualization, running scripts, the Python ecosystem, functions, and modeling.

### Primary Objectives
1. Expose students to the Python data science ecosystem's libraries, capabilities, and vocabularly.
2. Build students' proficiency in the core data wrangling skills: importing data, reshaping data, transforming data, and exporting data.
3. Develop students' ability to use Python within both interactive (Jupyter, REPL) and non-interactive (scripts) environments.
4. Explore various methods of producing output in Python: plotting, exporting various data formats, converting notebooks to static files as deliverables, and writing to a SQL database.
5. Expose students to modeling via scikit-learn and discuss the fundamentals of building models in Python.
6. Teach students how and when to teach themselves, through a discussion of widely-available Python resources.

### Pre-work
I try to limit pre-work as much as possible, but having Python, Jupyter, and the relevant packages installed is an unavoidable necessity.
Below are instructions to do so via Anaconda (a popular Python distribution):
1. Visit the Anaconda download page
2. Select your appropriate operating system
3. Click the "Download" button for Python 3.7 - this will begin to download the Anaconda installer
4. Open the installer when the download completes, and then follow the prompts. If you are prompted about installing PyCharm, elect not to do so.
5. Once installed, open the Anaconda Navigator and launch a Jupyter Notebook to ensure it works.
6. Follow the package installation instructions to ensure pandas and seaborn packages are installed.

I would also suggest, but not mandate, reading [the preface](https://jakevdp.github.io/PythonDataScienceHandbook/00.00-preface.html) and [Chapter 1](https://jakevdp.github.io/PythonDataScienceHandbook/01.00-ipython-beyond-normal-python.html) of the Python Data Science Handbook for an overview of data science and to gain familiarity with the Python environment and Jupyter notebooks.

### Bootcamp Agenda
The one-day bootcamp begins at 8am and finishes at 5pm or a little earlier.
Materials can be found in the notebooks folder of the [*Intro to Python for Data Science* repository](https://github.com/uc-python/intro-python-datasci).
The intended schedule is below.

{% comment %}
Super hack! I need to style [only] this particulary table but it's generated from a markdown file. This approach is stylistically terrible for a variety of reasons -- but it works.
{% endcomment %}
<style>
table td{
  border-top: 1px solid lightgray;
}
</style>

| Time        | Content                                                              |  Materials | 
|-------------|----------------------------------------------------------------------|------------|
| 8:00-8:15   | Introduction of Your Instructor; Overview of the Day's Agenda        |            |
| 8:15-8:45   | Basics of Python and Jupyter                                         | [Notebook 1](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/01-Python-and-Jupyter.ipynb) |
| 8:45-9:30   | Python Fundamentals                                                  | [Notebook 2](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/02-Fundamentals.ipynb) |
| 9:30-10:15  | The Mental Model of Python                                           | [Notebook 3](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/03-Packages-Modules-Function.ipynb) |
| 10:15-10:30 | Break                                                                |            |
| 10:30-11:00 | Importing and Exporting Data                                         | [Notebook 4](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/04-Importing-Data.ipynb), [Notebook 11](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/11-Exporting-Data.ipynb) |
| 11:00-11:45 | Selecting and Filtering Data                                         | [Notebook 5](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/05-Selecting-and-Filtering.ipynb) |
| 11:45-1:15  | Lunch                                                                |            |
| 1:15-2:00   | Manipulating Columns                                                 | [Notebook 6](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/06-Manipulating-Columns.ipynb) |
| 2:00-3:00   | Summarizing Data                                                     | [Notebook 8](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/08-Summarizing-Data.ipynb) |
| 3:00-3:15   | Break                                                                |              |
| 3:15-4:15   | Summarizing Data by Group                                            | [Notebook 9](https://github.com/uc-python/intro-python-datasci/blob/master/notebooks/09-Summarizing-Grouped-Data.ipynb) |
| 4:15-5:00   | Questions, Discussion, and Review                                    |       |

<br>

### Course Agenda
Class sessions will be structured as 110 minutes of lecture, a 10-minute break, and 110 minutes of lab.
Additional breaks will be given if time permits.

- *Session 1*: **Refresher on Python and DataFrames; Importing and Exporting Beyond CSVs; Reshaping and Melting**
  - *Supplemental Reading*: [The Python Data Science Handbook, starting at the beginning of Chapter 3 up to and including Pivot Tables](https://jakevdp.github.io/PythonDataScienceHandbook/03.00-introduction-to-pandas.html)
  - *Lab*:
- *Session 2*: **Control Flow; Functions; the `DataFrame.apply` Method**
  - *Supplemental Reading*:
    - Functions: [How to Think Like a Computer Scientist, Chapter 4](http://openbookproject.net/thinkcs/python/english3e/functions.html)
    - Conditionals: [How to Think Like a Computer Scientist, Sections 5.1-5.8](http://openbookproject.net/thinkcs/python/english3e/conditionals.html)
    - Iteration: [How to Think Like a Computer Scientist, Sections 7.1-7.4](http://openbookproject.net/thinkcs/python/english3e/iteration.html)
  - *Lab*:
- *Session 3*: **Modeling and Feature Engineering**
  - *Supplemental Reading*: [The Python Data Science Handbook, Chapter 5](https://jakevdp.github.io/PythonDataScienceHandbook/05.00-machine-learning.html)
  - *Lab*:
- *Session 4*: **Conda Environments; the Python REPL; Running Non-interactive Scripts**
  - *Supplemental Reading*:
  - *Lab*:
- *Session 5*: **Visualization with Seaborn and Matplotlib**
  - *Supplemental Reading*: [The Python Data Science Handbook, Chapter 4](https://jakevdp.github.io/PythonDataScienceHandbook/04.00-introduction-to-matplotlib.html)
  - *Lab*:
- *Session 6*: **Classes and Objects in Python; Deep-dive on Pandas DataFrames**
  - *Supplemental Reading*:
    - Classes and Objects: [How to Think Like a Computer Scientist, Sections 15.1-15.5, 15.8-15.11](http://openbookproject.net/thinkcs/python/english3e/classes_and_objects_I.html)
    - Numpy arrays: [The Python Data Science Handbook, Chapter 2](https://jakevdp.github.io/PythonDataScienceHandbook/02.00-introduction-to-numpy.html)
    - DataFrames: [The Python Data Science Handbook, from Vectorized String Operations to the end of the Chapter 3](https://jakevdp.github.io/PythonDataScienceHandbook/03.10-working-with-strings.html)
  - *Lab*:
- *Session 7*: **Bonus Topics -- Flask and RESTful APIs; Version Control with Git and GitHub; Python Packaging**
  - *Supplemental Reading*:
  - *Lab*:
