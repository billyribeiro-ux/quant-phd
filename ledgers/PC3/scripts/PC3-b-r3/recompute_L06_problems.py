"""Recompute the L06 problem-set numbers with exact Fractions, independent of the lab: E2 grid, R3 margin, M2, M3, E1.

Usage: python -I recompute_L06_problems.py
"""
from fractions import Fraction as F

I = F(15_000_000)  # cents
m = F(5000)
A10 = sum((F(1) / F(11, 10) ** t for t in range(1, 4)), F(0))
A12 = sum((F(1) / F(112, 100) ** t for t in range(1, 4)), F(0))
print("A10", A10, "A12", A12, float(A12))
print("E1 break-even 12% =", float(F(3000) / A12), " (3000 = I/m)")
npv = lambda u, A: -I + m * A * u
print("E2 NPV(1200) exact", npv(F(1200), A10), float(npv(F(1200), A10)))
print("E2 NPV(1300) exact", npv(F(1300), A10), float(npv(F(1300), A10)))
grid = range(200, 1601, 100)
pos = [u for u in grid if npv(F(u), A10) > 0]
neg_max = max(u for u in grid if npv(F(u), A10) < 0)
print("E2 positive grid points", pos, "count", len(pos), "largest negative", neg_max)
mstar = I / (F(1600) * A10)
print("R3 margin m* exact", mstar, "=", float(mstar), "cents; ratio to 5000:", float(mstar / 5000), "fall %:", float((1 - mstar / 5000) * 100))
print("R3 check: break-even at m*", float(I / (mstar * A10)))
# M2
print("M2 NPV", -100 + F(60) / F(11, 10) + F(60) / F(121, 100), float(-100 + F(60) / F(11, 10) + F(60) / F(121, 100)))
# M3
u = F(1000) * 1331 / (4 * 3310)
print("M3 u*", u, float(u))
