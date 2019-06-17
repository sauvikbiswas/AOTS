$ post_id : mro
$ post_title : Method Resolution Order
$ post_group : Clusters
$ post_last_update: 2018-07-09; 2018-06-23

# Method resolution order

In a complex hierarchy, it is difficult to figure out what exactly should a child class inherit from its parent. Let us take a simple example.

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
