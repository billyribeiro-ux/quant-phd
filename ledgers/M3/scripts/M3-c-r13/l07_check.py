import numpy as np
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n); noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8*x1 - 0.4*x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
print("A^T y =", np.round(a.T @ y, 4))
g = a.T @ a
beta = np.linalg.solve(g, a.T @ y)
print("beta", beta, "resid norm", np.linalg.norm(y - a @ beta))
# M1, M2, M3 exact checks
from fractions import Fraction as F
A = np.array([[1.0],[1.0]]); yy = np.array([2.0,0.0]); P = A @ np.linalg.inv(A.T@A) @ A.T
print("M1 P", P*2, "Py", P@yy, "res", yy-P@yy, "A.res", A.T@(yy-P@yy))
X = np.array([[1,0],[1,1],[1,2.]]); yv = np.array([1,2,2.])
b = np.linalg.solve(X.T@X, X.T@yv); print("M2 beta", b, "fitted", X@b, "res", yv-X@b, "sum", (yv-X@b).sum(), "x.res", np.array([0,1,2.])@(yv-X@b))
