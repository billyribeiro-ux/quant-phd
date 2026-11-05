"""E4 slice a, round 12: independent re-derivation of every number in the L01-L03 prose that the round-12 delta touches,
plus the numbers of the full L01-L03 proofs, examples and problem solutions.

Run from the checkout root: .venv/bin/python -I ledgers/E4/scripts/E4-a-r12/rederive_slice_a12.py
Uses only fractions, math, random and itertools. Each check prints PASS or FAIL with the value it computed.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F
from itertools import product

FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("PASS: " if cond else "FAIL: ") + msg)
    if not cond:
        FAILS.append(msg)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), F(0))


# ---------------- L01 ----------------
pi1 = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
x1 = (F(100), F(40), F(0), F(250))
q1 = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
other1 = (F(0), F(60), F(120), F(30))
check(sum(pi1) == 1, "L01 Example 1.5: probabilities (1/8,3/8,3/8,1/8) sum to 1")
check(dot(q1, x1) == F(340, 3), f"L01 hypothesis/Part B: V(claim) = {dot(q1, x1)} = 340/3")
check(dot(q1, other1) == 56, f"L01 Part B: V(other) = {dot(q1, other1)} = 56")
comb = tuple(2 * a - F(1, 2) * b for a, b in zip(x1, other1, strict=True))
check(dot(q1, comb) == 2 * dot(q1, x1) - F(1, 2) * dot(q1, other1), f"L01 Part C: linearity exact ({dot(q1, comb)} = 596/3)")
check(dot(q1, comb) == F(596, 3), "L01 Part C: value of combination is 596/3")
check(dot(pi1, x1) == F(235, 4) and F(235, 4) == F(58, 1) + F(3, 4), "L01 Part D: E[x] = 235/4 = 58.75")
check(float(F(340, 3)) == 113.33333333333333 and f"{float(F(340, 3)):.2f}" == "113.33", "L01 E3: 340/3 = 113.33 to 2 dp")
check(dot(pi1, x1) != dot(q1, x1), "L01 Part D: value under prices differs from E[x] (flag False)")
check(sum((F(1, 2), F(1, 2), F(1, 2), F(-1, 2))) == 1 and min((F(1, 2), F(1, 2), F(1, 2), F(-1, 2))) < 0,
      "L01 Part E: negative-entry vector sums to 1 but is rejected for sign")
check(sum((F(1, 8), F(3, 8), F(3, 8), F(1, 4))) == F(9, 8), "L01 Part E: overweight vector sums to 9/8")
# M1 solution
x_m1 = (F(10), F(0), F(30))
q_m1 = (F(1, 3), F(1, 5), F(1, 2))
pi_m1 = (F(1, 2), F(1, 4), F(1, 4))
check(dot(q_m1, x_m1) == F(55, 3), "L01 M1: V(x) = 55/3")
check(dot(pi_m1, x_m1) == F(25, 2), "L01 M1: E x = 25/2 = 12.5")
check(dot(q_m1, x_m1) - dot(pi_m1, x_m1) == F(35, 6), "L01 M1: difference 35/6")
check(f"{float(F(55, 3)):.2f}" == "18.33", "L01 M1: 55/3 is about 18.33 to two decimals")
# M2
check(F(5, 10) * 50 == 25, "L01 M2: V = 0.5 * 50 = 25")
# M3
x_m3 = (F(1), F(2), F(3))
y_m3 = (F(4), F(0), F(1))
q_m3 = (F(1, 2), F(1, 4), F(1, 8))
comb_m3 = tuple(3 * a - 2 * b for a, b in zip(x_m3, y_m3, strict=True))
check(comb_m3 == (F(-5), F(6), F(7)), "L01 M3: 3x - 2y = (-5,6,7)")
check(dot(q_m3, comb_m3) == F(-1, 8), "L01 M3: V(3x-2y) = -1/8")
check(dot(q_m3, x_m3) == F(11, 8) and dot(q_m3, y_m3) == F(17, 8), "L01 M3: V(x)=11/8, V(y)=17/8")
check(3 * F(11, 8) - 2 * F(17, 8) == F(-1, 8), "L01 M3: A2 gives -1/8")
# P3: S = 2, pi=(1/3,2/3), q=(1/4,1/2), x=e1
check(F(1, 4) != F(1, 3), "L01 P3: q_1 = 1/4 differs from pi_1 = 1/3")
# Misconception 1: prices vs probabilities differ in every state
check(all(a != b for a, b in zip(q1, pi1, strict=True)), "L01 misconception 1: prices and probabilities differ in every state")
# R2: V(x) = (sum q x)^2
q_r2 = F(1, 2)
check((q_r2 * 1) ** 2 == F(1, 4) and (q_r2 * 2) ** 2 == 1 and 2 * F(1, 4) == F(1, 2), "L01 R2: V(e1)=1/4, V(2e1)=1 != 1/2")
# Example 1.5 decomposition
check(tuple(x1) == (F(100), F(40), F(0), F(250)), "L01 Example 1.5 claim vector")

# ---------------- L02 ----------------
pi2 = (F(1, 2), F(1, 4), F(1, 4))
e1 = (F(3), F(4), F(1))
e2 = (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(e1, e2, strict=True))
check(ebar == (F(4), F(8), F(4)), "L02 Example 2.11: aggregate (4,8,4)")
th1 = sum(p * a / b for p, a, b in zip(pi2, e1, ebar, strict=True))
th2 = sum(p * a / b for p, a, b in zip(pi2, e2, ebar, strict=True))
check(th1 == F(9, 16) and th2 == F(7, 16) and th1 + th2 == 1, "L02 Example 2.11: theta = 9/16, 7/16")
qstar = tuple(p / b for p, b in zip(pi2, ebar, strict=True))
check(qstar == (F(1, 8), F(1, 32), F(1, 16)), "L02 Example 2.11: q* = (1/8, 1/32, 1/16)")
check(dot(qstar, ebar) == 1, "L02 Prop 2.9: q*.ebar = 1")
x1star = tuple(th1 * b for b in ebar)
x2star = tuple(th2 * b for b in ebar)
check(x1star == (F(9, 4), F(9, 2), F(9, 4)) and x2star == (F(7, 4), F(7, 2), F(7, 4)), "L02 Example 2.11: bundles (9/4,9/2,9/4), (7/4,7/2,7/4)")
check(tuple(a + b for a, b in zip(x1star, x2star, strict=True)) == ebar, "L02: bundles clear the market")
check(dot(qstar, e1) == th1 and dot(qstar, e2) == th2, "L02 Prop 2.9: wealth equals theta_i")
# Remark 2.6 at q=(2,1,1)
qr = (F(2), F(1), F(1))
w1r, w2r = dot(qr, e1), dot(qr, e2)
check(w1r == 11 and w2r == 9, "L02 Remark 2.6: wealths 11 and 9 at q=(2,1,1)")
d1 = tuple(p * w1r / q for p, q in zip(pi2, qr, strict=True))
d2 = tuple(p * w2r / q for p, q in zip(pi2, qr, strict=True))
check(d1 == (F(11, 4),) * 3 and d2 == (F(9, 4),) * 3, "L02 Remark 2.6: demands (11/4)x3 and (9/4)x3")
z = tuple(a + b - c for a, b, c in zip(d1, d2, ebar, strict=True))
check(z == (1, -3, 1) and sum(z) == -1 and dot(qr, z) == 0, "L02 Remark 2.6: z=(1,-3,1), unweighted sum -1, q.z=0")
# Misconception 2: v=(1,-1,0) at q*
v = (1, -1, 0)
check(dot(qstar, v) == F(3, 32), "L02 misconception 2: q*.v = 1/8 - 1/32 = 3/32")
# Misconception 3: endowment costs exactly w1 at q*
check(dot(qstar, e1) == F(9, 16), "L02 misconception 3: endowment costs 9/16 at q*")
# Misconception 1: price of state 2 vs state 3
check(qstar[1] == F(1, 32) and qstar[2] == F(1, 16) and pi2[1] == pi2[2], "L02 misconception 1: equal probabilities, prices 1/32 and 1/16")
# Lab 2 Part D ratios
check(pi2[0] / (x1star[0] * qstar[0]) == F(16, 9), "L02 Part D: ratio agent 1 = 16/9")
check(pi2[0] / (x2star[0] * qstar[0]) == F(16, 7), "L02 Part D: ratio agent 2 = 16/7")
check(F(1, th1) == F(16, 9) and F(1, th2) == F(16, 7), "L02 Part D: ratio = 1/wealth")
# Lab 2 Part E: scaling
qs = tuple(3 * q for q in qstar)
check(tuple(p * dot(qs, e1) / q for p, q in zip(pi2, qs, strict=True)) == x1star, "L02 Part E: demand unchanged after re-valuing wealth")
# Problem M1 (L02)
pm = (F(1, 2), F(1, 2))
qm = (F(1, 4), F(1, 8))
xm = (F(1, 2) * F(1, 2) / qm[0], F(1, 2) * F(1, 2) / qm[1])
check(xm == (1, 2) and dot(qm, xm) == F(1, 2), "L02 M1: demand (1,2), spends w=1/2")
# Problem M2
pm2 = (F(1, 4), F(1, 4), F(1, 2))
qm2 = (F(1), F(2), F(1))
xm2 = tuple(p * 3 / q for p, q in zip(pm2, qm2, strict=True))
check(xm2 == (F(3, 4), F(3, 8), F(3, 2)) and dot(qm2, xm2) == 3, "L02 M2: demand (3/4,3/8,3/2), spends 3")
# Problem M3 (L02)
pm3 = (F(1, 2), F(1, 2))
e1m3 = (F(1), F(3))
e2m3 = (F(3), F(1))
em = tuple(a + b for a, b in zip(e1m3, e2m3, strict=True))
qm3 = tuple(p / b for p, b in zip(pm3, em, strict=True))
thm3 = sum(p * a / b for p, a, b in zip(pm3, e1m3, em, strict=True))
check(em == (4, 4) and qm3 == (F(1, 8), F(1, 8)) and thm3 == F(1, 2), "L02 M3: ebar=(4,4), q*=(1/8,1/8), theta_1=1/2")
# Problem P2 and Remark 2.10: scaling
check(all(F(p) * (3 * F(1, 2)) / (3 * q) == p * F(1, 2) / q for p, q in zip(pi2, qstar, strict=True)), "L02 P2: scaling prices and wealth leaves demand unchanged")
# Lemma 2.4 witness y = (w/(2 q.iota)) iota : q.y = w/2
w_test = F(7, 3)
qt = (F(1, 4), F(2, 5), F(1, 3))
yt = tuple(w_test / (2 * sum(qt)) for _ in qt)
check(dot(qt, yt) == w_test / 2, "L02 Lemma 2.4 witness: q.y = w/2")
# Prop 2.8 exact spending identity and maximization by random sampling
rng = random.Random(12)
U = lambda xs: sum(p * math.log(x) for p, x in zip(pi2, xs, strict=True))
qq = (F(2), F(1), F(1))
ww = F(11)
xs_star = tuple(p * ww / q for p, q in zip(pi2, qq, strict=True))
ok = True
for _ in range(20000):
    raw = [rng.random() + 1e-6 for _ in range(3)]
    s = sum(float(q) * r for q, r in zip(qq, raw, strict=True))
    scale = float(ww) / s * rng.random()
    cand = [r * scale for r in raw]
    if U(cand) > U([float(x) for x in xs_star]) + 1e-12:
        ok = False
        break
check(ok, "L02 Prop 2.8: no random budget bundle beats x* (20000 draws, q=(2,1,1), w=11)")

# ---------------- L03 ----------------
PROBS = pi2
E = (e1, e2)
total = ebar
prices = qstar
dem = (x1star, x2star)
mrs = {}
for agent, b in enumerate(dem, start=1):
    for (s, t) in ((0, 1), (0, 2), (1, 2)):
        mrs[(agent, s, t)] = (PROBS[s] / b[s]) / (PROBS[t] / b[t])
check(mrs[(1, 0, 1)] == 4 and mrs[(1, 0, 2)] == 2 and mrs[(1, 1, 2)] == F(1, 2), "L03 Example 3.6: agent 1 MRS 4, 2, 1/2")
check(mrs[(2, 0, 1)] == 4 and mrs[(2, 0, 2)] == 2 and mrs[(2, 1, 2)] == F(1, 2), "L03 Example 3.6: agent 2 MRS 4, 2, 1/2")
check(prices[0] / prices[1] == 4 and prices[0] / prices[2] == 2 and prices[1] / prices[2] == F(1, 2), "L03 Example 3.6: price ratios 4, 2, 1/2")
# Grid enumeration (exact Fractions; utilities compared as floats with TOL=1e-12, as the lab does)
GRID = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
TOL = 1e-12


def util(bundle):
    if any(x == 0 for x in bundle):
        return -math.inf
    return sum(float(p) * math.log(float(x)) for p, x in zip(PROBS, bundle, strict=True))


def improves(cand, ref):
    return all(c >= r - TOL for c, r in zip(cand, ref, strict=True)) and any(c > r + TOL for c, r in zip(cand, ref, strict=True))


def count_improvements(ref_bundles, grid):
    n = 0
    first = None
    for fr in product(grid, repeat=3):
        a = tuple(f * t for f, t in zip(fr, total, strict=True))
        b = tuple((1 - f) * t for f, t in zip(fr, total, strict=True))
        if improves((util(a), util(b)), ref_bundles):
            n += 1
            if first is None:
                first = (a, b)
    return n, first


ref_eq = (util(x1star), util(x2star))
ref_end = (util(e1), util(e2))
n_eq, _ = count_improvements(ref_eq, GRID)
n_end, first_end = count_improvements(ref_end, GRID)
check(len(list(product(GRID, repeat=3))) == 125, "L03 Part B: 125 grid allocations")
check(n_eq == 0, f"L03 Part B: 0 improvements of the equilibrium on the grid (computed {n_eq})")
check(n_end == 2, f"L03 Part B: 2 improvements of the endowment on the grid (computed {n_end})")
check(first_end is not None and first_end[0] == (F(2), F(4), F(3)) and first_end[1] == (F(2), F(4), F(1)),
      "L03 Part B: first improvement is agent 1 (2,4,3), agent 2 (2,4,1)")
# Finer grid as a sanity check: the equilibrium admits no improvement on denominators up to 12
fine = tuple(F(k, 12) for k in range(13))
n_eq_fine, _ = count_improvements(ref_eq, fine)
check(n_eq_fine == 0, f"L03 sanity: 0 improvements of the equilibrium on a 13-point grid per state (computed {n_eq_fine})")
# E2 solution: the witness rises by (1/4) ln(4/3) for both agents, exactly
wa = (F(2), F(4), F(3))
wb = (F(2), F(4), F(1))
d_a = sum(float(p) * math.log(float(new) / float(old)) for p, new, old in zip(PROBS, wa, e1, strict=True))
d_b = sum(float(p) * math.log(float(new) / float(old)) for p, new, old in zip(PROBS, wb, e2, strict=True))
check(abs(d_a - 0.25 * math.log(4 / 3)) < 1e-15 and abs(d_b - 0.25 * math.log(4 / 3)) < 1e-15,
      "L03 E2: both agents gain (1/4) ln(4/3) at the first witness")
check(tuple(a + b for a, b in zip(wa, wb, strict=True)) == total, "L03 E2: witness feasible (sums to (4,8,4))")
# R2: explicit trade and derivatives at eps=0
d1_eps = F(1, 2) * F(-1, 3) + F(1, 4) * F(1)
d2_eps = F(1, 2) * F(1) + F(1, 4) * F(-1)
check(d1_eps == F(1, 12) and d2_eps == F(1, 4), "L03 R2: derivatives 1/12 and 1/4")
# R2 endowment MRS 8/3 and 8
mrs_e1 = (PROBS[0] / e1[0]) / (PROBS[1] / e1[1])
mrs_e2 = (PROBS[0] / e2[0]) / (PROBS[1] / e2[1])
check(mrs_e1 == F(8, 3) and mrs_e2 == 8, "L03 R2: endowment MRS_12 = 8/3 (agent 1) and 8 (agent 2)")
# R2 bundles sum to ebar and are positive for small eps
eps = F(1, 100)
y1 = (3 - eps, 4 + 4 * eps, F(1))
y2 = (1 + eps, 4 - 4 * eps, F(3))
check(tuple(a + b for a, b in zip(y1, y2, strict=True)) == ebar, "L03 R2: R2 bundles sum to ebar")
# Problem M1 (L03): MRS = 2
check((F(1, 3) / 1) / (F(2, 3) / 4) == 2, "L03 M1: MRS_12 = 2")
# Problem M2 (L03): x=(3/2,3), MRS=2=q1/q2
xm2b = (F(1, 2) * 6 / 2, F(1, 2) * 6 / 1)
check(xm2b == (F(3, 2), 3) and (F(1, 2) / xm2b[0]) / (F(1, 2) / xm2b[1]) == 2, "L03 M2: demand (3/2,3), MRS 2 = q1/q2")
# Problem P2 (L03) identity

print("FAILS:", len(FAILS))
raise SystemExit(1 if FAILS else 0)
