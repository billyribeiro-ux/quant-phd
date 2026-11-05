"""Independent re-derivation of every number on the E4 slice-a pages (L01-L03 and the hub), without the lab code.

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-a-r10/rederive.py
Exact arithmetic uses fractions.Fraction written here from the page statements, not copied from the twins.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction as F

F_ = F
print("== L01")
pi = [F_(1, 8), F_(3, 8), F_(3, 8), F_(1, 8)]
q = [F_(1, 2), F_(1, 3), F_(1, 4), F_(1, 5)]
x = [F_(100), F_(40), F_(0), F_(250)]
y = [F_(0), F_(60), F_(120), F_(30)]
val = lambda p, z: sum(a * b for a, b in zip(p, z))
print("sum pi", sum(pi), "sum q", sum(q))
print("V(x) =", val(q, x), " V(y) =", val(q, y), " E x =", val(pi, x))
print("V(2x-y/2) =", val(q, [2 * a - b / 2 for a, b in zip(x, y)]), " 2V(x)-V(y)/2 =", 2 * val(q, x) - val(q, y) / 2)
print("hub Pq: value of 3 states one cent each under 0.2,0.3,0.1 =", F_(2, 10) + F_(3, 10) + F_(1, 10))
print("M1 (page): x=(10,0,30), q=(1/3,1/5,1/2), pi=(1/2,1/4,1/4): V =", val([F_(1, 3), F_(1, 5), F_(1, 2)], [10, 0, 30]),
      " E x =", val([F_(1, 2), F_(1, 4), F_(1, 4)], [10, 0, 30]), " diff =", val([F_(1, 3), F_(1, 5), F_(1, 2)], [10, 0, 30]) - val([F_(1, 2), F_(1, 4), F_(1, 4)], [10, 0, 30]))
print("float check 340/3 =", float(F_(340, 3)), " 55/3 =", float(F_(55, 3)))
print("quiz: 0.5*5+0.25*7 =", F_(1, 2) * 5 + F_(1, 4) * 7, "; E x (0,4 w 1/4,3/4) =", F_(4) * F_(3, 4))
print("R2 (L01): V(e1)=", (F_(1, 2)) ** 2, " V(2e1)=", (2 * F_(1, 2)) ** 2)
print("P3 (L01): q1 =", F_(1, 4), " pi1 =", F_(1, 3))

print("== L02")
PI = [F_(1, 2), F_(1, 4), F_(1, 4)]
e1 = [F_(3), F_(4), F_(1)]
e2 = [F_(1), F_(4), F_(3)]
ebar = [a + b for a, b in zip(e1, e2)]
th1 = sum(p * a / b for p, a, b in zip(PI, e1, ebar))
th2 = sum(p * a / b for p, a, b in zip(PI, e2, ebar))
qs = [p / b for p, b in zip(PI, ebar)]
print("ebar", ebar, "theta", th1, th2, "q*", qs, "q*.ebar", val(qs, ebar))
d1 = [p * th1 * 1 / qq for p, qq in zip(PI, qs)]
d2 = [p * th2 / qq for p, qq in zip(PI, qs)]
print("demands", [str(a) for a in d1], [str(a) for a in d2], "wealth", val(qs, e1), val(qs, e2))
print("budget residuals", val(qs, d1) - val(qs, e1), val(qs, d2) - val(qs, e2))
print("market clearing", [a + b - c for a, b, c in zip(d1, d2, ebar)], "walras", val(qs, [a + b - c for a, b, c in zip(d1, d2, ebar)]))
print("ratio pi/(x q) agent1", [p / (a * qq) for p, a, qq in zip(PI, d1, qs)], "1/w1", 1 / th1)
print("ratio pi/(x q) agent2", [p / (a * qq) for p, a, qq in zip(PI, d2, qs)], "1/w2", 1 / th2)
print("scale by 3 check: demand at 3q, wealth 3*w:", [p * (3 * th1) / (3 * qq) for p, qq in zip(PI, qs)] == d1)
print("misc: q1 (1/8) vs q3 (1/16); endowment cost e1 at q*", val(qs, e1), "; v=(1,-1,0).q* =", qs[0] - qs[1])
# Remark 2.6 at q=(2,1,1) for the same economy
qr = [F_(2), F_(1), F_(1)]
w1, w2 = val(qr, e1), val(qr, e2)
dr1 = [p * w1 / qq for p, qq in zip(PI, qr)]
dr2 = [p * w2 / qq for p, qq in zip(PI, qr)]
zr = [a + b - c for a, b, c in zip(dr1, dr2, ebar)]
print("Remark 2.6: w1,w2 =", w1, w2, " demands", [str(a) for a in dr1], [str(a) for a in dr2], " z =", [str(a) for a in zr],
      " unweighted sum", sum(zr), " q.z", val(qr, zr))
# M1, M2, M3 of L02
print("L02 M1: x =", F_(1, 2) * F_(1, 2) / F_(1, 4), F_(1, 2) * F_(1, 2) / F_(1, 8), " spend", F_(1, 4) * 1 + F_(1, 8) * 2)
print("L02 M2: x =", [F_(1, 4) * 3 / 1, F_(1, 4) * 3 / 2, F_(1, 2) * 3 / 1], " spend", F_(3, 4) + 2 * F_(3, 8) + F_(3, 2))
print("L02 M3 ebar", [F_(1) + F_(3), F_(3) + F_(1)], " q*", [F_(1, 2) / 4, F_(1, 2) / 4])
print("L02 P2 / R2: d x/dq = -pi w / q^2 at q=1/2: ", -F_(1, 2) * 1 / F_(1, 4))
print("KKT: mu = 1/w; pi_s/x_s = mu q_s check for example 2.8 M1:",
      [F_(1, 2) / 1, F_(1, 2) / 2] == [F_(1, 2) / 1, F_(1, 2) / 2])
# utility -1/x: FOC pi/x^2 = mu q, and the log FOC pi/x = mu q
print("L02 canon: u=-1/x, u'(x)=1/x^2 ; at x=1: u'=", 1)

print("== L03")
def mrs(pi_, x_, s, t):
    return (pi_[s] / x_[s]) / (pi_[t] / x_[t])
for (s, t) in [(0, 1), (0, 2), (1, 2)]:
    print("MRS states", s + 1, t + 1, "agent1", mrs(PI, d1, s, t), "agent2", mrs(PI, d2, s, t), "price ratio", qs[s] / qs[t])
print("MRS at endowment agent1 (1,2)", mrs(PI, e1, 0, 1), " agent2", mrs(PI, e2, 0, 1))
print("Example 3.6 MRS_12 agent1 from page x=(9/4,9/2,9/4): ", mrs(PI, [F_(9, 4), F_(9, 2), F_(9, 4)], 0, 1))
print("M1 (L03): MRS12 at pi=(1/3,2/3), x=(1,4):", (F_(1, 3) / 1) / (F_(2, 3) / 4))
print("M2 (L03): x = (3/2, 3) at q=(2,1), w=6:", [F_(1, 2) * 6 / 2, F_(1, 2) * 6 / 1], " MRS", (F_(1, 2) / F_(3, 2)) / (F_(1, 2) / 3))

# independent grid search (floats, own implementation)
grid = [0.0, 0.25, 0.5, 0.75, 1.0]
tot = [4.0, 8.0, 4.0]
pr = [0.5, 0.25, 0.25]
def U(bundle):
    if any(b <= 0 for b in bundle):
        return -math.inf
    return sum(p * math.log(b) for p, b in zip(pr, bundle))
ref_eq = (U([9 / 4, 9 / 2, 9 / 4]), U([7 / 4, 7 / 2, 7 / 4]))
ref_en = (U([3.0, 4.0, 1.0]), U([1.0, 4.0, 3.0]))
def better(c, r):
    return all(ci >= ri - 1e-12 for ci, ri in zip(c, r)) and any(ci > ri + 1e-12 for ci, ri in zip(c, r))
cands = []
for f in itertools.product(grid, repeat=3):
    a = [fi * ti for fi, ti in zip(f, tot)]
    b = [(1 - fi) * ti for fi, ti in zip(f, tot)]
    cands.append((a, b))
print("grid size", len(cands))
imp_eq = [c for c in cands if better((U(c[0]), U(c[1])), ref_eq)]
imp_en = [c for c in cands if better((U(c[0]), U(c[1])), ref_en)]
print("improvements at equilibrium", len(imp_eq), " at endowment", len(imp_en), " first at endowment", imp_en[0] if imp_en else None)
print("R2 witness (2,4,3)/(2,4,1): U1 change", U([2, 4, 3]) - U([3, 4, 1]), " U2 change", U([2, 4, 1]) - U([1, 4, 3]))
eps = 1e-6
d_u1 = (U([3 - eps, 4 + 4 * eps, 1]) - U([3.0, 4.0, 1.0])) / eps
d_u2 = (U([1 + eps, 4 - 4 * eps, 3]) - U([1.0, 4.0, 3.0])) / eps
print("R2 finite-difference derivatives: dU1 =", round(d_u1, 6), "(page 1/12 =", round(1 / 12, 6), ") dU2 =", round(d_u2, 6), "(page 1/4 =", 0.25, ")")
print("endowment MRS agent1 8/3 =", 8 / 3, " agent2 8 =", 8.0)
print("E3 hub: 0 on grid 5^3 =", len(cands))
