from sympy import *
from sympy import symbols, diff, Symbol, lambdify
from PrimitivesCommon import *


class Cos(Unary):
    def apply(self,x1): return cos(x1)

class Tanh(Unary):
    def apply(self,x1): return tanh(x1)

#class Sin(Unary):
    #def apply(self,x1): return sin(x1)


class Sum(Binary):
    def apply(self,x1,x2): return x1 + x2 

    def set_jrow(self):
        self.jrow.append( lambda x1,x2: 1)
        self.jrow.append( lambda x1,x2: 1)

class Sub(Binary):
    def apply(self,x1,x2): return x1 - x2 

class Div(Binary):
    def apply(self,x1,x2): return x1 / x2 

class Mul(Binary):
    def apply(self,x1,x2): return x1 * x2 

class Pow(Unary):
    def __init__(self):
        self.params = [0]
        #super(Pow, self).__init__()

    def apply(self,x1): 
        p1 = self.params[0]
        return x1 ** p1 

    def set_jrow(self):
        p = self.params
        self.jrow.append( lambda x1: p[0]*x1**(p[0]-1))

#n = Nnn()
#n.params[0] = 3
#print(n.apply(2))
#print(n.jrow[0](2))

