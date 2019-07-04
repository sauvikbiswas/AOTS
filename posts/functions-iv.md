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

Let us say that we have a very large Python file called `vectors.py`. It contains a lot of functions. In Unix (or Unix-like systems) it is very easy to count the number of such functions. Here's one way to do it--

```
$ cat vectors.py | grep "^\s\+def " | wc -l
64
```

The contents of the file--line by line--is the output to `cat vectors.py`; which is fed as input to `grep "^\s\+def "` to filter those lines which match our RegEx; which in turn is fed into `wc -l` to count the number of lines.  Piping of output as input to a command is a fundamental concept of Unix. These pipelines are very similar to those built by generators, where the output of a generator is passed to the next. Let us try to emulate this behaviour.

~~~~
import re
def cat(filename):
    with open(filename, 'rU') as fp:
        while True:
          line = fp.readline()
          if not line:
              break
          else:
              yield line

def grep(regexp, str_gen_in):
    for line in str_gen_in:
        match = re.findall(regexp, line)
        if match:
            yield match

def wc_l(str_gen_in):
    return len(list(str_gen_in))
~~~~

The above method is a very convoluted and incomplete method of creating a proxy for the `cat` and `grep` command in Python. It's only for illustrative purposes.

We can chain these functions to create a pipe.

```
>>> wc_l(grep("^\s+def ", cat("vectors.py")))
64
```

The function `wc_l` is not a generator and has a `return` instead of `yield`. This is to consolidate the data from the generators. In fact, we are forcing `wc_l` to evaluate all the yields of the input generator by converting it into a list. The other two functions are effectively piped before `wc_l` just like the Unix command we saw earlier.

For the Python `cat` function, the generator stops when line returns an empty string. For the Python `grep` function, the generator pulls from `str_gen_in` only if `match` is not an empty list and stops when `str_gen_in` is exhausted.

One can build useful applications using this concept. Parsing large text files (like logs) and processing incoming data streams would be some of the more interesting usages of this concept.
