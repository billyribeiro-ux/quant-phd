"""Round-8 verifier (M3 slice d): independent NumPy re-derivation of every printed number on project.html.

Uses numpy.linalg.eigh and numpy.linalg.solve, not the page's Jacobi code. Run from the checkout root:
    .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/numpy_rederive_r8.py
"""

import numpy as np


def clip(a, floor=0.0):
    w, v = np.linalg.eigh(a)
    x = (v * np.maximum(w, floor)) @ v.T
    d = np.sqrt(np.diag(x))
    return x, x / np.outer(d, d)


def proj_step_P(m):
    w, v = np.linalg.eigh(m)
    return (v * np.maximum(w, 0.0)) @ v.T


def projection(a, tol=1e-10, max_iter=500):
    n = a.shape[0]
    x = a.copy()
    es = np.zeros((n, n))
    h = np.zeros((n, n))
    for _ in range(max_iter):
        j = proj_step_P(x + es)
        es = x + es - j
        nn = j + h
        np.fill_diagonal(nn, 1.0)
        h = j + h - nn
        gap = np.linalg.norm(nn - j)
        change = np.linalg.norm(nn - x)
        x = nn
        if gap <= tol and change <= tol:
            break
    return x


def projection_no_stop(a, steps):
    n = a.shape[0]
    x = a.copy()
    es = np.zeros((n, n))
    h = np.zeros((n, n))
    for _ in range(steps):
        j = proj_step_P(x + es)
        es = x + es - j
        nn = j + h
        np.fill_diagonal(nn, 1.0)
        h = j + h - nn
        x = nn
    return x


def weights(corr, vols):
    s = np.diag(vols)
    sigma = s @ corr @ s
    z = np.linalg.solve(sigma, np.ones(len(vols)))
    return z / z.sum()


# Lab 1 and Lab 2 (page matrices)
lab1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
lab2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
for name, a in [("lab1", lab1), ("lab2", lab2)]:
    w, v = np.linalg.eigh(a)
    d = np.diag((v * np.maximum(w, 0)) @ v.T)
    x = (v * np.maximum(w, 0)) @ v.T
    rep = x / np.sqrt(np.outer(d, d))
    print(name, "eigenvalues", " ".join(f"{t:.6f}" for t in w))
    print(name, "rebuilt diagonal", " ".join(f"{t:.6f}" for t in d))
    print(name, "repaired upper", " ".join(f"{rep[0, 1]:.6f}", ) if False else "", f"{rep[0,1]:.6f} {rep[0,2]:.6f} {rep[1,2]:.6f}")
    print(name, "repaired min eig", f"{np.linalg.eigvalsh(rep)[0]:.9f}")

# Lab 3
corr = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
vols = np.array([0.10, 0.20, 0.15, 0.30])
print("lab3 min eig input", f"{np.linalg.eigvalsh(corr)[0]:.12f}")
xc, clipm = clip(corr)
proj = projection(corr)
proj_long = projection_no_stop(corr, 5000)
print("lab3 clip Frobenius", f"{np.linalg.norm(clipm - corr):.12f}")
print("lab3 proj Frobenius", f"{np.linalg.norm(proj - corr):.12f}")
print("lab3 proj(500, tol) vs proj(5000 no stop) max abs diff", f"{np.abs(proj - proj_long).max():.3e}")
print("lab3 saved", f"{np.linalg.norm(clipm - corr) - np.linalg.norm(proj - corr):.12f}")
print("lab3 max entry diff", f"{np.abs(proj - clipm).max():.12f}")
print("lab3 clip diag dev", f"{np.abs(np.diag(clipm) - 1).max():.3e}", "proj diag dev", f"{np.abs(np.diag(proj) - 1).max():.3e}")
print("lab3 proj min eig", f"{np.linalg.eigvalsh(proj)[0]:.12e}", "clip min eig", f"{np.linalg.eigvalsh(clipm)[0]:.12e}")
print("lab3 det input", f"{np.linalg.det(corr):.12f}")
print("lab3 weights input", " ".join(f"{t:.12f}" for t in weights(corr, vols)))
print("lab3 X (clip before rescale) min eig", f"{np.linalg.eigvalsh(xc)[0]:.12e}", "diag", " ".join(f"{t:.12f}" for t in np.diag(xc)))
print("lab3 X diag all positive", bool(np.all(np.diag(xc) > 0)))
print("lab3 proj min eig (projection of proj, PSD check at 1e-8)", np.linalg.eigvalsh(proj)[0] >= -1e-8)
print("lab3 proj is PSD at 1e-8 and unit diag:", bool(np.linalg.eigvalsh(proj)[0] >= -1e-8), bool(np.allclose(np.diag(proj), 1)))
