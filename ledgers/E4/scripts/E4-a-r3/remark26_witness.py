"""Verifier check (E4 slice a, round 3): Remark 2.6 says unweighted excess demands need not add to zero.

Example 2.11 economy: pi = (1/2, 1/4, 1/4), e^1 = (3, 4, 1), e^2 = (1, 4, 3), u_i = ln.
At a price q != q*, the log demands are x^i_s = pi_s w_i / q_s with w_i = q . e^i (Proposition 2.8).
Computes the unweighted sum of the excess demands and the weighted sum q . z at q = (2, 1, 1), exactly.
"""

from fractions import Fraction as F

pi = (F(1, 2), F(1, 4), F(1, 4))
e1 = (F(3), F(4), F(1))
e2 = (F(1), F(4), F(3))
ebar = tuple(a + b for a, b in zip(e1, e2, strict=True))
q = (F(2), F(1), F(1))
w1 = sum((a * b for a, b in zip(q, e1, strict=True)), F(0))
w2 = sum((a * b for a, b in zip(q, e2, strict=True)), F(0))
x1 = tuple(p * w1 / qq for p, qq in zip(pi, q, strict=True))
x2 = tuple(p * w2 / qq for p, qq in zip(pi, q, strict=True))
z = tuple(a + b - c for a, b, c in zip(x1, x2, ebar, strict=True))
print("w1, w2 =", w1, w2)
print("x1 =", tuple(str(v) for v in x1), " x2 =", tuple(str(v) for v in x2))
print("z(q) =", tuple(str(v) for v in z))
print("unweighted sum of z =", sum(z, F(0)))
print("weighted q . z =", sum((a * b for a, b in zip(q, z, strict=True)), F(0)))
