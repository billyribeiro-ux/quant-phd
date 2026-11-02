# Independent recomputation of L09 numbers (python -I). Own implementations; no lab code imported.
import numpy as np
C0 = np.array([[1, .9, .9], [.9, 1, -.9], [.9, -.9, 1.]])
x = np.array([1, -1, -1.])
print("x^T C0 x =", x @ C0 @ x)
w, Qm = np.linalg.eigh(C0); print("eig C0", w)
# clip via explicit sum of outer products
B = sum(max(w[i], 0) * np.outer(Qm[:, i], Qm[:, i]) for i in range(3))
print("||C0-B||^2 =", np.sum((C0 - B)**2), " sum neg eig^2 =", sum(min(e, 0)**2 for e in w))
d = np.sqrt(np.diag(B)); R = B / np.outer(d, d)
print("R =\n", np.round(R, 6))
print("||C0-R||_F =", np.linalg.norm(C0 - R), "sq", np.sum((C0-R)**2))
# Example 3.6
A = np.array([[1, 1.2], [1.2, 1.]])
print("eig A", np.linalg.eigvalsh(A))
A0 = np.array([[1.1, 1.1], [1.1, 1.1]])
print("||A-A0||^2", np.sum((A - np.array([[1.1,1.1],[1.1,1.1]]))**2), "||A-R||^2", np.sum((A - np.ones((2,2)))**2))
# M3 example
Bm = np.array([[4, 2], [2, 9.]]); print("eig Bm", np.linalg.eigvalsh(Bm), (13 - np.sqrt(41))/2, (13+np.sqrt(41))/2)
# seeded experiment, own generator
rng = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    N = rng.normal(0.0, 0.35, size=(5, 5)); N = (N + N.T) / 2
    Aa = 0.5 + N; np.fill_diagonal(Aa, 1.0); mats.append(Aa)
def project(Aa, iters=500, tol=1e-12):
    X = Aa.copy()
    for _ in range(iters):
        ww, VV = np.linalg.eigh(X)
        Y = (VV * np.maximum(ww, 0)) @ VV.T
        np.fill_diagonal(Y, 1.0)
        if np.max(np.abs(Y - X)) < tol:
            return Y
        X = Y
    return Y
def clip_rescale(Aa):
    ww, VV = np.linalg.eigh(Aa)
    Bb = (VV * np.maximum(ww, 0)) @ VV.T
    dd = np.sqrt(np.diag(Bb)); return Bb / np.outer(dd, dd)
nonpsd = feas = closer = 0; first = None; ties = 0
for idx, Aa in enumerate(mats):
    lo = np.linalg.eigvalsh(Aa)[0]
    if lo >= -1e-9: continue
    nonpsd += 1
    Rr = clip_rescale(Aa); Ww = project(Aa)
    ok = np.max(np.abs(Ww - Ww.T)) < 1e-12 and np.max(np.abs(np.diag(Ww) - 1)) < 1e-12 and np.linalg.eigvalsh(Ww)[0] >= -1e-8
    feas += bool(ok)
    dR = np.linalg.norm(Aa - Rr); dW = np.linalg.norm(Aa - Ww)
    if dW < dR: closer += 1
    if dW == dR: ties += 1
    if first is None: first = (idx, dR, dW, lo)
print("nonpsd", nonpsd, "feasible", feas, "closer", closer, "ties", ties, "first", first)
