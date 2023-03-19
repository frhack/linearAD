from PrimitivesCommon import *
import math

class Mul(Binary):
    def apply(self,x1,x2): return x1*x2

    def set_jrow(self):
        self.jrow.append( lambda x1,x2:  x2  )
        self.jrow.append( lambda x1,x2:  x1  )

class Sin(Unary):
    def apply(self,x1): return math.sin(x1)

    def set_jrow(self):
        self.jrow.append( lambda x1: math.cos(x1))

class Pow(Unary):
    def __init__(self):
        self.params = [0]
        super(Pow, self).__init__()

    def apply(self,x1): return x1 ** self.params[0]

    def set_jrow(self):
        p = self.params
        self.jrow.append( lambda x1: p[0]*x1**(p[0]-1))
