$ post_id : mro
$ post_title : Method Resolution Order
$ post_group : Clusters
$ post_last_update: 2018-07-09; 2018-06-23

## Classes from `type`

We start from a blank class definition that Python supports. (The codes are in Python 3.)

    class A(object):
        pass


This class does nothing. If you try to instantiate the class, it inherits all the attributes from the default Python *object*. A quick way to check the attributes of this class is to use the `dir` function.

    print(dir(A))
    >>> ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
        '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
        '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
    print(A)
    >>> <class '__main__.A'>

We also see the output of `__repr__` function. This fuction returns a string (a representation of the class for display only). The `print` function calls this function to obtain a string that can be displayed.

There is an alternate way of declaring the class -- using the `type` function.

    B = type('B', (object,), {})

At this point, `B` is identical to `A`. Let's have a look.

    print(dir(B))
    >>> ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
        '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
        '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
    print(B)
    >>> <class '__main__.B'>

It is necessary to undertand the arguments that the `type` function takes. In fact, there are two separate implementations of `type`, one being completely different in its functionality to the other. The only way for Python to know which is which is to see if it has two or three arguments. This is what the official documentation of Python 3.6 says --

> `class type(object)`   
> `class type(name, bases, dict)`   
> With one argument, return the type of an object. The return value is a type object and generally the same object as returned by `object.__class__`.

The first argument is the name. This is the name that is displayed when `print(B)` is executed. It may or may not be same as the object variable B. The second one is a tuple of base classes. In fact, we need not inherit the `object` base class explicitely in Python 3. An empty tuple, `()`, would suffice. The call `B = type('B', (object,), {})` is identical to `B = type('B', (), {})`. So are the class declarations `class A(object):` and `class A():`.

## Attributes of a class

The `dir` function lists the objects that are objects. Classes are objects, too. The attributes of are what are inherited from the base classes and anything else that has been declared inside the class.

    class A(object):

        name = 'Class A'

        def whomai():
            print('I am a function')
            return

The class declaration is completely useless from a practical point of view. It is useful as a demonstator. You get two new objects -- the variable `name` and the function `whoami`. These are listed in the scope by `dir`.

    print(dir(A))
    >>> ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
        '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
        '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name', 'whoami']

It is possible to write these variables and methods outside the scope of the class definition and add them as an attribute to the class.

    B = type('B', (object,), {})

    name = 'Class B'

    def whoami():
        print('I am a function')
        return    

    setattr(B, 'name', name)
    setattr(B, 'whoami', whoami)

    print(dir(B))
    >>> ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
        '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
        '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name', 'whoami']

Note that this approach sets us up for creating class definitions from scratch. This involves two steps. First, declare the class using the `type` function and second, assimilate all attributes into the class. Other than `setattr`, there are three other functions that will help us in playing with the attributes of an object.

The retrival function to `setattr` is `getattr`. It returns the object (variable, method) inside another object. For example, check the following code --

    whoami_extracted = getattr(B, 'whoami')

    whoami_extracted()
    >>> I am a function

    B.whoami()
    >>> I am a function

In essence, `whoami_extracted = getattr(B, 'whoami')` is equivalent to `whoami_extracted = B.whoami`.

There is also a function called `delattr` that removes an attribute from an object. Here is an example.

    delattr(B, 'whoami')

    print(dir(B))
    >>> ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
        '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
        '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name']

Python has a predicate function called `hasattr` to check if an attribute is present in an object. For example, after we have deleted the `whoami` attribute from `B`, we could query `B` in the following manner --

    print(hasattr(B, 'whoami'))
    >>> False

    print(hasattr(B, 'name'))
    >>> True

## New and old style classes in Python 2.7

One of the first hurdles you'll find is in the discrepancy in the declaration of a class using the `class` statement. Unlike Python 3, the declarations `class A(object):` and `class A():` will yield two different types of objects. (Note: We'll use `print()` as a function instead of usual `print` used in Python 2.7. This is for consistency. For Python 2.6, this function must be imported `from __future__ import print_function`.)

class A:
    pass

class B(object):
    pass

print(A)
>>> __main__.A

print(dir(A))
>>> ['__doc__', '__module__']

print(B)   
>>> <class '__main__.B'>

print(dir(B))
>>> ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']

In the first declaration, the attributes listed are minimal. This is an example of an old-style class. The reason it exists is to preserve compatibility with older Python versions where this was the only behaviour.

In the second case, the inheritence from *object* has been explicitely declared. This yields what is known as new-style classes. These classes are similar to the ones created by Python 3. There are a number of things that were added and/or modified, including addition of low-level constructor `__new__`, `super` access to parent classes, descriptors, slots, alteration of method resolution order and descriptors, and some more. It is not that important to know all the changes at this point. This book will focus on some of the important aspect of these terminologies in coming chapters.

Let us see what the `type` function generates.

```
C = type('C', (), {})

print(C)
>>> <class '__main__.C'>

print(dir(C))
>>> ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__',  '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
```

 Voila! We observe that the `type` function creates a new-style class. There is no reason to use an old-style class anymore! Henceforth, if for some reason the only available choice is a Python 2.6+ installation, it is advised to use the declaration `class A(object):` instead of `class A:`. This is also recommended by the Python community.

# Method resolution order

In a complex hierarchy, it is difficult to figure out what exactly should a child class inherit from its parent. Let us take a simple example.

~~~~
class A(object):
    def speak(self):
        print('Function speak has been inherited from A in object:')
        print(self)

class B(object):
    def speak(self):
        print('Function speak has been inherited from B in object:')
        print(self)

class C(A,B):
    pass

class D(B,A):
    pass

a = A()
b = B()
c = C()
d = D()
~~~~

```
a.speak()
>>> Function speak has been inherited from A in object:
    <__main__.A object at 0x7fd5e89e4190>

b.speak()
>>> Function speak has been inherited from B in object:
    <__main__.B object at 0x7fd5e89e41d0>

c.speak()
>>> Function speak has been inherited from A in object:
    <__main__.C object at 0x7fd5e89e4210>

d.speak()
>>> Function speak has been inherited from B in object:
    <__main__.D object at 0x7fd5e89e4250>
```

So far, things are pretty straightforward. The order of inheritence for `class C` is not the same as in `class D`. The priority of the inheritence of `speak` method appears to be that which is passed first in the list of classes during the class declaration. While `class C` resolves to inheriting the `speak` method of `class A`, `class D` inherits the same method from `class B`.

Let us create a situation that will force the method resolution algorithm to get confused. Let us define the following inheritence hierarchy. Here, we let `class B` inherit from `class A`.

    class A(object):
        def speak(self):
            print('Function speak has been inherited from A in object:')
            print(self)

    class B(A):
        def speak(self):
            print('Function speak has been inherited from B in object:')
            print(self)

    class C(A, B):
        pass

    >>> Traceback (most recent call last):
        File "inherit.py", line 11, in <module>
            class C(A, B):
        TypeError: Error when calling the metaclass bases
            Cannot create a consistent method resolution order (MRO) for bases A, B

Clearly, there is some issue in the resolution. This can be corrected by changing the declation of `class C` to inherit `B` before `A`. Let us rewrite the code.

    class A(object):
        def speak(self):
            print('Function speak has been inherited from A in object:')
            print(self)

    class B(A):
        def speak(self):
            print('Function speak has been inherited from B in object:')
            print(self)

    class C(B, A):
        pass

    a = A()
    b = B()
    c = C()

    a.speak()
    >>> Function speak has been inherited from A in object:
        <__main__.A object at 0x7f5a8d13b190>

    b.speak()
    >>> Function speak has been inherited from B in object:
        <__main__.B object at 0x7f5a8d13b1d0>

    c.speak()
    >>> Function speak has been inherited from B in object:
        <__main__.C object at 0x7f5a8d13b210>

The question is, how did the second declaration correct the error thrown by the first one? In order to answer that question we will have to understand the method resolution order of Python's new-style classes.

## C3 Linearisation

The algorithm used to do so is known as **C3 linearisation**. It is a recursive algorithm and follows the following rules.

1. `L(O) = [O]` where `O` is the base class.
2. `L(A) = [A] + merge(L(A1), L(A2), L(A3), ..., [A1, A2, A3, ..., An])`, where `A` extends from `A1, A2, A3, ..., An`.
3. `merge(list1, list2, list3, ..., listn) = [K] + merge(list1', list2', list3', ..., listn')`, where `K` is a class occurring in only the first position (head) of any of the lists; `listk'` is `listk` without `K` if `K` was present in `listk`, else `listk'` is same as `listk`.
4. `merge([]) = []`

The merge operation may appear to be confusing but in reality it is not that complicated. The operation can be clarified by the use of a simple example. In fact, why dont we try it out on our "corrected" example? We will try to figure out the method resolution order of `class C`.

`O` is base class  
`A` extends `O`  
`B` extends `A`  
`C` extends `B, A`

1. `L(C) = [C] + merge(L(B), L(A), [B,A])`  
2. `L(C) = [C] + merge([B] + L(A), [A] + L(O), [B,A])` using rule 2: `L(A) = [A] + L(O)`  
3. `L(C) = [C] + merge([B] + [A] + L(O), [A] + [O], [B,A])` using rule 1: `L(O) = [O]` and rule 2: `L(A) = [A] + L(O)`  
4. `L(C) = [C] + merge([B] + [A] + [O], [A] + [O], [B,A])` using rule 1: `L(O) = [O]`  
5. `L(C) = [C] + merge([B,A,O], [A,O], [B,A])` compacting  
6. `L(C) = [C] + [B] + merge([A,O], [A,O], [A])` using rule 3: we can extract `B` as `B` is present in only head position of lists  
7. `L(C) = [C] + [B] + [A] + merge([O], [O])` using rule 3: we can extract `A` as `A` is present in only head position of lists  
8. `L(C) = [C] + [B] + [A] + [O] + merge([])`  using rule 3: we can extract `O` as `O` is present in only head position of lists  
9. `L(C) = [C,B,A,O]` using rule 4 and compacting  

Thus we can see how `class C` will try to resolve a method. Since `speak` is not available in `class C`, Python checks `class B` next. Sure enough, there is a `speak` method defined. Thus, Python called this method when `c.speak()` was invoked.

Now let us try to figure the method order resolution of `class C` for the case that gave us an error.

`O` is base class  
`A` extends `O`  
`B` extends `A`  
`C` extends `A, B`

1. `L(C) = [C] + merge(L(A), L(B), [A,B])`  
2. `L(C) = [C] + merge([A] + L(O), [B] + L(A), [A,B])` using rule 2: `L(A) = [A] + L(O)`  
3. `L(C) = [C] + merge([A] + [O], [B] + [A] + L(O), [A,B])` using rule 1: `L(O) = [O]` and rule 2: `L(A) = [A] + L(O)`  
4. `L(C) = [C] + merge([A] + [O], [B] + [A] + [O], [A,B])` using rule 1: `L(O) = [O]`  
5. `L(C) = [C] + merge([A,O], [B,A,O], [A,B])` compacting  

At this point there are three classes inside merge and none can be taken out. The heads of the three lists inside merge operator are `A`, `B` and `A` respectively. If we try to extract `A`, the second list stops us from doing so -- as `A` is present in a position other than the head. If we try to extract `B`, the third list stops us from doing so -- for exacly the same reason. Thus, we are stuck in a deadlock. No wonder, Python raises an error in this kind of declaration.

## The `mro` method

Python classes have a builtin classmethod called `mro` that returns a list of classes and types. As expected, the call `C.mro()` gives the following

    print(C.mro())
    >>> [<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <type 'object'>]

This is exactly the method resolution order we had computed earlier.
