"""E4 slice a, round 11: independent re-derivation of the numbers in index, L01, L02 and L03.

Run from any directory with the venv interpreter, isolated:
    .venv/bin/python -I ledgers/E4/scripts/E4-a-r11/rederive_slice_a.py
Everything is exact (fractions.Fraction) except the Pareto grid search, which is repeated with several
tolerances and with an exact-logarithm-free comparison (the sign of a sum of logs is decided with high-precision
decimal arithmetic) to test whether the printed counts depend on the tolerance.
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import product

getcontext().prec = 60
FAILS: list[str] = []


def ok(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), F(0))


# ---- L01 -------------------------------------------------------------------------------------------
pi1 = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
x1 = (F(100), F(40), F(0), F(250))
q1 = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
other = (F(0), F(60), F(120), F(30))
ok(sum(pi1) == 1, "L01 Example 1.5 probabilities sum to 1")
ok(dot(q1, x1) == F(340, 3), "L01 value of claim under (1/2,1/3,1/4,1/5) is 340/3")
ok(dot(q1, other) == 56, "L01 value of the second claim is 56 cents")
comb = tuple(2 * a - F(1, 2) * b for a, b in zip(x1, other, strict=True))
ok(comb == (F(200), F(50), F(-60), F(485)), "L01 combined payoff 2x - y/2 is (200,50,-60,485)")
ok(dot(q1, comb) == F(596, 3) and 2 * dot(q1, x1) - F(1, 2) * dot(q1, other) == F(596, 3), "L01 linearity 596/3")
ok(dot(pi1, x1) == F(235, 4), "L01 expected payoff 235/4")
ok(dot(q1, x1) != dot(pi1, x1), "L01 value at prices differs from expected payoff")
ok(sum(F(1, 2) if i < 3 else F(-1, 2) for i in range(4)) == 1, "L01 negative probability vector sums to 1 (rejected by negativity)")
ok(F(1, 8) + F(3, 8) + F(3, 8) + F(1, 4) == F(9, 8), "L01 Part E short vector sums to 9/8 (not 1)")
# M1: x=(10,0,30), pi=(1/2,1/4,1/4), q=(1/3,1/5,1/2)
ok(dot((F(1, 3), F(1, 5), F(1, 2)), (F(10), F(0), F(30))) == F(55, 3), "L01 M1 value 55/3")
ok(dot((F(1, 2), F(1, 4), F(1, 4)), (F(10), F(0), F(30))) == F(25, 2), "L01 M1 expected payoff 25/2")
ok(F(55, 3) - F(25, 2) == F(35, 6), "L01 M1 difference 35/6")
# M3
x, y, q = (F(1), F(2), F(3)), (F(4), F(0), F(1)), (F(1, 2), F(1, 4), F(1, 8))
lhs = dot(q, tuple(3 * a - 2 * b for a, b in zip(x, y, strict=True)))
ok(lhs == F(-1, 8) and 3 * dot(q, x) - 2 * dot(q, y) == F(-1, 8) and dot(q, x) == F(11, 8) and dot(q, y) == F(17, 8), "L01 M3 values")
# P3 and R2 and R3 quick checks
ok(F(1, 4) != F(1, 3), "L01 P3: V(e_1)=1/4 differs from E e_1 = 1/3")
ok((F(1, 2) ** 2) == F(1, 4) and (2 * F(1, 2)) ** 2 == 1 and 2 * F(1, 4) != 1, "L01 R2 values")
ok(F(1, 2) * 5 + F(1, 4) * 7 == F(17, 4), "L01 quiz 4.25")
ok(F(1, 4) * 0 + F(3, 4) * 4 == 3, "L01 quiz expected payoff 3")

# ---- L02 -------------------------------------------------------------------------------------------
PROBS = (F(1, 2), F(1, 4), F(1, 4))
E1 = (F(3), F(4), F(1))
E2 = (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(E1, E2, strict=True))
ok(ebar == (F(4), F(8), F(4)), "L02 aggregate (4,8,4)")
th1 = sum((p * e / t for p, e, t in zip(PROBS, E1, ebar, strict=True)), F(0))
th2 = sum((p * e / t for p, e, t in zip(PROBS, E2, ebar, strict=True)), F(0))
ok(th1 == F(9, 16) and th2 == F(7, 16) and th1 + th2 == 1, "L02 Example 2.11 theta shares 9/16, 7/16")
qstar = tuple(p / t for p, t in zip(PROBS, ebar, strict=True))
ok(qstar == (F(1, 8), F(1, 32), F(1, 16)), "L02 Prop 2.9 prices (1/8,1/32,1/16)")
ok(dot(qstar, ebar) == 1, "L02 q*.ebar = 1")
x1s = tuple(th1 * e for e in ebar)
x2s = tuple(th2 * e for e in ebar)
ok(x1s == (F(9, 4), F(9, 2), F(9, 4)) and x2s == (F(7, 4), F(7, 2), F(7, 4)), "L02 Example 2.11 bundles")
ok(tuple(a + b for a, b in zip(x1s, x2s, strict=True)) == ebar, "L02 market clearing of bundles")
w1, w2 = dot(qstar, E1), dot(qstar, E2)
ok((w1, w2) == (th1, th2), "L02 wealth equals theta")
ratios1 = [PROBS[s] / (x1s[s] * qstar[s]) for s in range(3)]
ratios2 = [PROBS[s] / (x2s[s] * qstar[s]) for s in range(3)]
ok(all(r == 1 / w1 for r in ratios1) and all(r == 1 / w2 for r in ratios2), "L02 Part D ratios equal 1/wealth (16/9, 16/7)")
# Remark 2.6 at q=(2,1,1)
qq = (F(2), F(1), F(1))
wa, wb = dot(qq, E1), dot(qq, E2)
da = tuple(p * wa / q for p, q in zip(PROBS, qq, strict=True))
db = tuple(p * wb / q for p, q in zip(PROBS, qq, strict=True))
z = tuple(a + b - e for a, b, e in zip(da, db, ebar, strict=True))
ok((wa, wb) == (11, 9), "L02 Remark 2.6 wealths 11 and 9")
ok(da == (F(11, 4),) * 3 and db == (F(9, 4),) * 3, "L02 Remark 2.6 demands 11/4 and 9/4")
ok(z == (1, -3, 1) and sum(z) == -1 and dot(qq, z) == 0, "L02 Remark 2.6 excess demand (1,-3,1), unweighted sum -1, value 0")
# Misconception 2: v=(1,-1,0) at q*
v = (F(1), F(-1), F(0))
ok(dot(qstar, v) == F(3, 32), "L02 Misconception 2 value 3/32")
# Misconception 1: prices of states 2 and 3
ok(qstar[1] == F(1, 32) and qstar[2] == F(1, 16), "L02 Misconception 1 prices")
# Misconception 3
ok(dot(qstar, E1) == F(9, 16), "L02 Misconception 3 endowment cost 9/16")
# M1
ok(F(1, 2) * F(1, 2) / F(1, 4) == 1 and F(1, 2) * F(1, 2) / F(1, 8) == 2 and F(1, 4) * 1 + F(1, 8) * 2 == F(1, 2), "L02 M1")
# M2
xm2 = (F(1, 4) * 3 / 1, F(1, 4) * 3 / 2, F(1, 2) * 3 / 1)
ok(xm2 == (F(3, 4), F(3, 8), F(3, 2)) and xm2[0] + 2 * xm2[1] + xm2[2] == 3, "L02 M2 demand and budget")
# M3 two-state
ok(F(1, 2) * F(1, 4) + F(1, 2) * F(3, 4) == F(1, 2), "L02 M3 theta_1 = 1/2")
# R2 elasticity: partial x_s / partial q_s = -x_s / q_s (symbolic check at one point)
ok(-(F(1, 2) * 1) / (F(1, 4) ** 2) == -8 and -(F(1, 2) * 1 / F(1, 4)) / F(1, 4) == -8, "L02 R2 derivative -pi w/q^2 = -x/q = -8 at (pi=1/2,w=1,q=1/4)")
# Example 2.11 MRS (L03 Example 3.6 uses these)

# ---- L03 -------------------------------------------------------------------------------------------
def mrs(x, s, t):
    return (PROBS[s] / x[s]) / (PROBS[t] / x[t])


ok(mrs(x1s, 0, 1) == 4 and mrs(x1s, 0, 2) == 2 and mrs(x1s, 1, 2) == F(1, 2), "L03 Example 3.6 agent 1 MRS 4, 2, 1/2")
ok(mrs(x2s, 0, 1) == 4 and mrs(x2s, 0, 2) == 2 and mrs(x2s, 1, 2) == F(1, 2), "L03 Example 3.6 agent 2 MRS 4, 2, 1/2")
ok(qstar[0] / qstar[1] == 4 and qstar[0] / qstar[2] == 2 and qstar[1] / qstar[2] == F(1, 2), "L03 price ratios 4,2,1/2")
ok(mrs(E1, 0, 1) == F(8, 3) and mrs(E2, 0, 1) == 8, "L03 endowment MRS_12 = 8/3 (agent 1), 8 (agent 2)")
# M1 MRS
pim = (F(1, 3), F(2, 3))
ok((pim[0] / F(1)) / (pim[1] / F(4)) == 2, "L03 M1 MRS_12 = 2")
# M2 L03: pi=(1/2,1/2), q=(2,1), w=6
xm = (F(1, 2) * 6 / 2, F(1, 2) * 6 / 1)
ok(xm == (F(3, 2), F(3)) and 2 * xm[0] + xm[1] == 6 and (F(1, 2) / xm[0]) / (F(1, 2) / xm[1]) == 2, "L03 M2 demand 3/2, 3; MRS 2")
# R2 derivatives at the endowment
d1 = -F(1, 2) / F(3) + F(1, 4) * 4 / 4
d2 = F(1, 2) * 1 + F(1, 4) * (-4) / 4
ok(d1 == F(1, 12) and d2 == F(1, 4), "L03 R2 derivatives 1/12 and 1/4")
# R2 trade: the two bundles add to ebar and are feasible
y1 = (3 - 0, 4, 1)
ok(tuple(a + b for a, b in zip((F(2), F(4), F(3)), (F(2), F(4), F(1)), strict=True)) == ebar, "L03 lab witness is feasible")
# E2 witness gains: (1/4) ln(4/3) each
import math

gain1 = (0.5 * math.log(2) + 0.25 * math.log(4) + 0.25 * math.log(3)) - (0.5 * math.log(3) + 0.25 * math.log(4))
gain2 = (0.5 * math.log(2) + 0.25 * math.log(4) + 0.0) - (0.25 * math.log(4) + 0.25 * math.log(3))
ok(abs(gain1 - 0.25 * math.log(4 / 3)) < 1e-12 and abs(gain2 - 0.25 * math.log(4 / 3)) < 1e-12,
   "L03 E2 witness gain = (1/4) ln(4/3) for both agents")
ok(math.isclose(0.25 * math.log(4 / 3), 0.0719205, rel_tol=0, abs_tol=1e-7), "L03 lab witness gain 0.0719205")


# Grid search (lab Part B): recount with float utilities at several tolerances, and with Decimal logs.
def util_float(bundle):
    if any(b == 0 for b in bundle):
        return -math.inf
    return sum(float(p) * math.log(float(b)) for p, b in zip(PROBS, bundle, strict=True))


def util_dec(bundle):
    from decimal import Decimal as D

    s = D(0)
    for p, b in zip(PROBS, bundle, strict=True):
        s += D(p.numerator) / D(p.denominator) * (D(b.numerator) / D(b.denominator)).ln()
    return s


GRID = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
total = ebar
cands = []
for fr in product(GRID, repeat=3):
    a = tuple(f * t for f, t in zip(fr, total, strict=True))
    b = tuple((1 - f) * t for f, t in zip(fr, total, strict=True))
    cands.append((a, b))
ok(len(cands) == 125, "L03 grid has 125 allocations")
eq_pair = (x1s, x2s)
end_pair = (E1, E2)


def count_float(ref, tol):
    ref_u = (util_float(ref[0]), util_float(ref[1]))
    n = 0
    for a, b in cands:
        ua, ub = util_float(a), util_float(b)
        if ua >= ref_u[0] - tol and ub >= ref_u[1] - tol and (ua > ref_u[0] + tol or ub > ref_u[1] + tol):
            n += 1
    return n


def count_dec(ref):
    ru = (util_dec(ref[0]), util_dec(ref[1]))
    n = 0
    for a, b in cands:
        ua, ub = util_dec(a), util_dec(b)
        if ua >= ru[0] and ub >= ru[1] and (ua > ru[0] or ub > ru[1]):
            n += 1
    return n


for tol in (1e-12, 1e-9, 0.0):
    print(f"count_float tol={tol}: at_equilibrium {count_float(eq_pair, tol)} at_endowment {count_float(end_pair, tol)}")
print("count_dec (exact sign, 60 digits): at_equilibrium", count_dec(eq_pair), "at_endowment", count_dec(end_pair))
ok(count_float(eq_pair, 1e-12) == 0, "L03 lab Part B: 0 improvements of the equilibrium at TOL 1e-12")
ok(count_float(end_pair, 1e-12) == 2, "L03 lab Part B: 2 improvements of the endowment at TOL 1e-12")
ok(count_dec(eq_pair) == 0, "L03 exact-sign recount: 0 improvements of the equilibrium")
ok(count_dec(end_pair) == 2, "L03 exact-sign recount: 2 improvements of the endowment")
first = next((a, b) for a, b in cands if util_float(a) > util_float(E1) - 1e-12 and util_float(b) > util_float(E2) - 1e-12 and (util_float(a) > util_float(E1) + 1e-12 or util_float(b) > util_float(E2) + 1e-12))
ok(tuple(str(z) for z in first[0]) == ("2", "4", "3") and tuple(str(z) for z in first[1]) == ("2", "4", "1"), "L03 first improvement is (2,4,3),(2,4,1) in enumeration order")

print("FAILS:", len(FAILS))
