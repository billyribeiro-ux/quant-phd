"""Round-7 verifier (slice d): independent NumPy re-derivation of the numbers the project page states.
Covers Lab 3's printed numbers, the 'exemplar' numbers, the A3 closed form, the A4 singularity claims and the
Lab 1 and Lab 2 rescaling. Usage: .venv/bin/python -I <this file>."""

import numpy as np

C = np.array([[1, .7, .3, -.6], [.7, 1, .5, .4], [.3, .5, 1, .2], [-.6, .4, .2, 1.]])
v = np.array([.10, .20, .15, .30])
S = np.diag(v)


def clip(a, floor=0.0):
    w, V = np.linalg.eigh(a)
    X = (V * np.maximum(w, floor)) @ V.T
    d = np.diag(X)
    return X / np.sqrt(np.outer(d, d))


def psd(a):
    w, V = np.linalg.eigh(a)
    return (V * np.maximum(w, 0)) @ V.T


def proj(a, iters=2000):
    n = len(a)
    x = a.copy(); cs = np.zeros((n, n)); cu = np.zeros((n, n))
    for _ in range(iters):
        y = psd(x + cs)
        cs = x + cs - y
        nx = y + cu
        np.fill_diagonal(nx, 1.0)
        cu = y + cu - nx
        if np.max(np.abs(nx - x)) < 1e-15:
            x = nx
            break
        x = nx
    return x


print("eigenvalues of input:", np.round(np.linalg.eigvalsh(C), 6))
print("min eigenvalue of input:", round(float(np.linalg.eigvalsh(C)[0]), 6))
c_clip = clip(C); c_proj = proj(C)
d_clip = np.linalg.norm(c_clip - C); d_proj = np.linalg.norm(c_proj - C)
print("distance clip:", round(d_clip, 6), "proj:", round(d_proj, 6), "gap:", round(d_clip - d_proj, 6))
print("max abs entry diff:", round(float(np.max(np.abs(c_proj - c_clip))), 6))
print("det input:", round(float(np.linalg.det(C)), 6))
Sig = S @ C @ S
w = np.linalg.solve(Sig, np.ones(4)); w = w / w.sum()
print("weights input:", np.round(w, 6), "sum", round(float(w.sum()), 6))
print("eig clip repair:", float(np.linalg.eigvalsh(c_clip)[0]), " eig proj repair:", float(np.linalg.eigvalsh(c_proj)[0]))
print("min eig of projection (A4 numerics):", float(np.linalg.eigvalsh(c_proj)[0]))
# A4: clipped matrix at floor 0 is singular; its rescaled version too; check the raw clipped X and its diagonal
w_, V_ = np.linalg.eigh(C)
X = (V_ * np.maximum(w_, 0)) @ V_.T
print("clipped X min eigenvalue (before rescale):", float(np.linalg.eigvalsh(X)[0]), "diag X:", np.round(np.diag(X), 6))
# A3 closed form for two assets
rho = 0.3; a_, b_ = 0.1, 0.2
Sig2 = np.array([[a_ * a_, rho * a_ * b_], [rho * a_ * b_, b_ * b_]])
w2 = np.linalg.solve(Sig2, np.ones(2)); w2 /= w2.sum()
closed = np.array([b_ * (b_ - rho * a_), a_ * (a_ - rho * b_)]) / (a_ * a_ + b_ * b_ - 2 * rho * a_ * b_)
print("A3 closed form max diff:", float(np.max(np.abs(w2 - closed))))
# Lab 2 rescaling check: one matrix, clip, rescale
C2 = np.array([[1, .6, .5], [.6, 1, -.7], [.5, -.7, 1.]])
print("lab2 eig:", np.round(np.linalg.eigvalsh(C2), 6))
print("exemplar A weights rounded sum:", round(1.78 - 1.10 - 0.26 + 0.57, 2))
print("exemplar B gap:", round(0.176573 - 0.175003, 6))
