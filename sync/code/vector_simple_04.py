class vector(object):

    def __init__(self, r1, r2, r3):
        self.data=[float(r1), float(r2), float(r3)]
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

    # Binary Operators

    def __add__(self, other):
        if not isinstance(other, vector):
            raise TypeError('Cannot add a vector and a non-vector')
        return vector(self[0]+other[0], self[1]+other[1], self[2]+other[2])

    def __sub__(self, other):
        return self+(-other)

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

    def __truediv__(self, other):
        if not isinstance(other, vector):
            try:
                val=float(other)
                return self*(1.0/val)
            except ValueError:
                raise TypeError('Cannot divide the vector with the specified type')
        raise TypeError('Cannot divide a vector with another vector')

    def __floordiv__(self, other):
        return NotImplemented

    def __mod__(self, other):
        return NotImplemented

    def __divmod__(self, other):
        return NotImplemented

    def __pow__(self, other):
        return NotImplemented

    def __lshift__(self, other):
        return NotImplemented

    def __rshift__(self, other):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __xor__(self, other):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented

    # Reverse Binary Operators

    def __radd__(self, other):
        if not isinstance(other, vector):
            raise TypeError('Cannot add a non-vector and a vector')

    def __rsub__(self, other):
        if not isinstance(other, vector):
            raise TypeError('Cannot add a non-vector and a vector')

    def __rmul__(self, other):
        return self*other

    def __rmatmul__(self, other):
        return self@other

    def __rtruediv__(self, other):
        return NotImplemented

    def __rfloordiv__(self, other):
        return NotImplemented

    def __rmod__(self, other):
        return NotImplemented

    def __rdivmod__(self, other):
        return NotImplemented

    def __rpow__(self, other):
        return NotImplemented

    def __rlshift__(self, other):
        return NotImplemented

    def __rrshift__(self, other):
        return NotImplemented

    def __rand__(self, other):
        return NotImplemented

    def __rxor__(self, other):
        return NotImplemented

    def __ror__(self, other):
        return NotImplemented

    # Augmented assignments

    def __iadd__(self, other):
        val=self+other
        self.data=val.data
        return self

    def __isub__(self, other):
        val=self-other
        self.data=val.data
        return self

    def __imul__(self, other):
        return NotImplemented

    def __imatmul__(self, other):
        return NotImplemented

    def __itruediv__(self, other):
        return NotImplemented

    def __ifloordiv__(self, other):
        return NotImplemented

    def __imod__(self, other):
        return NotImplemented

    def __ipow__(self, other):
        return NotImplemented

    def __ilshift__(self, other):
        return NotImplemented

    def __irshift__(self, other):
        return NotImplemented

    def __iand__(self, other):
        return NotImplemented

    def __ixor__(self, other):
        return NotImplemented

    def __ior__(self, other):
        return NotImplemented


    # Unary Operators

    def __neg__(self):
        return vector(-self[0], -self[1], -self[2])

    def __pos__(self):
        return vector(self[0], self[1], self[2])

    def __abs__(self):
        import math
        return math.sqrt(self[0]**2+self[1]**2+self[2]**2)

    def __invert__(self):
        return NotImplemented

    def __complex__(self):
        return NotImplemented

    def __int__(self):
        return NotImplemented

    def __float__(self):
        return abs(self)

    def __index__(self):
        return NotImplemented

    def __round__(self):
        return NotImplemented

    def __trunc__(self):
        return NotImplemented

    def __floor__(self):
        return NotImplemented

    def __ceil__(self):
        return NotImplemented
