$ post_id : functions-iii
$ post_title : 03: Persistence and Closure
$ post_group : 01: Functions
$ post_last_update: 2019-06-22

## Persistence of a function

The execution of a function with all its attributes and local bindings stays in the memory only for as long as it is needed. The moment it encounters a `return`, the control is passed back to wherever the call had originated from. At this point, the execution instance and its bindings are of no use and are taken care by the interpreter's garbage collector. The declaration and definition of the function is still available for a subsequent call; which when encountered will spawn another instance of an execution with its attributes and new local bindings.

Let us test this out with a program that tries to compute \\(\pi\\) using [Madhava-Leibniz series](https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80) up to an accuracy of n entries and compares it to the value of `math.pi`.

$${\displaystyle 1\,-\,{\frac {1}{3}}\,+\,{\frac {1}{5}}\,-\,{\frac {1}{7}}\,+\,{\frac {1}{9}}\,-\,\cdots \,=\,{\frac {\pi }{4}}.}$$

~~~~
import math
def ml_pi(n):
    sum = 0.0
    for i in range(n):
        sum = sum + pow(-1.0,i)/(2*i+1)
    sum = sum*4.0
    return sum, (math.pi-sum)
~~~~

The return statement appears to return two objects. This is not the case. Python actually returns one object--a tuple with two items.

```
>>> res = ml_pi(1)
>>> print(res)
(4.0, -0.8584073464102069)

>>> res = ml_pi(10)
>>> print(res)
(3.0418396189294032, 0.09975303466038987)

>>> res = ml_pi(100)
>>> print(res)
(3.1315929035585537, 0.00999975003123943)
```

With more and more terms, we seems to get closer to the actual value of \\(\pi\\). However, the result is not our focus here. When `res = ml_pi(1)` is called, the interpreter binds the local variable `n` to the value `1`, creates all other attributes necessary and proceeds to execute the code. Once the code returns the result and the difference, the entire instance of the function execution is lost. The statement, `res = ml_pi(10)`, spawns a new instance of the function execution with the binding `n=10`.

A function is persistent in the memory for as long as its needed.

The following function performs the same task but uses recursion. The recursive form uses an inductive reasoning, \\(\pi_{ml}(n)=f(\pi_{ml}(n-1))\\) and uses the tail case, \\(\displaystyle \frac {\pi_{ml}(1)} {4}=1\\)

~~~~
import math
def ml_pi_rec(n):
    if n==1:
        return 4.0, math.pi-4.0
    sum_n_minus_1, _ = ml_pi_rec(n-1)
    sum = 4.0*(sum_n_minus_1/4.0 + pow(-1.0,n-1)/(2*(n-1)+1))
    return sum, (math.pi-sum)
~~~~

In Python, the `_` is often used to capture a value that is not required at all. In `sum_n_minus_1, _ = ml_pi_rec(n-1)`, we are not interested in the deviation of the value for the series computed till `n-1` terms. So instead of writing something like `sum_n_minus_1, diff_n_minus_1 = ml_pi_rec(n-1)` and never using `diff_n_minus_1` later, we have used the `_`.

The results are identical to the `ml_pi` function and are not our objects of focus. What is interesting is the persistence of various instances of execution and binding while tracing a call. To keep our analysis simple, let us analyse a call that asks Python to compute \\(\pi\\) to only three terms. Let's say that we have called `res = ml_pi_rec(3)` from the Python REPL shell.

1. `ml_pi_rec(3)` is called by Python shell with the binding `n=3`
2. The code hits `sum_n_minus_1, _ = ml_pi_rec(n-1)` and spawns a new instance of the function `ml_pi_rec(2)` with the binding `n=2`. `ml_pi_rec(3)` is still persistent in memory as execution is not complete.
3. `ml_pi_rec(2)` again hits `sum_n_minus_1, _ = ml_pi_rec(n-1)` and spawns a new instance of the function `ml_pi_rec(1)` with the binding `n=1`. Both `ml_pi_rec(3)` and `ml_pi_rec(2)` are persistent in memory as neither of their execution is complete.
4. `ml_pi_rec(1)` executes `return 4.0, math.pi-4.0` and sends the value to `ml_pi_rec(2)`. This instance of `ml_pi_rec(1)`'s purpose is over and is no more accessible.
5. `ml_pi_rec(2)` assigns the first value of the return it has received from `ml_pi_rec(1)` to `ml_pi_rec(2)`'s own attribute `sum_n_minus_1`. It then proceeds with the execution and finally executes `return sum, (math.pi-sum)`. This instance of `ml_pi_rec(2)`'s purpose is over and is no more accessible.
6. `ml_pi_rec(3)` assigns the first value of the return it has received from `ml_pi_rec(2)` to `ml_pi_rec(3)`'s own attribute `sum_n_minus_1` and proceeds with the execution. Once it executes `return sum, (math.pi-sum)`, it returns the values to the Python shell. This instance of `ml_pi_rec(3)` becomes inaccessible.

We now understand that the execution instance of a function is persistent as long as it doesn't encounter a `return` statement. The astute reader may come up with a clever question--what if there is no return statement in a function declaration at all. Python takes care of that and adds a `return None` to the end of a declaration if the declaration doesn't end with `return` statement.

## Closures

In Python, there is persistence of another kind. It's called closure. In order to understand this, we'll have to run through an example.

~~~~
import time
import math
def timed_ml_pi(n):
  time_start = time.time()
  def ml_pi():
      sum = 0.0
      for i in range(n):
          sum = sum + pow(-1.0,i)/(2*i+1)
      sum = sum*4.0
      time_delta = time.time()-time_start
      return sum, (math.pi-sum), time_delta
  print("Closure variables: n=%d, time_start=%f"%(n, time_start))
  return ml_pi
~~~~

It is important to notice a few things. Firstly, there is a nested function. In our case, `ml_pi` is nested inside `timed_ml_pi`. Secondly, the return value of our outer function is actually the inner function. And thirdly, the inner function uses two values that are defined outside its scope but are accessible inside its scope--`n` and `time_start`.

Let us try to run this.

```
>>> pi_x=timed_ml_pi(3)
Closure variables: n=3, time_start=1562167077.854889
>>> pi_x()
(3.466666666666667, -0.32507401307687367, 13.790881156921387)
>>> pi_x()
(3.466666666666667, -0.32507401307687367, 114.324436902999878)
>>> pi_x()
(3.466666666666667, -0.32507401307687367, 497.8665351867676)
```

`pi_x` is a function that can be called at will. What is interesting is that the time_delta reported keeps increasing as we call it again and again. This is because the value of `time_start` was fixed when `pi_x=timed_ml_pi(3)` was executed (as was the value of `n`). Every time the function `pi_x` is called, it executes an instance of the function. We have seen that it requires the bound values of two variables `n` and `time_start` in order for the instance to be executed. However, these are the properties of a different function altogether--`timed_ml_pi`! The instance of this function call doesn't exist. One might be tempted to think that `pi_x` is an instance of `timed_ml_pi(3)` but in reality, `timed_ml_pi(3)` has already been evaluated and the result is stored in `pi_x`. The result in this case is an instance of the function `ml_pi`. It's an instance of the function and not the evaluation.

In order to mitigate this issue, Python stores both of these objects--known as closures--inside `py_x` in an attribute `__closure__` as tuples.

```
>>> pi_x.__closure__
(&lt;cell at 0x7f50d4f238b8: int object at 0xa67b00&gt;, &lt;cell at 0x7f50d4f23828: float object at 0x7f50d88c3e40&gt)
```

The values aren't very apparent unless we dig further into it. It's not hard to guess which holds which. (Just look at the types.) We can actually take each of the cell objects and see what's inside.

```
>>> pi_x.__closure__[0].cell_contents
3
>>> pi_x.__closure__[1].cell_contents
1562167077.8548887
```

Closures are the non-local attributes persistent in a function when there are no instances of their original scope--a parent function--in memory.
