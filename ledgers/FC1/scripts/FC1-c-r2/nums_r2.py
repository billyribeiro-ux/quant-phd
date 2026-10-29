"""Exact recomputation of the numbers cited on project.html, FC1 cards and the L01/L03/L05 lessons (round 2).

Run: .venv/bin/python -I ledgers/FC1/scripts/FC1-c-r2/nums_r2.py
"""

import math
from fractions import Fraction as F


def hu(x):
    return math.floor(x + F(1, 2))


def half_away(x):
    m = abs(x)
    w = math.floor(m + F(1, 2))
    return w if x >= 0 else -w


y = F(400, 10000)
print("project PV exact", float(sum(F(a) / (1 + y) ** t for t, a in [(1, 5000), (2, 5000), (3, 105000)])))
pv = sum(F(a) / (1 + y) ** t for t, a in [(1, 500), (2, 500), (3, 10500)])
print("rounding fixture PV", float(pv), "rounded once", half_away(pv), "terms", [half_away(F(a) / (1 + y) ** t) for t, a in [(1, 500), (2, 500), (3, 10500)]])
print("fixture B exact", float(F(10500) / F(95, 100)), half_away(F(10500) / F(95, 100)))
print("L01 S10 exact", float(F(1000) * (1 - F(9, 10) ** 11) / F(1, 10)), "cents", hu(F(1000) * (1 - F(9, 10) ** 11) / F(1, 10) * 100))
print("L01 half-redeposit limit cents", hu(F(1000) / (1 - F(1, 2) * F(9, 10)) * 100))
print("L05 net/gross exact", float(F(14282414, 68398886)), "half-up 3dp", hu(F(14282414, 68398886) * 1000))
print("L05 P5 receipt over gross, 2dp", float(F(11060360, 68398886) * 100), "over net", float(F(11060360, 14282414) * 100))
print("L03 relative spread", F(30, 5000), "L03 E3", F(6, 20000) * 100, "%")
print("L02 exposure check 13 entries with one two-value entry:", 13 + (2 - 1))
