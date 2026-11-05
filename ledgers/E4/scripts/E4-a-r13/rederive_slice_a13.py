"""E4 slice a, round 13: independent re-derivation of the numbers in L01-L03 and the hub (own code, not the lab twins).

Run from the checkout root: .venv/bin/python -I ledgers/E4/scripts/E4-a-r13/rederive_slice_a13.py
Exact Fraction arithmetic for every rational number; Decimal (50 digits) for the logarithms of the Pareto search.
"""

from __future__ import annotations

import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import product

getcontext().prec = 50
FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ---- L01 ----
pi = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
q = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
x = (F(100), F(40), F(0), F(250))
y = (F(0), F(60), F(120), F(30))
V = lambda p, z: sum((a * b for a, b in zip(p, z)), F(0))  # noqa: E731
check(V(q, x) == F(340, 3), f"L01 V(claim)=340/3 ({V(q, x)})")
check(V(q, y) == 56, f"L01 V(other)=56 ({V(q, y)})")
comb = tuple(2 * a - F(1, 2) * b for a, b in zip(x, y))
check(comb == (200, 50, -60, 485), f"L01 combined payoff {tuple(str(c) for c in comb)}")
check(V(q, comb) == F(596, 3), f"L01 V(combination)=596/3 ({V(q, comb)})")
check(V(pi, x) == F(235, 4), f"L01 expected payoff=235/4 ({V(pi, x)})")
check(V(pi, x) != V(q, x), "L01 value differs from expected payoff under lab prices")
check(sum(pi) == 1 and sum(pi) != F(9, 8), "L01 probabilities sum to 1 (overweight variant 9/8)")
check(sum((F(1, 8), F(3, 8), F(3, 8), F(1, 4))) == F(9, 8), "L01 overweight vector sums to 9/8")
# M1 (three-state) solution
pm, xm, qm = (F(1, 2), F(1, 4), F(1, 4)), (F(10), F(0), F(30)), (F(1, 3), F(1, 5), F(1, 2))
check(V(qm, xm) == F(55, 3) and V(pm, xm) == F(25, 2) and V(qm, xm) - V(pm, xm) == F(35, 6),
      "L01 M1: V=55/3, E x=25/2 (12.5), difference 35/6")
check(abs(float(F(55, 3)) - 18.33) < 0.005, "L01 M1 rounding 18.33 to two decimals")
# P3 two-state, R2 size effect, Ex 1.5 decomposition
check(F(1, 4) != F(1, 3), "L01 P3 q1 != pi1")
check((F(1, 2) ** 2) == F(1, 4) and (2 * F(1, 2)) ** 2 == 1 and 2 * F(1, 4) != 1, "L01 R2 size effect values")
check(F(5) * 0 + F(1, 2) * 5 + F(1, 4) * 7 == F(17, 4), "L01 quiz value 4.25 (17/4)")
check(F(1, 4) * 0 + F(3, 4) * 4 == 3, "L01 quiz expected payoff 3")
check(F(1, 5) + F(1, 4) == F(9, 20), "sanity")
check(F(2, 10) + F(3, 10) + F(1, 10) == F(6, 10), "L01 quiz 0.6 (sum of prices 0.2, 0.3, 0.1)")

# ---- L02 ----
PROBS = (F(1, 2), F(1, 4), F(1, 4))
E1, E2 = (F(3), F(4), F(1)), (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(E1, E2))
check(ebar == (4, 8, 4), "L02 aggregate (4,8,4)")
th1 = sum(p * a / b for p, a, b in zip(PROBS, E1, ebar))
th2 = sum(p * a / b for p, a, b in zip(PROBS, E2, ebar))
check(th1 == F(9, 16) and th2 == F(7, 16) and th1 + th2 == 1, f"L02 theta1=9/16, theta2=7/16 ({th1}, {th2})")
qs = tuple(p / b for p, b in zip(PROBS, ebar))
check(qs == (F(1, 8), F(1, 32), F(1, 16)), "L02 prices (1/8, 1/32, 1/16)")
check(sum(a * b for a, b in zip(qs, ebar)) == 1, "L02 q.ebar = 1")
x1 = tuple(th1 * b for b in ebar)
x2 = tuple(th2 * b for b in ebar)
check(x1 == (F(9, 4), F(9, 2), F(9, 4)) and x2 == (F(7, 4), F(7, 2), F(7, 4)), "L02 Example 2.11 bundles")
w1 = sum(a * b for a, b in zip(qs, E1))
w2 = sum(a * b for a, b in zip(qs, E2))
check(w1 == th1 and w2 == th2, "L02 wealth equals theta")
check(sum(a * b for a, b in zip(qs, x1)) == w1 and sum(a * b for a, b in zip(qs, x2)) == w2, "L02 budgets bind")
check(all(a + b == c for a, b, c in zip(x1, x2, ebar)), "L02 market clearing in each state")
check(sum(a * (b + c - d) for a, b, c, d in zip(qs, x1, x2, ebar)) == 0, "L02 Walras residual zero")
ratios1 = [PROBS[s] / (x1[s] * qs[s]) for s in range(3)]
ratios2 = [PROBS[s] / (x2[s] * qs[s]) for s in range(3)]
check(all(r == F(16, 9) for r in ratios1) and all(r == F(16, 7) for r in ratios2), "L02 Part D ratios 16/9, 16/7")
# Remark 2.6 numbers at q=(2,1,1)
qq = (F(2), F(1), F(1))
wr1, wr2 = sum(a * b for a, b in zip(qq, E1)), sum(a * b for a, b in zip(qq, E2))
check((wr1, wr2) == (11, 9), "L02 Remark 2.6 wealths 11 and 9")
dem1 = [PROBS[s] * wr1 / qq[s] for s in range(3)]
dem2 = [PROBS[s] * wr2 / qq[s] for s in range(3)]
check(dem1 == [F(11, 4)] * 3 and dem2 == [F(9, 4)] * 3, "L02 Remark 2.6 demands")
z = [dem1[s] + dem2[s] - ebar[s] for s in range(3)]
check(z == [1, -3, 1] and sum(z) == -1 and sum(a * b for a, b in zip(qq, z)) == 0, "L02 Remark 2.6 excess demand (1,-3,1)")
v = (1, -1, 0)
check(sum(a * b for a, b in zip(qs, v)) == F(3, 32), "L02 Misconception 2 value 3/32")
check(sum(a * b for a, b in zip(qs, E1)) == F(9, 16), "L02 Misconception 3 endowment cost 9/16")
# Example 3.6 MRS values
def mrs(bundle: tuple, s: int, t: int) -> F:
    return (PROBS[s] / bundle[s]) / (PROBS[t] / bundle[t])
for b in (x1, x2):
    check((mrs(b, 0, 1), mrs(b, 0, 2), mrs(b, 1, 2)) == (4, 2, F(1, 2)), "L02/L03 Example 3.6 MRS 4, 2, 1/2")
check((qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2]) == (4, 2, F(1, 2)), "L03 price ratios 4, 2, 1/2")
# L03 R2 (endowment improvement) and E2 witness
def ulog(p, b):
    return sum((Decimal(pp.numerator) / Decimal(pp.denominator)) * (Decimal(bb.numerator) / Decimal(bb.denominator)).ln()
               for pp, bb in zip(PROBS, b))
eps = F(1, 1000)
ya = (E1[0] - eps, E1[1] + 4 * eps, E1[2])
yb = (E2[0] + eps, E2[1] - 4 * eps, E2[2])
check(all(a + b == c for a, b, c in zip(ya, yb, ebar)), "L03 R2 trade is feasible")
d1 = (PROBS[0] * (-1) / E1[0] + PROBS[1] * 4 / E1[1])
d2 = (PROBS[0] * 1 / E2[0] + PROBS[1] * (-4) / E2[1])
check(d1 == F(1, 12) and d2 == F(1, 4), "L03 R2 derivatives 1/12 and 1/4")
check(ulog(PROBS, ya) > ulog(PROBS, E1) and ulog(PROBS, yb) > ulog(PROBS, E2), "L03 R2 small trade improves both (numeric)")
w2a = (F(2), F(4), F(3))
w2b = (F(2), F(4), F(1))
dA = ulog(PROBS, w2a) - ulog(PROBS, E1)
dB = ulog(PROBS, w2b) - ulog(PROBS, E2)
quarter = Decimal(1) / 4 * (Decimal(4) / Decimal(3)).ln()
check(abs(dA - quarter) < Decimal("1e-40") and abs(dB - quarter) < Decimal("1e-40"),
      f"L03 E2 witness gain = (1/4) ln(4/3) = {float(quarter):.6f} for both agents")
check(mrs(E1, 0, 1) == F(8, 3) and mrs(E2, 0, 1) == 8, "L03 R2 endowment MRS_12 = 8/3 (agent 1) and 8 (agent 2)")
check(ulog(PROBS, w2a) > ulog(PROBS, E1) and ulog(PROBS, w2b) > ulog(PROBS, E2), "L03 E2 witness improves both")

# Pareto grid search, exact feasibility, Decimal utilities, tolerance 1e-12 as in the twin
GRID = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
TOL = Decimal("1e-12")
def U(b):
    if any(z == 0 for z in b):
        return None
    return ulog(PROBS, b)
ref_eq = (U(x1), U(x2))
ref_en = (U(E1), U(E2))
cands = []
for fr in product(GRID, repeat=3):
    a = tuple(f * t for f, t in zip(fr, ebar))
    bb = tuple((1 - f) * t for f, t in zip(fr, ebar))
    cands.append((a, bb))
check(len(cands) == 125, f"L03 grid 125 allocations ({len(cands)})")
def improves(ua, ub, ref):
    if ua is None or ub is None:
        return False
    worse = ua < ref[0] - TOL or ub < ref[1] - TOL
    better = ua > ref[0] + TOL or ub > ref[1] + TOL
    return (not worse) and better
cnt_eq = 0
cnt_en = 0
first = None
min_margin = Decimal(1)
for a, bb in cands:
    ua, ub = U(a), U(bb)
    if improves(ua, ub, ref_eq):
        cnt_eq += 1
    if improves(ua, ub, ref_en):
        cnt_en += 1
        if first is None:
            first = (a, bb)
    if ua is not None and ub is not None:
        for val, ref in ((ua, ref_en[0]), (ub, ref_en[1])):
            m = abs(val - ref)
            if m > Decimal("1e-30") and m < min_margin:
                min_margin = m
check(cnt_eq == 0, f"L03 Part B: Pareto improvements of the equilibrium on grid = {cnt_eq} (expected 0)")
check(cnt_en == 2, f"L03 Part B: Pareto improvements of the endowment on grid = {cnt_en} (expected 2)")
check(first is not None and tuple(str(z) for z in first[0]) == ('2', '4', '3')
      and tuple(str(z) for z in first[1]) == ('2', '4', '1'), f"L03 first improvement {first}")
print(f"INFO smallest nonzero utility difference to the endowment reference across grid: {float(min_margin):.3e}")
# Also the two sides near the tolerance
near = 0
for a, bb in cands:
    ua, ub = U(a), U(bb)
    if ua is None or ub is None:
        continue
    for val, ref in ((ua, ref_en[0]), (ub, ref_en[1])):
        if Decimal("1e-15") < abs(val - ref) < Decimal("1e-9"):
            near += 1
check(near == 0, f"L03 no grid utility difference within (1e-15, 1e-9) of the endowment reference (near={near})")

print("FAILS:", len(FAILS))
sys.exit(1 if FAILS else 0)
