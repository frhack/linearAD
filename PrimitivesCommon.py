showed_jrow = {} 

class Primitives:
    def __init__(self): 
        self.list = []
        self.set_primitives()
 
    def set_primitives(self):
        self.sum  = self.set(Sum())
        self.sub  = self.set(Sub())
        self.mul  = self.set(Mul())
        self.div  = self.set(Div())
        self.sin  = self.set(Sin())
        self.cos  = self.set(Cos())
        self.tanh = self.set(Tanh()) 
        #self.tanh = self.set(Tanh(), False) # don't show sympy jrow
        self.pow  = self.set(Pow())


    def set(self,t, show_jrow = True):
        self.list.append(t)
        t.__class__.show_jrow = show_jrow
        t.set_jrow()
        return t 


class Primitive:
    def __init__(this): 
        this.jrow = []
        show_jrow = False

    def set_jrow(self):
        pass

    def do_set_jrow(self,*x):
        s = []
        for a in x:
           s.append(Symbol(a))
        y = self.apply(*s)
        #if (self.__class__.show_jrow ):
        if (self.__class__.show_jrow and not showed_jrow.get(self.__class__.__name__, False)):
            print("")
            print("# *** Primitive ",  self.__class__.__name__, " jacobian row: ")
            print("    def set_jrow(self):")
        for ssx in s:
           if (self.__class__.show_jrow and not showed_jrow.get(self.__class__.__name__, False)):
               print("        self.jrow.append( lambda "+ ",".join(x) +": ",end = "" )
           dsx = diff(y, ssx)
           if (self.__class__.show_jrow and not showed_jrow.get(self.__class__.__name__, False)):
               print(dsx, " )")

           ddx = lambdify(s, dsx) 
           self.jrow.append(ddx)
        if (self.__class__.show_jrow and not showed_jrow.get(self.__class__.__name__, False)):
           showed_jrow[self.__class__.__name__] = True 



    def do_jrow(*x):
        pass

    def do_apply(this,*x):
        pass

    def apply(this,*x):
        pass

    def do_lin(this,z,xs,ts):
        direction = xs[0].ad.direction
        for x,t in zip(xs,ts):
            if(direction):
               z.t += x.t * t 
            else:
               x.t += z.t * t 

    def get_lin(self,z,*xs):
        ts = []
        xp = []
        direction = xs[0].ad.direction
        for x in xs:
            xp.append(x.p)
        for j in self.jrow:
            ts.append(j(*xp))
        return lambda: self.do_lin(z,xs,ts)


class Unary(Primitive):

    def set_jrow(self):
        self.do_set_jrow("x1") 

    def do_apply(this,*x):
        x1 = x[0]
        r = this.apply(x1.p)
        obj =  type(x1)(r,x1.ad)
        return obj 

class Binary(Primitive):

    def set_jrow(self):
        self.do_set_jrow("x1","x2") 

    def do_jrow(this,*x):
        this.jrow(x[0].p,x[1].p)

    def do_apply(this,*x):
        (x1,x2) = x
        r = this.apply(x1.p,x2.p)
        obj =  type(x1)(r,x1.ad)
        return obj 


from PrimitivesSympy import *
from PrimitivesMath import *
