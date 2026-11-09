"""Round 19: independent re-derivation of every number in L01 prose, quiz and problem solutions (exact Fractions).

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r19/rederive_L01_r19.py
"""
import math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP


def rhu(x):
    return math.floor(x + F(1, 2))


def fund(d1, r, g, t):
    return F(d1) * (1 + g) ** t / (r - g)


r, g = F(9, 100), F(3, 100)
d1 = 400
f0 = fund(d1, r, g, 0)
q = (1 + g) / (1 + r)
print("q =", q, float(q))
print("F0 =", f0, float(f0), "rounded", rhu(f0))
print("F0 at 1% =", fund(d1, r, F(1, 100), 0), "F0 at 3%:", float(fund(d1, r, F(3, 100), 0)))
for N in (10, 60, 200):
    sN = sum(F(d1) * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    res = f0 * q**N
    print(f"N={N} S_N={float(sN):.6f} rounded {rhu(sN)} identity {sN == f0 * (1 - q**N)} F0 q^N={float(res):.6f} rounded {rhu(res)}")
# Mechanics 1-3
print("Mech1 F0 (250,10%,4%) =", F(250) / (F(10, 100) - F(4, 100)), float(F(250) / (F(10, 100) - F(4, 100))), rhu(F(250) / (F(10, 100) - F(4, 100))))
m3 = F(250) * (F(104, 100)) ** 3 / (F(10, 100) - F(4, 100))
print("Mech2 F3 =", float(m3), rhu(m3), " 1.04^3 =", (F(104, 100)) ** 3, " 281.216/0.06 =", F(281216, 1000) / F(6, 100), float(F(281216, 1000) / F(6, 100)))
print("Mech3 d1/(1+r)=", F(100) / F(105, 100), " 10 terms =", 10 * F(100) / F(105, 100), float(10 * F(100) / F(105, 100)), " 1000/1.05 =", F(1000) / F(105, 100), float(F(1000) / F(105, 100)))
# Section 2 witness
print("witness gap +1000 check:", F(6000) - F(5000), " -2000/3 check:", F(6000) - F(20000, 3), float(F(6000) - F(20000, 3)))
# Section 5 / misc 2 example
print("PV 400/1.09 =", F(400) / F(109, 100), "=40000/109 ->", F(40000, 109), float(F(40000, 109)), "rounded", rhu(F(40000, 109)))
print("misc3 closed form (400, 9%, 10%) =", F(400) / (F(9, 100) - F(10, 100)))
# Quiz
print("F2 =", float(fund(d1, r, g, 2)), "rounded", rhu(fund(d1, r, g, 2)), " 424.36/0.06 =", float(F(424.36 if False else F(42436, 100)) / F(6, 100)))
print("q to 6dp:", float(q), "103/109 =", float(F(103, 109)))
print("g* =", F(9, 100) - F(400, 6000), float(F(9, 100) - F(400, 6000)))
# Research 1 threshold check
gs = F(9, 100) - F(400, 6000)
print("benchmark at g* =", fund(d1, r, gs, 0))
# Empirical 1/2
print("9/13 =", float(F(9, 13)), "13-9 =", 13 - 9)
# Empirical 3: t=9
f9 = fund(d1, r, g, 9)
print("F9 exact =", float(f9), "rounded", rhu(f9), " 2175/8698 =", float(F(2175, 8698)), "pct", round(float(F(2175, 8698)) * 100, 2))
price9 = f9 * F(125, 100)
print("price9 exact =", float(price9), "rounded", rhu(price9), "gap exact =", float(price9 - f9), "gap rounded diff", rhu(price9) - rhu(f9), "pct exact", float((price9 - f9) / f9 * 100))
print("pct of printed-int gap:", 2175 / 8698)
# Section 5 example rounding 40000/109
print("367 =", rhu(F(40000, 109)))
# Remark: F_t grows check
print("F_t ratio check:", fund(d1, r, g, 3) / fund(d1, r, g, 2) == 1 + g)
# Interpretation: F0 q^N values and wedge range
