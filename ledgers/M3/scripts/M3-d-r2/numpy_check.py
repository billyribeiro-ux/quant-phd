"""Independent numeric check of the Lab 1 and Lab 3 printed numbers with numpy, and of the nearest correlation matrix.

Nearest unit-diagonal PSD matrix in Frobenius norm via Higham's alternating projections (Dykstra's correction), run to
convergence at 1e-14, independent of the lab's Jacobi code.
"""
import numpy as np

C3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
V3 = np.array([0.10, 0.20, 0.15, 0.30])
C1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
C1b = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])


def clip(a, floor=0.0):
    w, v = np.linalg.eigh(a)
    x = v @ np.diag(np.maximum(w, floor)) @ v.T
    d = np.sqrt(np.diag(x))
    return x / np.outer(d, d)


def nearest_corr(a, iters=200000, tol=1e-14):
    n = a.shape[0]
    y = a.copy()
    ds = np.zeros_like(a)
    for _ in range(iters):
        r = y - ds
        w, v = np.linalg.eigh(r)
        x = v @ np.diag(np.maximum(w, 0)) @ v.T
        ds = x - r
        y_new = x.copy()
        np.fill_diagonal(y_new, 1.0)
        if np.max(np.abs(y_new - y)) < tol:
            y = y_new
            break
        y = y_new
    return y


def lab1(c):
    w, v = np.linalg.eigh(c)
    print("eigenvalues sorted:", np.round(np.sort(w), 6))
    cl = v @ np.diag(np.maximum(w, 0)) @ v.T
    print("rebuilt diagonal:", np.round(np.diag(cl), 6))
    d = np.sqrt(np.diag(cl))
    rep = cl / np.outer(d, d)
    print("repaired:\n", np.round(rep, 6))
    print("min eig repaired:", np.min(np.linalg.eigvalsh(rep)))


print("== Lab 1 matrix")
lab1(C1)
print("== Lab 2 matrix")
lab1(C1b)
print("== Lab 3")
w = np.linalg.eigvalsh(C3)
print("smallest eigenvalue %.6f" % w[0])
cl = clip(C3)
ny = nearest_corr(C3)
dc = np.linalg.norm(cl - C3)
dp = np.linalg.norm(ny - C3)
print("distance clip %.6f" % dc)
print("distance nearest (Higham, converged) %.6f" % dp)
print("gap %.6f" % (dc - dp))
print("max abs entry difference clip vs nearest %.6f" % np.max(np.abs(cl - ny)))
print("min eig of nearest %.3e" % np.linalg.eigvalsh(ny)[0])
print("max diag dev nearest %.3e" % np.max(np.abs(np.diag(ny) - 1)))
print("det input %.6f" % np.linalg.det(C3))
S = np.diag(V3)
Sig = S @ C3 @ S
one = np.ones(4)
wts = np.linalg.solve(Sig, one)
wts = wts / wts.sum()
print("weights input", np.round(wts, 6), "sum", wts.sum())
# A3 closed form check, two assets
a, b, rho = 0.1, 0.2, 0.7
den = a * a + b * b - 2 * rho * a * b
S2 = np.diag([a, b]) @ np.array([[1, rho], [rho, 1]]) @ np.diag([a, b])
w2 = np.linalg.solve(S2, np.ones(2))
print("A3 check", w2 / w2.sum(), np.array([b * (b - rho * a), a * (a - rho * b)]) / den)
