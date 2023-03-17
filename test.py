from AD import *
import math


def getAD(mode):
    if (mode == "F"):
        return AD_F()
    if (mode == "l_F"):
        return ADl_F()
    if (mode == "l_B"):
        return ADl_B()

def test1(mode):
    ad = getAD(mode)
    print("derivative of y=x*x*x at x=3:",ad.derivative(lambda x: x+x+x, 3))
    print("derivative of y=x+x - x*x*x at x=3:",ad.derivative(lambda x: x+x - x*x*x, 3))
    print("derivative of y=x+x + x**3 at x=3:",ad.derivative(lambda x: x+x + x**3, 3))
    print("derivative of sin(x) x=pi:",ad.derivative(lambda x: sin(x), math.pi))
    print("derivative of cos(x) x=pi:",ad.derivative(lambda x: cos(x), math.pi))


def test_algorythm(mode):
    ad = getAD(mode)
    print("direction:",ad.direction)
    (x, ONE, TWO,THREE, FOUR) = (ad.D(3), ad.D(1), ad.D(2), ad.D(3), ad.D(4) )
    def babylon(x):
        t = (ONE+x)/TWO
        for i in range(0,100):
            t = (t + x / t) / TWO 
        return t

    babylon_d = ad.derive(babylon)
    print("derivative of sqrt at 2: ", babylon_d(2))
    print("derivative of sqrt at 4: ", babylon_d(4))

def test_algorythm_F():
    ad = getAD("F")
    (x, ONE, TWO,THREE, FOUR) = (ad.D(3), ad.D(1), ad.D(2), ad.D(3), ad.D(4) )
    def babylon(x):
        t = (ONE+x)/TWO
        for i in range(0,100):
            t = (t + x / t) / TWO 
        return t

    x.p = 2 
    x.t = 1
    y = babylon(x)
    #ad.propagate()
    print("derivative of sqrt at 2: ", y.t)
    #ad.clear()
    x.p = 4
    x.t = 1
    y = babylon(x)
    #ad.propagate()
    print("derivative of sqrt at 4: ", y.t)
    ad.clear()

def test_partial1(mode):
    ad = getAD(mode)
    ( ONE, TWO,THREE, FOUR) = ( ad.D(1), ad.D(2), ad.D(3), ad.D(4) )
    (x, y) = (ad.D(5), ad.D(2) )
    f = lambda x, y:  THREE*x*x - TWO * y*y*y
    z = f(x,y)
    ad.propagate_from_to(* ad.get_from_to(x,z))
    print("derivative wrt y of lambda x, y: 3x^2-2y^3  at x, y = 5,2: ", ad.get_from_to(z.t,x.t)[0])
    ad.propagate_from_to(* ad.get_from_to(y,z))
    print("derivative wrt y of lambda x, y: 3x^2-2y^3  at x, y = 5,2: ", ad.get_from_to(z.t,y.t)[0])

def test_wang(mode):
    ad = getAD(mode)
    (x1, x2) = (ad.D(0.5), ad.D(0.4) )
    f = lambda x1, x2: tanh(x2*(x1+x2))
    y = f(x1,x2)
    ad.propagate_from_to(* ad.get_from_to(x1,y))
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: ",ad.get_from_to(y.t,x1.t)[0] )
    ad.propagate_from_to(* ad.get_from_to(x2,y))
    print("derivative wrt y of lambda x, y: x*y*y + y*x  at y y = 2 3: ", ad.get_from_to(y.t,x2.t)[0])



def test_partial(mode):
    ad = getAD(mode)
    (x, y) = (ad.D(2), ad.D(3) )
    f = lambda x, y:  x*y*y + y*x
    z = f(x,y)
    #y.d = 0 # 9+3
    ad.propagate_from_to(* ad.get_from_to(x,z))
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: ",ad.get_from_to(z.t,x.t)[0] )
    #y.d = 1 # 2*2*3+2 
    ad.propagate_from_to(* ad.get_from_to(y,z))
    print("derivative wrt y of lambda x, y: x*y*y + y*x  at y y = 2 3: ", ad.get_from_to(z.t,y.t)[0])

def test_partial2(mode):
    ad = getAD(mode)
    (x, y) = (ad.D(2), ad.D(3) )
    f = lambda x, y:  x*y*y + y*x
    x.t = 1/2 
    y.t = 1/2  # 12+2 
    z = f(x,y)
    #y.d = 0 # 9+3
    ad.propagate()
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x = 2: ", z.t)
    #x.d = 0
    #ad.propagate(z,y)
    ##print("derivative wrt y of lambda x, y: x*y*y + y*x  at y = 3: ", y.d)

def test_partial3(mode):
    ad = getAD(mode)
    (x, y) = (ad.D(2), ad.D(3) )
    f = lambda x, y:  x*y*y + y*x
    x.t = 1 
    #y.d = 1 
    z = f(x,y)
    #y.d = 0 # 9+3
    #ad.propagate()
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x = 2: ", z.t)
    #print("derivative wrt x of lambda x, y: x*y*y + y*x  at x = 2: ", y.d)
    #x.d = 0
    #ad.propagate(z,y)
    ##print("derivative wrt y of lambda x, y: x*y*y + y*x  at y = 3: ", y.d)

def test_code(mode):
    ad = getAD(mode)
    (x, ONE, TWO,THREE, FOUR) = (ad.D(3), ad.D(1), ad.D(2), ad.D(3), ad.D(4) )
    f = lambda x: ONE if x.p == 1 else x*x
    print("derivative of if  x=1:",ad.derivative(f, 2))
    print("derivative of if  x=1:",ad.derivative(f, 4))


test1("l_F")
test1("l_B")
test_algorythm("l_F")
test_algorythm("l_B")
test_algorythm_F()
test_code("l_F")
test_code("l_B")
test_partial("l_F")
test_partial("l_B")
test_partial2("l_F")
test_partial3("F")
test_wang("l_B")
test_wang("l_F")
     #test_partial3("l_B")
test_partial1("l_F")
test_partial1("l_B")

