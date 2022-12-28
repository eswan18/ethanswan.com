---
title: "Python Exceptions: Bonus Content"
slug: python-exceptions-bonus
layout: post
date: 2022-12-10
tags:
- tech
- python
- programming languages
---

*This post is a followup to my article [The Basics of Exceptions in Python](/feed/2022/12/04/python-exceptions-basics), but should make sense on its own as long as you are familiar with `raise` and `try/except`.*

Let's cover a few more advanced aspects of the Python exception system.
We'll move a bit faster and talk at a higher level than we did in the last post.

Topics we'll hit:
- [More Python Built-in Exceptions](#more-python-built-in-exceptions)
- [User-defined Exception Classes](#user-defined-exception-classes)
- [Finally Blocks](#finally)
- [Keeping `try` Blocks Small](#keep-try-blocks-small)

 <!--more--> 
<br>

## More Python Built-in Exceptions

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
Maybe you're writing a function for parsing a file, and passing empty files to the function is invalid.
You might look through the docs to find the right type of exception to use, but nothing fits very well[^1].
In this case, the best option is to invent your own exception type.

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

Here, we create a new `EmptyFileError` class.
Its body has no contents, so it inherits all behavior from `Exception`.
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
But (importantly!) users can now look for our new error specifically by writing `except EmptyFileError` after a `try` block.

It can also make sense to subclass more specific errors.
Say you're writing a distributed filesystem application.
When a file on the system can't be found, you might raise an error specific to your application that is also a subclass of `FileNotFoundError`.

```python
class DistributedSystemFileNotFoundError(FileNotFoundError):
    pass
```

As a subclass of `FileNotFoundError`, this exception would match `except` blocks checking for it.

If `open_file` calls our distributed system, users could catch our custom error with the following code.

```python
def does_file_exist(path_to_file):
    try:
        open_file(path_to_file)
    except FileNotFoundError:
        return False
    return True
```

Why check for `FileNotFoundError` instead of the more specific `DistributedSystemFileNotFoundError`?

Maybe `open_file` can accept *both* local file paths *and* distributed filesystem paths[^2].
When receiving local paths, it would raise a `FileNotFoundError` if the file isn't there;
when receiving distributed filesystem paths, it would raise `DistributedSystemFileNotFoundError`.
Our `does_file_exist` function is able to gracefully handle both of these in the same `except` block, which is useful here because we want to take the same action either way.

But if for some reason calling code instead wanted to treat not-found issues differently when they occurred in the distributed filesystem, it could catch `DistributedSystemFileNotFoundError` specifically.
Subtyping existing exceptions when it makes sense enables this flexibility.

Since exceptions are classes like any other, you can also add attributes or methods to your custom errors if you want.
That's sometimes handy, but simple subclassing as we saw above is often enough.

## Finally

Up to this point we've only been using `try` and `except` in our error handling code.
Given that's what we call the construct, that's no surprise.
However, there's another keyword you can use: `finally`.

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

```python
f = open('file.txt')
try:
    contents = f.read()
except Exception:
    # If a file can't be read, just pretend it was empty.
    contents = ''
finally:
    f.close()

parse(contents)
```

### Else

Before moving on from `finally`, I'm obligated to mention that there is a rarely-used `else` construct that's legal after `try` blocks as well.
It's executed only if the `try` block completes without error.
That means that in situations where you use both `except` and `else`, exactly one of them will run.

If used in conjunction with with a `finally` clause, the `else` clause runs first.

When I first heard of it, I couldn't think of any possible use, but it has really come in handy a couple of times in my programming career.
That said, I wracked my mind for an example and couldn't come up with one.
It's not *that* useful.


## Keep `try` Blocks Small

You should put as little code as possible in the `try` block of a `try/except`.
This is stylistic advice, not a feature of Python, but worth mentioning all the same.

Having more code than necessary in the `try` block can lead to accidentally catching errors you didn't mean to.

Let's demonstrate thate by writing a quick script to copy one file to another.

```python
import sys

if len(sys.argv) != 3:
    print('usage: copyfile.py <fromfile> <tofile>')
    sys.exit(1)
from_filename = sys.argv[1]
to_filename = sys.argv[2]

try:
    with open(from_filename, 'rt') as f_in:
        contents = f_in.read()
    with open(to_filename, 'rt') as f_out:
        f_out.write(contents)
except FileNotFoundError:
    print(f"Error: fromfile '{from_filename}' must exist")
    sys.exit(1)
```

Here we're getting two filenames from the user, via command line arguments, and then copying the contents of one into another.
We wrap our copying code in a `try` block so that we can catch situations where the input file doesn't exist.
That way we can print a nice, terse error for the user instead of subjecting them to a full Python traceback[^3].

However, our code has a bug that might not be obvious.
Let's try it out.

We can check that if the input file doesn't exist, we get an error.

```text
$ python3 copyfile.py a.txt b.txt
Error: file 'a.txt' doesn't exist
```

But if we create the input file with some text in it, things should work.
```text
$ echo "hello world" > a.txt
$ python3 copyfile.py a.txt b.txt
Error: file 'a.txt' doesn't exist
```

Huh? Why are we still getting our error?
We know `a.txt` exists.

It's because we made a small mistake in our script, opening our destination file with `open(to_filename, 'rt')`.
`'rt'` is for *reading* text, even though we should be writing to this file.
If Python tries to open a file for reading and it doesn't exist, it throws a `FileNotFoundError`.

What makes this particularly confusing is that the code for writing was in our `try` block, so *any* `FileNotFoundError` led to us seeing the same error message.

Yes, we had a bug, but having too much code in the `try` block made it harder to detect.

Here's a better way.
```python
import sys

if len(sys.argv) != 3:
    print('usage: copyfile.py <fromfile> <tofile>')
    sys.exit(1)
from_filename = sys.argv[1]
to_filename = sys.argv[2]

try:
    with open(from_filename, 'rt') as f_in:
        contents = f_in.read()
except FileNotFoundError:
    print(f"Error: file '{from_filename}' doesn't exist")
    sys.exit(1)

with open(to_filename, 'wt') as f_out:
    f_out.write(contents)
```

Now we have the bare minimum amount of code in the `try` block, avoiding false positives.

The script works now, and if we made the same mistake (`'rt'` instead of `'wt'`), we'd get a much clearer error to help us track down the problem.

```bash
Traceback (most recent call last):
  File "/Users/eswan18/Develop/ethanswan.com/copyfile.py", line 16, in <module>
    with open(to_filename, 'rt') as f_out:
FileNotFoundError: [Errno 2] No such file or directory: 'b.txt'
```

Here, we get a full traceback -- indicating that the exception didn't get caught in `try/except` -- along with the true error, noting that it was `b.txt` (not `a.txt`!) that we couldn't find.
Knowing that Python tried to open our destination file might tip us off to the fact that we tried to *read* it instead of write it.

`try` blocks should contain only the line or couple of lines that could produce an error.
Additional logic belongs in the `finally` clause or outside the construct entirely.

[^1]: If I had to choose, `EOFError` is probably the closest thing, but it's not really right.
[^2]: An interface that supports multiple input sources is actually pretty common, and this is what [URIs]() are usually used for. A local file might be described as `file://path/to/file`. A system can use a different prefix to differentiate its type of files. Our hypothetical distributed filesystem might use "dfs", for example: `dfs://path/to/file`.
[^3]: A nice CLI shouldn't expose the user to internals. Give clear, one-line error messages if possible.
