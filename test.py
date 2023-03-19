from AD import *
import math


def eq(x,y):
    abs(x-y) < 1/100000000

def getAD(mode):
    if (mode == "F"):
        return AD_F()
    if (mode == "l_F"):
        return ADl_F()
    if (mode == "l_B"):
        return ADl_B()

def test1(mode):
    ad = getAD(mode)
    name = "test1"
    descr = f'test {name} mode {mode} failed '
    assert ad.derivative(lambda x: x+x+x, 3)==3, descr 
    assert ad.derivative(lambda x: x+x - x*x*x, 3) == -25,  descr 
    assert ad.derivative(lambda x: x+x - x**3, 3) == -25,  descr 
    assert ad.derivative(lambda x: x+x + x*x*x, 3) == 29,  descr 
    assert ad.derivative(lambda x: sin(x), math.pi) == -1,  descr
    assert ad.derivative(lambda x: cos(x), math.pi)**2 < 1/1000000,  descr


def test_algorythm(mode):
    ad = getAD(mode)
    name = "test_algorythm"
    descr = f'test {name} mode {mode} failed '
    (x, ONE, TWO,THREE, FOUR) = (ad.D(3), ad.D(1), ad.D(2), ad.D(3), ad.D(4) )
    def babylon(x):
        t = (ONE+x)/TWO
        for i in range(0,100):
            t = (t + x / t) / TWO 
        return t

    babylon_d = ad.derive(babylon)
    
    assert babylon_d(2) == 0.35355339059327373  ,  descr
    assert babylon_d(4) == 0.25  ,  descr

def test_algorythm_backward():
    mode = "l_B"
    ad = getAD(mode)
    name = "test_algorythm_backward"
    descr = f'test {name} mode {mode} failed '
    (x, ONE, TWO) = (ad.D(0), ad.D(1), ad.D(2))
    def babylon(x):
        t = (ONE+x)/TWO
        for i in range(0,100):
            t = (t + x / t) / TWO 
        return t

    x.p = 4
    y = babylon(x)
    y.t = 1
    ad.propagate()
    assert y.p == 2  ,  descr
    assert x.t == 1/4  ,  descr

def test_algorythm_linear_forwad():
    ad = getAD("l_F")
    (x, ONE, TWO,THREE, FOUR) = (ad.D(2), ad.D(1), ad.D(2), ad.D(3), ad.D(4) )
    def babylon(x):
        t = (ONE+x)/TWO
        for i in range(0,100):
            t = (t + x / t) / TWO 
        return t

    y = babylon(x)
    x.p = 2
    ad.propagate_from_to(* ad.get_from_to(x,y))
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: ",ad.get_from_to(x.t,y.t)[0] )
    #assert babylon_d(2) == 0.35355339059327373  ,  descr
    #assert babylon_d(4) == 0.25  ,  descr
    print(y.t)
    ad.clear()
    x.p = 4 
    y = babylon(x)
    ad.propagate_from_to(x,y)
    #assert babylon_d(2) == 0.35355339059327373  ,  descr
    #assert babylon_d(4) == 0.25  ,  descr
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: oooo",y.t )

def test_algorythm_F():
    mode = "F"
    ad = getAD(mode)
    name = "test_algorythm_F"
    descr = f'test {name} mode {mode} failed '
    (x, ONE, TWO) = (ad.D(0), ad.D(1), ad.D(2))
    def babylon(x):
        t = (ONE+x)/TWO
        for i in range(0,100):
            t = (t + x / t) / TWO 
        return t

    x.p = 2 
    x.t = 1
    y = babylon(x)
    assert y.t == 0.35355339059327373  ,  descr
    x.p = 4
    x.t = 1
    y = babylon(x)
    assert y.t == 0.25  ,  descr

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
    name = "test_wang"
    descr = f'test {name} mode {mode} failed '
    (x1, x2) = (ad.D(0.5), ad.D(0.4) )
    f = lambda x1, x2: tanh(x2*(x1+x2))
    y = f(x1,x2)
    ad.propagate_from_to(* ad.get_from_to(x1,y))
    assert ad.get_from_to(x1.t,y.t)[1]==0.35233090825435176, descr 
    ad.clear()
    y.t = 0
    x1.t = 0
    x2.t = 0
    y = f(x1,x2)
    ad.propagate_from_to(* ad.get_from_to(x2,y))
    assert ad.get_from_to(x2.t,y.t)[1]==1.1450754518266433, descr 

def test_wang_linear_forward():
    mode = "F"
    ad = getAD(mode)
    name = "test_wang_linear_forward"
    descr = f'test {name} mode {mode} failed '
    ad = getAD("l_F")
    (x1, x2) = (ad.D(0.5), ad.D(0.4) )
    f = lambda x1, x2: tanh(x2*(x1+x2))
    y = f(x1,x2)
    x1.t = 1
    ad.propagate();
    assert ad.get_from_to(x1.t,y.t)[1]==0.35233090825435176, descr 
    ad.clear()
    y = f(x1,x2)
    x1.t = 0
    x2.t = 1
    ad.propagate();
    assert ad.get_from_to(x2.t,y.t)[1]==1.1450754518266433, descr 

def test_wang_backward():
    ad = getAD("l_B")
    (x1, x2) = (ad.D(0.5), ad.D(0.4) )
    f = lambda x1, x2: tanh(x2*(x1+x2))
    y = f(x1,x2)
    ad.propagate_from_to(* ad.get_from_to(x1,y))
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: ",ad.get_from_to(x1.t,y.t)[1])
    #ad.propagate_from_to(* ad.get_from_to(x2,y))
    print("derivative wrt y of lambda x, y: x*y*y + y*x  at y y = 2 3: ", ad.get_from_to(x2.t,y.t)[1])

def test_transpose():
    ad = getAD("l_F")
    (x1, x2) = (ad.D(0.5), ad.D(0.4) )
    f = lambda x1, x2: tanh(x2*(x1+x2))
    y = f(x1,x2)
    ad.propagate_from_to(* ad.get_from_to(x1,y))
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: ",ad.get_from_to(x1.t,y.t)[1])
    ad.propagate_from_to(* ad.get_from_to(x2,y))
    print("derivative wrt y of lambda x, y: x*y*y + y*x  at y y = 2 3: ", ad.get_from_to(x2.t,y.t)[1])

    ad = transpose(ad)
    (x1, x2) = (ad.D(0.5), ad.D(0.4) )
    f = lambda x1, x2: tanh(x2*(x1+x2))
    y = f(x1,x2)
    ad.propagate_from_to(* ad.get_from_to(x1,y))
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: ",ad.get_from_to(x1.t,y.t)[1])
    ad.propagate_from_to(* ad.get_from_to(x2,y))
    print("derivative wrt y of lambda x, y: x*y*y + y*x  at y y = 2 3: ", ad.get_from_to(x2.t,y.t)[1])

    ad = transpose(ad)
    (x1, x2) = (ad.D(0.5), ad.D(0.4) )
    f = lambda x1, x2: tanh(x2*(x1+x2))
    y = f(x1,x2)
    ad.propagate_from_to(* ad.get_from_to(x1,y))
    print("derivative wrt x of lambda x, y: x*y*y + y*x  at x y = 2 3: ",ad.get_from_to(x1.t,y.t)[1])
    ad.propagate_from_to(* ad.get_from_to(x2,y))
    print("derivative wrt y of lambda x, y: x*y*y + y*x  at y y = 2 3: ", ad.get_from_to(x2.t,y.t)[1])






def test_partial():
    mode = "l_B"
    ad = getAD(mode)
    name = "test_partial"
    descr = f'test {name} mode {mode} failed '
    (x, y) = (ad.D(2), ad.D(3) )
    f = lambda x, y:  x*y*y + y*x
    z = f(x,y)
    z.t = 1
    ad.propagate()
    assert x.t==12, descr 
    assert y.t==14, descr 

def test_directional():
    mode = "l_F"
    ad = getAD(mode)
    name = "test_directional"
    descr = f'test {name} mode {mode} failed '
    (x, y) = (ad.D(2), ad.D(3) )
    f = lambda x, y:  x*y*y + y*x
    x.t = 1/2  # 9 +3 
    y.t = 1/2  # 12+2 
    z = f(x,y)
    ad.propagate()
    #print("derivative wrt x of lambda x, y: x*y*y + y*x  at x = 2: ", z.t)
    assert z.t==13, descr 

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
    name = "test1"
    descr = f'test {name} mode {mode} failed '
    (x, ONE, TWO,THREE, FOUR) = (ad.D(3), ad.D(1), ad.D(2), ad.D(3), ad.D(4) )
    f = lambda x: ONE if x.p == 1 else x*x
    assert ad.derivative(f,1)==0, descr 
    assert ad.derivative(f,2)==4, descr 


test1("l_F")
test1("l_B")
test_algorythm("l_F")
test_algorythm("l_B")
test_algorythm_F()
#test_algorythm("F")
test_code("l_F")
test_code("l_B")
test_partial()
test_directional()
#test_partial3("F")
test_wang("l_B")
test_wang("l_F")
test_wang_linear_forward()
#test_wang("F")
     #test_partial3("l_B")
#test_partial1("l_F")
#test_partial1("l_B")
#test_transpose()
#test_wang_linear_forward()
#test_wang_backward()
#test_algorythm_linear_forwad()
test_algorythm_backward()
