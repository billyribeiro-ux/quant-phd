"""Round-4 verifier: recompute every Lab 3 printed number with numpy (an independent algorithm: numpy.linalg.eigh and
Higham-style alternating projections to convergence) and compare with the page's expected block.

Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/lab3_numbers_independent_r4.py
"""

import numpy as np

C = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
v = np.array([0.10, 0.20, 0.15, 0.30])
n = 4


def clip(a, floor=0.0):
    w, U = np.linalg.eigh(a)
    x = (U * np.maximum(w, floor)) @ U.T
    d = np.sqrt(np.diag(x))
    return x / np.outer(d, d)


def nearest_corr(a, iters=20000):
    # Higham (2002) alternating projections with Dykstra corrections, run to a tight tolerance.
    x = a.copy()
    ds = np.zeros_like(a)
    for _ in range(iters):
        r = x - ds
        w, U = np.linalg.eigh((r + r.T) / 2)
        y = (U * np.maximum(w, 0)) @ U.T
        ds = y - r
        x_new = y.copy()
        np.fill_diagonal(x_new, 1.0)
        if np.max(np.abs(x_new - x)) < 1e-15:
            x = x_new
            break
        x = x_new
    return x


w = np.linalg.eigvalsh(C)
print("smallest eigenvalue:", f"{w.min():.6f}", "| psd at 1e-10:", w.min() >= -1e-10)
cl = clip(C)
pr = nearest_corr(C)
dc = np.linalg.norm(cl - C, "fro")
dp = np.linalg.norm(pr - C, "fro")
print("distance from the input, clipping:", f"{dc:.6f}")
print("distance from the input, projection:", f"{dp:.6f}")
print("distance saved by projection over clipping:", f"{dc - dp:.6f}")
print("largest absolute entry difference between the two repairs:", f"{np.max(np.abs(pr - cl)):.6f}")
print("largest diagonal deviation: clipping", f"{np.max(np.abs(np.diag(cl) - 1)):.6f}", "| projection", f"{np.max(np.abs(np.diag(pr) - 1)):.6f}")
print("projection positive semidefinite at tol 1e-8:", np.linalg.eigvalsh(pr).min() >= -1e-8)
print("determinant of the input:", f"{np.linalg.det(C):.6f}")
S = np.diag(v)
Sigma = S @ C @ S
wts = np.linalg.solve(Sigma, np.ones(n))
wts = wts / wts.sum()
print("weights, input:", " ".join(f"{x:.6f}" for x in wts), "| sum", f"{wts.sum():.6f}")
print("raw distances (full precision):", repr(dc), repr(dp), repr(dc - dp))
print("Sigma singular values of the clipped repair's Sigma:", np.linalg.svd(S @ cl @ S, compute_uv=False).min())
