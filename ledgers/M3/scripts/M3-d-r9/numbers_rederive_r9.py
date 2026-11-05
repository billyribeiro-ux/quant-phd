"""Round-9 verifier (M3 slice d): re-derive every printed number on project.html with numpy, independently of the page code.

Run: .venv/bin/python -I ledgers/M3/scripts/M3-d-r9/numbers_rederive_r9.py
"""
import numpy as np

np.set_printoptions(precision=6, suppress=True)


def clip(a, floor=0.0):
    w, v = np.linalg.eigh(a)
    x = (v * np.maximum(w, floor)) @ v.T
    d = np.diag(x)
    return x / np.sqrt(np.outer(d, d)), x


def psd_part(a):
    w, v = np.linalg.eigh(a)
    return (v * np.maximum(w, 0.0)) @ v.T


def projection(a, max_iter=500, tol=1e-10):
    n = a.shape[0]
    x = a.copy()
    cs = np.zeros((n, n))
    cu = np.zeros((n, n))
    for _ in range(max_iter):
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


def weights(c, v):
    s = np.diag(v)
    sig = s @ c @ s
    w = np.linalg.solve(sig, np.ones(len(v)))
    return w / w.sum()


# Lab 1
c1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
w1, v1 = np.linalg.eigh(c1)
print("L1 eigenvalues", np.round(w1, 6))
r1, x1 = clip(c1)
print("L1 rebuilt diag", np.round(np.diag(x1), 6))
print("L1 repaired", np.round(r1, 6).tolist())
print("L1 deviation", np.max(np.abs(np.diag(r1) - 1)))

# Lab 2 (completed blanks)
c2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
w2, _ = np.linalg.eigh(c2)
r2, x2 = clip(c2)
print("L2 eigenvalues", np.round(w2, 6))
print("L2 rebuilt diag", np.round(np.diag(x2), 6))
print("L2 repaired", np.round(r2, 6).tolist())
print("L2 deviation", np.max(np.abs(np.diag(r2) - 1)))

# Lab 3
c3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
vols = np.array([0.10, 0.20, 0.15, 0.30])
lam = np.linalg.eigvalsh(c3)
print("L3 smallest eigenvalue", f"{lam[0]:.9f}", "all", np.round(lam, 9))
clipm, x3 = clip(c3)
proj = projection(c3)
dc = np.linalg.norm(clipm - c3)
dp = np.linalg.norm(proj - c3)
print("L3 dist clip", f"{dc:.9f}", "proj", f"{dp:.9f}", "gap", f"{dc - dp:.9f}")
print("L3 max entry diff", f"{np.max(np.abs(proj - clipm)):.9f}")
print("L3 diag dev clip", f"{np.max(np.abs(np.diag(clipm) - 1)):.3e}", "proj", f"{np.max(np.abs(np.diag(proj) - 1)):.3e}")
print("L3 proj min eig", f"{np.linalg.eigvalsh(proj)[0]:.3e}", "tol 1e-8 PSD", np.linalg.eigvalsh(proj)[0] >= -1e-8)
print("L3 clip min eig", f"{np.linalg.eigvalsh(clipm)[0]:.3e}")
print("L3 det", f"{np.linalg.det(c3):.9f}")
sig = np.diag(vols) @ c3 @ np.diag(vols)
print("L3 det sigma", f"{np.linalg.det(sig):.3e}", "cond", f"{np.linalg.cond(sig):.3e}")
print("L3 weights", np.round(weights(c3, vols), 9), "sum", f"{weights(c3, vols).sum():.12f}")
print("L3 projection sigma min eig", f"{np.linalg.eigvalsh(np.diag(vols) @ proj @ np.diag(vols))[0]:.3e}")
print("L3 clip Y sigma min eig", f"{np.linalg.eigvalsh(np.diag(vols) @ clipm @ np.diag(vols))[0]:.3e}")
print("L3 X clip min eig (unrescaled)", f"{np.linalg.eigvalsh(x3)[0]:.3e}", "X diag", np.round(np.diag(x3), 9))

# Weights identity: Sigma w is constant
w = weights(c3, vols)
print("L3 Sigma w", np.round(sig @ w, 12))

# Two-asset closed form check (A3)
a, b, rho = 0.2, 0.3, 0.25
wa = np.array([b * (b - rho * a), a * (a - rho * b)]) / (a * a + b * b - 2 * rho * a * b)
s2 = np.array([[a * a, rho * a * b], [rho * a * b, b * b]])
ws = np.linalg.solve(s2, np.ones(2))
ws = ws / ws.sum()
print("A3 closed form vs solve", np.max(np.abs(wa - ws)))
