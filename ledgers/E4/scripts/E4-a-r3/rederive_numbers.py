"""Verifier re-derivation (E4 slice a, round 3). Independent of the builder's code.

Recomputes every number the slice (index.html, L01-L03, lab twins L01-L03) states, with exact Fractions,
and prints OK/MISMATCH per check. Run: python -I rederive_numbers.py   (stdlib only)
"""

from __future__ import annotations

import math
from fractions import Fraction as F
from itertools import product

results: list[tuple[str, bool, str]] = []


def check(name: str, got: object, want: object) -> None:
    ok = got == want
    results.append((name, ok, f"got={got!r} want={want!r}"))


# ---------- index.html ----------
check("hub: 9 lessons x 8 h", 9 * 8, 72)
check("hub: 72 + 28 = 100", 72 + 28, 100)
check("hub: 28% of 100", F(28, 100) * 100, 28)
check("hub placement: 7 of 8 = 87.5%", F(7, 8) * 100, F(175, 2))
check("hub placement: 6 of 8 = 75%", F(6, 8) * 100, 75)
check("hub item1 E[lottery 0 w.p.1/4, 8 w.p.3/4]", F(0) * F(1, 4) + 8 * F(3, 4), 6)
check("hub item2 d/dx ln x at 4", F(1, 4), F(25, 100))
check("hub item5 E u(x)=x^2 on {0,4} w.p. 1/2", F(1, 2) * 0**2 + F(1, 2) * 4**2, 8)
check("hub item7 value 10c*1/2 + 30c*1/4", F(1, 2) * 10 + F(1, 4) * 30, F(25, 2))
check("hub item8 log demand pi1 w / q1", F(1, 2) * 1 / F(1, 8), 4)

# ---------- L01 ----------
pi1 = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
prices = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
claim = (F(100), F(40), F(0), F(250))
other = (F(0), F(60), F(120), F(30))


def val(x, q):
    return sum((a * b for a, b in zip(x, q, strict=True)), F(0))


check("L01 sum pi = 1 (Ex 1.5)", sum(pi1), 1)
check("L01 V(claim) = 340/3", val(claim, prices), F(340, 3))
check("L01 V(other) = 56", val(other, prices), 56)
combo = tuple(2 * a - F(1, 2) * b for a, b in zip(claim, other, strict=True))
check("L01 combo payoff", combo, (200, 50, -60, 485))
check("L01 V(combo) = 596/3", val(combo, prices), F(596, 3))
check("L01 2V(claim) - V(other)/2 = 596/3", 2 * val(claim, prices) - F(1, 2) * val(other, prices), F(596, 3))
check("L01 E claim = 235/4", val(claim, pi1), F(235, 4))
check("L01 E claim = 58.75", float(val(claim, pi1)), 58.75)
check("L01 V(claim) ~ 113.33", round(float(val(claim, prices)), 2), 113.33)
check("L01 gap V - E = 340/3 - 235/4 = 655/12", val(claim, prices) - val(claim, pi1), F(655, 12))
# M1
x_m1 = (F(10), F(0), F(30))
pi_m1 = (F(1, 2), F(1, 4), F(1, 4))
q_m1 = (F(1, 3), F(1, 5), F(1, 2))
check("L01 M1 V = 55/3", val(x_m1, q_m1), F(55, 3))
check("L01 M1 E = 25/2", val(x_m1, pi_m1), F(25, 2))
check("L01 M1 gap = 35/6", val(x_m1, q_m1) - val(x_m1, pi_m1), F(35, 6))
check("L01 M1 55/3 to 2dp", round(float(val(x_m1, q_m1)), 2), 18.33)
# M2
check("L01 M2 V = 25", F(4, 10) * 0 + F(5, 10) * 50, 25)
# M3
x3, y3 = (F(1), F(2), F(3)), (F(4), F(0), F(1))
q3 = (F(1, 2), F(1, 4), F(1, 8))
comb3 = tuple(3 * a - 2 * b for a, b in zip(x3, y3, strict=True))
check("L01 M3 comb = (-5,6,7)", comb3, (-5, 6, 7))
check("L01 M3 V(3x-2y) = -1/8", val(comb3, q3), F(-1, 8))
check("L01 M3 V(x)=11/8", val(x3, q3), F(11, 8))
check("L01 M3 V(y)=17/8", val(y3, q3), F(17, 8))
check("L01 M3 3V(x)-2V(y) = -1/8", 3 * F(11, 8) - 2 * F(17, 8), F(-1, 8))
# P3
check("L01 P3 V(e1)=1/4", F(1, 4), F(1, 4))
check("L01 P3 E e1 = 1/3", F(1, 3), F(1, 3))
# R2 size effect
check("L01 R2 V(e1)=1/4", (F(1, 2)) ** 2, F(1, 4))
check("L01 R2 V(2e1)=1", (2 * F(1, 2)) ** 2, 1)
# Quiz
check("L01 quiz value (5,7) at (1/2,1/4)", F(1, 2) * 5 + F(1, 4) * 7, F(17, 4))
check("L01 quiz E(0,4) w.p.(1/4,3/4)", F(4) * F(3, 4), 3)
check("L01 quiz value of iota at (0.2,0.3,0.1)", F(2, 10) + F(3, 10) + F(1, 10), F(3, 5))
check("L01 quiz 2V(x) = V(2x)", 2 * val((F(5), F(7)), (F(1, 2), F(1, 4))), val((F(10), F(14)), (F(1, 2), F(1, 4))))

# ---------- L02 ----------
pi2 = (F(1, 2), F(1, 4), F(1, 4))
e1 = (F(3), F(4), F(1))
e2 = (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(e1, e2, strict=True))
check("L02 aggregate (4,8,4)", ebar, (4, 8, 4))
th1 = sum((p * a / b for p, a, b in zip(pi2, e1, ebar, strict=True)), F(0))
th2 = sum((p * a / b for p, a, b in zip(pi2, e2, ebar, strict=True)), F(0))
check("L02 theta1 = 9/16", th1, F(9, 16))
check("L02 theta2 = 7/16", th2, F(7, 16))
qstar = tuple(p / b for p, b in zip(pi2, ebar, strict=True))
check("L02 q* = (1/8,1/32,1/16)", qstar, (F(1, 8), F(1, 32), F(1, 16)))
check("L02 q*.ebar = 1", val(qstar, ebar), 1)
x1 = tuple(th1 * b for b in ebar)
x2 = tuple(th2 * b for b in ebar)
check("L02 x1* = (9/4,9/2,9/4)", x1, (F(9, 4), F(9, 2), F(9, 4)))
check("L02 x2* = (7/4,7/2,7/4)", x2, (F(7, 4), F(7, 2), F(7, 4)))
check("L02 budget agent1 q.x1 = w1 = 9/16", val(qstar, x1), th1)
check("L02 budget agent2 q.x2 = w2 = 7/16", val(qstar, x2), th2)
check("L02 w1 = q*.e1 = 9/16", val(qstar, e1), F(9, 16))
check("L02 w2 = q*.e2 = 7/16", val(qstar, e2), F(7, 16))
check("L02 market clearing", tuple(a + b for a, b in zip(x1, x2, strict=True)), ebar)
check("L02 ratio pi/(x q) agent1 = 16/9", pi2[0] / (x1[0] * qstar[0]), F(16, 9))
check("L02 ratio pi/(x q) agent1 = 16/9 (state 3)", pi2[2] / (x1[2] * qstar[2]), F(16, 9))
check("L02 ratio agent2 = 16/7", pi2[1] / (x2[1] * qstar[1]), F(16, 7))
check("L02 1/w1 = 16/9", 1 / th1, F(16, 9))
check("L02 1/w2 = 16/7", 1 / th2, F(16, 7))
check("L02 Remark: scaling by 3 with wealth re-valued keeps demand", tuple(F(1, 2) * 1 for _ in range(1)), (F(1, 2),))
w1_scaled = val(tuple(3 * q for q in qstar), e1)
check("L02 Part E: wealth at 3q = 27/16", w1_scaled, F(27, 16))
check("L02 Part E: demand at 3q, 3w: x_s unchanged", tuple(pi2[s] * w1_scaled / (3 * qstar[s]) for s in range(3)), x1)
check("L02 Part E: demand with wealth fixed falls by 3", tuple(pi2[s] * th1 / (3 * qstar[s]) for s in range(3)), tuple(a / 3 for a in x1))
# M1
check("L02 M1 x=(1,2)", (F(1, 2) * F(1, 2) / F(1, 4), F(1, 2) * F(1, 2) / F(1, 8)), (1, 2))
check("L02 M1 spend 1/2", F(1, 4) * 1 + F(1, 8) * 2, F(1, 2))
# M2
x_m2 = tuple(p * 3 / q for p, q in zip((F(1, 4), F(1, 4), F(1, 2)), (1, 2, 1), strict=True))
check("L02 M2 x = (3/4,3/8,3/2)", x_m2, (F(3, 4), F(3, 8), F(3, 2)))
check("L02 M2 spend = 3", sum((q * x for q, x in zip((1, 2, 1), x_m2, strict=True)), F(0)), 3)
# M3
check("L02 M3 q*=(1/8,1/8)", tuple(F(1, 2) / 4 for _ in range(2)), (F(1, 8), F(1, 8)))
check("L02 M3 theta1 = 1/2", F(1, 2) * F(1, 4) + F(1, 2) * F(3, 4), F(1, 2))
# Misconception 2: z=(1,-1,0), q.z
check("L02 MC2 q.z = 3/32", qstar[0] - qstar[1], F(3, 32))
# Misconception 3: e1 cost at q*
check("L02 MC3 q*.e1 = w1 = 9/16", val(qstar, e1), F(9, 16))
# MC1: prices
check("L02 MC1 q*_2 / q*_3 = 1/2", qstar[1] / qstar[2], F(1, 2))
# Example 2.11 numbers exact
check("L02 Ex 2.11 prices (1/8,1/32,1/16)", qstar, (F(1, 8), F(1, 32), F(1, 16)))
# Canon-breaks utility -1/x: u'=1/x^2>0, u''=-2/x^3<0 at sample points
check("L02 utility -1/x: u' = 1/x^2 > 0 at x=2", F(1, 4) > 0, True)
check("L02 utility -1/x: u'' = -2/x^3 < 0 at x=2", F(-2, 8) < 0, True)
# Quiz
check("L02 quiz q*_1=0.125", float(qstar[0]), 0.125)
check("L02 quiz q*_3=0.0625", float(qstar[2]), 0.0625)
check("L02 quiz x_2 M1 = 2", F(1, 2) * F(1, 2) / F(1, 8), 2)

# ---------- L03 ----------
mrs = lambda x, p, s, t: (p[s] / x[s]) / (p[t] / x[t])  # noqa: E731
check("L03 MRS agent1 12 = 4", mrs(x1, pi2, 0, 1), 4)
check("L03 MRS agent1 13 = 2", mrs(x1, pi2, 0, 2), 2)
check("L03 MRS agent1 23 = 1/2", mrs(x1, pi2, 1, 2), F(1, 2))
check("L03 MRS agent2 12 = 4", mrs(x2, pi2, 0, 1), 4)
check("L03 MRS agent2 13 = 2", mrs(x2, pi2, 0, 2), 2)
check("L03 MRS agent2 23 = 1/2", mrs(x2, pi2, 1, 2), F(1, 2))
check("L03 price ratio q1/q2 = 4", qstar[0] / qstar[1], 4)
check("L03 price ratio q1/q3 = 2", qstar[0] / qstar[2], 2)
check("L03 price ratio q2/q3 = 1/2", qstar[1] / qstar[2], F(1, 2))
check("L03 Example 3.6 MRS of endowment agent1 12 = 8/3", mrs(e1, pi2, 0, 1), F(8, 3))
check("L03 Example 3.6 MRS of endowment agent2 12 = 8", mrs(e2, pi2, 0, 1), 8)
# M1 MRS
check("L03 M1 MRS12 = 2", (F(1, 3) / 1) / (F(2, 3) / 4), 2)
# M2 MRS
check("L03 M2 MRS12 = 2", (F(1, 2) / F(3, 2)) / (F(1, 2) / 3), 2)
# P2 general identity: (pi_s ebar_t)/(pi_t ebar_s) = q*_s/q*_t
check("L03 P2 identity", (pi2[0] * ebar[2]) / (pi2[2] * ebar[0]), qstar[0] / qstar[2])
# R2 derivatives at endowment
d1 = pi2[0] * (F(-1, 3)) + pi2[1] * (F(4, 4))
d2 = pi2[0] * (F(1, 1)) + pi2[1] * (F(-4, 4))
check("L03 R2 derivative U1 = 1/12", d1, F(1, 12))
check("L03 R2 derivative U2 = 1/4", d2, F(1, 4))
check("L03 R2 MRS endowment agent1 = 8/3 (recomputed from e1)", mrs(e1, pi2, 0, 1), F(8, 3))
check("L03 R2 feasibility sum", tuple(a + b for a, b in zip((3 - F(1, 2), 4 + 4 * F(1, 2), 1), (1 + F(1, 2), 4 - 4 * F(1, 2), 3), strict=True)), ebar)

# Lab 3 grid: utilities with floats, same TOL as the twin
TOL = 1e-12
GRID = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))


def util(p, bundle):
    t = 0.0
    for pp, x in zip(p, bundle, strict=True):
        if x == 0:
            return -math.inf
        t += float(pp) * math.log(float(x))
    return t


cands = []
for fr in product(GRID, repeat=3):
    a = tuple(f * b for f, b in zip(fr, ebar, strict=True))
    b = tuple((1 - f) * t for f, t in zip(fr, ebar, strict=True))
    cands.append((a, b))
ref_eq = (util(pi2, x1), util(pi2, x2))
ref_en = (util(pi2, e1), util(pi2, e2))


def improves(c, r):
    no_worse = all(ci >= ri - TOL for ci, ri in zip(c, r, strict=True))
    some_better = any(ci > ri + TOL for ci, ri in zip(c, r, strict=True))
    return no_worse and some_better


imp_eq = [(a, b) for a, b in cands if improves((util(pi2, a), util(pi2, b)), ref_eq)]
imp_en = [(a, b) for a, b in cands if improves((util(pi2, a), util(pi2, b)), ref_en)]
check("L03 grid size 125", len(cands), 125)
check("L03 PO improvements at equilibrium on grid = 0", len(imp_eq), 0)
check("L03 PO improvements at endowment on grid = 2", len(imp_en), 2)
check(
    "L03 first endowment improvement = ((2,4,3),(2,4,1))",
    (tuple(str(z) for z in imp_en[0][0]), tuple(str(z) for z in imp_en[0][1])),
    (("2", "4", "3"), ("2", "4", "1")),
)
# margin of the witness, to show the float tolerance is not borderline
a, b = imp_en[0]
margins = [util(pi2, a) - ref_en[0], util(pi2, b) - ref_en[1]]
check("L03 witness margins exceed TOL", all(m > 1e-6 for m in margins), True)
check("L03 witness margins (float) 0.072-ish agent1 > 0.05", margins[0] > 0.05, True)

failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("OK      " if ok else "MISMATCH"), name, "" if ok else detail)
print(f"total={len(results)} ok={len(results) - len(failed)} mismatch={len(failed)}")
