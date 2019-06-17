$ post_id : func-prog
$ post_title : 02: Functions in Python
$ post_group : 99: Unsorted chapters
$ post_last_update: 2019-06-17

## Functions as first-class objects

There is a built-in function, `dir`, that return what attributes--methods and variables--are present in an object. Let us try it out on an integer and a string.

```
>>> an_int=5
>>> dir(an_int)
['__abs__', '__add__', '__and__', '__bool__', '__ceil__', '__class__', '__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getnewargs__', '__gt__', '__hash__', '__index__', '__init__', '__init_subclass__', '__int__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__xor__', 'bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes']

>>> a_string="Hello World"
>>> dir(a_string)
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
>>>
```

How about our `vector`-class implementation?

```
>>> dir(vector)
['__abs__', '__add__', '__and__', '__ceil__', '__class__', '__complex__', '__delattr__', '__dict__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__iand__', '__ifloordiv__', '__ilshift__', '__imatmul__', '__imod__', '__imul__', '__index__', '__init__', '__init_subclass__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__', '__isub__', '__itruediv__', '__ixor__', '__le__', '__lshift__', '__lt__', '__matmul__', '__mod__', '__module__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmatmul__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__weakref__', '__xor__']
```

The stuff in the above output seems familiar. Most of these are the methods we have implemented (or `NotImplemented`). There are a few that we do not recognise as of now.

How about the function `dir` itself?

```
>>> dir(dir)
['__call__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__text_signature__']
```

In essence, the entity `dir` is no different than `an_int`, `a_string` or `vector`. They all contain different things but structurally they are treated like each other--they are all objects.

## Lambda--the anonymous, single-line functions

Just like most functional programming languages, Python gives us the tools to define anonymous functions using the `lambda` keyword. The syntax is like this--

`lambda arg1, arg2, arg3,... : <return expression>`

In order to illustrate this, let us write a function two add two objects--one using `def` and the other using `lambda`.

```
>>> def add(a, b):
...    return a+b
...

>>> add_lambda = lambda a, b: a+b

>>> add(1,2)
3
>>> add_lambda(1,2)
3
```

They both behave the same way. In fact, `dir(add)` and `dir(add_lambda)` would display the same results. The only way to know which is which is to check the `__name__` attribute of both functions.

```
>>> add.__name__
'add'
>>> add_lambda.__name__
'&lt;lambda&gt;'
```

Python functions implement the concept of lazy evaluation.

To test it out, we can use a simple sinusoidal function \\(y = A \cos (\omega t + \phi) \\). There are four variables whose value must be provided in order for the function to be evaluated--

```
>>> w=lambda a, omega, t, phi: a*math.sin(omega*t+phi)
>>> w(1,1,2.5,0)
&lt;Traceback message&gt;
NameError: name 'math' is not defined

>>> import math
>>> w(1,1,2.5,0)
0.5984721441039565
```

We can safely write our function, which depends on the `math` module, without importing it. Python doesn't check if any dependency has been imported into the current namespace while declaring the function. Only when it tries to evaluate the function, it checks if everything is available.

This opens the door for partially applied functions as well. We can now use our pre-defined function `w` and write a sinusoidal function that has a frequency (`omega`) of 1.0 and an offset (`phi`) of 0.0.

```
>>> w_f1_o0=lambda a, t: w(a, 1.0, t, 0.0)
>>> w_f1_o0(1,2.5)
0.5984721441039565
```

This is the same value we saw in the earlier code block. Needless to say, the feature extends to full-fledged `def` constructs as well. This will come in handy when we study about decorators.

Anyone who has dabbled with Haskell or Lisp would know that it is possible to write fully-functional programs with this construct alone--including decision trees and loops replaced by recursive constructs. Since Python is a multi-paradigm language and encourages side-effects (change of state), it would be an over-the-top exercise to demonstrate programs without side-effects even if it is possible. Instead, we will try to focus on how functions--including anonymous ones--can be used in Python.

## Map, Filter, and Reduce

We now focus our attention to three things that were ported from the family of traditional functional programming languages. The first one is `map`.

`map` takes a function and iterables as its arguments, and returns another iterable whose values are the results of the function applied to individual objects yielded by the input iterables. Let's say that we have a function \\(f\\) that is defined as \\(f=f(x_1,x_2,x_3,...)\\). If we had a chain of values for \\(x_1\\), \\(x_2\\), \\(x_3\\), etc. we could obtain a chain of values by applying the function \\(f\\) on each of the corresponding values in \\(x_1\\), \\(x_2\\), \\(x_3\\), etc. In the world of Python, if `g=map(f, x1, x2, x3,...)`, then `g[0]=f(x1[0], x2[0], x3[0],...)`, `g[1]=f(x1[1], x2[1], x3[1],...)` and so on.

Let us use our `w_f1_o0` function that takes two arguments and feed it with the simplest form of iterators--i.e, lists.

```
>>> pi=math.pi
>>> a = [1]*5 + [2]*5
>>> t=[0, pi/4, pi/2, 3*pi/4, pi]*2

>>> map(w_f1_o0, a, t)
&lt;map object at 0x7f17c9eb79b0&gt;

>>> list(map(w_f1_o0, a, t))
[0.0, 0.7071067811865475, 1.0, 0.7071067811865476, 1.2246467991473532e-16, 0.0, 1.414213562373095, 2.0, 1.4142135623730951, 2.4492935982947064e-16]
```

We have constructed a list of amplitudes, `a=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2]`, and time points, `t=[0, pi/4, pi/2, 3*pi/4, pi, 0, pi/4, pi/2, 3*pi/4, pi]`. Both have a length of ten. The map function actually doesn't return a result but a map object which will be evaluated only if we ask of it; which is exactly what happens when we force it to be converted into a list object. The output is `[w_f1_o0(1, 0), w_f1_o0(1, pi/4), w_f1_o0(1, pi/2),...]`. The function `w_f1_o0` is applied until the shortest iterator is exhausted. Mark the word "shortest". The evaluation of map function terminates when any of the argument iterators exhausts itself.

Just to test out the exhaustion of shortest iterator, we can shorten the length of `a` to eight and run a test. (`t` is still of length ten.)

```
>>> a = [1]*5 + [2]*3
>>> list(map(w_f1_o0, a, t))
[0.0, 0.7071067811865475, 1.0, 0.7071067811865476, 1.2246467991473532e-16, 0.0, 1.414213562373095, 2.0]
```

As expected, the output is of length eight.

The `map` function's lazy evaluation is best exhibited when it is called as an iterator in a for-loop. We will use the enumerate function which will return an index and truncate the loop after the first five occurrences.

```
>>> for i, val in enumerate(map(w_f1_o0, a, t)):
...     if i>4:
...         break
...     print(val)
...
0.0
0.7071067811865475
1.0
0.7071067811865476
1.2246467991473532e-16
```

At no point is the sixth, seventh, and eight value evaluated as Python never gets to call `w_f1_o0(2, 0)`, `w_f1_o0(2, pi/4)`, and `w_f1_o0(2, pi/2)`.

The `filter` function takes in a predicate function, and an iterable and returns another another iterable in which the items are satisfied to be true by the predicate function. Think of the predicate function as something that takes in an object and returns `True` or `False`. In the chain of values of the input iterable, the predicate function acts like a gatekeeper and returns another iterable whose chain of values yield `True` against the predicate function.

Let us test it out on a list of numbers with a predicate function that tests if the number is even.

```
>>> input = list(range(10))
>>> input
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> is_even = lambda x: x%2==0
>>> filter(is_even, input)
&lt;filter object at 0x7fc748723160%gt;

>>> list(filter(is_even, input))
[0, 2, 4, 6, 8]
```

Just like `map` function, `filter` doesn't evaluate the values unless asked and instead returns a filter object.

It is possible to pass `None` as the function in filter. In that case, the expression `bool(item)` is used as a predicator where `item` is the object returned by the input iterator.

If we try it out on the same input, we get this--

```
>>> list(filter(None, input))
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

This is because `bool(0)` is `False`; for all other cases, it returns `True`. If we are writing our own class, we will have to define how bool built-in function would behave on an instance of that class. This can be done by defining the `__bool__` function inside the class.

What if the function is not a predicate function? Here is an example--

```
>>> is_odd = lambda x: x%2
>>> list(filter(is_odd, input))
[1, 3, 5, 7, 9]
```

The output of `is_odd` is not `True` of `False`. What Python does is force the most trivial predicate function on the output--the `bool` function. In this case, is_odd will either return a `0` or `1`. `bool(0)` and `bool(1)` yields `False` and `True` respectively. This is exactly what is used to filter.

The `reduce` function is an example of a "fold" function that we might find in Lisp or Haskell. In Python 2 it is a built-in function. Sadly, it's status as a built-in has been downgraded in Python 3 by none other than Guido van Rossum--the creator of Python--himself. You can read about it [here](https://www.artima.com/weblogs/viewpost.jsp?thread=98196). In order to call `reduce` in Python 3 we must import it from a library called `functools`.

\\(reduce(f, [x_1, x_2, x_3,...])\\), where \\([x_1, x_2, x_3,...]\\) is an iterator (not necessarily a list), and \\(f=f(p,q)\\) is a function that takes two arguments of similar type and returns one object of the same type, is equivalent to \\(f(...f(f(f(x_1, x_2),x_3),...)\\)

We can actually use it to calculate the magnitude of an n-dimensional vector that is defined by a `list`, or a `tuple` (or our very own `vector` although it only supports three-dimensional ones).

```
>>> from functools import reduce
>>> import math

>>> f = lambda x, y: math.sqrt(x**2 + y**2)
>>> a = [0.5, -0.4, 2, 0.5, -0.7]

>>> mag = reduce(f, a)
>>> print(mag)
2.2693611435820435
```

In essence, we are taking two adjacent entities of the summation and computing that before plugging that into the next cycle of computation.

$$|a| = \sqrt{\sum_{i=1}^n a_i^2} = \sqrt{...(\sqrt{(\sqrt{a_1^2 + a_2^2})^2 + a_2^2})^2 +...+a_n^2}$$

It is important to note that `f = lambda x, y: math.sqrt(x**2 + y**2)` is a valid fold function as the arguments are numbers and the output is also a number, thus fulfilling the type similarity condition. Python does the operation until the list (or the iterator) runs out of values.

As another example, let us try to emulate the `join` method of strings.

```
>>> s = ["I", "am", "a", "broken", "sentence."]
>>> join = lambda delim: lambda x, y: x+delim+y

>>> reduce(join(" "), s)
'I am a broken sentence.'

>>> reduce(join("_"), s)
'I_am_a_broken_sentence.'
```

This is a good example of nested functions. `join("delimeter")` returns not a value but a function `lambda x, y: x+"delimeter"+y` that can be used as a fold function in our `reduce`.

There is also a variant of the function where an initial value can be provided as the third argument of the `reduce` function. \\(reduce(f, [x_1, x_2, x_3,...], x_0)\\) is equivalent to \\(f(...f(f(f(f(x_0, x_1), x_2),x_3),...)\\).

## A Pythonic usage of functions--sorting
