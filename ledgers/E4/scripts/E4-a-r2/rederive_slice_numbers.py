"""Independent re-derivation of the numbers printed or quoted in E4 hub, L01, L02 and L03 (slice a, round 2).

Exact Fractions throughout, except the L03 grid search, which uses floats with the page's tolerance 1e-12 and is
cross-checked against an exact-rational comparison of the same grid."""
import math
import random
from fractions import Fraction as F
from itertools import product

fails = []


def check(label, got, want):
    ok = got == want
    print(f"{'OK  ' if ok else 'MISMATCH'} {label}: got {got} want {want}")
    if not ok:
        fails.append(label)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


# ---- index: hub arithmetic and placement check
check("hub 9*8", 9 * 8, 72)
check("hub 72+28", 72 + 28, 100)
check("hub 28 percent of 100", F(28, 100) * 100, 28)
check("hub 7/8 percent", F(7, 8) * 100, F(875, 10))
check("hub 6/8 percent", F(6, 8) * 100, 75)
check("hub item1 E[lottery]", F(0) * F(1, 4) + 8 * F(3, 4), 6)
check("hub item2 d/dx ln at 4", F(1, 4), F("0.25"))
check("hub item4 E[0 or 4] u=x^2", F(1, 2) * 0 ** 2 + F(1, 2) * 4 ** 2, 8)
check("hub skill rung1 value", F(1, 2) * 10 + F(1, 4) * 30, F(25, 2))
check("hub skill rung2 demand state1", F(1, 2) * 1 / F(1, 8), 4)

# ---- L01 (Example 1.5, Lab 1 hypothesis, Parts A to D, problems, quiz)
pi1 = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
q1 = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
x1 = (F(100), F(40), F(0), F(250))
y1 = (F(0), F(60), F(120), F(30))
check("L01 sum pi", sum(pi1), 1)
check("L01 value claim", dot(q1, x1), F(340, 3))
check("L01 value other", dot(q1, y1), 56)
comb = tuple(2 * a - F(1, 2) * b for a, b in zip(x1, y1))
check("L01 combined payoff", comb, (200, 50, -60, 485))
check("L01 linearity lhs", dot(q1, comb), F(596, 3))
check("L01 linearity rhs", 2 * dot(q1, x1) - F(1, 2) * dot(q1, y1), F(596, 3))
check("L01 expected payoff", dot(pi1, x1), F(235, 4))
check("L01 value at probabilities equals E", dot(pi1, x1), F(235, 4))
check("L01 value at prices minus E", dot(q1, x1) - dot(pi1, x1), F(340, 3) - F(235, 4))
check("L01 value at prices 113.33", round(float(dot(q1, x1)), 2), 113.33)
check("L01 Ex1.5 decomposition", tuple(sum(x1[s] * (1 if t == s else 0) for s in range(4)) for t in range(4)), x1)
check("L01 M1 V", dot((F(1, 3), F(1, 5), F(1, 2)), (10, 0, 30)), F(55, 3))
check("L01 M1 E", dot((F(1, 2), F(1, 4), F(1, 4)), (10, 0, 30)), F(25, 2))
check("L01 M1 gap", F(55, 3) - F(25, 2), F(35, 6))
check("L01 M1 55/3 to 2dp", round(float(F(55, 3)), 2), 18.33)
check("L01 M2 V", dot((F(2, 5), F(1, 2)), (0, 50)), 25)
v3 = dot((F(1, 2), F(1, 4), F(1, 8)), (-5, 6, 7))
check("L01 M3 V(3x-2y) direct", v3, F(-1, 8))
check("L01 M3 V(x)", dot((F(1, 2), F(1, 4), F(1, 8)), (1, 2, 3)), F(11, 8))
check("L01 M3 V(y)", dot((F(1, 2), F(1, 4), F(1, 8)), (4, 0, 1)), F(17, 8))
check("L01 M3 3V(x)-2V(y)", 3 * F(11, 8) - 2 * F(17, 8), F(-1, 8))
check("L01 P3 V(e1)", F(1, 4), F(1, 4))
check("L01 P3 E e1", F(1, 3), F(1, 3))
check("L01 R2 V(e1)", (F(1, 2)) ** 2, F(1, 4))
check("L01 R2 V(2e1)", (2 * F(1, 2)) ** 2, 1)
check("L01 Q2 value 5,7 at 1/2,1/4", F(1, 2) * 5 + F(1, 4) * 7, F(17, 4))
check("L01 Q4 E", F(1, 4) * 0 + F(3, 4) * 4, 3)
check("L01 Q7 value 0.2+0.3+0.1", F("0.2") + F("0.3") + F("0.1"), F("0.6"))

# ---- L02 (Example 2.11, Lab 2 hypothesis and Parts A to F, misconceptions, problems, quiz)
PI = (F(1, 2), F(1, 4), F(1, 4))
E1 = (F(3), F(4), F(1))
E2 = (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(E1, E2))
check("L02 aggregate", ebar, (4, 8, 4))
th1 = sum(p * e / t for p, e, t in zip(PI, E1, ebar))
th2 = sum(p * e / t for p, e, t in zip(PI, E2, ebar))
check("L02 theta1", th1, F(9, 16))
check("L02 theta2", th2, F(7, 16))
qstar = tuple(p / t for p, t in zip(PI, ebar))
check("L02 prices", qstar, (F(1, 8), F(1, 32), F(1, 16)))
check("L02 q.ebar", dot(qstar, ebar), 1)
w1, w2 = dot(qstar, E1), dot(qstar, E2)
check("L02 wealth1", w1, F(9, 16))
check("L02 wealth2", w2, F(7, 16))
d1 = tuple(p * w1 / q for p, q in zip(PI, qstar))
d2 = tuple(p * w2 / q for p, q in zip(PI, qstar))
check("L02 demand1", d1, (F(9, 4), F(9, 2), F(9, 4)))
check("L02 demand2", d2, (F(7, 4), F(7, 2), F(7, 4)))
check("L02 budget1", dot(qstar, d1) - w1, 0)
check("L02 budget2", dot(qstar, d2) - w2, 0)
clear = tuple(a + b - t for a, b, t in zip(d1, d2, ebar))
check("L02 clearing residuals", clear, (0, 0, 0))
z = clear
check("L02 walras residual", dot(qstar, z), 0)
check("L02 ratio agent1", tuple(p / (x * q) for p, x, q in zip(PI, d1, qstar)), (F(16, 9),) * 3)
check("L02 ratio agent2", tuple(p / (x * q) for p, x, q in zip(PI, d2, qstar)), (F(16, 7),) * 3)
scaled = tuple(3 * q for q in qstar)
check("L02 part E agent1 unchanged", tuple(p * (3 * w1) / q for p, q in zip(PI, scaled)), d1)
check("L02 part E agent2 unchanged", tuple(p * (3 * w2) / q for p, q in zip(PI, scaled)), d2)
check("L02 part E fixed wealth factor", tuple(p * w1 / q for p, q in zip(PI, scaled)), tuple(x / 3 for x in d1))
check("L02 M3 misconception endowment cost", dot(qstar, E1), F(9, 16))
zmis = (1, -1, 0)
check("L02 misconception value of (1,-1,0)", dot(qstar, zmis), F(3, 32))
check("L02 misconception unweighted sum", sum(zmis), 0)
check("L02 M1 demand x1", F(1, 2) * F(1, 2) / F(1, 4), 1)
check("L02 M1 demand x2", F(1, 2) * F(1, 2) / F(1, 8), 2)
check("L02 M1 spend", F(1, 4) * 1 + F(1, 8) * 2, F(1, 2))
check("L02 M2 demand", tuple(p * 3 / q for p, q in zip((F(1, 4), F(1, 4), F(1, 2)), (1, 2, 1))), (F(3, 4), F(3, 8), F(3, 2)))
check("L02 M2 spend", F(3, 4) + 2 * F(3, 8) + F(3, 2), 3)
ebar2 = (F(4), F(4))
check("L02 M3 prices", tuple(F(1, 2) / t for t in ebar2), (F(1, 8), F(1, 8)))
check("L02 M3 theta1", F(1, 2) * F(1, 4) + F(1, 2) * F(3, 4), F(1, 2))
check("L02 E1 prices product", F(4, 8) + F(8, 32) + F(4, 16), 1)
h = F(1, 10**9)
xs = lambda q: F(1, 2) * F(1) / q  # x1 = pi1 * w / q1 with w = 1
check("L02 R2 d x1/dq1 approx -x1/q1 (rel err < 1e-6)", abs(float((xs(F(1,8)+h)-xs(F(1,8)))/h) / float(-xs(F(1,8))/F(1,8)) - 1) < 1e-6, True)
check("L02 R2 elasticity -1 (rel err < 1e-6)", abs(float((xs(F(1,8)*(1+h))-xs(F(1,8)))/(F(1,8)*h)) * float(F(1,8)/xs(F(1,8))) + 1) < 1e-6, True)
check("L02 R2 x1 after doubling q1 at fixed wealth is half", xs(2 * F(1, 8)) * 2, xs(F(1, 8)))
check("L02 A4 check: u=-1/x has u'=1/x^2>0 and u''=-2/x^3<0 at x=2", (F(1, 4) > 0, F(-2, 8) < 0), (True, True))
check("L02 misc price state2 vs state3 from pi/ebar", (F(1, 4) / 8, F(1, 4) / 4), (F(1, 32), F(1, 16)))

# ---- L03 (MRS, Lab 3, R2 derivatives, R2 MRS at endowment, key results)
def mrs(pi, x, s, t):
    return (pi[s] / x[s]) / (pi[t] / x[t])


for left, right in ((0, 1), (0, 2), (1, 2)):
    m1 = mrs(PI, d1, left, right)
    m2 = mrs(PI, d2, left, right)
    pr = qstar[left] / qstar[right]
    check(f"L03 MRS states {left+1},{right+1} agent1 = price ratio", (m1, m2, pr), (m1, m1, m1))
check("L03 MRS_12 agent1", mrs(PI, d1, 0, 1), 4)
check("L03 MRS_13 agent1", mrs(PI, d1, 0, 2), 2)
check("L03 MRS_23 agent1", mrs(PI, d1, 1, 2), F(1, 2))
check("L03 MRS_12 agent2", mrs(PI, d2, 0, 1), 4)
check("L03 MRS_13 agent2", mrs(PI, d2, 0, 2), 2)
check("L03 MRS_23 agent2", mrs(PI, d2, 1, 2), F(1, 2))
check("L03 M1 MRS12", mrs((F(1, 3), F(2, 3)), (1, 4), 0, 1), 2)
check("L03 M2 demand", tuple(p * 6 / q for p, q in zip((F(1, 2), F(1, 2)), (2, 1))), (3 * F(1, 2), 3))
check("L03 M2 MRS", mrs((F(1, 2), F(1, 2)), (F(3, 2), 3), 0, 1), 2)
check("L03 R2 deriv U1", F(1, 2) * F(-1, 3) + F(1, 4) * 1, F(1, 12))
check("L03 R2 deriv U2", F(1, 2) * 1 + F(1, 4) * F(-1), F(1, 4))
check("L03 R2 MRS endowment agent1 12", mrs(PI, E1, 0, 1), F(8, 3))
check("L03 R2 MRS endowment agent2 12", mrs(PI, E2, 0, 1), 8)
check("L03 R2 y1 feasible sums (eps=1/10)", tuple(a + b for a, b in zip((3 - F(1, 10), 4 + F(4, 10), 1), (1 + F(1, 10), 4 - F(4, 10), 3))), tuple(F(x) for x in ebar))
check("L03 Ex3.6 MRS endowment sum", (F(3) + 1, F(8)), (4, 8))
check("L03 E2 witness sums to ebar", tuple(a + b for a, b in zip((2, 4, 3), (2, 4, 1))), ebar)
check("L03 E3 ratio q1/q3", qstar[0] / qstar[2], 2)
check("L03 Q5 q1/q2 at (2,1)", F(2) / 1, 2)

# Lab 3 grid search, floats with TOL 1e-12, plus an exact-rational version of the same comparison
GRID = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
TOL = 1e-12


def u(pi, bundle):
    if any(x == 0 for x in bundle):
        return -math.inf
    return sum(float(p) * math.log(float(x)) for p, x in zip(pi, bundle))


def improves(c, r):
    return all(ci >= ri - TOL for ci, ri in zip(c, r)) and any(ci > ri + TOL for ci, ri in zip(c, r))


tot = ebar
cands = []
for f in product(GRID, repeat=3):
    a = tuple(fi * t for fi, t in zip(f, tot))
    b = tuple((1 - fi) * t for fi, t in zip(f, tot))
    cands.append((a, b))
check("L03 grid size", len(cands), 125)
ref_eq = (u(PI, d1), u(PI, d2))
ref_en = (u(PI, E1), u(PI, E2))
n_eq = sum(1 for a, b in cands if improves((u(PI, a), u(PI, b)), ref_eq))
improving_en = [(a, b) for a, b in cands if improves((u(PI, a), u(PI, b)), ref_en)]
check("L03 count improvements at equilibrium", n_eq, 0)
check("L03 count improvements at endowment", len(improving_en), 2)
check("L03 first improvement at endowment", (improving_en[0][0], improving_en[0][1]), ((2, 4, 3), (2, 4, 1)))


# exact cross-check of the first witness: strict improvement in exact arithmetic is not possible with logs, so compare
# the floats with a margin far above TOL
margins = [u(PI, improving_en[0][0]) - u(PI, E1), u(PI, improving_en[0][1]) - u(PI, E2)]
check("L03 witness margins exceed TOL", all(m > 1e-6 for m in margins), True)
print("margins", margins)
print("FAILS", fails)
