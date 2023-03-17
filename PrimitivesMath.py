import math
from PrimitivesCommon import *

class Sin(Unary):
    def apply(self,x1): return math.sin(x1)

    def set_jrow(self):
        self.jrow.append( lambda x1: -math.sin(x1))

class Sub(Binary):
    def apply(self,x1,x2): return x1 + x2 

    def set_jrow(self):
        self.jrow.append( lambda x1,x2: 1)
        self.jrow.append( lambda x1,x2: -1)

class Sum(Binary):
    def apply(self,x1,x2): return x1 + x2 

    def set_jrow(self):
        self.jrow.append( lambda x1,x2: 1)
        self.jrow.append( lambda x1,x2: 1)

class Pow(Unary):
    def __init__(self):
        self.params = [0]
        super(Pow, self).__init__()

    def apply(self,x1): 
        p1 = self.params[0]
        return x1 ** p1 

    def set_jrow(self):
        p = self.params
        self.jrow.append( lambda x1: p[0]*x1**(p[0]-1))

