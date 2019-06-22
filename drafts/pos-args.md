## Handling arbitrary number of positional and keyword arguments

It is possible to
def w2(*args, **kwargs):
    print(args)
    print(kwargs)


    ## Generator functions

    We do understand that the execution instance of a function is persistent as long as it doesn't encounter a `return` statement. The astute reader may come up with a clever question--what if there is no return statement in a function declaration at all. Python takes care of that and adds a `return None` to the end of a declaration if the declaration doesn't end with `return` statement.

    This is where a different 
