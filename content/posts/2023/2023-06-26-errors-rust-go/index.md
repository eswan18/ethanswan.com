---
title: "Errors in Rust and Go"
slug: errors-rust-go
layout: post
date: 2023-06-26
tags:
- Rust
- Go
summary: "TODO"
---

I've been learning Rust in my free time recently.

It's full of bold design decisions that don't show up in most other popular languages, the most famous of which is the *borrow checker*, a new approach to memory management[^1].
Rust uses a style of enums that I've never encountered before, and it supports most aspects of object-oriented programming but disallows inheritance.

These must have been risky decisions at the time they were made, but I've been impressed at just how many of them feel great to use.
I've been working through last year's Advent of Code exercises in Rust and am coming to really like the language.
It's more low-level than anything I've used since college, but I feel very productive in it.
I'm definitely much slower in Rust than in Python (both due to inexperience and to the restrictions of the type system), but my code consistently has fewer bugs[^2].

Rust reminds me a lot of Go, another language I've used to a limited extent.
Go shares with Rust a spirit of *we-don't-care-if-you've-always-done-it-that-way*.
Its creators zagged on many language decisions, and even made similar decisions to Rust's team on things like disallowing inheritance and encoding nullability in the type system.

Both languages eschewed exception-style error handling, the approach used by Python, Java, JavaScript, C++, Ruby, and almost every other language common in industry.
"Exceptions" is the commonly-used term for errors that halt the currently-running function as soon as they're encountered.
The calling code can add special "handling" blocks that anticipate specific exceptions and dictate actions to be taken when they're encountered, but if there's no handling code around a function and it raises an exception, then the exception propagates up the stack to the next calling function.
If no function catches it before it surfaces at the top level of the program, the application will crash.
Earlier this year I wrote a [piece](/feed/2022/12/04/python-exceptions-basics/) detailing how Python implements exceptions, which you can reference for more details.

On the surface, Go and Rust seem similar in how they deal with errors.
There are no exceptions, and errors are returned from functions just like any other value.
However, to lay my cards on the table, I think Go's error idioms are bad and Rust's are a dramatic improvement.

Before we jump into these languages' errors, lets look at exception system and why language designers chose not to support it.

## Exceptions: full of surprises

Exceptions are very out-of-style in the language design community right now.
The claim is basically that because exceptions are a way of returning information without actually using a return value, programmers can easily forget to handle them and they make data flow harder to reason about.
And indeed, it's very easy to overlook potential exceptions; take for example this simple Python script to compute the decimal value of a fraction for a user.

```python
print("Hi, let's do fractions!")
raw_n = input("Numerator: ")
n = int(raw_n)
raw_d = input("Denominator: ")
d = int(raw_d)
result = n / d
print(result)
```

If you write code regularly, you can probably quickly spot some problems here, but do you see all of them?
There are at least three places where an error could occur:
- Parsing the numerator into an int
- Parsing the denominator into an int
- Dividing `n` by `d`, without checking that `d` isn't zero

Say the user enters `3` and `0`.
Crash!

```text
Hi, let's do fractions!
Numerator: 3
Denominator: 0
```
```text
Traceback (most recent call last):
  File "/Users/eswan18/Develop/advent-2022/15/rust/test.py", line 6, in <module>
    result = n / d
ZeroDivisionError: division by zero
```

Sure, Python is a pretty fast-and-loose language, but this problem persists in statically-typed Java[^3]:

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hi, let's do fractions!");
        Scanner scanner = new Scanner(System.in);
        System.out.print("Numerator: ");
        int n = scanner.nextInt();
        System.out.print("Denominator: ");
        int d = scanner.nextInt();
        double result = (double) n / d;
        System.out.println(result);
    }
}
```

What if the user entered values that aren't integers?
What if `d` is 0?

It's easy to miss one of these, and as programs grow larger, it's inevitable that certain error cases are forgotten.
And part of the purpose of functions is abstracting away implementation details, so you can forgive the programmer for not realizing that a certain function might return a specific type of error.
But that introduces the potential for unexpected crashes at any time.

## Errors as values: the hot new thing

So we've decided against exceptions.
What are our other options?

The C language doesn't have exceptions, but error handling is quite cumbersome.
It's been a long time since I've used C, but I recall functions returning special values like `-1` as a way to denote an error.
If your function must return an integer and there is no other way to propagate data to the calling code, that's probably your best option.
But we've come a long way since C and newer languages have pioneered different approaches.

In both Go and Rust, exceptions don't exist and errors are (mostly) treated like any other data value.
The interesting part – and the difference between the languages – is the set of features and idioms for dealing with them.
I'll show what I mean.

## Errors in Go

Here's how you'd write an idiomatic Go program that does what our Python script did:

```go
import (
	"fmt"
	"strconv"
	"bufio"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hi, let's do fractions!")

	fmt.Print("Numerator: ")
	raw_n, err := reader.ReadString('\n')
	if err != nil {
        fmt.Println("Couldn't read user input")
		os.Exit(1)
	}
	n, err := strconv.Atoi(raw_n[:len(raw_n)-1])
	if err != nil {
        fmt.Println("Couldn't convert numerator input to integer")
		os.Exit(1)
	}
	fmt.Print("Denominator: ")
	raw_d, err := reader.ReadString('\n')
	if err != nil {
        fmt.Println("Couldn't convert denominator input to integer")
		os.Exit(1)
	}
	d, err := strconv.Atoi(raw_d[:len(raw_d)-1])
	if err != nil {
        fmt.Println("Couldn't convert numerator input to integer")
		os.Exit(1)
	}

	result := float64(n) / float64(d)

	return result, nil
}
```

First of all: that's a lot of code.
Notice that every function that could encounter an error explicitly returns an `error` (conventionally stored in an `err` variable) along with its other data.
Go encourages you to write your own functions this way too.
Calling code has to explicitly assign both returned values:

```go
raw_n, err := reader.ReadString('\n')
```

Trying to do something like this will fail at compile time:

```go
raw_n := reader.ReadString('\n')
```
```text
assignment mismatch: 1 variable but reader.ReadString returns 2 values
```

Go makes an interesting choice in this regard: to treat multiple return values as completely independent, not allowing the user to assign them into a single variable as some kind of tuple or array.
That's a wise choice given this system of error propagation, since as long as you store the primary return value, you can't forget about the error value.

This explicitness makes it much harder to forget that a function could produce an error.
You are expected to always to see if `err` is `nil` afterward, and if not, take appropriate action[^4].

I'll show my cards here: I can see what the designers were going for, but I think this idea is bad for two reasons[^5]:

1. It's still too easy to forget to handle errors. And if an error does go unhandled, it can easily slip through silently and corrupt the whole application state.
2. I know it sounds silly, but it's ugly! So ugly! Half of your code is `if err != nil { return 0, err }`. Couldn't we come up with some nicer syntactic sugar for that at least?

### Forgetting to handle errors and wrecking application state

Let's say we're working with a function whose primary purpose is to modify an external system.
Imagine a `createUser` function that adds a new user to the database.
Its signature might be:

```go
func createUser(name string, email string, password string) error
```

So then we write some code to set up an account:

```go
import (
	"errors"
)

func setupAccount(user User) error {
	if emailExists(user.email) {
		return errors.New("Sorry, an account with that email exists!")
	}
	createUser(user.name, user.email, user.password)
	log("Created user")

	return nil
}
```

Seems okay, right?
And it'll compile fine.
But we forgot to assign the returned `error` value from `createUser`!
If an error prevents us from creating the user, we won't even notice.

It's all too easy to do this and I've encountered it many times in code I'm reading.
This situation is actually *worse* than exceptions, because the program will just keep running as if the user had been successfully created.
Eventually, another part of the system will probably run into trouble because of this and return an error, but it'll be hard to trace back to this source[^source].

Even in cases where the function returns a value, forgetting the `if err != nil` block is possible and can be catastrophic.

Here's a perfectly solid, idiomatic function that returns all usernames in the database, or an error if the database wasn't able to fetch them.
When it hits an error case, it returns the error along with an empty slice.

```go
func getAllUsernames(db Database) ([]string, error) {
	users, err := db.get_all_users()
	if err != nil {
		return []string{}, err
	}
	var usernames []string
	for _, user := range users {
		usernames = append(usernames, user.name)
	}
	return usernames, nil
}
```

Why do we have to include an empty slice?
Well, Go doesn't allow some kind of "invalid data" marker -- if you promised a slice of strings, you have to return a slice of strings even if there's an error (because the type system doesn't allow nulls unless explicitly noted).
Coupled with Go's approach to errors as values, that's a recipe for disaster.


Let's use this function to determine whether to let a user create an account.

```go
import (
	"github.com/golang/go/src/pkg/container/list"
)

func isUserAccountValid(db Database, user User) (bool, error) {
	if user.name == "" {
		// Can't have a zero-length username.
		return false, nil
	}
	if len(user.password) < 5 {
		// Password is insecure.
		return false, nil
	}
	existingUsernames, err := getAllUsernames(db)
	if list.Contains(existingUsernames, user.name) {
		// The username already exists.
		return false, nil
	}
	emailIsValid, err := validateEmailAddress(user.email)
	if err != nil {
		return false, err
	}
	if !emailIsValid {
		// Email address isn't valid.
		return false, nil
	}

	return true, nil
}
```

At first glance this code looks fine – we check for a variety of conditions that would preclude a user account from being created, and return errors if one of them is true.

But we missed something here: an `if err != nil` block after `getAllUsernames`.
That function returns not only a boolean value but also an error, if it was unable to access the database.
So if the database is unresponsive, `getAllUsernames` will an error along with an empty slice.


As it is, we're ignoring that error, so our code will just see an empty list of all taken usernames – and it'll give the go-ahead to create accounts with any username, even if it already exists in the database.
And that puts us in a very bad position, where our application has allowed users to do something they shouldn't be able to.
Hopefully they don't get too attached to that duplicate username we just issued!

Some language toolkits, like the Go extension for VSCode, will warn you in a situation like this because you assign to `err` twice in a row without reading from it.
But this is easy to miss, and the code will still compile.

All in all, this was a brave approach by the creators of Go but a mistake in my view[^6].
It's less common to ignore errors than it would be with exceptions, sure, but the consequences are much worse when it does happen.

For functions without non-error return values, their side effects just won't be executed and the program will proceed without noticing.
For functions that return additonal data, that additional data will likely come back as the "zero value" of its type – an empty list, a `false`, a `0`, an empty string – because Go doesn't offer any null-like abstraction for most data types.
The application will roll along with data that looks correct because it has the right type, but is actually completely wrong, and once the bug is discovered it will likely be hard to track down to the source.

Maybe if most languages took this approach then programmers would be so accustomed to it that they'd never forget to check returned errors.
But that's definitely not the world we live in.

## Errors in Rust


[^1]: The borrow checker is basically a way to encode variable lifetimes as typing information, so that most memory management decisions can be determined at compile time without a garbage collector. If that sounds like gibberish, you can understand why so many people think this is Rust's most intimidating feature.
[^2]: Though at least some of my productivity in Rust must be attributed to GitHub Copilot, which is a lifesaver when it comes to learning a new language. It has helped me get the hang of a lot of Rust idioms and often autocompletes repetitive code sections.
[^3]: I confess that I didn't write this code (ChatGPT did) and didn't test it, as I have never installed Java on my current laptop. I hope to keep it that way.
[^4]: Often, that "appropriate action" is to just return the error (or wrap it with additional metadata first, then return it). This defers the decision to the next level up of calling code.
[^5]: I wanted to add a third reason: that creating and differentiating different types of errors is very clunky. From what I can tell, it's quite common to always use `errors.New()` with a string to create new errors. That makes parsing the enclosed string the only way to tell different errors apart in the calling code. It seems to be possible to create custom error structs and to check which one is returned, but the one time I researched it I found it underdocumented online and cumbersome to implement.
[^6]: My overall view of Go is pretty negative at this point, though I reserve the right to change my mind. My thinking: if you want to change the way things have been done for decades, you'd better have good reasons (and turn out to be right). I think Go's error idioms are ultimately bad but reflect some good ideas. But its zero values, where anything uninitialized is automatically some default value, cause all kinds of bugs and seem like a worse version of null -- one that doesn't crash your program but instead corrupts all your application data. Even worse are its namespacing decisions: All files in the same package share a single namespace, so variables in different files in the package can be referenced without an import or a prefix (leading to much confusion and searching). And to export an identifier from a package or struct, you start it with a capital letter. That means that you can no longer use uppercase as a clue to what's a type and what's an instance when reading code, and that hampers readability enormously. And we already had many perfectly-good ways of marking things for export: an `export` or `pub` keyword (lots of languages) or using underscores in front of private fields/names (Python). Last, Go's built-in functionality and standard library are so limited that it can stretch belief. Checking if a slice contains an element requires installing an additional module! The Go community and creators are obsessed with minimalism and simplicity, but it's just not clear to me that limiting your options so substantially actually yields better results, and it certainly makes programming slower and more unpleasant. A lot of things about Go feel like zagging for the sake of it and being able to claim some kind of language purity, rather than just building the most usable language.
[^source]: Because we won't get a real traceback – errors as values don't automatically wrap themselves in a call stack the way exceptions in most languages do, since the language just passes them around like regular data and mostly doesn't touch them.