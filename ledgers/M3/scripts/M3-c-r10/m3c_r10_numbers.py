"""Independent recomputation of the numbers printed or quoted in L07, L08 and L09 (round 10).

Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-c-r10/m3c_r10_numbers.py
Routes differ from the lab twins on purpose: least squares by QR (not normal equations), PCA through the SVD of the
centred panel (not eigh of M), shapes by Gram-Schmidt (not the lab's projection code), and the clip-and-rescale and
alternating-projection repairs with an eigen-routine via np.linalg.eig on the symmetric input (real part), plus a
second stopping rule. Exact arithmetic is used for the hand-worked matrices.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

# ---------- L07 ----------
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
A = np.column_stack([np.ones(n), x1, x2])
q, r = np.linalg.qr(A)
beta_qr = np.linalg.solve(r, q.T @ y)
print(f"L07 beta (QR route) {beta_qr[0]:.4f} {beta_qr[1]:.4f} {beta_qr[2]:.4f}")
resid = y - A @ beta_qr
print(f"L07 residual norm {np.linalg.norm(resid):.4f}; max |A^T r| {np.max(np.abs(A.T @ resid)):.2e}")
print("L07 A^T y " + " ".join(f"{v:.2f}" for v in A.T @ y))
P = A @ np.linalg.inv(A.T @ A) @ A.T
print(f"L07 P idempotent {np.max(np.abs(P @ P - P)):.2e}; Py - A beta {np.max(np.abs(P @ y - A @ beta_qr)):.2e}")
dup = np.column_stack([A[:, 0], A[:, 1], A[:, 1]])
sv = np.linalg.svd(dup.T @ dup, compute_uv=False)
print(f"L07 singular values of duplicated A^T A {sv[0]:.4f} {sv[1]:.4f} {sv[2]:.2e}; rank {int(np.sum(sv > 1e-9 * sv[0]))}")
# hand examples in exact arithmetic
A2 = [[Fraction(1), Fraction(0)], [Fraction(1), Fraction(1)], [Fraction(1), Fraction(2)]]
yy = [Fraction(1), Fraction(2), Fraction(2)]
g = [[sum(A2[k][i] * A2[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
b = [sum(A2[k][i] * yy[k] for k in range(3)) for i in range(2)]
det = g[0][0] * g[1][1] - g[0][1] * g[1][0]
b0 = (g[1][1] * b[0] - g[0][1] * b[1]) / det
b1 = (-g[1][0] * b[0] + g[0][0] * b[1]) / det
print(f"L07 M2 exact: beta0 {b0}, beta1 {b1}, fitted {[b0 + b1 * k for k in range(3)]}")

# ---------- L08 ----------
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
rng8 = np.random.default_rng(8)
T = 750
# Gram-Schmidt shapes (independent of the lab's projection code)
level = np.ones(6)
slope = TENORS - TENORS.mean()
curv = TENORS**2 - (TENORS**2).mean()
basis = []
for v in (level, slope, curv):
    w = v.copy()
    for e in basis:
        w = w - (w @ e) * e
    basis.append(w / np.linalg.norm(w))
scores = np.column_stack(
    [rng8.normal(scale=8.0, size=T), rng8.normal(scale=4.0, size=T), rng8.normal(scale=2.0, size=T)]
)
panel = scores @ np.column_stack(basis).T + rng8.normal(scale=0.5, size=(T, 6))
xc = panel - panel.mean(axis=0)
_, s, vt = np.linalg.svd(xc, full_matrices=False)
lam_svd = s**2 / (T - 1)
shares = lam_svd / lam_svd.sum()
print(f"L08 shares (SVD route) {100 * shares[0]:.6f} {100 * shares[1]:.6f} {100 * shares[2]:.6f}")
print(f"L08 rounded {100 * shares[0]:.1f} {100 * shares[1]:.1f} {100 * shares[2]:.1f}")
for name, shape in zip(("level", "slope", "curvature"), basis):
    c = np.abs(vt @ shape)
    print(f"L08 {name}: best row {int(np.argmax(c)) + 1} |cos| {c.max():.6f}")
M = xc.T @ xc / (T - 1)
print(f"L08 M11 {M[0, 0]:.4f} trace {np.trace(M):.4f}; trace via sum of squared centred rows {np.sum(xc**2) / (T - 1):.4f}")
bound = 100 * M[0, 0] / (np.trace(M) + 99 * M[0, 0])
print(f"L08 E1 bound from unrounded M11, trace: {bound:.6f}")
panel2 = panel.copy()
panel2[:, 0] *= 10.0
xc2 = panel2 - panel2.mean(axis=0)
s2 = np.linalg.svd(xc2, compute_uv=False)
lam2 = s2**2 / (T - 1)
print(f"L08 first share after x10 on 0.25y column (SVD route) {lam2[0] / lam2.sum():.6f}; bound <= share: {bound <= lam2[0] / lam2.sum()}")
print(f"L08 doubled-panel shares unchanged: {np.max(np.abs(np.linalg.svd(2 * xc, compute_uv=False)**2 / np.sum(np.linalg.svd(2 * xc, compute_uv=False)**2) - s**2 / np.sum(s**2))):.2e}")
# exact hand example M1 of L08
X8 = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 9.0]])
Xt = X8 - X8.mean(axis=0)
M8 = Xt.T @ Xt / 2
print(f"L08 M1 M = {M8.tolist()}, trace {np.trace(M8)}, det {np.linalg.det(M8):.6f}, eigs {np.linalg.eigvalsh(M8).tolist()}")
print(f"L08 M1 (17 +- sqrt 277)/2 = {(17 - 277**0.5) / 2:.6f}, {(17 + 277**0.5) / 2:.6f}")

# ---------- L09 ----------
C0 = np.array([[1.0, 0.9, 0.9], [0.9, 1.0, -0.9], [0.9, -0.9, 1.0]])
w0, v0 = np.linalg.eig(C0)
print(f"L09 C0 eigenvalues (eig) {sorted(np.real(w0).round(6).tolist())}")
Bc = (v0 * np.maximum(np.real(w0), 0.0)) @ np.linalg.inv(v0)
Bc = np.real((Bc + Bc.T) / 2)
print(f"L09 ||C0-B||^2 {np.sum((C0 - Bc) ** 2):.10f}; diag B {np.round(np.diag(Bc), 6).tolist()}")
d = np.sqrt(np.diag(Bc))
R = Bc / np.outer(d, d)
print("L09 R\n" + np.array2string(R, precision=4))
print(f"L09 ||C0-R||_F {np.linalg.norm(C0 - R):.10f}; sqrt(0.96) {0.96**0.5:.10f}")
xq = np.array([1.0, -1.0, -1.0])
print(f"L09 witness {xq @ C0 @ xq}")
A6 = np.array([[1.0, 1.2], [1.2, 1.0]])
ww, vv = np.linalg.eigh(A6)
A0 = (vv * np.maximum(ww, 0)) @ vv.T
print(f"L09 Ex3.6 A0 {np.round(A0, 6).tolist()}; ||A-A0||^2 {np.sum((A6 - A0) ** 2):.6f}; ||A-R6||^2 {np.sum((A6 - np.array([[1, 1], [1, 1.0]])) ** 2):.6f}")


def clip(a: np.ndarray, floor: float = 0.0) -> np.ndarray:
    lam, vecs = np.linalg.eigh(a)
    return (vecs * np.maximum(lam, floor)) @ vecs.T


def clip_eig_route(a: np.ndarray) -> np.ndarray:
    """Alternative eigen-route: eig of the symmetric matrix, real part, reconstruction by solve."""
    lam, vecs = np.linalg.eig(a)
    lam = np.real(lam)
    vecs = np.real(vecs)
    q_mat, _ = np.linalg.qr(vecs)
    return np.real((q_mat * np.maximum(lam, 0.0)) @ q_mat.T)


def alt_proj(a: np.ndarray, tol: float, max_iter: int) -> np.ndarray:
    x = a.copy()
    y = x
    for _ in range(max_iter):
        y = clip(x)
        np.fill_diagonal(y, 1.0)
        if np.max(np.abs(y - x)) < tol:
            break
        x = y
    return y


def is_corr(a: np.ndarray) -> bool:
    return bool(
        np.max(np.abs(a - a.T)) < 1e-12
        and np.max(np.abs(np.diag(a) - 1.0)) < 1e-12
        and np.linalg.eigvalsh(a)[0] >= -1e-8
    )


rng9 = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    nz = rng9.normal(0.0, 0.35, size=(5, 5))
    nz = (nz + nz.T) / 2.0
    m = 0.5 + nz
    np.fill_diagonal(m, 1.0)
    mats.append(m)
nonpsd = [i for i, m in enumerate(mats) if np.linalg.eigvalsh(m)[0] < -1e-9]
print(f"L09 non-PSD count (smallest eig < -1e-9): {len(nonpsd)} of 40")
for label, tol, max_iter in (("lab rule", 1e-12, 500), ("tol 1e-10", 1e-10, 500), ("tol 1e-14, 5000 steps", 1e-14, 5000)):
    passes = 0
    closer = 0
    margins = []
    for i in nonpsd:
        m = mats[i]
        rr = rescale_ok = None
        rr = clip(m) / np.outer(np.sqrt(np.diag(clip(m))), np.sqrt(np.diag(clip(m))))
        w_alt = alt_proj(m, tol, max_iter)
        if is_corr(w_alt):
            passes += 1
            dw = np.linalg.norm(m - w_alt)
            dr = np.linalg.norm(m - rr)
            margins.append(dr - dw)
            if dw < dr:
                closer += 1
    print(f"L09 [{label}] alt passes {passes} of {len(nonpsd)}; closer than R {closer} of {len(nonpsd)}; min margin {min(margins):.6f}")
first = nonpsd[0]
m = mats[first]
rr = clip(m) / np.outer(np.sqrt(np.diag(clip(m))), np.sqrt(np.diag(clip(m))))
w_alt = alt_proj(m, 1e-12, 500)
print(f"L09 first non-PSD index {first}: ||A-R|| {np.linalg.norm(m - rr):.6f}; ||A-W|| {np.linalg.norm(m - w_alt):.6f}")
print(f"L09 clip route check on index {first}: {np.max(np.abs(clip_eig_route(m) - clip(m))):.2e}")
steps = 0
x_it = m.copy()
for steps in range(1, 501):
    yy_it = clip(x_it)
    np.fill_diagonal(yy_it, 1.0)
    if np.max(np.abs(yy_it - x_it)) < 1e-12:
        break
    x_it = yy_it
print(f"L09 index {first} alt-proj iterations to tolerance: {steps}")
print(f"L09 min eigenvalue of W (index {first}): {np.linalg.eigvalsh(w_alt)[0]:.3e}")
