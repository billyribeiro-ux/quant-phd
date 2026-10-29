from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 50
def ha(x):
    m = abs(x); r = (2*m.numerator + m.denominator)//(2*m.denominator)
    return r if x >= 0 else -r
def events(face, cbps, n):
    c = ha(F(face*cbps, 10000)); rows = [(t, c) for t in range(1, n+1)]; rows[-1] = (n, rows[-1][1]+face); return rows
def price(ev, ybps):
    y = F(ybps, 10000); return sum((F(a)/(1+y)**t for t, a in ev), F(0))
# Lab 1
ev = events(100000, 500, 3); ex = price(ev, 400)
print("lab1 events", ev, "exact", float(ex), "{:.6f}".format(float(ex)), "price", ha(ex))
# rounding fixture
ev = events(10000, 500, 3); ex = price(ev, 400)
print("rounding events", ev, "exact", "{:.6f}".format(float(ex)), "price", ha(ex))
print("terms", [ "{:.4f}".format(float(F(a)/(F(104,100))**t)) for t,a in ev], "rounded", [ha(F(a)/(F(104,100))**t) for t,a in ev], sum(ha(F(a)/(F(104,100))**t) for t,a in ev))
# fixtures
print("A", events(10000,500,1), ha(price(events(10000,500,1),500)))
print("B", ha(price(events(10000,500,1),-500)), "{:.4f}".format(float(F(10500)/F(95,100))), float(F(210000,19)))
print("C", events(10001,5000,2), F(10001*5000,10000))
print("D", events(1,5000,1))
print("F", events(1,0,1), price(events(1,0,1),10000), hi:=ha(price(events(1,0,1),10000)))
print("G", events(10001,0,1), price(events(10001,0,1),10000), ha(price(events(10001,0,1),10000)))
print("Bond(10000,500,1) price@500", ha(price(events(10000,500,1),500)))
print("Rounding-case: 500/1.04=", float(F(500)/F(104,100)), "500/1.0816=", float(F(500)/F(10816,10000)), "10500/1.04^3=", float(F(10500)/F(104,100)**3))
