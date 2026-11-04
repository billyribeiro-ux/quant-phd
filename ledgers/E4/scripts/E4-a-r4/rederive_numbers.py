"""Independent re-derivation of the E4 slice numbers (L01 to L03 and the hub), without importing the twins.

Exact checks use fractions.Fraction; the grid search uses floats with the page's TOL = 1e-12 and reports the
smallest gap to the threshold so that no count depends on a near-tie.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction as F

# ---- L01 (four-state claim) ----
pi = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
q = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
x = [F(100), F(40), F(0), F(250)]
y = [F(0), F(60), F(120), F(30)]
V = lambda z, p: sum(a * b for a, b in zip(p, z))  # noqa: E731
print("L01 V(x)", V(x, q), "V(y)", V(y, q), "E x", sum(a * b for a, b in zip(pi, x)), "V at pi", V(x, pi))
z = [2 * a - F(1, 2) * b for a, b in zip(x, y)]
print("L01 combo", V(z, q), 2 * V(x, q) - F(1, 2) * V(y, q), "combo payoff", z)
print("L01 M1 V", F(10) * F(1, 3) + F(30) * F(1, 2), "E", F(10) * F(1, 2) + F(30) * F(1, 4))
print("L01 M3", V([F(3) * a - 2 * b for a, b in zip([F(1), F(2), F(3)], [F(4), F(0), F(1)])], [F(1, 2), F(1, 4), F(1, 8)]))
print("L01 short sum", sum([F(1, 8), F(3, 8), F(3, 8), F(1, 4)]))

# ---- L02 (three-state log economy, Example 2.11) ----
P = [F(1, 2), F(1, 4), F(1, 4)]
E1 = [F(3), F(4), F(1)]
E2 = [F(1), F(4), F(3)]
E = [a + b for a, b in zip(E1, E2)]
w1 = sum(a * b for a, b in zip(q, E1))
th1 = sum(p * e / t for p, e, t in zip(P, E1, E))
th2 = sum(p * e / t for p, e, t in zip(P, E2, E))
qs = [p / t for p, t in zip(P, E)]
print("L02 agg", E, "theta", th1, th2, "q*", qs, "q*.E", sum(a * b for a, b in zip(qs, E)))
x1 = [th1 * t for t in E]
x2 = [th2 * t for t in E]
print("L02 x1", x1, "x2", x2, "clear", [a + b - t for a, b, t in zip(x1, x2, E)])
print("L02 budget", sum(a * b for a, b in zip(qs, x1)) - th1, sum(a * b for a, b in zip(qs, x2)) - th2)
print("L02 ratios agent1", [P[s] / (x1[s] * qs[s]) for s in range(3)], "1/th1", 1 / th1)
print("L02 ratios agent2", [P[s] / (x2[s] * qs[s]) for s in range(3)], "1/th2", 1 / th2)
# Remark 2.6 witness at q = (2,1,1)
qq = [F(2), F(1), F(1)]
wa, wb = sum(a * b for a, b in zip(qq, E1)), sum(a * b for a, b in zip(qq, E2))
da = [P[s] * wa / qq[s] for s in range(3)]
db = [P[s] * wb / qq[s] for s in range(3)]
zz = [a + b - t for a, b, t in zip(da, db, E)]
print("Remark 2.6: wealths", wa, wb, "demands", da, db, "z", zz, "unweighted sum", sum(zz), "q.z", sum(a * b for a, b in zip(qq, zz)))
# Misconception 2 vector at q*
v = [F(1), F(-1), F(0)]
print("Misc2 q*.v", sum(a * b for a, b in zip(qs, v)))
print("Misc3 q*.e1", sum(a * b for a, b in zip(qs, E1)), "theta1", th1)
print("Misc1 prices state2 vs state3", qs[1], qs[2])
# Problem M1..M3 in L02

pm2 = [F(1, 4), F(1, 4), F(1, 2)]; qm2 = [F(1), F(2), F(1)]
print("L02 M2 x", [pm2[s] * 3 / qm2[s] for s in range(3)], "spend", sum(a * b for a, b in zip(qm2, [pm2[s] * 3 / qm2[s] for s in range(3)])))
# R2 L02 (log own price): not numeric

# ---- L03 ----
def u(bundle, probs=P):
    return sum(p * math.log(b) for p, b in zip(probs, bundle))

GRID = [0, 0.25, 0.5, 0.75, 1]
ref_eq = (u(x1), u(x2))
ref_end = (u(E1), u(E2))
Ef = [float(t) for t in E]
Pf = [float(p) for p in P]
TOL = 1e-12
cands = []
for f in itertools.product(GRID, repeat=3):
    a = [f[s] * Ef[s] for s in range(3)]
    b = [(1 - f[s]) * Ef[s] for s in range(3)]
    cands.append((a, b))
print("L03 grid size", len(cands))

def ua(bundle):
    if any(t <= 0 for t in bundle):
        return -math.inf
    return sum(p * math.log(t) for p, t in zip(Pf, bundle))

def count(ref):
    n = 0
    worst = math.inf
    for a, b in cands:
        ua_ = ua(a)
        ub_ = ua(b)
        ra, rb = ref
        ok_both = ua_ >= ra - TOL and ub_ >= rb - TOL
        strict = ua_ > ra + TOL or ub_ > rb + TOL
        worst = min(worst, abs(min(ua_ - ra, ub_ - rb)))
        if ok_both and strict:
            n += 1
    return n, worst

print("L03 improvements at equilibrium (count, closest-gap)", count(ref_eq))
print("L03 improvements at endowment (count, closest-gap)", count(ref_end))
first = None
for a, b in cands:
    if ua(a) >= ref_end[0] - TOL and ua(b) >= ref_end[1] - TOL and (ua(a) > ref_end[0] + TOL or ua(b) > ref_end[1] + TOL):
        first = (a, b)
        break
print("L03 first improvement at endowment", first)
# Example 3.6 MRS and P2 identity
print("L03 MRS agent1 12/13/23", [(P[s] / x1[s]) / (P[t] / x1[t]) for s, t in ((0, 1), (0, 2), (1, 2))])
print("L03 MRS agent2 12/13/23", [(P[s] / x2[s]) / (P[t] / x2[t]) for s, t in ((0, 1), (0, 2), (1, 2))])
print("L03 price ratios", [qs[s] / qs[t] for s, t in ((0, 1), (0, 2), (1, 2))])
print("L03 R2 endowment MRS 12 agent1, agent2", (P[0] / E1[0]) / (P[1] / E1[1]), (P[0] / E2[0]) / (P[1] / E2[1]))
print("L03 R2 derivatives", F(1, 2) * F(-1, 3) + F(1, 4) * 1, F(1, 2) * 1 + F(1, 4) * -1)
