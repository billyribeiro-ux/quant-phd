from fractions import Fraction as F
import math
def ha(x):
    m=abs(x); w=(2*m.numerator+m.denominator)//(2*m.denominator)
    return w if x>=0 else -w
# Lab 1 numbers
y=F(400,10000)
ev=[(1,5000),(2,5000),(3,105000)]
pv=sum(F(a)/(1+y)**t for t,a in ev)
print("lab1 pv", float(pv), ha(pv))
# rounding fixture
ev3=[(1,500),(2,500),(3,10500)]
pv3=sum(F(a)/(1+y)**t for t,a in ev3)
print("round fixture exact", float(pv3), ha(pv3), [float(F(a)/(1+y)**t) for t,a in ev3], [ha(F(a)/(1+y)**t) for t,a in ev3])
print("fixture B", float(F(10500)/F(95,100)), float(F(210000,19)))
# seed 496 case
c=ha(F(1704285*179,10000)); print("coupon",float(F(1704285*179,10000)),c)
e=1704285+0; ev=[(1,c+1704285)]
pv=F(ev[0][1])/(1+F(496,10000)); print("496 pv", ev, float(pv), pv, ha(pv), pv==F(3305625,2)*1 if False else pv)
print("float", (1734792/1.0496))
# 400bps 13
print("13/1.04", F(13)/F(104,100))
# 13..15 periods at par
for n in (13,14,15):
    ev=[(t,500) for t in range(1,n+1)]; ev[-1]=(n,500+10000)
    print(n, ha(sum(F(a)/(1+F(500,10000))**t for t,a in ev)))
# 2^40+1
print((2**40+1)*9851)
print("big face", (10**17+4999)/10000, 10**13)
