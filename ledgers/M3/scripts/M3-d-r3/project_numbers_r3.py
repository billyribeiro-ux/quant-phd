"""Independent recomputation of every printed number in the M3 project labs and report prose (verifier round 3, slice d).

Uses numpy.linalg.eigh and numpy only as an independent oracle; the page's own Jacobi code is not reused.
Run as: .venv/bin/python -I ledgers/M3/scripts/M3-d-r3/project_numbers_r3.py   (from the checkout root)
"""

import numpy as np

np.set_printoptions(precision=17)


def clip_rescale(c):
    w, v = np.linalg.eigh(c)
    x = (v * np.maximum(w, 0.0)) @ v.T
    d = np.sqrt(np.diag(x))
    return x / np.outer(d, d)


def project(a, tol=1e-10, max_iter=500):
    """Dykstra-style alternating projections, written independently from the page's code."""
    n = a.shape[0]
    x = a.copy()
    cs = np.zeros((n, n))
    cu = np.zeros((n, n))
    for _ in range(max_iter):
        w, v = np.linalg.eigh(x + cs)
        y = (v * np.maximum(w, 0.0)) @ v.T
        cs = x + cs - y
        nx = y + cu
        np.fill_diagonal(nx, 1.0)
        cu = y + cu - nx
        gap = np.linalg.norm(nx - y)
        step = np.linalg.norm(nx - x)
        x = nx
        if gap <= tol and step <= tol:
            break
    return x


def weights(c, v):
    s = np.diag(v)
    sig = s @ c @ s
    z = np.linalg.solve(sig, np.ones(len(v)))
    return z / z.sum()


print("== Lab 1 (3x3, SIMULATED)")
c1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
w1, _ = np.linalg.eigh(c1)
print("eigs", np.sort(w1))
r1 = clip_rescale(c1)
print("repaired", r1)
print("max |diag-1| repaired lab1 (unrounded):", np.max(np.abs(np.diag(r1) - 1.0)))
print("min eig repaired lab1:", np.linalg.eigvalsh(r1).min())
print("rebuilt diagonal lab1:", np.diag((np.linalg.eigh(c1)[1] * np.maximum(w1, 0)) @ np.linalg.eigh(c1)[1].T))

print("== Lab 2 (3x3, completion)")
c2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
w2, v2 = np.linalg.eigh(c2)
print("eigs", np.sort(w2))
print("rebuilt diagonal lab2:", np.diag((v2 * np.maximum(w2, 0)) @ v2.T))
r2 = clip_rescale(c2)
print("repaired lab2:\n", r2)
print("max |diag-1| repaired lab2 (unrounded):", np.max(np.abs(np.diag(r2) - 1.0)))
print("min eig repaired lab2:", np.linalg.eigvalsh(r2).min())

print("== Lab 3 (4x4, report reference)")
c3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
vols = [0.10, 0.20, 0.15, 0.30]
print("smallest eig input:", repr(np.linalg.eigvalsh(c3).min()))
clip = clip_rescale(c3)
proj = project(c3)
dc = np.linalg.norm(clip - c3)
dp = np.linalg.norm(proj - c3)
print("dist clip:", repr(dc), "dist proj:", repr(dp), "gap:", repr(dc - dp))
print("max abs entry diff repairs:", repr(np.max(np.abs(proj - clip))))
print("clip max |diag-1|:", repr(np.max(np.abs(np.diag(clip) - 1))), " proj max |diag-1|:", repr(np.max(np.abs(np.diag(proj) - 1))))
print("proj min eig:", repr(np.linalg.eigvalsh(proj).min()), " clip min eig:", repr(np.linalg.eigvalsh(clip).min()))
print("det input:", repr(np.linalg.det(c3)))
print("weights input:", weights(c3, vols), weights(c3, vols).sum())
