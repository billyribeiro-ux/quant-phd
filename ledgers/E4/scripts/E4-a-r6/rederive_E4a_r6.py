"""E4 slice a round 6: independent re-derivation of the numbers printed on L01-L03 and the hub.

Usage: python -I rederive_E4a_r6.py. Uses only fractions, math and itertools; written from the page text, not from the lab code.
"""
from __future__ import annotations

import math
from fractions import Fraction as F
from itertools import product

# L01 Example 1.5 and Lab 1
pi = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
claim = [F(100), F(40), F(0), F(250)]
q = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
other = [F(0), F(60), F(120), F(30)]
val = lambda x, p: sum(a * b for a, b in zip(x, p))
print("L01 value claim", val(claim, q), "=340/3?", val(claim, q) == F(340, 3))
print("L01 value other", val(other, q), "=56?", val(other, q) == 56)
comb = [2 * a - F(1, 2) * b for a, b in zip(claim, other)]
print("L01 combination", comb, "value", val(comb, q), "=596/3?", val(comb, q) == F(596, 3))
print("L01 expected payoff", val(claim, pi), "=235/4?", val(claim, pi) == F(235, 4), "sum pi", sum(pi))
print("L01 short vector sum", F(1, 8) + F(3, 8) + F(3, 8) + F(1, 4), "=9/8?", F(1, 8) + F(3, 8) + F(3, 8) + F(1, 4) == F(9, 8))
# L01 M1, M3, P3, R2, Q2 numbers
print("L01 M1 V", val([10, 0, 30], [F(1, 3), F(1, 5), F(1, 2)]), "E", val([10, 0, 30], [F(1, 2), F(1, 4), F(1, 4)]))
print("L01 M3 V(3x-2y)", val([3 * a - 2 * b for a, b in zip([1, 2, 3], [4, 0, 1])], [F(1, 2), F(1, 4), F(1, 8)]))
print("L01 R2 V(e1)", (F(1, 2)) ** 2, "V(2e1)", (2 * F(1, 2)) ** 2)
print("L01 quiz 4.25", F(1, 2) * 5 + F(1, 4) * 7, "E x quiz", F(1, 4) * 0 + F(3, 4) * 4)
print("L01 quiz 0.6", 0.2 + 0.3 + 0.1)

# L02 Example 2.11 and Lab 2
PI = [F(1, 2), F(1, 4), F(1, 4)]
e1 = [F(3), F(4), F(1)]
e2 = [F(1), F(4), F(3)]
ebar = [a + b for a, b in zip(e1, e2)]
theta1 = sum(p * a / t for p, a, t in zip(PI, e1, ebar))
theta2 = sum(p * a / t for p, a, t in zip(PI, e2, ebar))
qs = [p / t for p, t in zip(PI, ebar)]
print("L02 ebar", ebar, "theta", theta1, theta2, "q*", qs, "q.ebar", sum(a * b for a, b in zip(qs, ebar)))
x1 = [t * theta1 for t in ebar]
x2 = [t * theta2 for t in ebar]
print("L02 x1", x1, "x2", x2)
print("L02 wealth", sum(a * b for a, b in zip(qs, e1)), sum(a * b for a, b in zip(qs, e2)))
z = [a + b - c for a, b, c in zip(x1, x2, ebar)]
print("L02 residual z", z, "q.z", sum(a * b for a, b in zip(qs, z)))
print("L02 ratios agent1", [PI[s] / (x1[s] * qs[s]) for s in range(3)], "1/w1", 1 / theta1)
print("L02 ratios agent2", [PI[s] / (x2[s] * qs[s]) for s in range(3)], "1/w2", 1 / theta2)
# Remark 2.6 at q=(2,1,1)
qr = [F(2), F(1), F(1)]
w1 = sum(a * b for a, b in zip(qr, e1))
w2 = sum(a * b for a, b in zip(qr, e2))
d1 = [p * w1 / q_ for p, q_ in zip(PI, qr)]
d2 = [p * w2 / q_ for p, q_ in zip(PI, qr)]
zr = [a + b - c for a, b, c in zip(d1, d2, ebar)]
print("Remark 2.6 w", w1, w2, "d1", d1, "d2", d2, "z", zr, "sum z", sum(zr), "q.z", sum(a * b for a, b in zip(qr, zr)))
# Misconception 2 of L02: v=(1,-1,0) at q*
print("L02 misc2 q.v", qs[0] - qs[1])
# Misconception 3: e1 cost at q*
print("L02 cost e1", sum(a * b for a, b in zip(qs, e1)))
# M1, M2, M3 of L02
print("L02 M1", F(1, 2) * F(1, 2) / F(1, 4), F(1, 2) * F(1, 2) / F(1, 8), "spend", F(1, 4) * 1 + F(1, 8) * 2)
print("L02 M2", [F(1, 4) * 3 / 1, F(1, 4) * 3 / 2, F(1, 2) * 3 / 1], "spend", F(3, 4) + 2 * F(3, 8) + F(3, 2))
print("L02 M3 theta", F(1, 2) * F(1, 4) + F(1, 2) * F(3, 4))
# L02 R2 check and Lab 2 interpretation residual count
# L02 quiz Q5 q*_1 and q*_3
print("L02 q1*", F(1, 2) / 4, "q3*", F(1, 4) / 4)

# L03 Example 3.6 MRS with u = ln (MRS = (pi_s/x_s)/(pi_t/x_t))
for name, x in (("agent1", x1), ("agent2", x2)):
    m12 = (PI[0] / x[0]) / (PI[1] / x[1])
    m13 = (PI[0] / x[0]) / (PI[2] / x[2])
    m23 = (PI[1] / x[1]) / (PI[2] / x[2])
    print("L03", name, "MRS12", m12, "MRS13", m13, "MRS23", m23)
print("L03 price ratios", qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2])
# endowment MRS (for R2)
for name, x in (("agent1 endow", e1), ("agent2 endow", e2)):
    print("L03 endowment MRS12", name, (PI[0] / x[0]) / (PI[1] / x[1]))
# L03 R2 derivatives
g1 = F(1, 2) * F(-1, 3) + F(1, 4) * F(4, 4)
g2 = F(1, 2) * F(1, 1) + F(1, 4) * F(-4, 4)
print("L03 R2 derivative agent1", g1, "agent2", g2)

# L03 Lab 3 grid counts (independent): grid fractions {0,1/4,1/2,3/4,1}; agent 1 gets f*ebar, agent 2 gets (1-f)*ebar
GRID = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
TOL = 1e-12


def U(bundle: list[F]) -> float:
    if any(b == 0 for b in bundle):
        return -math.inf
    return sum(float(p) * math.log(float(b)) for p, b in zip(PI, bundle))


def better(cand: tuple[float, float], ref: tuple[float, float]) -> bool:
    no_worse = all(c >= r - TOL for c, r in zip(cand, ref))
    some_better = any(c > r + TOL for c, r in zip(cand, ref))
    return no_worse and some_better


ref_eq = (U(x1), U(x2))
ref_end = (U(e1), U(e2))
grid = list(product(GRID, repeat=3))
print("L03 grid size", len(grid))
cnt_eq = cnt_end = 0
first = None
for f in grid:
    a = [fi * t for fi, t in zip(f, ebar)]
    b = [(1 - fi) * t for fi, t in zip(f, ebar)]
    cand = (U(a), U(b))
    if better(cand, ref_eq):
        cnt_eq += 1
    if better(cand, ref_end):
        cnt_end += 1
        if first is None:
            first = (a, b)
print("L03 improvements at equilibrium", cnt_eq, "at endowment", cnt_end, "first", first)
# the equilibrium bundles are off-grid
print("L03 equilibrium fractions", [x / t for x, t in zip(x1, ebar)], "on grid?", all(x / t in GRID for x, t in zip(x1, ebar)))

# Lab 3 Part A alternative: all three rates equal the price ratios exactly
print("L03 rate equality exact", all(((PI[0] / x1[0]) / (PI[1] / x1[1]) == qs[0] / qs[1],
                                       (PI[0] / x2[0]) / (PI[1] / x2[1]) == qs[0] / qs[1]) == (True, True)
                                      for x1_, x2_ in [(x1, x2)] for x1 in [x1_] for x2 in [x2_]))
# M2 of L03: pi=(1/2,1/2), q=(2,1), w=6
xm = [F(1, 2) * 6 / 2, F(1, 2) * 6 / 1]
print("L03 M2 x", xm, "MRS", (F(1, 2) / xm[0]) / (F(1, 2) / xm[1]), "spend", 2 * xm[0] + xm[1])
# L03 M1: pi=(1/3,2/3), x=(1,4)
print("L03 M1 MRS12", (F(1, 3) / 1) / (F(2, 3) / 4))
# L03 P1 / E2: witness feasibility
print("L03 witness sum", [a + b for a, b in zip([2, 4, 3], [2, 4, 1])], "ebar", ebar)
