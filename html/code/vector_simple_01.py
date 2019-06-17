class vector(object):

    def __init__(self, r1, r2, r3):
        self.data = [float(r1), float(r2), float(r3)]
        return

    # version 01
    # def __str__(self):
    #     return 'vector['+str(self.data[0])+', '+str(self.data[1])+', '+str(self.data[2])+']'
    
    # version 02
    def __str__(self):
        return 'vector'+str(self.data)+' at '+hex(id(self))

    # version 01
    # def __repr__(self):
    #     return 'vector('+str(self.data[0])+', '+str(self.data[1])+', '+str(self.data[2])+')'

    # version 02
    def __repr__(self):
        return 'vector'+str(tuple(self.data))

