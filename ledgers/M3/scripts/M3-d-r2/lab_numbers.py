"""Round-2 independent recomputation (numpy, not the reference module) of the printed numbers in Labs 1 to 3."""
import numpy as np
np.set_printoptions(precision=6, suppress=True)
def clip_rescale(C):
    vals, V = np.linalg.eigh(C)
    X = (V * np.maximum(vals, 0.0)) @ V.T
    d = np.diag(X)
    return X, X / np.sqrt(np.outer(d, d))
# Lab 1
C1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
w, V = np.linalg.eigh(C1); print("L1 eig", w)
X1, R1 = clip_rescale(C1); print("L1 rebuilt diag", np.diag(X1)); print("L1 repaired\n", R1)
print("L1 max dev", np.max(np.abs(np.diag(R1) - 1)), "min eig repaired", np.linalg.eigvalsh(R1)[0])
# Lab 2
C2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
w2 = np.linalg.eigvalsh(C2); print("L2 eig", w2)
X2, R2 = clip_rescale(C2); print("L2 rebuilt diag", np.diag(X2)); print("L2 repaired\n", R2)
print("L2 repaired min eig", np.linalg.eigvalsh(R2)[0])
# Lab 3
C3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
v = np.array([0.10, 0.20, 0.15, 0.30])
print("L3 smallest eig", np.linalg.eigvalsh(C3)[0])
_, clip = clip_rescale(C3)
# nearest PSD unit-diagonal matrix: Higham alternating projections with Dykstra, independent code, tight tolerance
def proj(A, iters=20000):
    n = A.shape[0]; x = A.copy(); S = np.zeros_like(A); U = np.zeros_like(A)
    for _ in range(iters):
        vals, V = np.linalg.eigh(x + S); Y = (V * np.maximum(vals, 0)) @ V.T
        S = x + S - Y
        Xn = Y + U; np.fill_diagonal(Xn, 1.0)
        U = Y + U - Xn
        if np.max(np.abs(Xn - x)) < 1e-14: x = Xn; break
        x = Xn
    return x
P = proj(C3)
dc = np.linalg.norm(clip - C3); dp = np.linalg.norm(P - C3)
print("dist clip", dc, "dist proj", dp, "gap", dc - dp)
print("max entry diff", np.max(np.abs(P - clip)))
print("max diag dev clip", np.max(np.abs(np.diag(clip) - 1)), "proj", np.max(np.abs(np.diag(P) - 1)))
print("proj min eig", np.linalg.eigvalsh(P)[0])
def wts(S_mat):
    Sg = np.diag(v) @ S_mat @ np.diag(v)
    u = np.linalg.solve(Sg, np.ones(4)); return u / u.sum()
print("weights clip", wts(clip)); print("weights proj", wts(P))
print("largest weight diff", np.max(np.abs(wts(P) - wts(clip))))
print("nearest PSD (projection of clip?) check: dist to clip", np.linalg.norm(clip - C3))
