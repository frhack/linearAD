from sympy import *
from sympy import symbols, diff, Symbol, lambdify
from PrimitivesCommon import *


class Cos(Unary):
    def apply(self,x1): return cos(x1)

class Tanh(Unary):
    def apply(self,x1): return tanh(x1)

#class Sin(Unary):
    #def apply(self,x1): return sin(x1)


class Div(Binary):
    def apply(self,x1,x2): return x1 / x2 

class Mul(Binary):
    def apply(self,x1,x2): return x1 * x2 

#n = Nnn()
#n.params[0] = 3
#print(n.apply(2))
#print(n.jrow[0](2))
