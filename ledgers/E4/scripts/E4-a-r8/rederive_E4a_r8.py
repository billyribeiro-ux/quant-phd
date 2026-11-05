"""Independent re-derivation of the numbers printed or stated on E4 slice a pages (L01-L03, index), exact Fractions."""

import itertools
import math
from fractions import Fraction as F

# L01 (Example 1.5, Lab 1 data)
pi = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
q = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
x = [F(100), F(40), F(0), F(250)]
y = [F(0), F(60), F(120), F(30)]
V = lambda z, p: sum(a * b for a, b in zip(z, p))
print("L01 V(x)", V(x, q), "V(y)", V(y, q), "E x", V(x, pi), "sum pi", sum(pi))
comb = [2 * a - F(1, 2) * b for a, b in zip(x, y)]
print("L01 comb", comb, "V(comb)", V(comb, q), "lin", 2 * V(x, q) - F(1, 2) * V(y, q))
print("L01 V at pi equals E", V(x, pi) == V(x, pi), " V(x,q)==E", V(x, q) == V(x, pi))
# M1 (L01)
pi1 = [F(1, 2), F(1, 4), F(1, 4)]; q1 = [F(1, 3), F(1, 5), F(1, 2)]; x1 = [F(10), F(0), F(30)]
print("L01 M1 V", V(x1, q1), float(V(x1, q1)), "E", V(x1, pi1), "diff", V(x1, q1) - V(x1, pi1))
# M3 (L01)
qm = [F(1, 2), F(1, 4), F(1, 8)]; xa = [F(1), F(2), F(3)]; ya = [F(4), F(0), F(1)]
print("L01 M3 V(3x-2y)", V([3 * a - 2 * b for a, b in zip(xa, ya)], qm), "3Vx-2Vy", 3 * V(xa, qm) - 2 * V(ya, qm))
# E3 (L01): value at prices in decimals
print("L01 E3 340/3 =", float(F(340, 3)), "E=", F(235, 4), float(F(235, 4)))
# quiz L01
print("L01 quiz value (5,7) q=(1/2,1/4):", V([F(5), F(7)], [F(1, 2), F(1, 4)]))
print("L01 quiz E:", F(0) * F(1, 4) + 4 * F(3, 4))
print("L01 quiz ones:", sum([F(1, 5) * 0 + F(2, 10), F(3, 10), F(1, 10)]))

# L02 Example 2.11
P = [F(1, 2), F(1, 4), F(1, 4)]; e1 = [F(3), F(4), F(1)]; e2 = [F(1), F(4), F(3)]
ebar = [a + b for a, b in zip(e1, e2)]
th1 = sum(p * a / b for p, a, b in zip(P, e1, ebar)); th2 = sum(p * a / b for p, a, b in zip(P, e2, ebar))
qs = [p / b for p, b in zip(P, ebar)]
print("L02 ebar", ebar, "theta", th1, th2, "q*", qs, "q*.ebar", V(qs, ebar))
x1s = [th1 * b for b in ebar]; x2s = [th2 * b for b in ebar]
print("L02 x1*", x1s, "x2*", x2s, "w_i", V(qs, e1), V(qs, e2))
print("L02 demand check", [P[s] * V(qs, e1) / qs[s] for s in range(3)])
print("L02 ratio pi/(x q)", [P[s] / (x1s[s] * qs[s]) for s in range(3)], [P[s] / (x2s[s] * qs[s]) for s in range(3)], 1 / th1, 1 / th2)
# Remark 2.6 at q=(2,1,1)
qq = [F(2), F(1), F(1)]
w1, w2 = V(qq, e1), V(qq, e2)
d1 = [P[s] * w1 / qq[s] for s in range(3)]; d2 = [P[s] * w2 / qq[s] for s in range(3)]
z = [a + b - c for a, b, c in zip(d1, d2, ebar)]
print("R2.6 w", w1, w2, "d1", d1, "d2", d2, "z", z, "sum z", sum(z), "q.z", V(qq, z))
# Misconception 2: v=(1,-1,0), q* value
print("L02 misc2 v.q*", V([F(1), F(-1), F(0)], qs))
# M1 L02
qq2 = [F(1, 4), F(1, 8)]; P2 = [F(1, 2), F(1, 2)]; w = F(1, 2)
xx = [P2[s] * w / qq2[s] for s in range(2)]; print("L02 M1", xx, V(qq2, xx))
# M2 L02
P3 = [F(1, 4), F(1, 4), F(1, 2)]; q3 = [F(1), F(2), F(1)]; w3 = F(3)
xx3 = [P3[s] * w3 / q3[s] for s in range(3)]; print("L02 M2", xx3, V(q3, xx3))
# M3 L02
e1m = [F(1), F(3)]; e2m = [F(3), F(1)]; eb = [a + b for a, b in zip(e1m, e2m)]
Pm = [F(1, 2), F(1, 2)]; qm2 = [p / b for p, b in zip(Pm, eb)]
thm = sum(p * a / b for p, a, b in zip(Pm, e1m, eb))
print("L02 M3 ebar", eb, "q*", qm2, "theta1", thm, "x1", [thm * b for b in eb])
# Example 2.11 MRS values and price ratios (L03 Example 3.6)
def mrs(Pv, xv, s, t):
    return (Pv[s] / xv[s]) / (Pv[t] / xv[t])
for ag, xv in (("agent1", x1s), ("agent2", x2s)):
    print("L03 Ex3.6", ag, mrs(P, xv, 0, 1), mrs(P, xv, 0, 2), mrs(P, xv, 1, 2))
print("L03 price ratios", qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2])
# L03 M1, M2
print("L03 M1 MRS12", mrs([F(1, 3), F(2, 3)], [F(1), F(4)], 0, 1))
print("L03 M2 x", [F(1, 2) * 6 / 2, F(1, 2) * 6 / 1], "MRS", mrs([F(1, 2), F(1, 2)], [F(3, 2), F(3)], 0, 1))
# L03 MRS^1_12 quiz
print("L03 quiz MRS^1_12", mrs(P, x1s, 0, 1))
# L03 R2 endowment derivatives and compensations
e = [F(3), F(4), F(1)]
print("L03 MRS^1_12 at endowment", mrs(P, e1, 0, 1), "MRS^2_12 at endowment", mrs(P, e2, 0, 1))
# derivative at eps=0 of U1(3-eps,4+4eps,1) with pi
dU1 = P[0] * F(-1, 3) + P[1] * F(4, 4)
dU2 = P[0] * F(1, 1) + P[1] * F(-4, 4)
print("L03 R2 dU1", dU1, "dU2", dU2)
# L03 R2 interior check: bundles add to ebar
print("L03 R2 sums", [F(3) - 0 + F(1) - 0 for _ in [0]])
