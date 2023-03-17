from PrimitivesCommon import *
from PrimitivesMath import *
from PrimitivesSympy import *
from Tape import *
from Dual import *

class ADl:
    def __init__(this):
        this.direction = None 
        this.tape = None
        this.primitives = None
        this.mutated = []

    def trace(this, closure):
        this.tape.append( closure )

    def propagate(this):
        this.clear_linear()
        for closure in this.tape.list: closure()

    def clear_linear(this):
        for x in this.mutated: x.t = 0
        this.mutated = []

    def clear(this):
        this.clear_linear()
        this.tape.clear()

    def D(this,x): return D(x,this)

    def propagate_from_to(this,fromvar,tovar):
        this.clear_linear()
        fromvar.t = 1
        for closure in this.tape.list: closure()
        fromvar.t = 0
        return tovar.t

    def derive(this,f): return lambda x: this.derivative(f,x)

    def derivative(this,f,x):
        x = this.D(x)
        this.clear()
        y = f(x)
        return this.propagate_from_to(* this.get_from_to(x,y))

    def get_from_to(this,a,b): return (a,b) if this.direction else (b,a)

class ADl_F(ADl):
    def __init__(this):
        super(ADl_F, this).__init__()
        this.direction = True;
        this.tape = Tape(this.direction)
        this.primitives = Primitives(this.direction)



class AD_F(ADl):
    def __init__(this):
        super(AD_F, this).__init__()
        this.direction = True;
        this.tape = Tape(this.direction)
        this.primitives = Primitives(this.direction)

    def trace(this, closure):
        closure()

class ADl_B(ADl_F):
    def __init__(this, *args, **kwargs):
        super(ADl_B, this).__init__(*args, **kwargs)
        this.direction = not this.direction  # invert the direction
        this.tape = this.tape.get_transpose()
        this.primitives = this.primitives.get_transpose()


    def get_from_to(this,a,b):
        return (b,a)
