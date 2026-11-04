"""Independent re-derivation of the numbers printed on L07, L08 and L09 (M3 slice c, round 7).

Uses algorithms different from the lab twins: QR and SVD instead of normal equations and eigh (L07, L08),
and alternative alternating-projection stopping rules and a Dykstra-corrected projection (L09).
Run: python -I -W error ledgers/M3/scripts/M3-c-r7/m3c_r7_numbers.py  (from the checkout root)
"""
import numpy as np

print("== L07 (seed 7 design, re-derived with QR and SVD; no normal equations)")
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
q, r = np.linalg.qr(a)
beta_qr = np.linalg.solve(r, q.T @ y)
p_qr = q @ q.T
resid = y - p_qr @ y
print("beta (QR):", np.round(beta_qr, 6), "printed 4dp:", [f"{v:.4f}" for v in beta_qr])
print("residual norm (QR):", f"{np.linalg.norm(resid):.6f}", "printed 4dp:", f"{np.linalg.norm(resid):.4f}")
print("A^T y (exact dot products):", [f"{v:.6f}" for v in a.T @ y], "printed 2dp:", [f"{v:.2f}" for v in a.T @ y])
print("max |A^T resid| (QR):", f"{np.max(np.abs(a.T @ resid)):.3e}")
print("P from QR equals P from normal equations, max diff:",
      f"{np.max(np.abs(p_qr - a @ np.linalg.solve(a.T @ a, a.T))):.3e}")
dup = np.column_stack([a[:, 0], a[:, 1], a[:, 1]])
print("rank of A^T A with a duplicated column (matrix_rank of A^T A):", int(np.linalg.matrix_rank(dup.T @ dup)), "of 3")

print("\n== L08 (seed 8 panel, re-derived with SVD of the centred data)")
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
T_DAYS = 750
rng = np.random.default_rng(8)


def unit(v):
    return v / np.linalg.norm(v)


level = unit(np.ones(6))
slope = unit(TENORS - TENORS.mean())
quad = TENORS ** 2
quad = quad - quad.mean()
quad = quad - (quad @ level) * level - (quad @ slope) * slope
curv = unit(quad)
scores = np.column_stack([rng.normal(scale=8.0, size=T_DAYS), rng.normal(scale=4.0, size=T_DAYS),
                          rng.normal(scale=2.0, size=T_DAYS)])
panel = scores @ np.column_stack([level, slope, curv]).T + rng.normal(scale=0.5, size=(T_DAYS, 6))
xc = panel - panel.mean(axis=0)
_, s, vt = np.linalg.svd(xc, full_matrices=False)
lam_svd = s ** 2 / (T_DAYS - 1)
shares = lam_svd / lam_svd.sum()
print("eigenvalues via SVD^2/(T-1):", np.round(lam_svd, 6))
print("shares 1dp %:", [f"{100 * v:.1f}" for v in shares[:3]], " unrounded %:", [f"{100 * v:.6f}" for v in shares[:3]])
print("sum of printed top-3 rounded shares:", round(sum(round(100 * v, 1) for v in shares[:3]), 1),
      "vs unrounded top-3 sum %:", f"{100 * shares[:3].sum():.6f}")
vsvd = vt.T
for name, shp in (("level", level), ("slope", slope), ("curvature", curv)):
    c = np.abs(vsvd.T @ shp)
    print(f"planted {name}: best PC{int(np.argmax(c)) + 1}, |cos| {c.max():.6f}, second best {np.sort(c)[-2]:.6f}")
xc2 = 2.0 * panel - (2.0 * panel).mean(axis=0)
s2 = np.linalg.svd(xc2, compute_uv=False)
print("doubled-panel shares max diff:", f"{np.max(np.abs(s2 ** 2 / (s2 ** 2).sum() - shares)):.3e}")
resc = panel.copy()
resc[:, 0] *= 10.0
xr = resc - resc.mean(axis=0)
sr = np.linalg.svd(xr, compute_uv=False)
print("first share after 10x column 1 (SVD):", f"{sr[0] ** 2 / (sr ** 2).sum():.6f}", "printed 4dp:",
      f"{sr[0] ** 2 / (sr ** 2).sum():.4f}")
m11 = float((xc.T @ xc)[0, 0] / (T_DAYS - 1))
tr = float(np.trace(xc.T @ xc) / (T_DAYS - 1))
bound = 100 * m11 / (tr + 99 * m11)
print("E1 bound from unrounded M11, trace:", f"{bound:.6f}", "| from printed 13.6818, 88.2028:",
      f"{100 * 13.6818 / (88.2028 + 99 * 13.6818):.6f}")
print("E1 check: bound <= new first share:", bound <= sr[0] ** 2 / (sr ** 2).sum() + 1e-12)

print("\n== L09 (seeded 40 matrices; alternative correct repairs and stopping rules)")
SEED = 20261028
N, SIZE = 40, 5


def mats():
    g = np.random.default_rng(SEED)
    out = []
    for _ in range(N):
        z = g.normal(0.0, 0.35, size=(SIZE, SIZE))
        z = (z + z.T) / 2.0
        a = 0.5 + z
        np.fill_diagonal(a, 1.0)
        out.append(a)
    return out


def clip(a, floor=0.0):
    w, v = np.linalg.eigh(a)
    return (v * np.maximum(w, floor)) @ v.T


def rescale(b):
    d = np.sqrt(np.diag(b))
    return b / np.outer(d, d)


def ap_default(a, tol=1e-12, max_iter=500):
    x = a.copy()
    for _ in range(max_iter):
        y = clip(x)
        np.fill_diagonal(y, 1.0)
        if np.max(np.abs(y - x)) < tol:
            return y
        x = y
    return y


def ap_long(a):
    return ap_default(a, tol=1e-14, max_iter=20000)


def dykstra(a, iters=2000):
    """Higham (2002)-style alternating projections with Dykstra correction (PSD cone, unit diagonal)."""
    y = a.copy()
    ds = np.zeros_like(a)
    for _ in range(iters):
        r = y - ds
        x = clip(r)
        ds = x - r
        y = x.copy()
        np.fill_diagonal(y, 1.0)
    return y


def is_corr(a, tol=1e-12, feas=1e-8):
    return bool(np.max(np.abs(a - a.T)) < tol and np.max(np.abs(np.diag(a) - 1.0)) < tol
                and np.linalg.eigvalsh(a)[0] >= -feas)


def run(label, repair):
    nonpsd = feas = closer = 0
    margins = []
    first = None
    for i, a in enumerate(mats()):
        if np.linalg.eigvalsh(a)[0] >= -1e-9:
            continue
        nonpsd += 1
        r_mat = rescale(clip(a))
        w = repair(a)
        dr = np.linalg.norm(a - r_mat)
        dw = np.linalg.norm(a - w)
        if is_corr(w):
            feas += 1
            if dw < dr:
                closer += 1
            margins.append(dr - dw)
        if first is None:
            first = (i, dr, dw)
    print(f"{label}: nonPSD={nonpsd} W_is_corr={feas} W_corr_and_closer={closer} "
          f"min_margin={min(margins) if margins else float('nan'):.6f} first={first}")


run("default AP (tol 1e-12, 500 steps, as page)", ap_default)
run("long AP (tol 1e-14, 20000 steps)", ap_long)
run("Dykstra-corrected projections (2000 steps)", dykstra)
