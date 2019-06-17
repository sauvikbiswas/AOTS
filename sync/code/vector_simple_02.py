class vector(object):

    def __init__(self, r1, r2, r3):
        self.data = [float(r1), float(r2), float(r3)]
        return

    def __str__(self):
        return 'vector'+str(self.data)+' at '+hex(id(self))

    def __repr__(self):
        return 'vector'+str(tuple(self.data))

    # Sequence Operations

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('Index must be an integer')
        if (key>2 or key<0):
            raise IndexError('Index for a vector can be 0, 1 or 2')
        return self.data[key]


    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError('Index must be an integer')
        if (key>2 or key<0):
            raise IndexError('Index for a vector can be 0, 1 or 2')
        self.data[key]=float(value)
        return
