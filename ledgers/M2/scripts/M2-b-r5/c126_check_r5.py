"""Round-5 check of card M2-c126 (L09 Lab 1 part B): partition points (i/10)^2 for f(x) = x^2 on [0, 1]."""
from fractions import Fraction as F
n = 10
pts = [F(i, n) ** 2 for i in range(n + 1)]
w = [pts[i] - pts[i - 1] for i in range(1, n + 1)]
f = lambda t: t * t
U = sum(f(pts[i]) * w[i - 1] for i in range(1, n + 1))
L = sum(f(pts[i - 1]) * w[i - 1] for i in range(1, n + 1))
print("mesh", float(max(w)), "U-L", float(U - L), "exact", U - L, "bound", float(max(w) * (f(F(1)) - f(F(0)))))
