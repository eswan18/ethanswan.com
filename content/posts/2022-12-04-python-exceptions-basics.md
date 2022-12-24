---
layout: post
date: 2022-12-04
tags:
- tech
- python
- programming languages
slug: python-exceptions-basics
title: The Basics of Exceptions in Python
excerpt: "Python's model of exceptions is quite similar to that of other popular object-oriented languages like Ruby, JavaScript, and Java. If not \"handled\", they rise up through the entire function stack and crash the program. Developers are encouraged to write code to anticipate those exceptions."
preview_image: ""
---

*This post was originally meant to be a small part of my discussion of the Go programming language (coming soon) as a way of drawing contrast between Python and Go, but turned out to be extensive enough to justify its own post.*

## Overview

Python's model of exceptions is quite similar to that of other popular object-oriented languages like Ruby, JavaScript, and Java[^0].
Errors flow differently than regular data; if not "handled", they rise up through the entire function stack and crash the program.
Developers are encouraged to write code to anticipate those exceptions, handle them before everything explodes, and change the logic flow of the program accordingly.

What exactly needs to be done in that "handling" step typically depends on what went wrong, and so there are many *types* of errors.
Programmers can check the type of an error to determine what went wrong and react accordingly.
Errors can be thought of as objects and their types as classes that can be subclassed like any other class.
But unlike other data, they follow an error-specific path through the code, short-circuitiing functions all the way up the stack until handled.

## Example

If that all sounded like gibberish to you, let's walk through an example, starting with how you'd signal an error in your own code.

### Raising Errors

Let's write a toy function to divide two numbers, aware of the fact that dividing a number by 0 isn't permitted.

```python
def divide(x, y):
    if y == 0:
        raise Exception("Can't divide by zero")
    return x / y
```

The interesting thing here is the `raise` keyword, which causes the function to **exit prematurely**;
if `y` is 0, the line `return x / y` never executes.
Instead, we say that the function "errors".

You can run this function in the Python REPL and see that it works fine most of the time but prints an error when the second argument is 0.

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
Returning a value and raising an error are mutually exclusive: a function either *returns* something or it *errors*.

Errors, unlike return values, automatically rise through calling functions as well (that's why we call it *raising* an error).
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

### Handling Errors

Functions that call `divide`, like `calculate_percent`, should ideally be aware of the exceptions it might raise and handle them accordingly.

While errors aren't returned per se, they can be "caught" in a variable through a mechanism called `try/except` blocks.

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
If we run into an exception in the `try` block, Python immeditely stops what it's doing and switches execution over to the `except` block instead of propagating the error further.

While `raw_quotient` still isn't defined (because `divide` didn't return a value), we as the programmer get a chance to take appropriate actions to rescue[^1] the program.
In this case, we might decide that in the rare case where we encounter an error in `divide`, it's safe to return 0 as long as we print a warning[^2].
The function returns a value and it's stored in the `pct` variable, which wouldn't have happened if we'd let the exception go unhandled.

`except` blocks will catch errors in the corresponding `try` block no matter how many functions deep they were originally raised.
Here, the exception is actually coming from the `divide` function, a layer down from `calculate_percent`, but it still gets trapped here.
We could also catch the error in any function that calls `calculate_percent`, or even more levels up.

Unfortunately, our code has a flaw: it will also catch any *type* of exception in Python because of the `except Exception` bit.
Any error that is a type of `Exception` will trigger it -- which is pretty much all errors!

It would be better to be more specific.

Luckily there is a more granular type of error in Python to signal dividing by zero, the `ZeroDivisionError`.
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
Rather than catching all exceptions, we can update our calling function to catch only that one.

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
>>> pct = calculate_percent(5, 3)
>>> pct
166.66666666666669
>>> pct = calculate_percent(5, 0)
Uh oh, ran into a divide-by-zero error: Can't divide by zero
>>> pct
0
```

Other types of errors will still cause our function to short-circuit though.

```text
>>> del pct
>>> pct = calculate_percent(5, 'abc')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in calculate_percent
  File "<stdin>", line 4, in divide
TypeError: unsupported operand type(s) for /: 'int' and 'str'
>>> pct
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'pct' is not defined.
```

Dividing an integer by a string is a `TypeError`, which isn't a `ZeroDivisionError`, so our function fails just the same as if we hadn't used `try/except` at all.

To handle different types of errors, developers can chain multiple `except` clauses with different exception types.
Python will check each one sequentially and enter the first `except` block that the error matches against -- or raise the error as usual if no blocks match.

```python
def calculate_percent(numerator, denominator):
    try:
        raw_quotient = divide(numerator, denominator)
    except ZeroDivisionError:
       print("Division by 0 is not supported; returning 0")
       return 0
    except TypeError:
        print("It looks like you entered data types that can't be divided; returning 0")
        return 0
    except Exception as exc:
        print("Uh oh, an error I didn't anticipate:", exc)
        raise exc
    return 100 * raw_quotient
```

When an error arises in the `try` block, Python first checks if it's a `ZeroDivisionError`.
If so, it enters that block and runs the code inside, then exits the `try/except` structure (it doesn't check any of the following cases).
If not, it checks if the error is a `TypeError`.
Again, it runs the code inside and then exits the `try/except`.
Last, it checks if the error is an `Exception`, which is so general that it will catch basically anything else.

A few other things to note:
1. Because of this sequential checking, it's important to list exception types from most specific to most general.
If we'd listed `except Exception` as the first case, even `ZeroDivisionError`s and `TypeError`s would fall into that block and skip the others, since they are subtypes of `Exception`.
2. The `as exc` part of the exception clause isn't required.
If it's not present, errors of that type will still fall into the following block, but the error object won't be stored in a variable for the developer to use.
In the cases of `TypeError` and `ZeroDivisionError` error, we omitted it, but we kept it in the general `Exception` case in order to print the error's text.
3. `Exception` is the most general class of error[^4], so `except Exception` will catch anything.
Catching *all* types of exception is helpful to demonstrate how exceptions are matched against different clauses, but rarely a good idea in real applications[^5].
4. Errors can be "re-raised", as we do here with `raise exc`.
You may want an error to still propagate up the stack, but only after you take some other actions.
Here, we print a special message before re-raising the original error.

Let's see our new code in action.

```text
>>> pct = calculate_percent(5, 10)
>>> pct
50.0
```
```text
>>> pct = calculate_percent(5, 0)
Division by 0 is not supported; returning 0
>>> pct
0
```
```text
>>> pct = calculate_percent(5, 'abc')
It looks like you entered data types that can't be divided; returning 0
>>> pct
0
```

Our code now gracefully handles "edge cases".
Were we to encounter an unexpected error though, it would still surface via the `except Exception` clause, making us aware of an additional edge case we should address in our code.

## Wrap up

While this is a toy example, these are the tools used in real-world code to manage errors.
High quality libraries should raise meaningful exceptions for their calling code to handle.
Robust applications must anticipate a variety of possible error conditions and recover gracefully from them when possible.
With just `raise` and `try/except`, we're able to do that in Python.

I cover a few more advanced topics about exceptions in a [separate post](/feed/2022/12/10/python-exceptions-bonus).
<br>

---

[^0]: I can't vouch for Java firsthand since I avoid it like the plague, but I did some research and it looks similar
[^1]: Interesting, in Ruby this block is actually called `rescue` instead of `except`.
[^2]: To be clear, in production code, you would probably do something entirely different -- maybe discard this input if it's a data processing application, or return an error status if it's a Rest API. But you'd use the `except` block to initiate that action.
[^3]: Experienced Python users will know that this is what happens by default if you try to divide a number by 0 in Python. We didn't need to do a check to see if the denominator was 0 because Python actually raises this error for us when appropriate. But hey, this is a teaching example so I needed something simple.
[^4]: Not *technically* true, actually. There are certain errors in Python that aren't a subclass of `Exception`; it only covers ["all built-in, non-system-exiting exceptions"](https://docs.python.org/3/library/exceptions.html#Exception). Generally you shouldn't try to catch non-`Exception` based errors in your code because they're things like [`KeyboardInterrupt`](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt) -- things that aren't meant to be suppressed in most applications.
[^5]: If an unforeseen error occurs in an application, you usually want to discover it and not allow it to pass silently through the system. That isn't absolute though: in some cases it may be more important that the program doesn't ever crash, so you might just log the error and move on.
