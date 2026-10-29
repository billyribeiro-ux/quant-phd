from fractions import Fraction as F
import math
def hu(x):
    m=abs(x); w=(2*m.numerator+m.denominator)//(2*m.denominator); return w if x>=0 else -w
y=F(400,10000)
ev=[(1,5000),(2,5000),(3,105000)]
pv=sum(F(a)/(1+y)**t for t,a in ev)
print("lab1 pv", float(pv), hu(pv))
print("lab1 pv 6dp", f"{float(pv):.6f}")
# rounding fixture
ev3=[(1,500),(2,500),(3,10500)]
pv3=sum(F(a)/(1+y)**t for t,a in ev3)
print("rounding exact", float(pv3), f"{float(pv3):.6f}", hu(pv3), sum(hu(F(a)/(1+y)**t) for t,a in ev3))
print([float(F(a)/(1+y)**t) for t,a in ev3])
# fixture B
print(F(10500)/F(95,100), float(F(10500)/F(95,100)), hu(F(10500)/F(95,100)))
print(F(210000,19), float(F(210000,19)))
# lab3 fixtures and the 1/2
