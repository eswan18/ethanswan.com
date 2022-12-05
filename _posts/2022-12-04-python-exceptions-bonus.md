---
layout: post
date: 2022-12-04
tags:
- tech
- python
- programming languages
title: "Python Exceptions: Bonus Content"
excerpt: ""
preview_image: ""
---

*This post is a followup to my article [The Basics of Exceptions in Python](/feed/2022/12/04/python-exceptions-basics), but this one should still make sense if you haven't read it.*

Let's cover a few more advanced aspects of the Python exception system.
We'll move a bit faster and talk at a higher level of abstraction than we did in the last post.

## Other Types of Errors

In the last article we talked about a few specific classes of exceptions in Python, like `ZeroDivisionError` and `TypeError`.
There are many built-in classes of exception in Python, enough that I didn't bother to count them when I checked the [docs](https://docs.python.org/3/library/exceptions.html).
If you're going to raise an error in your own code, it's a good idea to look through these and figure out which one best represents the situation you're in.

The ones I find myself raising most often in my own code:
- `TypeError` -- The type of something is invalid. Sounds broad, but the emphasis here is on *type*: the calling code provided an object of invalid class.
- `ValueError` -- A value passed to a function/class is invalid for one reason or another. Emphasis here on *value*, as opposed to type.
- `NotImplementedError` -- A special error to raise in a function you haven't implemented yet.
- `RuntimeError` -- A bit of a catch-all for errors that don't fall into any other category.
This is so vague that it only makes sense in quick projects that aren't meant for production;
in serious code it's too generic to be caught easily in an `except` clause.
In those cases, it would be better to define a custom error class, which we'll cover in the next section.

## User-defined Exception Classes

I considered discussing custom exceptions in the *Basics* article.
They're a staple of high quality code, letting you signal errors that are specific to the logic in your application.
However, creating them requires an understanding of OOP and is a bit of a leap from `raise` and `try/except`, so I thought it was better to move them here.

Python exception types can be subclassed like any other class in Python.
Maybe you're writing a function for parsing a file and empty files are invalid.
You might look through the docs to find the right type of exception to use, but nothing fits very well.
If I had to choose, `EOFError` is probably the closest thing, but it's not really right.
A better alternative is to invent your own exception type.

```python
class EmptyFileError(Exception):
    pass

def parse_file(filename):
    with open(filename, 'rt') as f:
        contents = f.read()
    if len(contents) == 0:
        raise EmptyFileError(f"file {filename} has no contents")
    ... # If all is well, go on and parse the contents.
```

Here, we create a new `EmptyFileError`.
The body of the class has no contents, so it inherits all behavior from `Exception`.
In our function, we instantiate and raise this custom error if the file's contents are empty.

When we pass it the name of an empty file, our custom error is raised just like any other.

```text
>>> parse_file("empty.txt")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in parse_file
__main__.EmptyFileError: file empty.txt has no contents
```

Because our `EmptyFileError` is a subclass of `Exception`, it will match `except` blocks that check against either of those types.
That's good, because users who use `except Exception` as a fallback case will still be able to catch our error there.

It can also make sense to subclass more specific errors.
Say you're writing a distributed filesystem application.
When a file on the system can't be found, you might raise an error specific to your application that is also a subclass of `FileNotFoundError`.

```python
class DistributedSystemFileNotFoundError(FileNotFoundError):
    pass
```

As a subclass of `FileNotFoundError`, this exception would match `except` blocks checking for it.

```python
def does_file_exist(path_to_file):
    try:
        open_file(path_to_file)
    except FileNotFoundError:
        return False
    return True
```

Why check for `FileNotFoundError` instead of the more specific `DistributedSystemFileNotFoundError`?
Maybe `open_file` can accept local file paths (like `file://home/user/file.txt`) *or* distributed filesystem paths (using a different URI scheme, like `dfs://path/to/file.txt`).
When receiving local paths, it would raise a `FileNotFoundError` if the file isn't there;
when receiving distributed filesystem paths, it would raise `DistributedSystemFileNotFoundError`.

Our `does_file_exist` function is able to handle both of these in the same `except` block, which is useful here because we want to take the same action either way.
But if calling code instead wanted to treat not-found issues differently when they occurred in the distributed filesystem, it could catch `DistributedSystemFileNotFoundError` specifically.

Since exceptions are classes like any other, you can add attributes or methods to your custom errors if you want.
That's sometimes handy, but simple subclassing as we saw above is often enough.

## Finally

Up to this point we've only been using `try` and `except` in our error handling blocks.
Given that's what we call them, it's no surprise those are the most important aspects of the construct, but there's also another: `finally`.

Code in the `finally` block executes after everything else in the construct finishes.
That makes it a good candidate for "clean-up code" that needs to execute *no matter what*.
The canonical example is closing a file after some other operations.

```python
f = open('file.txt')
try:
    contents = f.read()
finally:
    f.close()

parse(contents)
```

In this example, if no error occurs, the file will be opened, read, closed, and parsed.
But if we hit an error while trying to read the file, the `finally` clause will close the file before Python crashes.
The error will still cause the current interpreter session to exit early, but not before `f.close()` is run.

The key point is that `finally` is different from `except` in that it runs even if the `try` block finishes without error.
You can use both `except` and `finally` together to modify the same `try` block, which is occasionally useful.

Before I end this section, I'm obligated to mention that there is a rarely-used `else` construct that's legal after `try` blocks as well.
It's executed only if the `try` block completes without error, and happens before the `finally` clause, if there is one.
When I first heard of it, I couldn't think of any possible use, but it has really come in handy a couple of times in my programming career.