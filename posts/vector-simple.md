$ post_id : vector-simple
$ post_title : 01: Writing a custom mathematical data type
$ post_group : 99: Unsorted chapters
$ post_last_update: 2019-06-12

In this chapter, we will look into a simple example. We will write a class to implement vector operations in three-dimensional space. The idea is to get familiar with some of Python's implementation of various functions and operators and define how our own class would behave when interacting with these.

## Defining a Vector Object

A vector in three-dimensional space is an array of length 3. We would want to store this in an object that supports a sequence--a tuple, or perhaps a list. For this particular implementation, let us choose a list to store our data. Since lists are mutable, the data in the vector can be directly altered if the user chooses to do so.

A vector is represented as  \\( \vec{a} = (r_1,r_2,r_3) \\) where \\( r_i \in R \\). Let us create a constructor that takes three values as input and stores it in a variable called `data` in the class.

~~~~
class vector(object):

  def __init__(self, r1, r2, r3):
    self.data=[float(r1), float(r2), float(r3)]
    return
~~~~

We can now import the class and write some lines to instantiate a few vectors.

```
>>> a=vector(1,2,3)
>>> print(a.data)
[1.0, 2.0, 3.0]

>>> b=vector(2,1,4.6)
>>> print(b.data)
[2.0, 1.0, 4.6]

>>> c=vector("f","g","h")
&lt;Traceback message&gt;
ValueError: could not convert string to float: 'f'
```

This is the expected behaviour of the code. It converts all `int` values before storing into data but fails to instantiate a `vector` object when any of the arguments do not have a float representation.

## Visual representation of an object

Notice that in order to print the components of the vector `a`, we have to print `a.data`. We would want to have this exact same behaviour when `print(a)` is invoked. Also, just to differentiate our `vector` object from a list, we would want to print the word "vector" before the list. This is what we would want to see--

```
>>> a=vector(1,2,3)
>>> print(a)
vector[1.0, 2.0, 3.0]
```

To do so, we will have to define a method called `__str__` in our class definition. The output would be a string--the exact string that we would want to see when the `print` function is called.

~~~~
  def __str__(self):
    return 'vector['+str(self.data[0])+', '+str(self.data[1])+', '+str(self.data[2])+']'
~~~~

If we re-import the class and print the vector, we'll see exactly what we wanted to see. In fact, we can even call the built-in `str` function and it in turn calls this method to return a string.

```
>>> a=vector(1,2,3)
>>> print(a)
vector[1.0, 2.0, 3.0]

>>> str(a)
'vector[1.0, 2.0, 3.0]'
```

Python has another representation function called `__repr__`. This too, is supposed to return a string. The buit-in function `repr()` in turn calls this function. There is no set rule to what this string should be. However, it is usually the constructor call of the object. Programmers often use that idea so that the object can be re-built using the `eval` function.

For our code, we will have to copy the code and replace the square braces of the `__str__` function with the round ones.

~~~~
  def __repr__(self):
    return 'vector('+str(self.data[0])+', '+str(self.data[1])+', '+str(self.data[2])+')'
~~~~

We can test it out in our Python shell.

```
>>> a=vector(1,2,3)
>>> repr(a)
'vector(1.0, 2.0, 3.0)'

>>> b=eval(repr(a))
>>> print(b)
'vector[1.0, 2.0, 3.0]'
```

Check the last three lines. `repr(a)` returns a string that could be used as a `vector` constructor in a code. We are doing exactly that. We evaluate the string for executable code using `eval()` function and then assign the output to `b`. This is identical to executing `b=vector(1.0, 2.0, 3.0)`.

At this point we would want to improve our code. Firstly, we can leverage the fact that `vector[1.0, 2.0, 3.0]` is nothing but the concatenation of the word 'vector' and the string representation of a list and `vector(1.0, 2.0, 3.0)` is the concatenation of the word 'vector' and the string representation of a tuple that has same items as a list. Secondly, we would want to know the memory location of the instance when we invoke `print`. This can be obtained using the built-in function `id`. `id(<object>)` returns an integer which is guaranteed to be unique and constant for the object during its lifetime.

Here is version 2 of our `__str__` and `__repr__` functions

~~~~
  def __str__(self):
    return 'vector'+str(self.data)+' at '+hex(id(self))

  def __repr__(self):
    return 'vector'+str(tuple(self.data))
~~~~

Here is a Python-shell test for the above functions--

```
>>> a=vector(1,2,3)
>>> print(a)
vector[1.0, 2.0, 3.0] at 0x7f965898dac8

>>> repr(a)
'vector(1.0, 2.0, 3.0)'

>>> a
vector(1.0, 2.0, 3.0)
```

See that last test? Python shell uses `repr` to display an object in its REPL.

The code can be downloaded from <a href="code/vector_simple_01.py">code/vector_simple_01.py</a>.

## Vectors as a sequence of three real numbers

At its core, the data is a sequence of three real numbers. If we want to retrieve our y-component data, we might do something like this--

```
>>> a=vector(1,2,3)
>>> print(a.data[1])
2.0
```

There is a way to modify this behaviour so that by invoking `print(a[1])` instead of `print(a.data[1])`, we get our desired output. In this case we must define what does the phrase "key `1` in `vector` object `a`" mean. The way to implement this behaviour is by defining the `__getitem__` method.

~~~~
def __getitem__(self, key):
    if not isinstance(key,int):
        raise TypeError('Index must be an integer')
    if (key>2 or key<0):
        raise IndexError('Index for a vector can be 0, 1 or 2')
    return self.data[key]
~~~~

Notice that there are two error-catchers. The code checks if the key is an integer--an instance of the Python data type `int`--and raises `TypeError`. This is the recommended behaviour. The second one is to check if the index makes sense. It should raise an `IndexError` otherwise. This is also a recommended behaviour so that the sequence object plays nicely with the `for` keyword. Notice that we have removed interpretation of negative indices--something that is present in a `list` object.

Let us do some testing in our Python shell.

```
>>> a=vector(1,2,3)
>>> a[0]
1.0

>>> a[1]
2.0

>>> a[2]
3.0

>>> a[3]
&lt;Traceback message&gt;
IndexError: Index for a vector can be 0, 1 or 2

>>> a[-1]
&lt;Traceback message&gt;
IndexError: Index for a vector can be 0, 1 or 2

>>> a['f']
&lt;Traceback message&gt;
TypeError: Index must be an integer
```

Remember the statement about implementation of an `IndexError` so that the sequence can play nicely with `for`? We have automatically implemented a sequence that can be used by the `for` keyword. Since for-loops expect that an `IndexError` will be raised for illegal indexes to allow proper detection of the end of the sequence, Python knows when the item list gets exhausted. We can test it out in the Python shell.

```
>>> for x in a:
...     print(x)
...
1.0
2.0
3.0
```

*Note:* Since our `data` is an instance of `list`, the implementation of an `IndexError` for index out-of-bounds is already present. Hence, this may not be the best example to illustrate this point. However, if instead of storing the three values in a list, we used three individual variables, this implementation would become necessary for the `for` loop to stop.

We would want a similar method to implement the alteration of a component of a vector. The way to do that is by using the `__setitem__` method.

~~~~
def __setitem__(self, key, value):
    if not isinstance(key, int):
        raise TypeError('Index must be an integer')
    if (key>2 or key<0):
        raise IndexError('Index for a vector can be 0, 1 or 2')
    self.data[key]=float(value)
    return
~~~~

Notice that we have kept our error checking consistent with the `__getitem__` method. We can test it out in our Python shell.

```
>>> a=vector(1,2,3)
>>> print(a)
vector[1.0, 2.0, 3.0] at 0x7f3164eb7128

>>> a[2]=5
>>> print(a)
vector[1.0, 2.0, 5.0] at 0x7f3164eb7128
```

The code with these sequence implementations can be downloaded from <a href="code/vector_simple_02.py">code/vector_simple_02.py</a>.

## Emulating mathematical operations

We know how mathematical operators behave on numbers. If we write `2+3`, Python will compute that for us and return `5`. The `+` operator behaves exactly as we would want it to behave. What about `[1, 2, 3]+[4, 5, 6]` or `'Monty'+' '+'Python'`? It is not very obvious what the `+` operator should mean. What should it do when there is a `+` sign between two lists or two strings. Testing it out in Python shell shows this--

```
>>> [1, 2, 3]+[4, 5, 6]
[1, 2, 3, 4, 5, 6]

>>> 'monty'+' '+'python'
'monty python'
```

Python interprets the meaning of `+` to be *concatenation* in both of these cases. It is not accidental but by design. We would likewise want to define our own interpretation of the `+` symbol in the context of vectors. We know how addition of vectors work--the result is a new vector whose components are the summation of the corresponding components of the summands.  If \\( \vec{a} = (a_1,a_2,a_3) \\) and \\( \vec{b} = (b_1,b_2,b_3) \\), then for the operation, \\( \vec{c} = \vec{a} + \vec{b} \\),  \\( \vec{c} \\) will be equal to  \\( (a_1+b_1,a_2+b_2,a_3+b_3) \\).

The way to implement this behaviour is by writing an `__add__` function--

~~~~
  def __add__(self, other):
      if not isinstance(other, vector):
          raise TypeError('Cannot add a vector and a non-vector')
      return vector(self[0]+other[0], self[1]+other[1], self[2]+other[2])
~~~~

We have safeguarded our code from adding a vector and a non-vector. Again, let's test it out in the Python shell

```
>>> a=vector(1,2,3)
>>> b=vector(4,5,6)
>>> a+b
vector(5.0, 7.0, 9.0)

>>> a+9
&lt;Traceback message&gt;
TypeError: Cannot add a vector and a non-vector
```

What if we flip the order of operands?

```
>>> 9+a
&lt;Traceback message&gt;
TypeError: unsupported operand type(s) for +: 'int' and 'vector'
```

Here, the `TypeError` exception is raised via `int`'s `__add__` method rather than the one in our `vector` implementation. That too, the exception is not directly raised by `int`. Python's `int` type and its `__add__` method has no knowledge of how to deal with `vectors`. So, it returns a special value called `NotImplemented`. The *interpreter* recognises this special value and raises a `TypeError` exception which kills the execution.

It is possible to redirect the `NotImplemented` output of `__add__` in `int` by implementing the `__radd__` method in `vector`. When Python detects `NotImplemented` from `__add__` in `int`, it checks if a reverse add or `__radd__` method is present in the right operand's type.

~~~~
  def __radd__(self, other):
      if not isinstance(other, vector):
          raise TypeError('Cannot add a non-vector and a vector')
~~~~

Now, if the same request is made in Python shell, we get this--

```
>>> 9+a
&lt;Traceback message&gt;
TypeError: Cannot add a non-vector and a vector
```

The astute reader may observe that by overriding the behaviour of the left-hand operand, it is also possible to force an operation like `[1,2,3]+vector(4,5,6)` or `(1,2,3)+vector(4,5,6)`. I leave it up to the reader as an exercise for the brevity of this document.

It might be worthwhile to explore how we can handle multiplication of vector with a number. For that, we need to implement multiplication. Vectors have a dot product and a cross product. We can use the `__mul__` method associated with `*` operator for dot product and `__matmul__` method associated with the `@` operator as cross product. (Python 2 doesn't have `__matmul__`. We have to use a different method like `__mod__` associated with % to do the same.)

~~~~
  def __mul__(self, other):
      if not isinstance(other, vector):
          try:
              val=float(other)
              return vector(self[0]*val, self[1]*val, self[2]*val)
          except ValueError:
              raise TypeError('Cannot multiply the vector with the specified type')
      return self[0]*other[0]+self[1]*other[1]+self[2]*other[2]

  def __matmul__(self, other):
      if not isinstance(other, vector):
          raise TypeError('Cross product not defined between a vector and a non-vector')
      u1, u2, u3 = self.data
      v1, v2, v3 = other.data
      return vector((u2*v3 - u3*v2), (u3*v1 - u1*v3), (u1*v2 - u2*v1))
~~~~

Note how we treat multiplication of vector with a non-vector. If it is a number or a data type that has float representation, we just scale up the vector. Otherwise, we catch the `ValueError` that the statement `val=float(other)` would raise and raise a `TypeError` instead.

For the reverse multiplication cases, we can take a bit of shortcut. We can let their forward counterpart do all the work--including exception handling.

~~~~
  def __rmul__(self, other):
      return self*other

  def __rmatmul__(self, other):
      return self@other
~~~~

It is easy to implement similar behaviour for subtraction of two vectors, `c=a-b` using `__sub__` method. We can implement a negation using `__neg__` so that `-b` can be computed and then implement subtraction as `c=a+(-b)`.

```
  def __neg__(self):
      return vector(-self[0], -self[1], -self[2])

  def __sub__(self, other):
      return self+(-other)
```

As usual, let's test this out in Python shell.

```
>>> a=vector(1,2,3)
>>> b=vector(4,5,6)
>>> -b
vector(-4.0, -5.0, -6.0)

>>> a-b
vector(-3.0, -3.0, -3.0)
```

There is one last set of operators to tackle before we jump to a summary--the increment operators or augmented assignments. How do we implement something like `a+=b`. For most common data types like `int` or `float`, it's usually interpreted as `a=a+b`. We will emulate the same behaviour.

~~~~
  def __iadd__(self, other):
      val=self+other
      self.data=val.data
      return self
~~~~

At this point, we are banking on the already implemented addition and overwriting the `data` inside itself with the resultant's `data`. It is not necessary to return `self` but convention states that it should return a result--whatever the result may mean.

```
>>> a=vector(1,2,3)
>>> b=vector(4,5,6)
>>> a+=b
>>> a
vector(5.0, 7.0, 9.0)
```

The code with these numerical operator implementations can be downloaded from <a href="code/vector_simple_03.py">code/vector_simple_03.py</a>.

At this point, instead of an explanation of the code, let us look at a summary of operators and their corresponding increment operators.

| Operator     |  Method       | Reverse Method   | Incr. Operator | Incr. Op. Method |
|:------------:|---------------|------------------|:--------------:|------------------|
| `+`          | ` __add__`    | `__radd__`       | `+=`           | `__iadd__`       |
| `-`          | ` __sub__`    | `__rsub__`       | `-=`           | `__isub__`       |
| `*`          | ` __mul__`    | `__rmul__`       | `*=`           | `__imul__`       |
| `@`          | ` __matmul__` | `__rmatmul__`    | `@=`           | `__imatmul__`    |
| `/`          | ` __truediv__` | `__rtruediv__`  | `/=`           | `__itruediv__`   |
| `//`         | ` __floordiv__`| `__rfloordiv__` | `//=`          | `__ifloordiv__`  |
| `%`          | ` __mod__`    | `__rmod__`       | `%=`           | `__imod__`       |
| `divmod()`   | ` __divmod__` | `__rdivmod__`    | n.a.           | n.a.             |
| `pow()` or `**` | ` __pow__` | `__rpow__`       | `**=`          | `__ipow__`       |
| `<<`         | ` __lshift__` | `__rlshift__`    | `<<=`          | `__ilshift__`    |
| `>>`         | ` __rshift__` | `__rrshift__`    | `>>=`          | `__ilshift__`    |
| `&`          | ` __and__`    | `__rand__`       | `&=`           | `__iadd__`       |
| `^`          | ` __xor__`    | `__rxor__`       | `^=`           | `__ixor__`       |
| `|`          | ` __or__`     | `__ror__`        | `|=`           | `__ior__`        |

And here is a table of the unary operators.

| Operator     |  Method       |
|:------------:|---------------|
|`-`|`__neg__`|
|`+`|`__pos__`|
|`abs()`|`__abs__`|
|`~`|`__invert__`|
|`complex()`|`__complex__`|
|`int()`|`__int__`|
|`float()`|`__float__`|
|`round()`|`__round__`|
|`trunc()`|`__trunc__`|
|`floor()`|`__floor__`|
|`ceil()`|`__ceil__`|
|*see note*|`__index__`|

*Note:* `__index__` is called to convert the data to an integer object. This is used for slicing and for the built-in `bin()`, `hex()` and `oct()` functions.

The code with all numerical operator implementations can be downloaded from <a href="code/vector_simple_04.py">code/vector_simple_04.py</a>. For most of the cases, we have set the return value to `NotImplemented`. This will ensure that a different data type (may not be the built-in ones) can implement their own procedures when interacting with our `vector` objects. The `__abs__` method has been implemented and it returns the magnitude of a vector when `abs()` is called. Also, the `__float__` method--invoked when `float()` is called--redirects to `abs()`.

## Implementing rich comparison methods

One of the final things we will touch upon in this chapter are the rich comparison methods. In other words, how we can implement the logical operators like `==`, `!=`, `<`, `<=`, `>` and `>=`.

We will start with equality and inequality. In this case, two vectors are equal when their components are equal

~~~~
  def __eq__(self, other):
      return self[0]==other[0] and self[1]==other[1] and self[2]==other[2]

  def __ne__(self, other):
      return not self==other`
~~~~

As usual, let's test it out in Python shell.

```
>>> a=vector(1,2,3)
>>> b=vector(1,2,3)
>>> a==b
True

>>> a!=b
False

>>> c=vector(4,5,6)
>>> a!=c
True
>>>
```

For the other four operators, we could just compare the magnitude--something we have already implemented using the `__abs__` method. Here are the `<=`, `>`, `>=`, and `<` implementations respectively.

~~~~
  def __le__(self, other):
      return abs(self)<=abs(other)

  def __gt__(self, other):
      return not self<=other

  def __ge__(self, other):
      return abs(self)>=abs(other)

  def __lt__(self, other):
      return not self>=other
~~~~

I leave it up to the reader to test the behaviour. The code with all implementations (and non-implementations) can be downloaded from <a href="code/vector_simple_05.py">code/vector_simple_05.py</a>.

## Assignment by memory

There is one last thing to touch upon before wrapping this chapter up. Let us run a test case. In our Python shell, we can import our `vector` class and run the following

```
>>> a=vector(0.5,0.5,0.5)
>>> b=a
>>> b+=a
>>> b
vector(1.0, 1.0, 1.0)
>>> a
vector(1.0, 1.0, 1.0)
```

This is not an intended outcome. We haven't asked Python to alter the values of `a`. Something must have happened. This is where our `__str__` method will help us.

```
>>> print(a)
vector[1.0, 1.0, 1.0] at 0x7f94870ed160
>>> print(b)
vector[1.0, 1.0, 1.0] at 0x7f94870ed160
```

We can clearly see that both the variables `a` and `b` point to the same object. The `id` value points to the same memory location. In truth, this behaviour is not unique to our `vector`. Whenever a statement like `b=a` is executed, Python merely points `b` to the same object at the same memory location as `a` was pointing. Thus a procedure to change the contents of `b` gets reflected in `a` an vice versa. The reader can test this out using numbers, lists, etc.
