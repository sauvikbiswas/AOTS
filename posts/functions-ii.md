$ post_id : functions-ii
$ post_title : 02: Arguments and calls to a function
$ post_group : 01: Functions
$ post_last_update: 2019-06-18

## Arguments to Python functions

In the previous section, we had encountered two functions that had some optional arguments--the `reduce` function with its optional initial value and the `sorted` function with its optional key function and reverse flag.

Let us try to write rewrite our earlier sinusoidal function \\(y = A \cos (\omega t + \phi) \\). This time if time, \\(t\\), or offset, \\(\phi\\), is not specified, we will assume them to be 1 and 0 respectively.

~~~~
import math
def w(a, omega, t=1, phi=0):
    return a*math.sin(omega*t+phi)
~~~~

Let us do some test runs--

```
>>> w(1,2.5,1,3.14)
-0.599747328794043

>>> w(1,2.5,1,0)
0.5984721441039565

>>> w(1,2.5,1)
0.5984721441039565

>>> w(1,2.5)
0.5984721441039565
```

The last three calls are identical. In the absence of any value for our third and fourth positional argument, `t` and `phi`, Python takes the default value of 1 and 0 respectively.

What if we want to specify the value of `phi` but use the default value of `t`?

```
>>> w(1,2.5,phi=3.14)
-0.599747328794043
```

Here, `phi` must be passed as a named argument or keyword argument. Otherwise, Python will take its position and bind it to the argument in the definition occurring in the corresponding location.

What about the following two cases?

```
>>> w(t=1, a=1, omega=2.5)
0.5984721441039565

>>> w(t=1, phi=0, a=1, omega=2.5)
0.5984721441039565
```

These are function calls that uses keyword arguments for all the bindings. When using such a call style, even the arguments without default values can be positioned anywhere.

*Note:* If positional arguments are specified, then the positional arguments must come before keyword arguments. Thus, `w(t=1, phi=0, 1, 2.5)` is an invalid call.

It is also possible to pass all positional arguments as a sequence--list or tuple--and all keyword arguments as a dictionary. Here are some sets of identical calls.

```
>>> w(1,2.5,1,3.14)
-0.599747328794043
>>> w(*[1,2.5,1,3.14])
-0.599747328794043

>>> w(1,2.5,phi=3.14)
-0.599747328794043
>>> w(*(1,2.5), **{'phi': 3.14})
-0.599747328794043

>>> w(t=1, phi=0, a=1, omega=2.5)
0.5984721441039565
>>> w(**{'t': 1, 'phi': 0, 'a': 1, 'omega': 2.5})
0.5984721441039565
```

If you have been a C programmer, the first instinct would be to think of them as pointers and pointers to pointers. However, it is not the case. A `*` indicates that the list or tuple must be unpacked as positional arguments and a `**` indicates that the keys of the dictionary must be matched up with the argument names and the values of the keys must be assigned to the corresponding arguments.

There is a caveat that must be taken into consideration while defining default values. Let us say that our code file looks like this--

~~~~
import math

t_default = 1
phi_default = 0

def w(a, omega, t=t_default, phi=phi_default):
    return a*math.sin(omega*t+phi)

t_default = 0
~~~~

If the function is called in the following fashion: `w(1,2.5)`, the defaults would be `t=1` and `phi=0` and not `t=0` and `phi=0`. This is because Python evaluates the defaults when it encounters the `def` statement. However, the body of the function is not evaluated at that stage--we can still take advantage of Python's lazy evaluation.

We now focus on the arguments of `sorted`. What if we pass the values in position instead of named arguments. According to our example, it should work.

```
>>> a = [2,5,4,1,3]
>>> sorted(a, None, True)
&lt;Traceback message&gt;
TypeError: must use keyword argument for key function
```

This is an interesting scenario. sorted doesn't allow positional arguments for certain positions. We can implement the same, too. In our sinusoidal function, we can force something like this: the first two can be positional or named arguments and the last two would be strictly named ones. In order to do so, we will have to sneak in the `*` in the declaration. Anything after that would have to be strictly named arguments. They need not even have default values.

~~~~
import math
def w(a, omega, *, t, phi):
    return a*math.sin(omega*t+phi)
~~~~

If we now test a simple cases--

```
>>> w(1,2.5,1,3.14)
TypeError: w() takes 2 positional arguments but 4 were given

>>> w(1, 2.5, t=1, phi=0)
0.5984721441039565

>>> w(t=1, phi=0, a=1, omega=2.5)
0.5984721441039565
```

The first two arguments can be positional or named. We can even force all of the arguments to be named by writing `def w(*, a, omega, t, phi)`.

*Note:* From Python 3.9, it is also possible to enforce a strict positional argument by using `/` in the `def` declaration. Anything before `/` must be passed as positional, between `/` and `*` as positional or named and strictly named after `*`. In the declaration `def w(a, /, omega, *, t, phi)`, Python expects at least one positional argument whose first value would be assigned to `a` and at least two named arguments--`t` and `phi`. If two positional arguments are passed, the second one would be assigned to `omega`. If only one positional argument is passed, `omega` must be named. We can even force all of the arguments to be positional by writing `def w(a, omega, t, phi, /)`.


## Arguments of unknown length

It is possible to accept arguments of any arbitrary length into a function. The best way to demonstrate this is to write a function that prints its arguments.

~~~~
def print_args(*args, **kwargs):
    print(args)
    print(kwargs)
    return
~~~~

Let us take some of the earlier calls and test them out.

```
>>> print_args(1,2.5,phi=3.14)
(1, 2.5)
{'phi': 3.14}

>>> print_args(t=1, phi=0, a=1, omega=2.5)
()
{'t': 1, 'phi': 0, 'a': 1, 'omega': 2.5}
```

All positional arguments are stored in `args` are tuple and all named arguments are stored in `kwargs` as dictionary. The names of these attributes need not be `args` and `kwargs`. They can be anything. However, these specific ones have become part of many Python programmers' vocabulary and thus have become informal standard.

It is possible to have some fixed arguments and some free (or extra) ones. As usual, the positional ones must come first.

~~~~
def print_args(a1, a2, *args, kw1, kw2, **kwargs):
    print(a1, a2, args)
    print(kw1, kw2, kwargs)
    return
~~~~

That is the correct order of arguments in the `def` statement--fixed positional arguments, followed by free positional arguments, followed by fixed keyword arguments, and finally, the free keyword arguments.

```
>>> print_args(1, 2, 3, 4, kw1=5, kw2=6, kw3=7, kw4=8)
1 2 (3, 4)
5 6 {'kw3': 7, 'kw4': 8}
```

Here is a nice usage of the free-form arguments. Let us write a `timer` function that transparently wraps the input and output of a function as well as prints the time taken to run the function.

~~~~
import time
def timer(f, *args, **kwargs):
    start_time = time.time()
    f_out = f(*args, **kwargs)
    exec_time = time.time()-start_time
    print("The function "+f.__name__+" was executed in "+str(exec_time)+" seconds.")
    return f_out
~~~~

We pass the function we want to time as the first argument. Since we have no idea what are the arguments of this function *a priori*, we catch all the rest arguments in `*args` and `**kwargs` and pass them as-is to the function call. Let us try it out on two examples we have already seen before.

```
>>> from functools import reduce
>>> s = ["I", "am", "a", "broken", "sentence."]
>>> join = lambda delim: lambda x, y: x+delim+y
>>> joined_s = timer(reduce, join(" "), s)
The function reduce was executed in 1.1682510375976562e-05 seconds.
>>> print(joined_s)
I am a broken sentence.

>>> k_q_n = lambda x: (x[1], x[0])
>>> sorted_inventory = timer(sorted, inventory, key=k_q_n)
The function sorted was executed in 1.7642974853515625e-05 seconds.
>>> print(sorted_inventory)
[('banana', 2), ('pineapple', 2), ('apple', 3), ('orange', 3), ('pear', 5)]
```

If we take one of the examples--let's say the `reduce` one--we can break down the workings of the function. We have already seen that the normal call to join our list of strings with space is `reduce(join(" "), s)`. The call `timer(reduce, join(" "), s)` assigns `f=reduce` and `args=(join(" "), s)`. The line `f_out = f(*args, **kwargs)` on substitution becomes `f_out=reduce(*(join(" "), s))`, which in turn is identical to `f_out=reduce(join(" "), s)`. This is exactly the normal call we have seen earlier. The output is captured in `f_out` and is returned as-is by the `timer` function but not before it has printed the time taken to execute the call `f_out=reduce(*(join(" "), s))`.
