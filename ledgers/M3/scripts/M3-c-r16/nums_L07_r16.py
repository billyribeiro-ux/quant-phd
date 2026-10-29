import numpy as np
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
gram = a.T @ a
beta = np.linalg.solve(gram, a.T @ y)
p = a @ np.linalg.solve(gram, a.T)
res = y - p @ y
print("A^T y:", np.round(a.T @ y, 4))
print("beta unrounded:", beta)
print("residual norm:", np.linalg.norm(res))
print("max|A^T res|:", np.max(np.abs(a.T @ res)))
print("A^T y -> check False with beta=0 (max abs >= 1e-9):", np.max(np.abs(a.T @ y)) >= 1e-9)
dup = np.column_stack([a[:, 0], a[:, 1], a[:, 1]])
print("rank dup gram:", np.linalg.matrix_rank(dup.T @ dup))
# M2 / P worked examples
A=np.array([[1.0],[1.0]]); y2=np.array([2.0,0.0]); P1=A@np.linalg.inv(A.T@A)@A.T; print("M1 P:",P1.tolist(), "Py:", P1@y2)
A2=np.array([[1,0],[1,1],[1,2.]]); y3=np.array([1,2,2.]); b=np.linalg.solve(A2.T@A2,A2.T@y3); print("M2 beta:",b, "fitted", A2@b, "resid", y3-A2@b)
A3=np.array([[1.0],[0.0]]); P3=A3@np.linalg.inv(A3.T@A3)@A3.T; print("M3 P:", P3.tolist(), P3@np.array([3.,4.]))
