# Independent recomputation for L07 (round 3): different algorithms (QR, explicit inverse-free, SVD).
import numpy as np
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n); noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
A = np.column_stack([np.ones(n), x1, x2])
Q, R = np.linalg.qr(A)
beta_qr = np.linalg.solve(R, Q.T @ y)
U, s, Vt = np.linalg.svd(A, full_matrices=False)
beta_svd = Vt.T @ ((U.T @ y) / s)
print("beta (QR):", beta_qr, " beta (SVD):", beta_svd)
print("beta printed 4dp:", f"{beta_qr[0]:.4f} {beta_qr[1]:.4f} {beta_qr[2]:.4f}")
fitted = A @ beta_qr; r = y - fitted
print("residual norm 4dp:", f"{np.linalg.norm(r):.4f}", " unrounded:", np.linalg.norm(r))
print("A^T y (E2 claim (18.38, 3.10, -17.60)):", A.T @ y)
print("A^T y to 2dp:", np.round(A.T @ y, 2))
# P via orthonormal Q (independent of inverse)
P = Q @ Q.T
print("P sym:", np.max(np.abs(P - P.T)), " P^2-P:", np.max(np.abs(P @ P - P)), " rank(P)=", np.linalg.matrix_rank(P))
print("residual orth max:", np.max(np.abs(A.T @ r)))
# duplicated-design rank
dup = np.column_stack([A[:, 0], A[:, 1], A[:, 1]])
print("rank(dup^T dup) =", np.linalg.matrix_rank(dup.T @ dup), " rank(dup) =", np.linalg.matrix_rank(dup))
# Worked problems check
A1 = np.array([[1.0],[1.0]]); y1 = np.array([2.0,0.0]); P1 = A1 @ np.linalg.inv(A1.T@A1) @ A1.T
print("M1 Py:", P1 @ y1, " residual:", y1 - P1 @ y1)
A2 = np.array([[1,0],[1,1],[1,2]],float); y2 = np.array([1,2,2],float)
b2 = np.linalg.solve(A2.T@A2, A2.T@y2); print("M2 beta:", b2, "fitted:", A2@b2, "resid:", y2-A2@b2)
