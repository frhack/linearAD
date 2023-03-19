from sympy import *
from PrimitivesCommon import *

class Sum(Binary):
    def apply(self,x1,x2): return x1 + x2 

class Sub(Binary):
    def apply(self,x1,x2): return x1 - x2 

class Div(Binary):
    def apply(self,x1,x2): return x1 / x2 

class Cos(Unary):
    def apply(self,x1): return cos(x1)

class Tanh(Unary):
    def apply(self,x1): return tanh(x1)
    
class Mul(Binary):
    def apply(self,x1,x2): return x1*x2

class Sin(Unary):
    def apply(self,x1): return math.sin(x1)
