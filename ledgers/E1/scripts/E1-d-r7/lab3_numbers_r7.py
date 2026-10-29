"""Recomputes the Lab 3 table (a = 120 and 121, b = 1, c = 20) and the memo numbers from first principles."""
from fractions import Fraction as F
import math
def hu(x): return math.floor(x + F(1, 2))
def table(a, b, c, s):
    d = F(a - b * c)
    vol, fee = {"monopoly": (d / 2, F(a + b * c, 2 * b)), "cournot": (2 * d / 3, F(a + 2 * b * c, 3 * b)), "bertrand": (d, F(c))}[s]
    profit = (fee - c) * vol; cs = vol * vol / (2 * b); w = cs + profit; dwl = (d - vol) ** 2 / (2 * b)
    return [hu(vol), hu(fee), hu(profit), hu(cs), hu(w), hu(dwl)]
for a in (120, 121):
    for s in ("monopoly", "cournot", "bertrand"):
        print(a, s, table(a, 1, 20, s))
# memo claims
print("monopoly profit - cournot total (exact):", F(100**2, 4) - F(2 * 100**2, 9), "=", float(F(100**2, 36)), "cents; d^2/(36b)=", F(100**2, 36))
print("cournot welfare exact", F(40000, 9), "deadweight exact", F(5000, 9), "=", float(F(5000, 9)))
print("fee diff monopoly-cournot", F(70) - F(160, 3), "= d/(6b) =", F(100, 6))
print("a=121 monopoly profit exact", F(101, 2) * F(101, 2), "= 10201/4")
