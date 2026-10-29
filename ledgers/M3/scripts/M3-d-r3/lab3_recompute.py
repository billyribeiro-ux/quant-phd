"""Independent recomputation of the Lab 3 reference numbers with NumPy (verifier-side only; the page is stdlib)."""

import numpy as np

C = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
V = np.array([0.10, 0.20, 0.15, 0.30])
w, U = np.linalg.eigh(C)
print("eig", w)
clip_x = U @ np.diag(np.maximum(w, 0)) @ U.T
d = np.sqrt(np.diag(clip_x))
clip = clip_x / np.outer(d, d)
# Dykstra with NumPy, long run, to the nearest unit-diagonal PSD matrix
x = C.copy()
S = np.zeros_like(C)
Uc = np.zeros_like(C)
for _ in range(200000):
    z, Vv = np.linalg.eigh(x + S)
    y = Vv @ np.diag(np.maximum(z, 0)) @ Vv.T
    S = x + S - y
    nx = y + Uc
    np.fill_diagonal(nx, 1.0)
    Uc = y + Uc - nx
    if np.max(np.abs(nx - x)) < 1e-14 and np.max(np.abs(nx - y)) < 1e-14:
        x = nx
        break
    x = nx
proj = x
dc = np.linalg.norm(clip - C)
dp = np.linalg.norm(proj - C)
print("dist clip", repr(dc), "dist proj", repr(dp), "gap", repr(dc - dp))
print("max entry diff proj-clip", repr(np.max(np.abs(proj - clip))))
print("proj min eig", np.linalg.eigvalsh(proj).min(), "diag dev proj", np.max(np.abs(np.diag(proj) - 1)), "clip diag dev", np.max(np.abs(np.diag(clip) - 1)))
print("det C", repr(np.linalg.det(C)))
Sig = np.diag(V) @ C @ np.diag(V)
u = np.linalg.solve(Sig, np.ones(4))
wt = u / u.sum()
print("weights", wt, "sum", wt.sum())
print("displayed gap from rounded distances", f"{round(0.176573-0.175003,6):.6f}", "unrounded gap display", f"{dc-dp:.6f}")
print("eig of clip min", np.linalg.eigvalsh(clip_x).min())
