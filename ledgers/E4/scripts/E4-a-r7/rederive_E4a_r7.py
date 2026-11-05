"""Verifier re-derivation (E4 slice a, round 7) of every number in the hub, L01, L02 and L03 prose.

Independent of the lab code: exact Fractions, and a separate float grid search with a different comparison rule.
"""

from __future__ import annotations

import math
from fractions import Fraction as F
from itertools import product

checks: list[tuple[str, bool]] = []


def chk(name: str, ok: bool) -> None:
    checks.append((name, ok))
    print(("OK   " if ok else "FAIL ") + name)


# ---- L01
pi4 = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
x4 = (F(100), F(40), F(0), F(250))
q4 = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
o4 = (F(0), F(60), F(120), F(30))
chk("L01 pi sums to 1", sum(pi4) == 1)
V = sum(q * x for q, x in zip(q4, x4))
chk("L01 V(claim)=340/3", V == F(340, 3))
chk("L01 340/3 rounds to 113.33", f"{float(V):.2f}" == "113.33")
chk("L01 V(other)=56", sum(q * x for q, x in zip(q4, o4)) == 56)
comb = tuple(2 * a - F(1, 2) * b for a, b in zip(x4, o4))
chk("L01 combo payoff (200,50,-60,485)", comb == (200, 50, -60, 485))
chk("L01 V(combo)=596/3", sum(q * x for q, x in zip(q4, comb)) == F(596, 3))
E = sum(p * x for p, x in zip(pi4, x4))
chk("L01 E(claim)=235/4", E == F(235, 4))
chk("L01 58.75", float(E) == 58.75)
chk("L01 prices differ from probabilities in every state", all(a != b for a, b in zip(q4, pi4)))
chk("L01 negative-entry probs (1/2,1/2,1/2,-1/2) sum to 1 but have negative entry",
    sum((F(1, 2), F(1, 2), F(1, 2), F(-1, 2))) == 1 and F(-1, 2) < 0)
chk("L01 short probs (1/8,3/8,3/8,1/4) sum to 9/8", sum((F(1, 8), F(3, 8), F(3, 8), F(1, 4))) == F(9, 8))
# M1
q3 = (F(1, 3), F(1, 5), F(1, 2))
p3 = (F(1, 2), F(1, 4), F(1, 4))
x3 = (F(10), F(0), F(30))
V3 = sum(a * b for a, b in zip(q3, x3))
E3v = sum(a * b for a, b in zip(p3, x3))
chk("L01 M1 V=55/3", V3 == F(55, 3))
chk("L01 M1 E=12.5", E3v == F(25, 2))
chk("L01 M1 gap 35/6", V3 - E3v == F(35, 6))
chk("L01 M1 55/3 to 2dp = 18.33", f"{float(V3):.2f}" == "18.33")
# M2
chk("L01 M2 V=25", F(0) * F(2, 5) + F(1, 2) * 50 == 25)
# M3
q3b = (F(1, 2), F(1, 4), F(1, 8))
xa, yb = (F(1), F(2), F(3)), (F(4), F(0), F(1))
comb3 = tuple(3 * a - 2 * b for a, b in zip(xa, yb))
chk("L01 M3 3x-2y=(-5,6,7)", comb3 == (-5, 6, 7))
chk("L01 M3 V(3x-2y)=-1/8", sum(p * c for p, c in zip(q3b, comb3)) == F(-1, 8))
chk("L01 M3 V(x)=11/8", sum(p * c for p, c in zip(q3b, xa)) == F(11, 8))
chk("L01 M3 V(y)=17/8", sum(p * c for p, c in zip(q3b, yb)) == F(17, 8))
# R2 size effect
chk("L01 R2 V(e1)=1/4, V(2e1)=1", (F(1, 2) * 1) ** 2 == F(1, 4) and (F(1, 2) * 2) ** 2 == 1)
# quiz
chk("L01 quiz 4.25", F(1, 2) * 5 + F(1, 4) * 7 == F(17, 4))
chk("L01 quiz E=3", F(4) * F(3, 4) == 3)
chk("L01 quiz value of (0.2,0.3,0.1) = 0.6", abs(0.2 + 0.3 + 0.1 - 0.6) < 5e-4)

# ---- L02 Example 2.11
pi = (F(1, 2), F(1, 4), F(1, 4))
e1 = (F(3), F(4), F(1))
e2 = (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(e1, e2))
chk("L02 aggregate (4,8,4)", ebar == (4, 8, 4))
th1 = sum(p * a / b for p, a, b in zip(pi, e1, ebar))
th2 = sum(p * a / b for p, a, b in zip(pi, e2, ebar))
chk("L02 theta1=9/16", th1 == F(9, 16))
chk("L02 theta2=7/16", th2 == F(7, 16))
qs = tuple(p / b for p, b in zip(pi, ebar))
chk("L02 q*=(1/8,1/32,1/16)", qs == (F(1, 8), F(1, 32), F(1, 16)))
chk("L02 q*.ebar=1", sum(a * b for a, b in zip(qs, ebar)) == 1)
x1 = tuple(th1 * b for b in ebar)
x2 = tuple(th2 * b for b in ebar)
chk("L02 x1*=(9/4,9/2,9/4)", x1 == (F(9, 4), F(9, 2), F(9, 4)))
chk("L02 x2*=(7/4,7/2,7/4)", x2 == (F(7, 4), F(7, 2), F(7, 4)))
chk("L02 budget w1=q.e1=9/16", sum(a * b for a, b in zip(qs, e1)) == th1)
chk("L02 demand formula x=pi w/q", tuple(p * th1 / q for p, q in zip(pi, qs)) == x1)
chk("L02 market clearing", all(a + b == c for a, b, c in zip(x1, x2, ebar)))
chk("L02 ratio pi/(x q)=16/9 agent1", all(p / (x * q) == F(16, 9) for p, x, q in zip(pi, x1, qs)))
chk("L02 ratio pi/(x q)=16/7 agent2", all(p / (x * q) == F(16, 7) for p, x, q in zip(pi, x2, qs)))
chk("L02 1/w1=16/9", 1 / th1 == F(16, 9))
chk("L02 1/w2=16/7", 1 / th2 == F(16, 7))
# Remark 2.6 at q=(2,1,1)
qr = (F(2), F(1), F(1))
w1r = sum(a * b for a, b in zip(qr, e1))
w2r = sum(a * b for a, b in zip(qr, e2))
d1 = tuple(p * w1r / q for p, q in zip(pi, qr))
d2 = tuple(p * w2r / q for p, q in zip(pi, qr))
zr = tuple(a + b - c for a, b, c in zip(d1, d2, ebar))
chk("L02 Remark2.6 wealths 11, 9", (w1r, w2r) == (11, 9))
chk("L02 Remark2.6 demands 11/4, 9/4", d1 == (F(11, 4),) * 3 and d2 == (F(9, 4),) * 3)
chk("L02 Remark2.6 excess (1,-3,1)", zr == (1, -3, 1))
chk("L02 Remark2.6 unweighted sum -1, q.z=0", sum(zr) == -1 and sum(a * b for a, b in zip(qr, zr)) == 0)
# Misconception 2: v=(1,-1,0)
v = (F(1), F(-1), F(0))
chk("L02 misc2 q*.v = 3/32", sum(a * b for a, b in zip(qs, v)) == F(3, 32))
# Misconception 3: e1 costs 9/16
chk("L02 misc3 q*.e1 = 9/16", sum(a * b for a, b in zip(qs, e1)) == F(9, 16))
# Remark 2.10 scale invariance
psi = F(3)
chk("L02 scale invariance", tuple(p * (psi * 1) / (psi * q) for p, q in zip(pi, qs)) == tuple(
    p * 1 / q for p, q in zip(pi, qs)))
# M1-M3 problems
chk("L02 M1 x=(1,2), spend 1/2", (F(1, 4) * 1 + F(1, 8) * 2) == F(1, 2))
chk("L02 M2 x=(3/4,3/8,3/2), spend 3", F(3, 4) + 2 * F(3, 8) + F(3, 2) == 3)
m3e1=(F(1,1),F(3,1)); m3e2=(F(3,1),F(1,1)); m3ebar=(F(4,1),F(4,1)); m3pi=(F(1,2),F(1,2)); m3q=tuple(p/t for p,t in zip(m3pi,m3ebar)); m3th1=sum(p*a/t for p,a,t in zip(m3pi,m3e1,m3ebar)); m3x1=tuple(m3th1*t for t in m3ebar); m3x2=tuple((1-m3th1)*t for t in m3ebar)
chk("L02 M3 q*=(1/8,1/8), theta1=1/2, x1=(2,2), x2=(2,2), clears", m3q==(F(1,8),F(1,8)) and m3th1==F(1,2) and m3x1==(2,2) and m3x2==(2,2) and all(a+b==c for a,b,c in zip(m3x1,m3x2,m3ebar)))
chk("L02 E1 sum 1", F(4, 8) + F(8, 32) + F(4, 16) == 1)
chk("L02 quiz 0.125 and 0.0625", F(1, 8) == 0.125 and F(1, 16) == 0.0625)
chk("L02 quiz demand state 2 = 2", F(1, 2) * F(1, 2) / F(1, 8) == 2)

# ---- L03
chk("L03 MRS agent1 12 = 4", (F(1, 2) / x1[0]) / (F(1, 4) / x1[1]) == 4)
chk("L03 MRS agent1 13 = 2", (F(1, 2) / x1[0]) / (F(1, 4) / x1[2]) == 2)
chk("L03 MRS agent1 23 = 1/2", (F(1, 4) / x1[1]) / (F(1, 4) / x1[2]) == F(1, 2))
chk("L03 MRS agent2 12 = 4", (F(1, 2) / x2[0]) / (F(1, 4) / x2[1]) == 4)
chk("L03 MRS agent2 13 = 2", (F(1, 2) / x2[0]) / (F(1, 4) / x2[2]) == 2)
chk("L03 MRS agent2 23 = 1/2", (F(1, 4) / x2[1]) / (F(1, 4) / x2[2]) == F(1, 2))
chk("L03 price ratios 4, 2, 1/2", (qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2]) == (4, 2, F(1, 2)))
# endowment MRS 8/3 (agent 1) and 8 (agent 2)
m1 = (pi[0] / e1[0]) / (pi[1] / e1[1])
m2 = (pi[0] / e2[0]) / (pi[1] / e2[1])
chk("L03 endowment MRS agent1 12 = 8/3", m1 == F(8, 3))
chk("L03 endowment MRS agent2 12 = 8", m2 == 8)
# R2 derivative of U1 and U2 along the trade
d_u1 = F(1, 2) * (-F(1, 3)) + F(1, 4) * F(4, 4)
d_u2 = F(1, 2) * F(1) + F(1, 4) * (-F(4, 4))
chk("L03 R2 derivative U1 = 1/12", d_u1 == F(1, 12))
chk("L03 R2 derivative U2 = 1/4", d_u2 == F(1, 4))
# the sentence in the R2 solution: agent 1 needs 8/3 units of state 2 per unit of state 1 given up; trade gives 4
chk("L03 R2 compensation needed by agent 1 is 8/3 (not 3/8); trade gives 4 > 8/3", F(8, 3) < 4 and F(3, 8) != F(8, 3))
# R2 witness utilities
import math as _m  # noqa: E402

def util(bundle: tuple[float, float, float]) -> float:
    return sum(float(p) * _m.log(x) for p, x in zip(pi, bundle))

y1 = (3 - 0.1, 4 + 0.4, 1.0)
y2 = (1 + 0.1, 4 - 0.4, 3.0)
chk("L03 R2 witness improves both (eps 0.1)", util(y1) > util(tuple(map(float, e1))) and util(y2) > util(tuple(map(float, e2))))
# E3 grid claims and first improvement (independent float implementation)
GRID = (0.0, 0.25, 0.5, 0.75, 1.0)
tot = (4.0, 8.0, 4.0)
E1f = (3.0, 4.0, 1.0)
E2f = (1.0, 4.0, 3.0)
pif = (0.5, 0.25, 0.25)


def u(b: tuple[float, float, float]) -> float:
    s = 0.0
    for p, x in zip(pif, b):
        if x <= 0:
            return -math.inf
        s += p * math.log(x)
    return s


x1f = (9 / 4, 9 / 2, 9 / 4)
x2f = (7 / 4, 7 / 2, 7 / 4)
ref_eq = (u(x1f), u(x2f))
ref_en = (u(E1f), u(E2f))
cands = []
for f in product(GRID, repeat=3):
    a = tuple(fi * ti for fi, ti in zip(f, tot))
    b = tuple((1 - fi) * ti for fi, ti in zip(f, tot))
    cands.append((a, b))
chk("L03 grid has 125 allocations", len(cands) == 125)


def better(c: tuple[float, float], r: tuple[float, float], tol: float) -> bool:
    return all(ci >= ri - tol for ci, ri in zip(c, r)) and any(ci > ri + tol for ci, ri in zip(c, r))


imp_eq = sum(1 for a, b in cands if better((u(a), u(b)), ref_eq, 1e-9))
imp_en = [(a, b) for a, b in cands if better((u(a), u(b)), ref_en, 1e-9)]
chk(f"L03 grid improvements at equilibrium = 0 (got {imp_eq})", imp_eq == 0)
chk(f"L03 grid improvements at endowment = 2 (got {len(imp_en)})", len(imp_en) == 2)
chk("L03 first improvement at endowment is agent1 (2,4,3)", tuple(round(z, 9) for z in imp_en[0][0]) == (2.0, 4.0, 3.0))
chk("L03 equilibrium fraction 9/16 is not a grid value", all(abs(9 / 16 - g) > 1e-12 for g in GRID))

# ---- hub
chk("hub 9 x 8 = 72", 9 * 8 == 72)
chk("hub 72 + 28 = 100", 72 + 28 == 100)
chk("hub 72% and 28% of 100", 72 / 100 == 0.72 and 28 / 100 == 0.28)
chk("hub 6 of 8 = 75%", 6 / 8 == 0.75)
chk("hub 7 of 8 = 87.5%", 7 / 8 == 0.875)
chk("hub 80% of 8 = 6.4, so 7 needed", 0.8 * 8 == 6.4)
chk("hub numeric 0*1/4+8*3/4=6", F(0) * F(1, 4) + 8 * F(3, 4) == 6)
chk("hub numeric (1/2)0^2+(1/2)4^2=8", F(1, 2) * 0 + F(1, 2) * 16 == 8)
chk("hub skill G: -e^{ac}F_I - (-F_U) = F_U - e^{ac}F_I (symbolic identity, checked at a=2,c=0.13,F_U=1.3,F_I=0.4)", abs((-math.exp(2*0.13)*0.4 - (-1.3)) - (1.3 - math.exp(2*0.13)*0.4)) < 1e-12)
# KKT at x* (L02 line 164): stationarity pi_s/x_s = mu q_s with mu = 1/w, complementary slackness, nonnegativity slack
mu1 = 1 / th1
chk("L02 KKT stationarity pi_s/x*_s = (1/w1) q_s", all(p / x == mu1 * q for p, x, q in zip(pi, x1, qs)))
chk("L02 KKT complementary slackness: budget binds (q.x1* - w1 = 0)", sum(a * b for a, b in zip(qs, x1)) == th1)
chk("L02 KKT nonnegativity slack: x1*_s > 0 all s", all(x > 0 for x in x1))
n_fail = sum(1 for _, ok in checks if not ok)
print(f"TOTAL {len(checks)} checks, FAIL {n_fail}")
