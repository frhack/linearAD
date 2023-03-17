from PrimitivesCommon import *
from PrimitivesMath import *
from PrimitivesSympy import *

class D():

    def __init__(self, x, ad):
        self.p = x 
        self.t = 0 
        self.ad = ad

    def __add__(this, that): return this.trace_binary(this.ad.primitives.sum,that)

    def __sub__(this, that): return this.trace_binary(this.ad.primitives.sub,that)

    def __mul__(this, that): return this.trace_binary(this.ad.primitives.mul,that)

    def __truediv__(this, that): return this.trace_binary(this.ad.primitives.div,that)

    def __cos(this, that): return this.trace_unary(this.ad.primitives.cos)

    def __pow__(this, that):
        this.ad.primitives.pow.params[0] = that
        return this.trace_unary(this.ad.primitives.pow)

    def trace_binary(this,op,that): 
        return trace_op( this.ad, op.do_apply(this,that), lambda z:  op.lin(z,this,that))

    def trace_unary(this,op):
        return trace_op( this.ad, op.do_apply(this), lambda z:  op.lin(z,this))

    def __str__(self): return(f'D({self.p},{self.t})')

def trace_op(ad,v,c):
    ad.trace(lambda : c(v))
    return v


def sin(this): return this.trace_unary(this.ad.primitives.sin)
def cos(this): return this.trace_unary(this.ad.primitives.cos)
def tanh(this): return this.trace_unary(this.ad.primitives.tanh)


