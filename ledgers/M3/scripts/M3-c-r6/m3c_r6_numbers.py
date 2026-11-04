"""Round-6 independent recomputation of every printed number in L08 Lab 1 (SIMULATED panel), L09 Lab 1,
L09 Example 2.3 / 3.6 and the L08 Problem E1, E3 and Remark values, using algorithms different from the twins.

Algorithms used here, independent of the twins:
- eigenvalues of M from the singular values of the centred data (SVD of Xc), not from eigh of M;
- PSD part of a symmetric matrix from the SVD (|A| = V |S| V^T), not from clipping eigh output;
- alternating projections with a Frobenius-change stopping rule and a fixed iteration cap;
- the C0 eigenvalues from the roots of the characteristic polynomial.
The generators replicate the page's specification (seeded draws), not the twins' code.
Run from the checkout root with: .venv/bin/python ledgers/M3/scripts/M3-c-r6/m3c_r6_numbers.py
"""

from __future__ import annotations

import numpy as np

# ---------------- L08 ----------------
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
T_DAYS = 750


def gram_schmidt(vectors: list[np.ndarray]) -> list[np.ndarray]:
    out: list[np.ndarray] = []
    for v in vectors:
        w = v.astype(float).copy()
        for q in out:
            w = w - (w @ q) * q
        out.append(w / np.linalg.norm(w))
    return out


def shapes() -> list[np.ndarray]:
    level = np.ones(6)
    slope = TENORS - TENORS.mean()
    curv = TENORS**2 - (TENORS**2).mean()
    return gram_schmidt([level, slope, curv])


rng = np.random.default_rng(8)
f_level, f_slope, f_curv = shapes()
scores = np.column_stack(
    [
        rng.normal(scale=8.0, size=T_DAYS),
        rng.normal(scale=4.0, size=T_DAYS),
        rng.normal(scale=2.0, size=T_DAYS),
    ]
)
panel = scores @ np.column_stack([f_level, f_slope, f_curv]).T + rng.normal(scale=0.5, size=(T_DAYS, 6))

xc = panel - panel.mean(axis=0)
m = xc.T @ xc / (T_DAYS - 1)
_, s, vt = np.linalg.svd(xc, full_matrices=False)
eig_from_svd = (s**2) / (T_DAYS - 1)  # eigenvalues of M, descending
shares = eig_from_svd / eig_from_svd.sum()
print("L08 eigenvalues of M from SVD of Xc (descending):", " ".join(f"{x:.8f}" for x in eig_from_svd))
print("L08 unrounded shares (%):", " ".join(f"{100 * x:.6f}" for x in shares[:3]))
print("L08 printed shares to one decimal:", " ".join(f"{100 * x:.1f}" for x in shares[:3]))
print("L08 sum of printed one-decimal shares:", f"{sum(round(100 * x, 1) for x in shares[:3]):.1f}")
print("L08 sum of unrounded first three shares (%):", f"{100 * shares[:3].sum():.6f}")
print("L08 max |rounding error| of printed shares (pp):", f"{max(abs(round(100*x,1)-100*x) for x in shares[:3]):.6f}")
print(
    "L08 sum of printed minus unrounded first three (pp):",
    f"{sum(round(100 * x, 1) for x in shares[:3]) - 100 * shares[:3].sum():.6f}",
)
v_svd = vt.T  # right singular vectors = eigenvectors of M
for name, f in (("level", f_level), ("slope", f_slope), ("curvature", f_curv)):
    cosv = np.abs(v_svd.T @ f)
    order = np.argsort(cosv)[::-1]
    print(
        f"L08 {name}: max |cos| {cosv[order[0]]:.6f} at PC{order[0] + 1}; runner-up |cos| {cosv[order[1]]:.6f}"
    )
print("L08 planted shapes orthonormal, max |Gram - I|:", f"{np.max(np.abs(np.column_stack([f_level, f_slope, f_curv]).T @ np.column_stack([f_level, f_slope, f_curv]) - np.eye(3))):.2e}")

# doubling: eigenvalues scale by 4, shares unchanged
s2 = np.linalg.svd(2 * xc, compute_uv=False)
print("L08 doubled shares equal original to 1e-9:", bool(np.max(np.abs((s2**2) / np.sum(s2**2) - shares)) < 1e-9))

# rescaling first column by 10: new first share, and the E1 bound from M11 and trace
resc = panel.copy()
resc[:, 0] *= 10.0
xr = resc - resc.mean(axis=0)
sr = np.linalg.svd(xr, compute_uv=False)
new_share1 = (sr[0] ** 2) / np.sum(sr**2)
print(f"L08 first share after rescaling column 1 by 10 (SVD): {new_share1:.6f}")
m11 = float(m[0, 0])
tr = float(np.trace(m))
bound = 100 * m11 / (tr + 99 * m11)
print(f"L08 E1 bound from unrounded M11 {m11:.8f} trace {tr:.8f}: {bound:.6f}")
print(f"L08 E1 bound from printed inputs 13.6818 and 88.2028: {100 * 13.6818 / (88.2028 + 99 * 13.6818):.6f}")
print(f"L08 E1 bound from printed inputs at 4 dp (rounded): {100 * 13.6818 / (88.2028 + 99 * 13.6818):.4f}")
print(f"L08 check trace equals sum of eigenvalues: {abs(tr - eig_from_svd.sum()):.3e}")
# lower bound respects the actual rescaled first eigenvalue
print("L08 bound <= new share:", bool(bound <= new_share1 + 1e-12), f"{bound:.6f} <= {new_share1:.6f}")
print("L08 bound > old share 0.7587:", bool(bound > shares[0]))

# M1 worked example (page, Solution M1)
X1 = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 9.0]])
C1 = X1 - X1.mean(axis=0)
M1 = C1.T @ C1 / 2
print("L08 M1 matrix:", M1.tolist(), "trace", np.trace(M1), "det", round(float(np.linalg.det(M1)), 10))
print("L08 M1 eigenvalues:", np.linalg.eigvalsh(M1).tolist(), "formula (17 +- sqrt 277)/2:", (17 - 277**0.5) / 2, (17 + 277**0.5) / 2)
print("L08 M1 squared row norms of centred rows:", (C1**2).sum(axis=1).tolist())

# M2 and M3 numbers
print("L08 M2 shares:", [4 / 6, 1 / 6, 1 / 6], "sum", 4 / 6 + 1 / 6 + 1 / 6)
print("L08 M3 shares of 9*(2,1):", [18 / 27, 9 / 27])

# E3 printed shares
print("L08 E3 printed sum:", round(75.9 + 18.1 + 5.2, 1))

# Example: rescaled eigenvalues via SVD for the full six-column panel (Prop 2.3 check, c = -3)
s3 = np.linalg.svd(-3 * xc, compute_uv=False)
print("L08 Prop 2.3 with c=-3 shares unchanged to 1e-9:", bool(np.max(np.abs((s3**2)/np.sum(s3**2) - shares)) < 1e-9))

# ---------------- L09 ----------------


def psd_part(a: np.ndarray) -> np.ndarray:
    """Clip eigenvalues at zero via the SVD: A_+ = (A + |A|)/2, |A| = V |S| V^T (symmetric A)."""
    u, sv, vtt = np.linalg.svd(a)
    absa = vtt.T @ np.diag(sv) @ vtt
    return (a + absa) / 2.0


def nearest_pd_rescale(a: np.ndarray) -> np.ndarray:
    b = psd_part(a)
    d = np.sqrt(np.diag(b))
    return b / np.outer(d, d)


def min_eig(a: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((a + a.T) / 2)[0])


def alt_proj(a: np.ndarray, cap: int = 500) -> np.ndarray:
    x = a.copy()
    for _ in range(cap):
        y = psd_part(x)
        np.fill_diagonal(y, 1.0)
        if np.linalg.norm(y - x) < 1e-12:
            return y
        x = y
    return y


c0 = np.array([[1.0, 0.9, 0.9], [0.9, 1.0, -0.9], [0.9, -0.9, 1.0]])
# characteristic polynomial roots
coeffs = np.poly(c0)
print("L09 C0 eigenvalues from characteristic polynomial roots:", sorted(np.roots(coeffs).real.round(6).tolist()))
print("L09 C0 witness x^T C0 x:", float(np.array([1, -1, -1]) @ c0 @ np.array([1, -1, -1])))
b0 = psd_part(c0)
print("L09 ||C0-B||_F^2 =", f"{np.sum((c0 - b0) ** 2):.10f}", "| eig(B) min", f"{min_eig(b0):.3e}")
r0 = nearest_pd_rescale(c0)
print("L09 R entries:", np.round(r0, 6).tolist())
print("L09 is R unit diagonal and symmetric:", bool(np.allclose(np.diag(r0), 1.0) and np.allclose(r0, r0.T)))

# Example 3.6
A36 = np.array([[1.0, 1.2], [1.2, 1.0]])
A0 = psd_part(A36)
print("L09 Ex3.6 A0 =", np.round(A0, 10).tolist(), "||A-A0||^2 =", round(float(np.sum((A36 - A0) ** 2)), 10))
R36 = nearest_pd_rescale(A36)
print("L09 Ex3.6 R =", np.round(R36, 10).tolist(), "||A-R||^2 =", round(float(np.sum((A36 - R36) ** 2)), 10))
print("L09 Ex3.6 eigenvalues of A:", np.linalg.eigvalsh(A36).tolist())

# Example 2.3 / Problem values: ||C0-R||_F
print(f"L09 ||C0 - R||_F = {np.linalg.norm(c0 - r0):.10f}")

# seeded matrices (replicate the spec: rng seed 20261028, 40 draws of 5x5 noise, symmetrised)
rng9 = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    nz = rng9.normal(0.0, 0.35, size=(5, 5))
    nz = (nz + nz.T) / 2.0
    a = 0.5 + nz
    np.fill_diagonal(a, 1.0)
    mats.append(a)

nonpsd = [i for i, a in enumerate(mats) if min_eig(a) < -1e-9]
print("L09 count non-PSD (min eig < -1e-9):", len(nonpsd), "of 40; PSD count:", 40 - len(nonpsd))
print("L09 min eigenvalue of the nearest-PSD check, smallest |min eig| among non-PSD:", f"{max(min_eig(mats[i]) for i in nonpsd):.6e}")
print("L09 closest-to-threshold PSD (min eig, largest):", f"{max(min_eig(a) for i, a in enumerate(mats) if i not in nonpsd):.6e}")

def is_corr(a: np.ndarray) -> bool:
    sym = np.max(np.abs(a - a.T)) < 1e-12
    unit = np.max(np.abs(np.diag(a) - 1.0)) < 1e-12
    return bool(sym and unit and min_eig(a) >= -1e-8)


feas = 0
closer = 0
min_feas_margin = 1.0
for i in nonpsd:
    a = mats[i]
    rr = nearest_pd_rescale(a)
    ww = alt_proj(a)
    dR = np.linalg.norm(a - rr)
    dW = np.linalg.norm(a - ww)
    if is_corr(ww):
        feas += 1
        if dW < dR:
            closer += 1
    min_feas_margin = min(min_feas_margin, min(dR - dW, 1.0))
    if i == nonpsd[0]:
        print(f"L09 first non-PSD index {i}: ||A-R||_F = {dR:.6f}, ||A-W||_F = {dW:.6f}")
print(f"L09 alternating projections pass is_correlation: {feas} of {len(nonpsd)}")
print(f"L09 pass and strictly closer than R: {closer} of {len(nonpsd)}")
print(f"L09 smallest (dR - dW) over the non-PSD matrices: {min_feas_margin:.6f}")

# rounding of the count-related statements: 23 of 40 and 17 PSD
print("L09 PSD count", 40 - len(nonpsd))

# Why-it-matters: 23 vs threshold sensitivity: count below -1e-8 and below -1e-10
print("L09 count below -1e-8:", sum(min_eig(a) < -1e-8 for a in mats), " below -1e-10:", sum(min_eig(a) < -1e-10 for a in mats))
