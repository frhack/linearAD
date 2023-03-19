# linearAD
## Automatic Differentiation library 

- forward mode: the classic foward mode AD
- linearized reverse mode: reverse mode AD, with a non linear foward pass and a linear backward pass. Here the backward pass is a chain of linear closures aka *propagate pass*
- linearized forward mode: two step like reverse mode, a forward pass, and a linear pass aka *propagate pass*, a chain of linear closures 
- optional autodiscovery of primitives derivatives via Sympy


Example usage:

## Backward
```python 
mode = "l_B"
ad = ADl_B() # backward 
name = "test_algorythm_backward"
descr = f'test {name} mode {mode} failed '
(x, ONE, TWO) = (ad.D(0), ad.D(1), ad.D(2)) # instantiate some dual numbers

def babylon(x):  # compute square root with babylon algorythm
    t = (ONE+x)/TWO
    for i in range(0,100):  # 100 iterations
        t = (t + x / t) / TWO 
    return t

x.p = 4                 # the input var: x = 4 (real)
y = babylon(x)
y.t = 1
ad.propagate()
assert y.p == 2  ,  descr    # square root of 4
assert x.t == 1/4  ,  descr  # derivative of square root at 4 
```


## Linear Forward
```python 
mode = "l_F"
ad = ADl_F() # backward 
name = "test_algorythm_linear_forward"
descr = f'test {name} mode {mode} failed '
(x, ONE, TWO) = (ad.D(0), ad.D(1), ad.D(2)) # instantiate some dual numbers

def babylon(x):  # compute square root with babylon algorythm
    t = (ONE+x)/TWO
    for i in range(0,100):  # 100 iterations
        t = (t + x / t) / TWO 
    return t

x.p = 4                 # the input var: x = 4 (real)
y = babylon(x)
x.t = 1
ad.propagate()
assert y.p == 2  ,  descr    # square root of 4
assert y.t == 1/4  ,  descr  # derivative of square root at 4 
```


## Forward
```python 
mode = "F"
ad = AD_F() # backward 
name = "test_algorythm_forward"
descr = f'test {name} mode {mode} failed '
(x, ONE, TWO) = (ad.D(0), ad.D(1), ad.D(2)) # instantiate some dual numbers

def babylon(x):  # compute square root with babylon algorythm
    t = (ONE+x)/TWO
    for i in range(0,100):  # 100 iterations
        t = (t + x / t) / TWO 
    return t

x.p = 4                 # the input var: x = 4 (real)
x.t = 1
y = babylon(x)
assert y.p == 2  ,  descr    # square root of 4
assert y.t == 1/4  ,  descr  # derivative of square root at 4 
```


## Primitives definition

```python 

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
```

## Primitives derivatives autodiscovery

```python 

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
```

