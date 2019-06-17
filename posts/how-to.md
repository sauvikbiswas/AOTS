$ post_id : how-to
$ post_title : 00: How the code blocks have been laid out
$ post_group : 99: Unsorted chapters
$ post_last_update: 2019-06-12

This is a code in a file--

~~~~
class vector(object):

  def __init__(self, r1, r2, r3):
    self.data=[float(r1), float(r2), float(r3)]
    return
~~~~

Let's say that the file is saved as `vector_functions.py`.

This is a code that must be executed in Python shell--

```
>>> a=vector(1,2,3)
>>> print(a.data)
[1.0, 2.0, 3.0]
```
The lines that must be manually typed is prefixed by the Python REPL prompt--`>>> `. The ones without are the outputs.

What is not explicitly mentioned is that the reader will have to import the code before executing the instructions.

```
>>> from vector_functions import vector
>>> a=vector(1,2,3)
>>> print(a.data)
[1.0, 2.0, 3.0]
```
