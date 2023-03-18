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

    def __pow__(this, that):
        this.ad.primitives.pow.params[0] = that
        return this.trace_unary(this.ad.primitives.pow)

    def trace_binary(this,op,that): 
        return trace_op_binary( this.ad, op.do_apply(this,that),op,this,that )
        #return trace_op_binary( this.ad, op.do_apply(this,that), op.get_lin(z,this,that))

    def trace_unary(this,op):
        return trace_op_unary( this.ad, op.do_apply(this),op,this )

    def __str__(self): return(f'D({self.p},{self.t})')

def trace_op_binary(ad,z,op,this,that):
    l = op.get_lin(z,this,that)
    ad.trace(l)
    return z 

def trace_op_unary(ad,z,op,this):
    l = op.get_lin(z,this)
    ad.trace(l)
    return z 

def sin(this): return this.trace_unary(this.ad.primitives.sin)
def cos(this): return this.trace_unary(this.ad.primitives.cos)
def tanh(this): return this.trace_unary(this.ad.primitives.tanh)


