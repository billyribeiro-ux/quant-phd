import numpy as np
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
print("A^T y =", np.round(a.T @ y, 4))
gram = a.T @ a
beta = np.linalg.solve(gram, a.T @ y)
print("beta =", np.round(beta, 4))
r = y - a @ beta
print("residual norm =", round(float(np.linalg.norm(r)), 4))
print("max |A^T r| =", float(np.max(np.abs(a.T @ r))))
