import numpy as np
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
print("A^T y", a.T @ y)
g=a.T@a
b=np.linalg.solve(g,a.T@y)
print("beta", b, "norm", np.linalg.norm(y-a@b))
print("M2 check", np.linalg.solve(np.array([[3.,3],[3,5]]), np.array([5.,6])))
print("dup rank", np.linalg.matrix_rank(np.column_stack([a[:,0],a[:,1],a[:,1]]).T@np.column_stack([a[:,0],a[:,1],a[:,1]])))
