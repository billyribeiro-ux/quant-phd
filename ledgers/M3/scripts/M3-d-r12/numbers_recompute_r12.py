"""Round-12 verifier (M3 slice d): independent numpy recomputation of every number in project.html Labs 1-3 and of
the rounding claims in the prose (unrounded gap, deviations, determinant, weights, eigenvalues of repairs)."""

import numpy as np

np.set_printoptions(precision=9, suppress=True, linewidth=150)


def clip_rescale(m, floor=0.0):
    w, v = np.linalg.eigh(m)
    x = (v * np.maximum(w, floor)) @ v.T
    d = np.diag(x).copy()
    return x / np.sqrt(np.outer(d, d)), x


def psd_part(m):
    w, v = np.linalg.eigh(m)
    return (v * np.maximum(w, 0.0)) @ v.T


def proj(m, iters=200000, tol=1e-15):
    x = m.copy()
    n = len(m)
    cs = np.zeros((n, n))
    cu = np.zeros((n, n))
    for _ in range(iters):
        y = psd_part(x + cs)
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


print("== Lab 1 matrix")
c1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
print("eig", np.linalg.eigvalsh(c1))
r1, x1 = clip_rescale(c1)
print("rebuilt diag", np.diag(x1))
print("repaired", r1)
print("dev", np.max(np.abs(np.diag(r1) - 1)), "min eig repaired", np.linalg.eigvalsh(r1)[0])
print("== Lab 2 matrix")
c2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
print("eig", np.linalg.eigvalsh(c2))
r2, x2 = clip_rescale(c2)
print("rebuilt diag", np.diag(x2))
print("repaired", r2)
print("dev", np.max(np.abs(np.diag(r2) - 1)), "min eig repaired", np.linalg.eigvalsh(r2)[0])
print("== Lab 3 matrix")
c3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
vols = np.array([0.10, 0.20, 0.15, 0.30])
print("eig input", np.linalg.eigvalsh(c3))
clip, xc = clip_rescale(c3)
pr = proj(c3)
dc = np.linalg.norm(clip - c3)
dp = np.linalg.norm(pr - c3)
print("dist clip %.12f proj %.12f gap %.12f" % (dc, dp, dc - dp))
print("max abs entry diff %.12f" % np.max(np.abs(pr - clip)))
print("eig clip", np.linalg.eigvalsh(clip))
print("eig proj", np.linalg.eigvalsh(pr))
print("max diag dev clip %.3g proj %.3g" % (np.max(np.abs(np.diag(clip) - 1)), np.max(np.abs(np.diag(pr) - 1))))
print("proj psd 1e-8:", np.linalg.eigvalsh(pr)[0] >= -1e-8)
print("det input %.12f" % np.linalg.det(c3))
S = np.diag(vols)
sig = S @ c3 @ S
w = np.linalg.solve(sig, np.ones(4))
w = w / w.sum()
print("weights input", w, "sum", w.sum())
print("det Sigma", np.linalg.det(sig), "expected (prod v)^2 det C =", (np.prod(vols) ** 2) * np.linalg.det(c3))
print("clip diag", np.diag(clip), "clipped Y singular check min|eig| =", np.min(np.abs(np.linalg.eigvalsh(clip))))
sp = S @ pr @ S
print("projection Sigma min eig", np.linalg.eigvalsh(sp)[0], "cond", np.linalg.cond(sp))
print("sum of differences of squared entries check: dp^2 + gap relation", dp**2, dc**2)
print("clip has negative eigen of input:", np.linalg.eigvalsh(c3)[0] < 0)
