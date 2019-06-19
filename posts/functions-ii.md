$ post_id : functions-ii
$ post_title : 03: Functions--II. Arguments and returns
$ post_group : 99: Unsorted chapters
$ post_last_update: 2019-06-18

## Arguments to Python functions

In the previous section, we had encountered two functions that had some optional arguments--the `reduce` function with its optional initial value and the `sorted` function with its optional key function and reverse flag.

Let us try to write rewrite our earlier sinusoidal function \\(y = A \cos (\omega t + \phi) \\). This time if offset, \\(phi\\) is not specified, we will assume it to be 0.

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

If the function is called in the following fashion: `w(1,2.5)`, the defaults would be `t=1` and `phi=0` and not `t=0` and `phi=0`. This is because the evaluation of defaults happen when the `def` statement is encountered. However, the body of the function is not evaluated at that stage--we can still take advantage of Python's lazy evaluation.
