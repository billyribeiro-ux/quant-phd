# Independent recomputation of L07 numbers (run with python -I).
import numpy as np
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n); noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8*x1 - 0.4*x2 + noise
A = np.column_stack([np.ones(n), x1, x2])
G = A.T @ A
beta = np.linalg.solve(G, A.T @ y)
r = y - A @ beta
print("beta", np.round(beta, 6), "beta0 4dp", f"{beta[0]:.4f}", "resid norm", f"{np.linalg.norm(r):.6f}")
print("A^T y (E2 claim 18.38, 3.10, -17.60):", np.round(A.T @ y, 4))
# E2 claim: check prints False since |A^T y| >= 1e-9
print("max |A^T y|:", np.max(np.abs(A.T @ y)))
# M2 hand example
A2 = np.array([[1,0],[1,1],[1,2]], float); y2 = np.array([1,2,2], float)
b2 = np.linalg.solve(A2.T@A2, A2.T@y2); print("M2 beta", b2, "fitted", A2@b2, "resid", y2-A2@b2, "resid.x", (y2-A2@b2)@A2[:,1])
# M1
A1 = np.array([[1.],[1.]]); P1 = A1@np.linalg.inv(A1.T@A1)@A1.T; print("M1 P", P1, "p", P1@np.array([2.,0.]))
# R1/Q: P^2 = P, Q
