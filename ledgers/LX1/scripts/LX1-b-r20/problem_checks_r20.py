"""Round 20 exact checks of worked-solution and quiz numbers on L03 and L04 (and L03 Part A against the twin run).

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/problem_checks_r20.py
"""
import math
import re
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def hu(x, p):
    return Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP)

# L03 M1-M3 (Under m = 4 economy Y)
P4 = F(49, 50) ** 4
V4 = F(1000000) / P4
K4 = F(4000000) - (V4 - 1000000)
L4 = V4 / K4
print("L03 M1 P4", P4, "V4", float(V4), "rounded", int(V4 + F(1, 2)))
print("L03 M2 K4", float(K4), "rounded", int(K4 + F(1, 2)))
print("L03 M3 L4", float(L4), "4dp", hu(L4, 4))
# L03 quiz 8: V_12 for economy X
V12 = F(1000000) / (F(49, 50) ** 12)
print("L03 quiz8 V12", float(V12), "rounded", int(V12 + F(1, 2)))
# L03 E1/E2
print("L03 E2 9.20-2.69 =", F(920, 100) - F(269, 100), "vs unrounded diff 6.517884 ->", hu(6.517884, 2))
# L04 M1: ln 1.1 and the simple change
print("L04 M1 ln1.1", hu(math.log(1.1), 6), "simple", F(1375, 1000) / F(125, 100) - 1, "diff", hu(0.1 - math.log(1.1), 6))
# L04 M2: three changes
ls = [0.01, 0.03, -0.02]
mu = sum(ls) / 3
sd = math.sqrt(sum((v - mu) ** 2 for v in ls) / 2)
print("L04 M2 mean", hu(mu, 6), "sd", hu(sd, 6), "exact 19/30000 sqrt", hu(math.sqrt(19 / 30000), 6))
# L04 E2: simple change from the 2008-10 log change
z = -0.09657473997621150
print("L04 E2 simple", hu(math.exp(z) - 1, 6))
# L04 R2: band half-width for the largest move
zz = 0.13584567275950138
h = math.tanh(zz / 2)
print("L04 R2 h exact", hu(h, 6), "4dp", hu(h, 4), "bound at 0.0678", hu(math.log((1 + 0.0678) / (1 - 0.0678)), 6))
print("L04 quiz11 bound at 0.0678 to 4dp", hu(math.log((1 + 0.0678) / (1 - 0.0678)), 4))
print("L04 M1 quiz ln 1.1 check", hu(math.log(1.1), 6))
# L01 Research 1 threshold growth
print("L01 R1 g*", hu(F(9, 100) - F(400, 6000), 6), "2dp", hu(float(F(9, 100) - F(400, 6000)) * 100, 2), "4dp pct", hu(float(F(9, 100) - F(400, 6000)) * 100, 4))
# L03 Part A table check against the twin run output (independent of the lab): see rederive_L03_r20.py
# L01 s5 example: 400/1.09 and the closed form at g = 3 percent
print("L01 s5 example 40000/109", float(F(40000, 109)), "rounded", hu(float(F(40000, 109)), 0), "closed form at g=3%", hu(float(F(400) / (F(9, 100) - F(3, 100))), 0))
