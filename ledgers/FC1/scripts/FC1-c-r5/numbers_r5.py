from fractions import Fraction as F
import math
y = F(400, 10000)
ev = [(1, 500), (2, 500), (3, 10500)]
terms = [F(a) / (1 + y) ** t for t, a in ev]
exact = sum(terms, F(0))
print("terms float", [round(float(x), 6) for x in terms])
print("exact", float(exact), "exact6", f"{float(exact):.6f}")
def hv(x):
    m = abs(x); w = (2*m.numerator + m.denominator)//(2*m.denominator)
    return w if x >= 0 else -w
print("rounded once", hv(exact), "per-term", [hv(x) for x in terms], sum(hv(x) for x in terms))
# lab1
face=100000; c=hv(F(face*500,10000)); evs=[(1,c),(2,c),(3,c+face)]
pv = sum((F(a)/(1+y)**t for t,a in evs), F(0))
print("lab1", evs, f"{float(pv):.6f}", hv(pv), exact_pv := float(pv))
# fixture B
print("B", float(F(10500)/F(95,100)), hv(F(10500)/F(95,100)))
# lab3 rounding case
print("F", hv(F(1,2)), "G", hv(F(10001,2)), "C coupon", hv(F(10001*5000,10000)))
print("ratios", float(F(10500,1)/F(105,100)))
