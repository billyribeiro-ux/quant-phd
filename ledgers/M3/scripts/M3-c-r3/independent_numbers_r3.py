"""Independent re-derivation of the numbers printed on L07, L08 and L09 (written by the round-3 verifier).

Own implementations: SVD instead of eigh for PCA, Gram-Schmidt for the shapes, an exact Fraction solve for
the L07 example, and a feasibility margin check for the L09 counts. Run: python -I independent_numbers_r3.py
"""
from fractions import Fraction

import numpy as np

print("== L07")
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
A = np.column_stack([np.ones(n), x1, x2])
beta = np.linalg.pinv(A) @ y
print("beta (own pinv):", " ".join(f"{b:.4f}" for b in beta))
res = y - A @ beta
print("residual norm:", f"{np.linalg.norm(res):.4f}")
print("A^T y:", " ".join(f"{v:.2f}" for v in A.T @ y))
print("max |A^T res|:", f"{np.max(np.abs(A.T @ res)):.3e}")

# Exact M2 solve over Fractions
pts = [(0, 1), (1, 2), (2, 2)]
ata = [[Fraction(3), Fraction(3)], [Fraction(3), Fraction(5)]]
aty = [Fraction(5), Fraction(6)]
det = ata[0][0] * ata[1][1] - ata[0][1] * ata[1][0]
b0 = (aty[0] * ata[1][1] - ata[0][1] * aty[1]) / det
b1 = (ata[0][0] * aty[1] - ata[1][0] * aty[0]) / det
fitted = [b0 + b1 * x for x, _ in pts]
resid = [yy - f for (_, yy), f in zip(pts, fitted)]
print("M2 exact beta0, beta1:", b0, b1, "fitted:", fitted, "resid:", resid)
print("M2 residual sum and dot with x:", sum(resid), sum(r * x for (x, _), r in zip(pts, resid)))

print("== L08")
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])


def gs(vectors):
    out = []
    for v in vectors:
        w = v.astype(float).copy()
        for q in out:
            w = w - (w @ q) * q
        out.append(w / np.linalg.norm(w))
    return out


ones = np.ones(6)
tau_c = TENORS - TENORS.mean()
level, slope, curv = gs([ones, tau_c, TENORS**2])
rng = np.random.default_rng(8)
T = 750
sc = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
shapes = np.column_stack([level, slope, curv])
panel = sc @ shapes.T + rng.normal(scale=0.5, size=(T, 6))
xc = panel - panel.mean(axis=0)
U, s, Vt = np.linalg.svd(xc, full_matrices=False)
lam = s**2 / (T - 1)  # eigenvalues of M = Xc^T Xc/(T-1), descending
V = Vt.T
M = xc.T @ xc / (T - 1)
print("eigen residual via SVD:", f"{np.max(np.abs(M @ V - V * lam)):.3e}")
shares = lam / lam.sum()
print("shares % (unrounded):", " ".join(f"{100 * v:.6f}" for v in shares[:3]), "top3 sum", f"{100 * shares[:3].sum():.6f}")
print("printed-form shares:", " ".join(f"{100 * v:.1f}" for v in shares[:3]), "sum of printed", f"{sum(round(100 * v, 1) for v in shares[:3]):.1f}")
for name, shp in zip(("level", "slope", "curvature"), (level, slope, curv)):
    c = np.abs(V.T @ shp)
    print(f"planted {name}: best PC{int(np.argmax(c)) + 1} |cos| {c.max():.4f}")
p2 = xc.copy()
rescaled = panel.copy()
rescaled[:, 0] *= 10.0
xr = rescaled - rescaled.mean(axis=0)
lam_r = np.linalg.svd(xr, compute_uv=False) ** 2 / (T - 1)
print("first share after column-1 x10:", f"{lam_r[0] / lam_r.sum():.6f}")
m11 = float(M[0, 0])
tr = float(np.trace(M))
print("M11, trace:", f"{m11:.6f} {tr:.6f}")
print("E1 bound 100 M11/(trace+99 M11):", f"{100 * m11 / (tr + 99 * m11):.6f}")
print("E1 bound from printed inputs 13.6818, 88.2028:", f"{100 * 13.6818 / (88.2028 + 99 * 13.6818):.6f}")
print("shares of first 3 printed to 4 dp, first share before rescale:", f"{shares[0]:.4f}")

print("== L09")
TOL, FEAS, NONPSD, MAXIT = 1e-12, 1e-8, 1e-9, 500


def clip(a, floor=0.0):
    w, q = np.linalg.eigh(a)
    return (q * np.maximum(w, floor)) @ q.T


def rescale(b):
    d = 1.0 / np.sqrt(np.diag(b))
    return b * np.outer(d, d)


def alt(a):
    x = a.copy()
    for _ in range(MAXIT):
        y = clip(x)
        np.fill_diagonal(y, 1.0)
        if np.max(np.abs(y - x)) < TOL:
            return y
        x = y
    return y


def feasible(a):
    return bool(np.max(np.abs(a - a.T)) < TOL and np.max(np.abs(np.diag(a) - 1)) < TOL and np.linalg.eigvalsh(a)[0] >= -FEAS)


C0 = np.array([[1, 0.9, 0.9], [0.9, 1, -0.9], [0.9, -0.9, 1.0]])
w0 = np.linalg.eigvalsh(C0)
print("C0 eig", np.round(w0, 6), "x^T C0 x", float(np.array([1, -1, -1.0]) @ C0 @ np.array([1, -1, -1.0])))
Bc = clip(C0)
print("||C0-B||^2", f"{np.sum((C0 - Bc) ** 2):.10f}", "neg eig sq", f"{np.sum(np.minimum(w0, 0) ** 2):.10f}")
R0 = rescale(Bc)
print("R0", np.round(R0, 4).tolist())
print("||C0-R0||_F", f"{np.linalg.norm(C0 - R0):.6f}", "sqrt(0.96)", f"{np.sqrt(0.96):.6f}")

r2 = np.random.default_rng(20261028)
rows = []
for _ in range(40):
    nz = r2.normal(0.0, 0.35, size=(5, 5))
    nz = (nz + nz.T) / 2.0
    a = 0.5 + nz
    np.fill_diagonal(a, 1.0)
    rows.append(a)
count_nonpsd = 0
count_feas = 0
count_closer = 0
margins = []
min_eigs_W = []
robust = 0
for a in rows:
    lmin = np.linalg.eigvalsh(a)[0]
    if lmin >= -NONPSD:
        continue
    count_nonpsd += 1
    R = rescale(clip(a))
    W = alt(a)
    dR = np.linalg.norm(a - R)
    dW = np.linalg.norm(a - W)
    if feasible(W):
        count_feas += 1
        if dW < dR:
            count_closer += 1
    margins.append(dR - dW)
    min_eigs_W.append(np.linalg.eigvalsh(W)[0])
    Wexact = rescale(clip(W))  # exact PSD, unit diagonal
    if np.linalg.norm(a - Wexact) < dR:
        robust += 1
print("non-PSD:", count_nonpsd, "W feasible:", count_feas, "W closer:", count_closer)
print("min margin dR-dW over non-PSD:", f"{min(margins):.6e}", "min eig of W:", f"{min(min_eigs_W):.6e}", "max eig neg of W:", f"{min(min_eigs_W):.3e}")
print("exact repair Wexact (clip+rescale of W) closer than R in", robust, "of", count_nonpsd)
