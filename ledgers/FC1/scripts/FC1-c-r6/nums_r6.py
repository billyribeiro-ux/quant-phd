from fractions import Fraction as F
import math
def half_away(x):
    m=abs(x); w=(2*m.numerator+m.denominator)//(2*m.denominator)
    return w if x>=0 else -w
def pv(events,bps):
    y=F(bps,10000); return sum((F(a)/(1+y)**t for t,a in events),F(0))
def dec(x,n=6):
    from decimal import Decimal, getcontext, ROUND_HALF_EVEN
    getcontext().prec=60
    return str((Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal(1).scaleb(-n)))
# Lab 1
coupon=half_away(F(100000*500,10000)); ev=[(1,coupon),(2,coupon),(3,coupon+100000)]
print("lab1 events",ev, "coupon",coupon)
p=pv(ev,400); print("lab1 exact",dec(p,6),"float",float(p),"price",half_away(p))
# rounding fixture
ev3=[(1,500),(2,500),(3,10500)]
p3=pv(ev3,400); print("round fixture exact",dec(p3,6),float(p3),"rounded",half_away(p3))
for t,a in ev3:
    term=F(a)/(1+F(400,10000))**t; print(" term",t,dec(term,6),half_away(term))
# fixture B
print("B", F(10500)/F(95,100), dec(F(10500)/F(95,100),4), half_away(pv([(1,10500)],-500)))
print("B exact fraction", F(10500)/F(95,100) == F(210000,19))
# fixture C/D/E/F/G
print("C coupon", F(10001*5000,10000), half_away(F(10001*5000,10000)))
print("F PV", pv([(1,1)],10000), half_away(pv([(1,1)],10000)))
print("G PV", pv([(1,10001)],10000), half_away(pv([(1,10001)],10000)))
# test: 496 bps
c=half_away(F(1704285*179,10000)); print("496 coupon", F(1704285*179,10000), float(F(1704285*179,10000)), c)
ev496=[(1,c+1704285)]; v=pv(ev496,496); print("496 exact", v, float(v), half_away(v), F(1734792)/F(10496,10000)==v, F(3305625,2))
print("496 float", float(F(1704285)) )
# half-cent tests
print("10^10+1", half_away(pv([(1,10**10+1)],10000)), dec(pv([(1,10**10+1)],10000),2))
print("10^12+1", half_away(pv([(1,10**12+1)],10000)))
# 13 at 400
print("13@400", pv([(1,13)],400), half_away(pv([(1,13)],400)), 13*(1+0.04)**-1, (1+0.04)**-1)
# just under half cent
ev_h=[(3,300075005)]; ph=pv(ev_h,1); print("hair", float(ph), half_away(ph), ph - (299985000 + F(1,2)), F(-1,2*1000300030001) , ph-(299985000+F(1,2)) == F(-1,2*1000300030001)*0 + (ph-(299985000+F(1,2))))
print("hair exact diff", ph-(299985000+F(1,2)), F(-1,(2*1000300030001)))
# yield > 100 %
print("150pct", pv([(1,10500)],15000), half_away(pv([(1,10500)],15000)))
# trade 2**40+1
print("trade", (2**40+1)*9851)
# test 2: 10**17+4999 at 1 bps
f=10**17+4999; cc=half_away(F(f*1,10000)); print("big face coupon", F(f,10000), cc, 10**13)
# 10000 bps: fixture for 13
