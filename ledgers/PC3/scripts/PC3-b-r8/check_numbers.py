from fractions import Fraction as F
import random
A = lambda r: sum((1/(1+r)**t for t in range(1,4)), F(0))
for r in (F(8,100),F(10,100),F(12,100)):
    be = F(15000000,5000)/A(r)
    print("rate", r, "be", float(be), "A", A(r) if r==F(10,100) else float(A(r)))
print("diffs", float(F(1206.3444) if False else 0))
be8=float(F(3000)/A(F(8,100))); be10=float(F(3000)/A(F(10,100))); be12=float(F(3000)/A(F(12,100)))
print("unrounded", be8, be10, be12, be10-be8, be12-be10, be12-be8, (be12-be8)/4)
# NPV grid values at the bounds at each rate
def npv(cfs, r): return sum((c/(1+r)**t for t,c in enumerate(cfs)), F(0))
def cf(u): return [F(-15000000)] + [u*5000]*3
for r in (F(8,100),F(10,100),F(12,100)):
    print("rate", r, "npv lower", float(npv(cf(F(200)),r)), "upper", float(npv(cf(F(1600)),r)))
# E2 of L06 at 1200, 1300
print("1200", float(npv(cf(F(1200)),F(1,10))), float(-F(105000000,1331)))
print("1300", float(npv(cf(F(1300)),F(1,10))), float(F(1550000000,1331)))
# R3 of L06
m=F(15000000)*1331/(1600*3310); print("m*", float(m), float(m/5000), float(1-m/5000)*100)
# L06 remark 4.3 / E1
print("E1 1249", float(F(3000)/A(F(12,100))), float(F(1,1)/F(112,100)+F(1,1)/F(112,100)**2+F(1,1)/F(112,100)**3))
