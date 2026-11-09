from fractions import Fraction as F
import math
def half_away(x):
    m = abs(x); w = math.floor(m + F(1,2)); return w if x >= 0 else -w
# Lab 1
y = F(400,10000)
ev = [(1,5000),(2,5000),(3,105000)]
pv = sum((F(a)/(1+y)**t for t,a in ev), F(0))
print("L1 exact PV", float(pv), "rounded", half_away(pv), "%.6f" % float(pv))
# rounding fixture
ev3 = [(1,500),(2,500),(3,10500)]
terms = [F(a)/(1+y)**t for t,a in ev3]
print("rounding exact", float(sum(terms, F(0))), "terms", [float(t) for t in terms], "rounded terms", [half_away(t) for t in terms], sum(half_away(t) for t in terms), half_away(sum(terms,F(0))))
# Fixture B
print("B", F(10500,1)/F(95,100), float(F(10500)/F(95,100)), half_away(F(10500)/F(95,100)))
# 496 bps
print("496 coupon", F(1704285*179,10000), half_away(F(1704285*179,10000)))
ev496 = [(1, half_away(F(1704285*179,10000)) + 1704285)]
pv496 = F(ev496[0][1]) / (1+F(496,10000))
print("496 pv", ev496, pv496, pv496 == F(3305625,2), half_away(pv496))
# float check
yf = 496/10000
print("float 496 disc", 1734792/(1+yf), 1734792*(1+yf)**-1, round(1734792/(1+yf)))
print("float 400 disc 13", 13*(1+0.04)**-1, 13/(1+0.04), 13*(1/(1+0.04)), (1+0.04)**-1*13)
# just under half cent
p = F(300075005) / (F(10001,10000))**3
print("just under: exact", float(p), " claim 299985000.5 - 1/(2*1000300030001): ", F(299985000)+F(1,2)-F(1,2*1000300030001) == p, p - F(299985000))
print("claim diff", F(1,2)-F(1,2*1000300030001) - (p-F(299985000)))
print("round just under", half_away(p))
# 2^53 float check
print("face 1e17+4999 coupon", float(F(10**17+4999,10000)), half_away(F(10**17+4999,10000)))
