showed_jrow = {} 

class Primitives:
    def __init__(self): 
        self.sum  = self.set(Sum())
        self.sub  = self.set(Sub())
        self.mul  = self.set(Mul())
        self.div  = self.set(Div())
        self.sin  = self.set(Sin())
        self.cos  = self.set(Cos())
        self.tanh = self.set(Tanh()) 
        self.pow  = self.set(Pow())

    def set(self,t, show_jrow = True):
        t.set_jrow()
        return t 

class Primitive: #def do_jrow(*x): pass #def do_apply(this,*x): pass #def apply(this,*x): pass
    def __init__(this): 
        this.jrow = []
        show_jrow = False

    def set_jrow(self): pass

    def do_set_jrow(self,*x):
        s = [Symbol(a) for a in x]
        y = self.apply(*s)
        if ( not showed_jrow.get(self.__class__.__name__, False)): print("\n# *** Primitive ",  self.__class__.__name__, " jacobian row:\n    def set_jrow(self):")
        for ssx in s:
           dsx = diff(y, ssx)
           if (not showed_jrow.get(self.__class__.__name__, False)): print("        self.jrow.append( lambda "+ ",".join(x) +": ",dsx, " )")
           self.jrow.append(  lambdify(s, dsx) )
        if (not showed_jrow.get(self.__class__.__name__, False)): showed_jrow[self.__class__.__name__] = True 

    def do_lin(this,direction,z,xs,ts):
        for x,t in zip(xs,ts):
            if(direction):
                z.t += x.t * t
            else:
                x.t += z.t * t 

    def get_lin(self,z,*xs):
        xp = [x.p for x in xs]
        ts = [j(*xp) for j in self.jrow]
        direction = xs[0].ad.direction
        return lambda: self.do_lin(direction,z,xs,ts)

class Unary(Primitive):
    def set_jrow(self): self.do_set_jrow("x1") 

    def do_apply(this,*x):
        x1 = x[0]
        r = this.apply(x1.p)
        return type(x1)(r,x1.ad)

class Binary(Primitive):
    def set_jrow(self): self.do_set_jrow("x1","x2") 

    def do_apply(this,*x):
        (x1,x2) = x
        r = this.apply(x1.p,x2.p)
        return type(x1)(r,x1.ad)

from PrimitivesSympy import *
from PrimitivesMath import *
