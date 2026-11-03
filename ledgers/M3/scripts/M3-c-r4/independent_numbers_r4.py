"""Verifier r4 independent recomputation of the numbers printed or quoted on L07, L08 and L09.

Uses its own implementations (QR/SVD and power iteration, not eigh/lstsq) and prints unrounded values."""
import numpy as np

# ---- L07: seeded regression (same generator call order as the page twin)
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
A = np.column_stack([np.ones(n), x1, x2])
Q, R = np.linalg.qr(A)
beta_qr = np.linalg.solve(R, Q.T @ y)
U, s, Vt = np.linalg.svd(A, full_matrices=False)
beta_svd = Vt.T @ ((U.T @ y) / s)
res = y - A @ beta_qr
print("L07 beta (QR)           ", beta_qr)
print("L07 beta (SVD)          ", beta_svd)
print("L07 residual norm       ", np.linalg.norm(res))
print("L07 A^T y               ", A.T @ y)
print("L07 A^T res max abs     ", np.max(np.abs(A.T @ res)))
P = A @ np.linalg.inv(A.T @ A) @ A.T
print("L07 P sym/idem          ", np.max(np.abs(P - P.T)), np.max(np.abs(P @ P - P)))

# ---- L08: panel (same generator call order as the page twin), independent PCA by power iteration + Jacobi-free route
rng = np.random.default_rng(8)
T = 750
tenors = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
lev = np.ones(6) / np.sqrt(6)
sl = tenors - tenors.mean(); sl = sl / np.linalg.norm(sl)
qd = tenors ** 2; qd = qd - qd.mean(); qd = qd - (qd @ lev) * lev - (qd @ sl) * sl; cv = qd / np.linalg.norm(qd)
scores = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
shapes = np.column_stack([lev, sl, cv])
noise = rng.normal(scale=0.5, size=(T, 6))
panel = scores @ shapes.T + noise
xc = panel - panel.mean(axis=0)
M = xc.T @ xc / (T - 1)
# eigenvalues via SVD of M (symmetric PSD, so singular values = eigenvalues)
Uu, sv, Vv = np.linalg.svd(M)
print("L08 eig (svd, desc)     ", sv)
shares = sv / sv.sum()
print("L08 shares unrounded    ", shares)
print("L08 shares percent      ", 100 * shares[:3])
print("L08 sum of top3 shares  ", 100 * shares[:3].sum())
for name, sh in zip(["level", "slope", "curv"], [lev, sl, cv]):
    c = np.abs(Uu.T @ sh)
    print("L08 |cos| to", name, np.round(c, 6), "argmax", int(np.argmax(c)) + 1)
# rescaled first share and bound
Xr = xc.copy(); Xr[:, 0] *= 10
Mr = Xr.T @ Xr / (T - 1)
svr = np.linalg.svd(Mr, compute_uv=False)
print("L08 first share after  ", svr[0] / svr.sum(), " before", sv[0] / sv.sum())
M11 = M[0, 0]; tr = np.trace(M)
print("L08 M11, trace          ", M11, tr, "bound", 100 * M11 / (tr + 99 * M11))
print("L08 bound from rounded inputs 13.6818, 88.2028:", 100 * 13.6818 / (88.2028 + 99 * 13.6818))
print("L08 doubled shares equal:", np.max(np.abs(np.linalg.svd(4 * M, compute_uv=False) / np.linalg.svd(4 * M, compute_uv=False).sum() - shares)))
print("L08 E3 sum rounded      ", round(100*shares[0],1)+round(100*shares[1],1)+round(100*shares[2],1))

# ---- L09: 40 seeded 5x5 matrices, independent repairs (eigh vs SVD-based clipping; own loop)
C0 = np.array([[1, .9, .9], [.9, 1, -.9], [.9, -.9, 1.]])
w, V = np.linalg.eigh(C0)
print("L09 C0 eig              ", w)
x = np.array([1., -1, -1]); print("L09 witness             ", x @ C0 @ x)
Bc = V @ np.diag(np.maximum(w, 0)) @ V.T
print("L09 ||C0-B||^2          ", np.sum((C0 - Bc) ** 2), " sum neg^2", np.sum(np.minimum(w, 0) ** 2))
d = np.sqrt(np.diag(Bc)); Rc = Bc / np.outer(d, d)
print("L09 R                   \n", Rc)

def clip_svd(a):
    # PSD part via polar decomposition: (|a| + a)/2 with |a| from SVD of symmetric a
    U_, s_, Vt_ = np.linalg.svd(a)
    sgn = np.sign(np.diag(Vt_ @ U_))  # eigen-sign for symmetric a: a = U S Vt, a = U diag(sgn) S... use eigen via sign
    lam_signed = np.diag(U_.T @ a @ U_)  # eigenvalues in the U basis (exact for symmetric a with distinct |lambda|)
    return U_ @ np.diag(np.maximum(lam_signed, 0)) @ U_.T

def proj_iter(a):
    xk = a.copy()
    for _ in range(500):
        yk = clip_svd(xk)
        np.fill_diagonal(yk, 1.0)
        if np.max(np.abs(yk - xk)) < 1e-12:
            return yk
        xk = yk
    return yk

rng = np.random.default_rng(20261028)
nonpsd = 0; closer = 0; feas = 0; margins = []
dR_first = dW_first = None
for idx in range(40):
    nz = rng.normal(0.0, 0.35, size=(5, 5)); nz = (nz + nz.T) / 2.0
    a = 0.5 + nz; np.fill_diagonal(a, 1.0)
    lam_a = np.linalg.eigvalsh(a)[0]
    if lam_a >= -1e-9:
        continue
    nonpsd += 1
    la, va = np.linalg.eigh(a)
    Ba = va @ np.diag(np.maximum(la, 0)) @ va.T
    da = np.sqrt(np.diag(Ba)); R_a = Ba / np.outer(da, da)
    W_a = proj_iter(a)
    dR = np.linalg.norm(a - R_a); dW = np.linalg.norm(a - W_a)
    ok = (np.max(np.abs(W_a - W_a.T)) < 1e-12 and np.max(np.abs(np.diag(W_a) - 1)) < 1e-12 and np.linalg.eigvalsh(W_a)[0] >= -1e-8)
    feas += ok
    if ok and dW < dR:
        closer += 1
    margins.append(dR - dW)
    if dR_first is None:
        dR_first, dW_first, first_idx = dR, dW, idx
print("L09 non-PSD count", nonpsd, "W feasible", feas, "closer", closer)
print("L09 first non-PSD index", first_idx, "dR %.6f dW %.6f" % (dR_first, dW_first))
print("L09 min margin dR-dW over non-PSD:", min(margins))
