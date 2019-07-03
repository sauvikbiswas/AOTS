$ post_id : functions-iv
$ post_title : 04: Generator functions
$ post_group : 01: Functions
$ post_last_update: 2019-06-22

## Generator functions

We now know that once the interpreter executes a `return` statement in a function, the control is given back permanently to the place where the function was called from. Sure, we may be able to access some values of this expired function using closures. Sometimes it is necessary to pass the control back to the function even after the caller has received something from the function. This is where a different keyword comes into play--`yield`.

In order to understand this, let us write a function.

~~~~
def yield_demo():
    yield 1
    yield "two"
    yield 3.0
~~~~

There is no `return` statement here. In fact, Python 2 doesn't allow mixing yield and return and throws a `SyntaxError`. Python 3 is slightly forgiving and treats `return` as a syntactic sugar for raising a `StopIteration` exception.

```
>>> g=yield_demo()
>>> print(g)
<generator object yield_demo at 0x7f5af3a51db0>
>>> next(g)
1
>>> next(g)
'two'
>>> next(g)
3.0
>>> next(g)
&lt;Traceback message&gt;
StopIteration
```

The first thing we notice is that `yield_demo` doesn't return a value when called. Instead, it returns a generator object whose subsequent value must be extracted using the `next` built-in function.

Where does the persistence of function come into play? Take a look at the line `next(g)` and the output is `1`. At this point, Python has executed the line `yield 1` in the execution instance `yield_demo` that has been bound to a generator object `g`. Although the control of execution is send back to Python's REPL shell, the state of that particular execution instance of `yield_demo` is still in the memory. When `next(g)` is called again, the execution resumes from the last encountered yield statement. This goes on until no more yield is available and Python automatically raises a `StopIteration` exception.

The simplest way to call `next` is not to use use the `next` statement itself but instead use a `for` loop.

```
>>> g=yield_demo()
>>> for item in g:
...     print(item)
...
1
two
3.0
```

`for` statement uses the `StopIteration` exception to terminate loop. In case a for loop doesn't catch any  item, it may mean that the generator has been exhausted. This can occur if a few `nexts` or some `for` loops have already extracted some items from the generator earlier.

## Pipelines using generators

It is possible to chain generators. A generator function can in turn call another generator function which in turn can call another, and so on. In this fashion, we can build pipelines.

Here is a piece of code that generates a Bruce Lee and a Neil Gaiman quote line-by-line. It also has a generator function `count_word` that takes in a generator function, receives a yielded line, counts the number of words and yields that.

~~~~
def source_lee():
    quote = ["Empty your mind, be formless, shapeless, like water.",
            "If you put water into a cup, it becomes the cup.",
            "You put water into a bottle and it becomes the bottle.",
            "You put it in a teapot it becomes the teapot."
            "Now, water can flow or it can crash.",
            "Be water my friend."]
    for line in quote:
        yield line

def source_gaiman():
    quote = ["Husband runs off with a politician? Make good art.",
            "Leg crushed and then eaten by mutated boa constrictor? Make good art.",
            "IRS on your trail? Make good art.",
            "Cat exploded? Make good art.",
            "Somebody on the Internet thinks what you do is stupid or evil or it's all been done before? Make good art.",
            "Probably things will work out somehow, and eventually time will take the sting away, but that doesn't matter.",
            "Do what only you do best. Make good art."]
    for line in quote:
        yield line

def count_word(source):
    gen_source=source()
    for line in gen_source:
        yield len(line.split(" "))
~~~~

We can now chain generators to create a master generator.

```
>>> wc_lee = count_word(source_lee)
>>> next(wc_lee)
8
>>> next(wc_lee)
11
>>> next(wc_lee)
11
>>> wc_gaiman = count_word(source_gaiman)
>>> next(wc_gaiman)
9
>>> next(wc_gaiman)
12
>>> next(wc_lee)
17
```

The `next` call propagates itself down the nested generators and pulls up the data while each generator (in this case, `count_word`) processes the data (in this case, counts words) and passes it on.

This is very similar to building Unix pipelines.
