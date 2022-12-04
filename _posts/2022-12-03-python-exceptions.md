---
layout: post
date: 2022-12-03
tags:
- tech
- python
- programming languages
title: The Basics of Exceptions in Python
excerpt: ""
preview_image: ""
---

*This post was originally meant to be part of my discussion of the Go programming language (link coming soon, when I finish it), but turned out to be extensive enough to justify its own post.*

Python's model of exceptions is quite similar to other popular "modern" languages like Ruby, JavaScript, and Java (I can't vouch for Java firsthand since I avoid it like the plague, but I did some research and it looks similar).
Errors flow differently than regular data; if not "handled", they rise up through the entire function stack and crash the program.
Developers are encouraged to write code to anticipate those exceptions, handle them before everything explodes, and change the logic flow of the program accordingly.

What exactly needs to be done in that "handling" step typically depends on what went wrong, and so there are many *types* of errors.
Programmers can check the type of an error to determine what went wrong and react accordingly.
Developers sometimes even create their own types of errors, to signal particular issues that can arise in the logic they wrote.
Errors can be thought of as objects and their types as classes that can be subclassed like any other class.
But unlike other data, they follow a different path through the code, short-circuitiing functions all the way up the stack until handled.

If that all sounds like gibberish to you, let's walk through an example, starting with how you'd signal an error in your own code.

```python
def divide(x, y):
    if y == 0:
        raise Exception("Can't divide by zero")
    return x / y
```

The interesting thing here is the `raise` keyword, which causes the function to **exit prematurely**;
if `y` is 0, the line `return x / y` never executes.
Instead, we say that the function "errors".

You can run this function in the Python REPL and see that it works fine most of the time, but prints an error when the second argument is 0.

```text
>>> divide(5, 10)
0.5
>>> divide(3, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in divide
Exception: Can't divide by zero
```

It's important to understand that the exception isn't *returned* from the function, it's propagated via an entirely different pathway.
You can see this a few ways -- one is by trying to assign the result of `divide` to a variable.

```text
>>> x = divide(3, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in divide
Exception: Can't divide by zero
>>> x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'x' is not defined
```

No value is returned and the variable is never set.
The error short-circuits the function before it returns anything.
Returning a value and raising an error are mutually exclusive: a function either returns something or it errors.

Errors, unlike return values, automatically rise through calling functions as well.
For example, if `divide` is called within another function, the error will escalate through both layers and short-circuit the calling function as well.

```python
def calculate_percent(numerator, denominator):
    raw_quotient = divide(numerator, denominator)
    return 100 * raw_quotient
```
```text
>>> calculate_percent(10, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in calculate_percent
  File "<stdin>", line 3, in divide
Exception: Can't divide by zero
```

You can see what's called the "stack trace" of the error as it bubbles up from its origin (the `raise` line in `divide`) up through `calculate_percent` and finally into `<module>` (which is actually the Python REPL).
Having a stack trace is extremely helpful; `divide` could be called multiple times in our program, but with this knowledge we can quickly understand the exact provenance of the error and know where to look in order to fix it.

Even though errors in Python aren't *returned* per se, they can be "caught" in a variable through a mechanism called try/except blocks.

```python
def calculate_percent(numerator, denominator):
    try:
        raw_quotient = divide(numerator, denominator)
    except Exception as exc:
       print("Uh oh, ran into an error:", exc)
       return 0
    return 100 * raw_quotient
```
```text
>>> pct = calculate_percent(3, 0)
Uh oh, ran into an error: Can't divide by zero
>>> pct
0
```

Here, we "catch" the exception and prevent it from short-circuting this function.
If we run into an exception in the `try` block, Python switches execution over to the `except` block instead of propagating the error further.

While `raw_quotient` still isn't defined, we as the programmer get a chance to take appropriate actions to rescue[^1] the program.
In this case, we might decide that in the rare case where we encounter an error in division, it's safe to return 0% as long as we print a warning[^2].
The function returns a value and it's stored in the `pct` variable, which wouldn't have happened if we'd let the exception go unhandled.

`except` blocks will catch any error in the corresponding `try` block, no matter how many functions deep.
Here, the exception is actually coming from the `divide` function, a layer down from `calculate_percent`, but it still gets trapped here.
We could also catch the error in any function that calls `calculate_percent`, or even more levels up.

Unfortunately, our code will also catch any *type* of exception in Python because of the `except Exception` bit.
This clause means that we should switch to that `except` block on anything that is a type of `Exception` -- which is pretty much all errors!

It would be better to be more specific.

Luckily there is a more granular type of error in Python for dividing by zero, the `ZeroDivisionError`.
We'll update our `divide` function to use it[^3].

```python
def divide(x, y):
    if y == 0:
        raise ZeroDivisionError("Can't divide by zero")
    return x / y
```
```
>>> divide(3, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in divide
ZeroDivisionError: Can't divide by zero
```

Notice that our error message now shows the precise type of error: `ZeroDivisionError`.
Rather than catching all exceptions, we can update our calling function to catch only `ZeroDivisionError`s.

```python
def calculate_percent(numerator, denominator):
    try:
        raw_quotient = divide(numerator, denominator)
    except ZeroDivisionError as exc:
       print("Uh oh, ran into a divide-by-zero error:", exc)
       return 0
    return 100 * raw_quotient
```
```text
>>> calculate_percent(5, 3)
166.66666666666669
>>> calculate_percent(5, 0)
Uh oh, ran into a divide-by-zero error: Can't divide by zero
0
```





[^1]: Interesting, in Ruby this block is actually called `rescue` instead of `except`.
[^2]: To be clear, in production code, you would probably do something entirely different -- maybe discard this input if it's a data processing application, or return an error status if it's a Rest API. But you'd initiate those actions in the `except` block.
[^3]: The experienced Python users following along will know that this is what happens by default if you try to divide a number by 0 in Python. We didn't need to do a check to see if the denominator was 0 because Python actually raises this error for us when appropriate.