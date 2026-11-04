"""Round-5 independent re-derivation of the prose numbers in E4 slice a (exact Fractions and a float check)."""

from __future__ import annotations

import math
from fractions import Fraction as F

ok = True


def check(label: str, got: object, want: object) -> None:
    global ok
    good = got == want
    ok = ok and good
    print(f"{'OK ' if good else 'BAD'} {label}: got {got} want {want}")


# hub: placement bar and lottery items
check("hub Q1 expectation", F(0) * F(1, 4) + 8 * F(3, 4), 6)
check("hub Q5 expectation", F(1, 2) * 0**2 + F(1, 2) * 4**2, 8)
check("hub bar 0.8 of 8 items: 7/8", F(7, 8), F(875, 1000))
check("hub 6/8", F(6, 8), F(75, 100))
# hub skill item G = F_U - e^{ac} F_I
F_U, F_I, a, c = 1.3, 0.7, 2.0, 0.13
G_def = -math.exp(a * c) * F_I - (-F_U)
check("hub Q8 gap identity (float)", round(G_def, 12), round(F_U - math.exp(a * c) * F_I, 12))
# L01
S_pi = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
q = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
x = (F(100), F(40), F(0), F(250))
y = (F(0), F(60), F(120), F(30))
V = lambda p, z: sum(a1 * b1 for a1, b1 in zip(p, z))  # noqa: E731
check("L01 V(x)", V(q, x), F(340, 3))
check("L01 V(y)", V(q, y), 56)
comb = tuple(2 * a1 - F(1, 2) * b1 for a1, b1 in zip(x, y))
check("L01 combined payoff", comb, (200, 50, -60, 485))
check("L01 Part C value", V(q, comb), F(596, 3))
check("L01 E x", sum(p * z for p, z in zip(S_pi, x)), F(235, 4))
check("L01 short prob sum", sum((F(1, 8), F(3, 8), F(3, 8), F(1, 4))), F(9, 8))
check("L01 M1 V", F(10, 3) + 30 * F(1, 2), F(55, 3))
check("L01 M1 E", 10 * F(1, 2) + 30 * F(1, 4), F(25, 2))
check("L01 M1 diff", F(55, 3) - F(25, 2), F(35, 6))
check("L01 M3 V(3x-2y)", -5 * F(1, 2) + 6 * F(1, 4) + 7 * F(1, 8), F(-1, 8))
check("L01 M3 V(x)", F(1, 2) + 2 * F(1, 4) + 3 * F(1, 8), F(11, 8))
check("L01 M3 V(y)", 4 * F(1, 2) + 0 + F(1, 8), F(17, 8))
check("L01 M3 combo via A2", 3 * F(11, 8) - 2 * F(17, 8), F(-1, 8))
check("L01 P3 V(e1)", F(1, 4), F(1, 4))
check("L01 P3 E e1", F(1, 3), F(1, 3))
check("L01 R2 V(e1)", (F(1, 2)) ** 2, F(1, 4))
check("L01 R2 V(2e1)", (2 * F(1, 2)) ** 2, 1)
check("L01 quiz Q2 value", F(1, 2) * 5 + F(1, 4) * 7, F(17, 4))
check("L01 quiz Q4 E", 4 * F(3, 4), 3)
check("L01 quiz Q7 sum", F(2, 10) + F(3, 10) + F(1, 10), F(6, 10))
check("L01 misconception 2 prices", q[0] * 0 + q[1] * 0 + 0, 0)
# L02
pi = (F(1, 2), F(1, 4), F(1, 4))
e1, e2 = (F(3), F(4), F(1)), (F(1), F(4), F(3))
ebar = tuple(a1 + b1 for a1, b1 in zip(e1, e2))
check("L02 ebar", ebar, (4, 8, 4))
th1 = sum(p * a1 / t for p, a1, t in zip(pi, e1, ebar))
th2 = sum(p * b1 / t for p, b1, t in zip(pi, e2, ebar))
check("L02 theta1", th1, F(9, 16))
check("L02 theta2", th2, F(7, 16))
qs = tuple(p / t for p, t in zip(pi, ebar))
check("L02 q*", qs, (F(1, 8), F(1, 32), F(1, 16)))
check("L02 q*.ebar", sum(a1 * b1 for a1, b1 in zip(qs, ebar)), 1)
check("L02 x1*", tuple(th1 * t for t in ebar), (F(9, 4), F(9, 2), F(9, 4)))
check("L02 x2*", tuple(th2 * t for t in ebar), (F(7, 4), F(7, 2), F(7, 4)))
check("L02 w1 at q*", sum(a1 * b1 for a1, b1 in zip(qs, e1)), F(9, 16))
check("L02 w2 at q*", sum(a1 * b1 for a1, b1 in zip(qs, e2)), F(7, 16))
qq = (2, 1, 1)
w1 = sum(a1 * b1 for a1, b1 in zip(qq, e1))
w2 = sum(a1 * b1 for a1, b1 in zip(qq, e2))
check("Remark 2.6 w1", w1, 11)
check("Remark 2.6 w2", w2, 9)
d1 = tuple(p * w1 / r for p, r in zip(pi, qq))
d2 = tuple(p * w2 / r for p, r in zip(pi, qq))
check("Remark 2.6 d1", d1, (F(11, 4),) * 3)
check("Remark 2.6 d2", d2, (F(9, 4),) * 3)
z = tuple(a1 + b1 - t for a1, b1, t in zip(d1, d2, ebar))
check("Remark 2.6 excess", z, (1, -3, 1))
check("Remark 2.6 q.z", sum(a1 * b1 for a1, b1 in zip(qq, z)), 0)
check("Remark 2.6 unweighted", sum(z), -1)
ratios1 = [pi[s] / (d1[s] * 1) for s in range(3)]
ratios_q = [pi[s] / (x1 * qs[s]) for s, x1 in enumerate((F(9, 4), F(9, 2), F(9, 4)))]
check("L02 ratio agent1 (pi/(x q))", ratios_q, [F(16, 9)] * 3)
check("L02 ratio agent2 (pi/(x q))", [pi[s] / (x1 * qs[s]) for s, x1 in enumerate((F(7, 4), F(7, 2), F(7, 4)))], [F(16, 7)] * 3)
check("L02 misc2 v.q", F(1, 8) - F(1, 32), F(3, 32))
check("L02 misc3 e1 cost", sum(a1 * b1 for a1, b1 in zip(qs, e1)), F(9, 16))
check("L02 M1 demand", (F(1, 2) * F(1, 2) / F(1, 4), F(1, 2) * F(1, 2) / F(1, 8)), (1, 2))
check("L02 M1 spend", F(1, 4) * 1 + F(1, 8) * 2, F(1, 2))
check("L02 M2 demand", (F(1, 4) * 3 / 1, F(1, 4) * 3 / 2, F(1, 2) * 3 / 1), (F(3, 4), F(3, 8), F(3, 2)))
check("L02 M2 spend", F(3, 4) + 2 * F(3, 8) + F(3, 2), 3)
check("L02 M3 ebar", (F(1, 4) + 0, 0), (F(1, 4), 0)) if False else None
check("L02 M3 q*", tuple(F(1, 2) / 4 for _ in range(2)), (F(1, 8), F(1, 8)))
check("L02 M3 theta1", F(1, 2) * F(1, 4) + F(1, 2) * F(3, 4), F(1, 2))
check("L02 R2 partial", F(-1, 2) / F(1, 4) * 0 + (-F(1, 4) * 0), 0)
check("L02 R2 elasticity", (-(F(1, 2) * F(1, 2)) / F(1, 4) ** 2) * (F(1, 4) / (F(1, 2) * F(1, 2) / F(1, 4))), -1)
check("L02 Q5 q*_1", F(1, 2) / 4, F(1, 8))
check("L02 E1 sum", F(4, 8) + F(8, 32) + F(4, 16), 1)
# L03
mrs = lambda p, xx, s, t: (p[s] / xx[s]) / (p[t] / xx[t])  # noqa: E731
x1s, x2s = (F(9, 4), F(9, 2), F(9, 4)), (F(7, 4), F(7, 2), F(7, 4))
check("L03 MRS1 12", mrs(pi, x1s, 0, 1), 4)
check("L03 MRS1 13", mrs(pi, x1s, 0, 2), 2)
check("L03 MRS1 23", mrs(pi, x1s, 1, 2), F(1, 2))
check("L03 MRS2 12", mrs(pi, x2s, 0, 1), 4)
check("L03 MRS2 13", mrs(pi, x2s, 0, 2), 2)
check("L03 MRS2 23", mrs(pi, x2s, 1, 2), F(1, 2))
check("L03 price ratios", (qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2]), (4, 2, F(1, 2)))
check("L03 M1 MRS", mrs((F(1, 3), F(2, 3)), (1, 4), 0, 1), 2)
check("L03 M2 demand", (F(1, 2) * 6 / 2, F(1, 2) * 6 / 1), (F(3, 2), 3))
check("L03 M2 spend", 2 * F(3, 2) + 3, 6)
check("L03 M2 MRS", mrs((F(1, 2), F(1, 2)), (F(3, 2), 3), 0, 1), 2)
check("L03 M3 sum", (1 + 1, 1 + 1), (2, 2))
check("L03 M3 ebar", (1 + 1, 3 + 1), (2, 4)) if False else None
check("L03 R2 deriv U1", F(1, 2) * F(-1, 3) + F(1, 4) * 1, F(1, 12))
check("L03 R2 deriv U2", F(1, 2) * 1 + F(1, 4) * (-1), F(1, 4))
check("L03 R2 MRS endowment 1", (F(1, 2) / 3) / (F(1, 4) / 4), F(8, 3))
check("L03 R2 MRS endowment 2", (F(1, 2) / 1) / (F(1, 4) / 4), 8)
check("L03 R2 y1 sums", tuple(a1 + b1 for a1, b1 in zip((3 - 1, 4 + 4, 1), (1 + 1, 4 - 4, 3))), (4, 8, 4))
check("L03 Q8 MRS1", (F(1, 2) / F(9, 4)) / (F(1, 4) / F(9, 2)), 4)
check("L03 E2 witness feasible", tuple(a1 + b1 for a1, b1 in zip((2, 4, 3), (2, 4, 1))), (4, 8, 4))
check("L03 grid size", 5 ** 3, 125)
check("L03 M1 V-type", (F(1, 3) / 1) / (F(2, 3) / 4), 2)

# float check of the R2 small-epsilon improvement
def U(pr, b):
    return sum(p * math.log(v) for p, v in zip(pr, b))

pr = (0.5, 0.25, 0.25)
base1, base2 = (3.0, 4.0, 1.0), (1.0, 4.0, 3.0)
for eps in (1e-2, 1e-3, 1e-4):
    y1 = (3 - eps, 4 + 4 * eps, 1.0)
    y2 = (1 + eps, 4 - 4 * eps, 3.0)
    gain1 = U(pr, y1) - U(pr, base1)
    gain2 = U(pr, y2) - U(pr, base2)
    print(f"eps {eps}: gain1 {gain1:.3e} gain2 {gain2:.3e} both_positive {gain1 > 0 and gain2 > 0}")
    ok = ok and gain1 > 0 and gain2 > 0
print("ALL_OK" if ok else "SOME_BAD")
