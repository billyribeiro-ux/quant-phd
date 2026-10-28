"""Independent check of L05 Lab 1 numbers with sympy-free Fractions and a numpy cross-check."""
from fractions import Fraction as F
import itertools
import numpy as np

Q = [[F(4), F(1), F(0)], [F(1), F(3), F(1)], [F(0), F(1), F(2)]]
c = [F(-1), F(0), F(2)]
A = [[F(1), F(1), F(1)], [F(0), F(1), F(-1)]]
b = [F(1), F(0)]
K = [[Q[i][j] for j in range(3)] + [A[k][i] for k in range(2)] for i in range(3)] + [[A[k][j] for j in range(3)] + [F(0), F(0)] for k in range(2)]
rhs = [-x for x in c] + b
print("numpy det", np.linalg.det(np.array([[float(x) for x in r] for r in K])))
# exact solve by Cramer via Fraction Gauss
def solve(M, r):
    n = len(r)
    R = [list(M[i]) + [r[i]] for i in range(n)]
    for col in range(n):
        p = next(i for i in range(col, n) if R[i][col] != 0)
        R[col], R[p] = R[p], R[col]
        pv = R[col][col]
        R[col] = [x / pv for x in R[col]]
        for i in range(n):
            if i != col and R[i][col] != 0:
                f = R[i][col]
                R[i] = [x - f * y for x, y in zip(R[i], R[col])]
    return [R[i][n] for i in range(n)]
sol = solve(K, rhs)
print("x", sol[:3], "lambda", sol[3:])
x = sol[:3]; lam = sol[3:]
stat = [sum(Q[i][j] * x[j] for j in range(3)) + c[i] + sum(A[k][i] * lam[k] for k in range(2)) for i in range(3)]
print("stationarity residuals", stat, "constraint residuals", [sum(A[k][i] * x[i] for i in range(3)) - b[k] for k in range(2)])
f = lambda y: F(1, 2) * sum(y[i] * Q[i][j] * y[j] for i in range(3) for j in range(3)) + sum(c[i] * y[i] for i in range(3))
print("objective", f(x), float(f(x)))
v = [F(-2), F(1), F(1)]
vqv = sum(v[i] * Q[i][j] * v[j] for i in range(3) for j in range(3))
print("v'Qv", vqv, "Qv", [sum(Q[i][j] * v[j] for j in range(3)) for i in range(3)])
ok = all(f([x[i] + F(k, 4) * v[i] for i in range(3)]) - f(x) == F(1, 2) * (F(k, 4) ** 2) * vqv for k in range(-8, 9))
print("null line identity exact", ok)
# Part B: Q_B, c_B, x>=0, all active sets, brute force via KKT over subsets; and grid
QB = [[F(2), F(1)], [F(1), F(2)]]; cB = [F(-3), F(1)]
fB = lambda y: F(1, 2) * sum(y[i] * QB[i][j] * y[j] for i in range(2) for j in range(2)) + sum(cB[i] * y[i] for i in range(2))
best = None
for zs in [(), (0,), (1,), (0, 1)]:
    free = [i for i in range(2) if i not in zs]
    xx = [F(0), F(0)]
    if free:
        M = [[QB[i][j] for j in free] for i in free]
        s = solve(M, [-cB[i] for i in free])
        for p, val in zip(free, s):
            xx[p] = val
    g = [sum(QB[i][j] * xx[j] for j in range(2)) + cB[i] for i in range(2)]
    print("set", zs, "x", xx, "primal", all(t >= 0 for t in xx), "dual", all(g[i] >= 0 for i in zs))
grid = [F(k, 16) for k in range(33)]
vals = [fB([a, b2]) for a in grid for b2 in grid]
print("grid points", len(vals), "below -9/4:", sum(1 for t in vals if t < F(-9, 4)), "min equals -9/4:", min(vals) == F(-9, 4))
