---
title: "Errors as Values in Rust and Go"
slug: errors-as-values-rust-go
layout: post
date: 2023-07-10
tags:
- Rust
- Go
- Programming Languages
summary: "Rust reminds me a lot of Go. Both languages eschewed exception-style error handling, a feature present in almost every language that's popular in industry. However, the idioms they use instead are very different."
---

I've been learning Rust in my free time recently.

It's full of bold design decisions that don't show up in most other popular languages, the most famous of which is the *borrow checker*, a new approach to memory management[^1].
Rust uses a style of enums that I've never encountered before, and it disallows inheritance despite supporting most other aspects of object-oriented programming.

Rust reminds me a lot of Go, a language I use regularly in my job.
Go shares a willingness to change the way things have been done for decades in language design: it too doesn't support inheritance and restricts the presence of nulls using the type system.

Both languages also eschewed exception-style error handling[^exceptions], a feature present in almost every language that's popular in industry.
However, the idioms they use instead are very different.
Now that I've used both languages a fair amount, I think that Go's approach is bad and Rust's is a dramatic improvement.
I'll discuss both.

Let's start by looking at the traditional exception system and why language designers might choose not to support it.

## Exceptions: full of surprises

Exceptions are very out-of-style.
They're fundamentally a way of returning information from within a function through a mechanism other than the return value, so (the claim goes) they make data flow harder to reason about and to anticipate.

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

If you write code regularly, you can probably spot some problems here, but do you see all of them?
There are at least three places where an error could occur:
- Parsing the numerator into an int
- Parsing the denominator into an int
- Dividing `n` by `d`, without checking that `d` isn't zero

Say the user enters `3` for the numerator and `0` for the denominator.
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

Sure, Python is a pretty fast-and-loose language, but this problem persists in statically-typed Java[^gpt-java]:

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
Again: crash!

Ideally, chunks of code that could produce an excption would be wrapped in special handling code at some level.
In Python that might look like this:

```python
import sys

print("Hi, let's do fractions!")

raw_n = input("Numerator: ")
try:
	n = int(raw_n)
except ValueError:
	print("Invalid input. You must enter an integer.")
	sys.exit(1)

raw_d = input("Denominator: ")
try:
	d = int(raw_d)
except ValueError:
	print("Invalid input. You must enter an integer.")
	sys.exit(1)

try:
	result = n / d
except ZeroDivisionError:
	print("Invalid input. Your denominator can't be zero.")

print(result)
```

It's easy to forget a try/except block though, and as programs grow larger, it's inevitable that certain error cases are missed.
Additionally, the programmer is expected to know that the specific type of error that could be raised (like how `int()` an produce a `ValueError`).

It's a lot to ask, but mistakes here lead to the potential for unexpected crashes at runtime.

## Errors as values: the hot new thing

If we've decided against exceptions in favor of only sending back data from our function via the return value, how can we represent error states?

This is sometimes called "errors as values", since errors are treated just like any other data type in the language and there are a few different ways to implement it.
Let's look at both Go and Rust.

### Errors in Go

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
        fmt.Println("Couldn't read user input")
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

First of all: that's a lot of code[^unhandled-go-error].
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

Go makes an interesting choice in this regard: to treat multiple return values as completely independent, not just parts of a larger tuple or array that can be assigned into a single variable.
That's a wise choice given this system of error propagation, since it makes it difficult to store the main return value and forget about the error value.

This explicitness makes it less likely that the programmer forgets that a function could produce an error.
You are expected to always to see if `err` is `nil` afterward, and if not, take appropriate action[^appropriate-action].

I'll show my cards here: I can see what the designers were going for, but I think this idea is bad for two reasons[^custom-errors-go]:

1. It's *still* too easy to forget to handle errors. And if an error does go unhandled, it can easily slip through silently and corrupt the whole application state.
2. I know it sounds silly, but it's ugly! So ugly! Half of your code is `if err != nil { return 0, err }`. Couldn't we come up with some nicer syntactic sugar for that at least?

### Forgetting to handle errors and wrecking application state

Let's say we're working with a function whose primary purpose is to modify an external system.

Imagine a `createUser` function that adds a new user to the database.
It takes in a few details about the user and return an error value.

```go
func createUser(name string, email string, password string) error
```

So then we write some code to set up an account:

```go
import "errors"

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
Eventually, another part of the system will probably request details about the user and run into trouble.
At that point an error will finally be returned (hopefully), but it'll have occurred in a completely different part of the system so tracing it back to the source will be difficult[^source].

Even in cases where the function returns a value, forgetting the `if err != nil` block is possible and can be catastrophic.

Here's a perfectly solid, idiomatic function that returns all usernames in the database, or an error if the database wasn't able to fetch them.
If it hits an error case, it returns the error along with an empty slice.

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
Well, Go doesn't allow some kind of "invalid data" marker -- if you promised a slice of strings, you have to return a slice of strings even if there's an error (because the type system doesn't allow nulls unless explicitly noted)[^slice-strings].
Coupled with Go's approach to errors as values, that's a recipe for disaster.


Let's use this function to as part of our code that checks whether to allow a user to create an account.

```go
import "github.com/golang/go/src/pkg/container/list"

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

At first glance this code looks fine – we check for a variety of conditions that would preclude a user account from being created, and return false if so.
If we run into an error, we return that along with `false` (again, there's no way to avoid returning a valid value along with the error).

But we missed something here: an `if err != nil` block after `getAllUsernames`.
So if the database is unresponsive and `getAllUsernames` returns an error along with an empty slice, then we'll just carry on as if it correctly returned an empty list of usernames.
It'll give the go-ahead to create accounts with any username, even if it already exists in the database.

And that puts us in a very bad position, where our application has allowed users to do something they shouldn't be able to.
Hopefully they don't get too attached to that duplicate username we just issued!

Some language toolkits, like the Go extension for VSCode, will warn you in a situation like this because you assign to `err` twice in a row without reading from it.
But this is easy to miss, and the code will still compile.

All in all, this was a brave approach by the creators of Go but a big mistake in my view[^negative-view-go].
It's less common to ignore errors than it would be with exceptions, sure, but the consequences are much worse when it does happen.
I think I actually prefer exceptions to this error-handling model.

Some functions that are useful only for side effects will typically return an error value and nothing else.
Programmers often forget to assign their output to a variable at all, in my experience, so the side effects may silently fail.

For functions that return additonal data, that additional data will likely come back as the "zero value" of its type – an empty list, a `false`, a `0`, an empty string – because Go doesn't offer any null-like abstraction for most data types.
The application will roll along with data that *looks* correct because it has the right type, but is actually completely wrong, and once the bug is discovered it will likely be hard to track down to the source.

Maybe if most languages took this approach then programmers would be so accustomed to it that they'd never forget to check returned errors.
But that's definitely not the world we live in.

## Errors in Rust

Now let's go back to our earlier example of a script that lets a user input a numerator and denominator to be divided.
Here's a Rust version:

```rust
use std::io::{self, Write};
use std::process;

fn get_number_input(prompt: &str) -> Result<i32, String> {
    let stdin = io::stdin();
    let mut stdout = io::stdout();
    print!("{}", prompt);
    stdout.flush().map_err(|e| e.to_string())?;

    let mut input_buffer = String::new();
    stdin.read_line(&mut input_buffer).map_err(|e| e.to_string())?;

    let number = input_buffer.trim().parse::<i32>().map_err(|e| e.to_string())?;
    Ok(number)
}

fn main() {
    let numerator = match get_number_input("numerator: ") {
        Ok(number) => number,
        Err(e) => {
            println!("Exiting due to error: {}", e);
            process::exit(1);
        }
    };
    let denominator = match get_number_input("denominator: ") {
        Ok(number) => number,
        Err(e) => {
            println!("Exiting due to error: {}", e);
            process::exit(1);
        }
    };

    let quotient = numerator / denominator;
    println!("Answer: {}", quotient);
}
```

Just on readability, I think we have to give Go some props after seeing this Rust code.
Rust has lots of constructs and patterns that aren't obvious until you've learned them, and this code is probably hard to decipher if you don't know Rust.

Let's break down some potentially-confusing bits.

```rust
fn get_number_input(prompt: &str) -> Result<i32, String>
```

Our `get_number_input` function takes a reference to a string and returns a `Result`.
`Result`s are Rust's convention for returning errors as values, and I haven't encountered a similar construct in any other language.

A `Result` can *either* hold an `Ok` value (indicating that the function returned without errors) *or* an `Err` value (indicating a failure)[^results-are-enums].
In order to extract either of those values from a `Result`, we have to write code that handles both[^result-handle-both].

That's pretty abstract, so let's look at it in action.

```rust
let numerator = match get_number_input("numerator: ") {
	Ok(number) => number,
	Err(e) => {
		println!("Exiting due to error: {}", e);
		process::exit(1);
	}
};
```

This construct is common in Rust but a bit jarring if you come from another language.
It calls `get_number_input` and then "matches" its `Result`.

If the `Result` contains an `Ok` value – so the function ran successfully – it extracts the returned value from the `Ok`, and that value is what gets assigned to the `numerator` variable.
If the `Result` was actually an `Err`, it extracts the contents of the error (a string in this case) and prints a message before exiting.

There is no way to have both a return value and an error value present -- every `Result` is *either* an `Ok` with a return value *or* an `Err` with an error value.
To "look" at which one it is, we have to write code that handles both.

This is completely different from Go's approach.
Remember that in Go, we had to always return an error *alongside* our regular return values, and the calling code would store the error in its own variable.

```go
usernames, err := getAllUsernames(db)
```

In this code, the `usernames` variable will always be created and we could try to read from it without first checking the value of `err`.

```go
if len(usernames) == 0 {
	fmt.println("No users, let's shut down the app")
}
```

In Rust, a mistake like this doesn't really even make sense because using `match` forces us to explicitly write code for both cases -- and the code path for errors doesn't have access to the `usernames` value.

```rust
result = get_usernames(db);
let usernames = match result {
	Ok(usernames) => usernames,
	Err(e) => panic!(e)
}
```

The Rust compiler won't even let you write a `match result` construct without checking both cases.
Say we called `get_numerator` and matched its result without an `Err` case:

```rust
let numerator = match get_number_input("numerator: ") {
	Ok(number) => number,
};
```

```text
error[E0004]: non-exhaustive patterns: `Err(_)` not covered
   --> src/main.rs:18:27
    |
18  |     let numerator = match get_number_input("numerator: ") {
    |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ pattern `Err(_)` not covered
    |
note: `Result<i32, String>` defined here
   --> /Users/eswan18/.rustup/toolchains/stable-aarch64-apple-darwin/lib/rustlib/src/rust/library/core/src/result.rs:512:5
    |
503 | pub enum Result<T, E> {
    | ---------------------
...
512 |     Err(#[stable(feature = "rust1", since = "1.0.0")] E),
    |     ^^^ not covered
    = note: the matched value is of type `Result<i32, String>`
help: ensure that all possible cases are being handled by adding a match arm with a wildcard pattern or an explicit pattern as shown
    |
19  ~         Ok(number) => number,
20  ~         Err(_) => todo!(),
    |
```

This approach to errors is new to me and I love it.

There are ways to get around it though;
`match` isn't the only way to convert `Result`s into the values they hold.
There are numerous methods, the simplest of which is `.unwrap()`.
"Unwrapping" a result extracts its `Ok` value without acknowledging the `Err` possibility in any way, so the program will just crash if it runs into an `Err` at runtime.

```rust
// In this case, `numerator` will be the `i32` value returned by the
// function as long as it doesn't error.
let numerator = get_number_input("numerator: ").unwrap()
```

This is handy when you're in a hurry and not trying to write terribly robust code.
But it still requires explicitly calling an extra method.

Adding `.unwrap()` in Rust is like *omitting* `if err != nil { ... }` in Go.
While the latter is extra code that needs to be added (and can easily be forgotten), the former is a conscious decision and – in some sense – an acknowledgement of the risk.

Rust also has no compunction about adding syntactic sugar (again, in stark contrast to Go).
It has a wonderfully convenient `?` operator, which we used in our `get_number_input` function.

```rust
let number = input_buffer.trim().parse::<i32>().map_err(|e| e.to_string())?;
```

This line gets the user's input, trims whitespace off the sides, and then tries to parse it as an `i32` (an integer).
`.parse()` returns a `Result` though, not a bare `i32`, so we need to handle the potential error case before we can extract the parsed integer.
We do that with `.map_err()`, which (if the `Result` is an `Err`) converts the value to a string.

Then we can use a `?` at the very end.
This tells Rust to extract the `Result`'s value if it was an `Ok`.
But if it was an `Err`, Rust will return the error from the function immediately (wrapped in a `Result` so that it still conforms to the function's annotated return type).

That is, it's the same as this code:

```rust
let result = input_buffer.trim().parse::<i32>()
let number = match result {
	// Extract Ok values to use them in the variable assignment.
	Ok(number) => number,
	// If we get an error, just return it immediately.
	Err(e) => return e.to_string(),
}
```

The question mark seems like a small feature but turns out to simplify a lot of code.
It allows you to handle error cases very tersely, keeping the "happy path" still very apparent to the readers of the code.

Here's a function I wrote recently while working on Advent of Code.

```rust
pub fn scenic_score(&self, x: usize, y: usize) -> Result<usize, String> {
	let current_tree = self.at(x, y)?.clone();

	let trees_left = self.left_of(x, y)?;
	let visible_left = take_until_inclusive(&trees_left, |t| t >= &current_tree);
	let left_score = visible_left.len();

	let trees_right = self.right_of(x, y)?;
	let visible_right = take_until_inclusive(&trees_right, |t| t >= &current_tree);
	let right_score = visible_right.len();

	let trees_above = self.above(x, y)?;
	let visible_above = take_until_inclusive(&trees_above, |t| t >= &current_tree);
	let above_score = visible_above.len();

	let trees_below = self.below(x, y)?;
	let visible_below = take_until_inclusive(&trees_below, |t| t >= &current_tree);
	let below_score = visible_below.len();

	Ok(left_score * right_score * above_score * below_score)
}
```

Look how many question marks are just quietly nestled in there.
If I had to write a `match` statement every time, this code would be much longer and harder to read.
As it is though, we can clearly see that the successful result of `self.left_of(x, y)` should be assigned to `trees_left`.
And the error case is quietly handled with the simple `?`, removing a lot of non-happy-path noise in the logic.

Imagine what this would look like in Go!
It would probably be at least twice as long (and maybe twice as likely to have a mistake).

There are a lot of helper methods on `Result`s beyond `.unwrap()`, such as `.map_err()` that we used above.
It takes some time to get familiar with the options, but once you do, dealing with errors becomes really elegant – without increasing the chance of overlooking them.


## Overall Thoughts

I'm no expert in either of these languages, and honestly am still much more familiar with the exception system than with errors-as-values implementations.
My experience with Go is limited to a single institution, so my observations about common mistakes and poor practice may not be representative in the wider world.
And my use of Rust has been on smaller, toy projects – so it's possible that I just haven't been involved in a large enough codebase (or seen enough legacy code) for the weaknesses of its error approach to shine through.

That said, I have confidence asserting:

- Rust's error system makes a programmer much less likely to overlook errors.
- The Go system can easily lead to invalid data (zero values) flowing through a system in dangerous ways.

I would be surprised if the next decade's new languages didn't borrow[^borrow] more idioms from Rust.



[^1]: The borrow checker is basically a way to encode variable lifetimes as typing information, so that most memory management decisions can be determined at compile time without a garbage collector. If that sounds like gibberish, you can understand why so many people think this is Rust's most intimidating feature.
[^exceptions]: "Exceptions" are errors in Python, Java, JavaScript, C++, Ruby, and almost every other language common in industry. The term specifically denotes errors that halt the currently-running function as soon as they're encountered and escalate up the function stack automatically. Calling code can add special "handling" blocks that anticipate specific exceptions and dictate actions to be taken when they're encountered, but if there's no handling code around a function and it raises an exception, then the exception propagates further up the stack to the next calling function. If no function catches it before it surfaces at the top level of the program, the application will crash. Earlier this year I wrote a [piece](/feed/2022/12/04/python-exceptions-basics/) detailing how Python implements exceptions, which you can reference for more details.
[^gpt-java]: I confess that I didn't write this code (ChatGPT did) and didn't test it, as I have never installed Java on my current laptop. I hope to keep it that way.
[^unhandled-go-error]: And in fact, we didn't even deal with one of the potential errors: the risk of dividing by zero. This is an instructive example of the limits of the errors-as-values approach. The division operation isn't a function, so it can only yield one value; if an error happens to occur, as it would when zero is the demonimator, the program will crash (or "panic" in Go parlance) at runtime.
[^appropriate-action]: Often, that "appropriate action" is to just return the error (or wrap it with additional metadata first, then return it). This defers the decision to the next level up of calling code.
[^custom-errors-go]: I considered adding a third reason: that creating and differentiating different types of errors is very clunky. From what I can tell, it's quite common to always use `errors.New()` with a string to create new errors. That makes parsing the enclosed string the only way to tell different errors apart in the calling code. It seems to be possible to create custom error structs and to check which one is returned, but the one time I researched it I found it underdocumented online and cumbersome to implement. However, I might just not be aware of the "best practice" for this and my narrow exposure to Go (pretty much only through work) might mean that I haven't encountered some modern patterns.
[^negative-view-go]: My overall view of Go is pretty negative, though I reserve the right to change my mind. If you want to change the way things have been done for decades, you'd better have good reasons (and turn out to be right). In the case of errors specifically, I think Go's idioms are ultimately bad but reflect some good ideas. However, many other aspects of the language are just clearly worse than the existing standars. Using `iota` instead of `enum` is sort of nifty, though not worth the confusion of introducing an unfamiliar language feature. But its zero values, where anything uninitialized is automatically some default value, cause all kinds of bugs and seem like a worse version of null -- one that doesn't crash your program but instead corrupts all your application data before you even notice. Even worse are its namespacing decisions: All files in the same package share a single namespace, so variables in different files in the package can be referenced without an import or a prefix (leading to much confusion and searching). To export an identifier from a package or struct, you start it with a capital letter. But that means that you can no longer use uppercase as a clue to what's a type and what's an instance when reading code, hampering readability enormously. We already had perfectly-good ways of marking things for export: an `export` or `pub` keyword (lots of languages) or using underscores in front of private fields/names (Python), all of which are more explicit. Last, Go's built-in functionality and standard library are so limited that it can stretch belief. Checking if a slice contains an element requires installing an additional module! The Go community and creators are obsessed with minimalism and simplicity, but it's just not clear to me that limiting your options so substantially actually yields better code, and it certainly makes programming slower and more unpleasant. A lot of things about Go feel like zagging for the sake of it and fixating on a notion of language purity, rather than just building the most usable language.
[^source]: Finding the root cause of errors is especially tricky because errors as values don't automatically wrap themselves in a call stack the way exceptions in most languages do, since the language just passes them around like regular data and mostly doesn't touch them.
[^slice-strings]: Experienced Go users may correctly disagree with this characterization. In fact, a slice of strings is a pointer value in Go, so it *can* be `nil` – returning `nil, err` in this function would work fine. The problem is that a `nil` value of type `[]string` is nearly indistinguishable from an empty slice, so it doesn't do much good: passing either to `len()` yields 0, and appending to either does the same thing (create a 1-element slice with the new item). This is another odd choice by Go's designers.
[^results-are-enums]: For simplicity, I'm glossing over the general construct that `Result` derives from: `Enum`. An appealing part of Rust is that it uses enums as the standard idiom for errors-as-values and for nullable values, two tricky issues for language designers. And enums are a handy feature on their own! It's a really elegant approach that I appreciate as a programming language nerd.
[^result-handle-both]: That's a slight simplification, as you can extract `Ok` values with a method like `.unwrap()`, but doing this means explicitly accepting that your program will crash if the `Result` turns out to hold an `Err` at runtime. So the simple `match` construct is a better starting point for thinking about error handling in Rust.
[^borrow]: Just one borrow pun for anyone who was waiting.