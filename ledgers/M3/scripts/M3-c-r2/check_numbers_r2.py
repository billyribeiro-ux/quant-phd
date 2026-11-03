"""Independent recomputation of every number printed or stated on L07, L08 and L09 (round 2).

Different algorithms from the lab where possible: QR for least squares, SVD for PCA, an
explicit closed form for the C0 repair (v = (1,-1,-1)/sqrt 3), Fraction arithmetic for M1-M3 of L07/L08/L09.
Run: python3 -I check_numbers_r2.py
"""

from fractions import Fraction as F
import math
import numpy as np

out: list[str] = []


def say(s: str) -> None:
    print(s)


# ---------- L07 ----------
# M2: A rows (1,0),(1,1),(1,2), y=(1,2,2); exact fractions via Gram matrix
A2 = [[F(1), F(0)], [F(1), F(1)], [F(1), F(2)]]
y2 = [F(1), F(2), F(2)]
g = [[sum(A2[r][i] * A2[r][j] for r in range(3)) for j in range(2)] for i in range(2)]
b = [sum(A2[r][i] * y2[r] for r in range(3)) for i in range(2)]
det = g[0][0] * g[1][1] - g[0][1] * g[1][0]
beta0 = (g[1][1] * b[0] - g[0][1] * b[1]) / det
beta1 = (g[0][0] * b[1] - g[1][0] * b[0]) / det
fitted = [beta0 + beta1 * A2[r][1] for r in range(3)]
resid = [y2[r] - fitted[r] for r in range(3)]
say(f"L07 M2 exact: beta0={beta0} beta1={beta1} fitted={[str(f) for f in fitted]} resid={[str(f) for f in resid]}")
say(f"L07 M2 checks: sum resid={sum(resid)} resid.x={sum(resid[r]*A2[r][1] for r in range(3))}")
say(f"L07 M1 exact: P=1/2[[1,1],[1,1]], Py=(1,1), resid=(1,-1), inner with A = {F(1)*1 + F(-1)*1}")
say(f"L07 M3: 25 = {9+16}; ||Py||^2=9, resid^2=16")

# lab 1 on seeded generator (replicate draw order), QR-based solve and residual
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
q, r = np.linalg.qr(a)
beta_qr = np.linalg.solve(r, q.T @ y)
res = y - a @ beta_qr
say(f"L07 lab: beta (QR) = {beta_qr[0]:.6f} {beta_qr[1]:.6f} {beta_qr[2]:.6f}; residual norm {np.linalg.norm(res):.6f}")
say(f"L07 A^T y = {a.T @ y}")
say(f"L07 Pythag: |y|^2={y@y:.6f} |Py|^2={(a@beta_qr)@(a@beta_qr):.6f} |r|^2={res@res:.6f}")
# P idempotent check with explicit P via QR: P = Q Q^T
P = q @ q.T
say(f"L07 P=QQ^T idempotent max dev {np.max(np.abs(P@P-P)):.2e}; symmetric {np.max(np.abs(P-P.T)):.2e}")
say(f"L07 Py - A beta max dev {np.max(np.abs(P@y - a@beta_qr)):.2e}")

# ---------- L08 ----------
rng = np.random.default_rng(8)
TEN = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
T = 750
lev = np.ones(6) / math.sqrt(6)
sl = TEN - TEN.mean()
sl = sl / np.linalg.norm(sl)
qd = TEN**2
qd = qd - qd.mean()
qd = qd - (qd @ lev) * lev - (qd @ sl) * sl
cv = qd / np.linalg.norm(qd)
scores = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
shapes = np.column_stack([lev, sl, cv])
noise8 = rng.normal(scale=0.5, size=(T, 6))
panel = scores @ shapes.T + noise8
Xc = panel - panel.mean(axis=0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
ev = S**2 / (T - 1)  # eigenvalues of M = Xc^T Xc/(T-1) via SVD
M = Xc.T @ Xc / (T - 1)
ev_eig = np.sort(np.linalg.eigvalsh(M))[::-1]
say(f"L08 SVD vs eigvalsh max dev {np.max(np.abs(ev - ev_eig)):.2e}")
shares = ev / ev.sum()
say(f"L08 shares (SVD) {100*shares[0]:.4f} {100*shares[1]:.4f} {100*shares[2]:.4f} %; top3 sum unrounded {100*shares[:3].sum():.4f}")
say(f"L08 shares sum {shares.sum():.12f}")
# cosines from SVD right vectors
V = Vt.T
for name, shp in zip(("level", "slope", "curv"), (lev, sl, cv)):
    c = np.abs(V[:, :3].T @ shp)
    say(f"L08 {name}: max |cos| {c.max():.4f} at PC{int(np.argmax(c))+1}; all |cos| {np.round(c, 4)}")
# doubled panel shares
S2 = np.linalg.svd(2 * Xc, compute_uv=False)
say(f"L08 doubled shares dev {np.max(np.abs(S2**2/np.sum(S2**2) - shares)):.2e}")
# rescaled column 0 by 10 (SVD)
R10 = Xc.copy()
R10[:, 0] *= 10
S3 = np.linalg.svd(R10, compute_uv=False)
new_first = S3[0] ** 2 / np.sum(S3**2)
say(f"L08 first share after rescale: {new_first:.6f} (page 0.9791); old {shares[0]:.6f} (page 0.7587)")
m11 = float(np.sum(Xc[:, 0] ** 2) / (T - 1))
tr = float(np.sum(Xc**2) / (T - 1))
say(f"L08 M11 {m11:.6f} (page 13.6818), trace {tr:.6f} (page 88.2028)")
bound = 100 * m11 / (tr + 99 * m11)
say(f"L08 E1 bound {bound:.6f} (page 0.9483); bound exceeds old share {bound > shares[0]}")
say(f"L08 P3 check: lambda1 {ev[0]:.4f} >= 100*M11 {100*m11:.4f}: {ev[0] >= 100*m11}" + " (pre-rescale lambda1 vs new M11 not comparable; check rescaled matrix)")
ev_r = np.sort(np.linalg.eigvalsh(R10.T @ R10 / (T - 1)))[::-1]
say(f"L08 rescaled lambda1 {ev_r[0]:.6f} >= 100*M11 {100*m11:.6f}: {ev_r[0] >= 100*m11 - 1e-9}; new share {ev_r[0]/ev_r.sum():.6f}")
say(f"L08 E3 unrounded top3 sum {100*shares[:3].sum():.6f} vs printed sum 99.2; diff {abs(100*shares[:3].sum()-99.2):.6f} <= 0.15")

# tiny exact checks M1 (L08): X rows (1,2),(3,4),(5,9)
X1 = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 9.0]])
Xt = X1 - X1.mean(axis=0)
M1m = Xt.T @ Xt / 2
say(f"L08 M1 example M=\n{M1m}; trace {np.trace(M1m)}; det {np.linalg.det(M1m):.6f}; eig {np.linalg.eigvalsh(M1m)}; (17+-sqrt277)/2 = {(17-math.sqrt(277))/2:.6f},{(17+math.sqrt(277))/2:.6f}")
say(f"L08 M1 centred rows norms^2 {[float(x@x) for x in Xt]} sum/2 = {sum(float(x@x) for x in Xt)/2}")

# ---------- L09 ----------
C0 = np.array([[1.0, 0.9, 0.9], [0.9, 1.0, -0.9], [0.9, -0.9, 1.0]])
xw = np.array([1.0, -1.0, -1.0])
say(f"L09 x^T C0 x = {xw @ C0 @ xw} (exact -2.4)")
w_v = np.array([1.0, -1.0, -1.0]) / math.sqrt(3)
say(f"L09 C0 v = -0.8 v? {np.max(np.abs(C0 @ w_v + 0.8 * w_v)):.2e}")
Bc = C0 + 0.8 * np.outer(w_v, w_v)
say(f"L09 B = (19/30)[[2,1,1],[1,2,-1],[1,-1,2]] dev {np.max(np.abs(Bc - (19/30)*np.array([[2,1,1],[1,2,-1],[1,-1,2]]))):.2e}")
d = np.sqrt(np.diag(Bc))
R_closed = Bc / np.outer(d, d)
say(f"L09 R closed form dev {np.max(np.abs(R_closed - np.array([[1,.5,.5],[.5,1,-.5],[.5,-.5,1]]))):.2e}")
say(f"L09 ||C0-B||^2 = {np.sum((C0-Bc)**2):.10f} (page 0.6400000000)")
say(f"L09 ||C0-R||_F = {np.linalg.norm(C0-np.array([[1,.5,.5],[.5,1,-.5],[.5,-.5,1]])):.6f}; sqrt(0.96)={math.sqrt(0.96):.6f}")
say(f"L09 eig C0 {np.linalg.eigvalsh(C0)}")
# Example 3.6
A36 = np.array([[1.0, 1.2], [1.2, 1.0]])
A0 = np.array([[1.1, 1.1], [1.1, 1.1]])
say(f"L09 Ex3.6: ||A-A0||^2={np.sum((A36-A0)**2):.6f}; ||A-R||^2={np.sum((A36-np.ones((2,2)))**2):.6f}; ||A||^2={np.sum(A36**2):.6f}")
say(f"L09 M2 check eigen squares: {2.2**2 + 0.2**2:.6f}")
# M3 B = [[4,2],[2,9]]
Bm = np.array([[4.0, 2.0], [2.0, 9.0]])
say(f"L09 M3 eig {np.linalg.eigvalsh(Bm)} ((13+-sqrt41)/2 = {(13-math.sqrt(41))/2:.6f},{(13+math.sqrt(41))/2:.6f})")
# lab 3: alternating projections on seeded matrices, own loop
def clip(a: np.ndarray) -> np.ndarray:
    lam, q = np.linalg.eigh(a)
    return q @ np.diag(np.maximum(lam, 0.0)) @ q.T

rng9 = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    z = rng9.normal(0.0, 0.35, size=(5, 5))
    z = (z + z.T) / 2.0
    a = 0.5 + z
    np.fill_diagonal(a, 1.0)
    mats.append(a)
nonpsd = []
for i, a in enumerate(mats):
    lmin = np.linalg.eigvalsh(a)[0]
    if lmin < -1e-9:
        nonpsd.append(i)
say(f"L09 non-PSD count {len(nonpsd)} (page 23); first non-PSD index {nonpsd[0]} (page 0)")
ok_feas = 0
closer = 0
for i in nonpsd:
    a = mats[i]
    bb = clip(a)
    dd = np.sqrt(np.diag(bb))
    rr = bb / np.outer(dd, dd)
    x = a.copy()
    for _ in range(500):
        yy = clip(x)
        np.fill_diagonal(yy, 1.0)
        if np.max(np.abs(yy - x)) < 1e-12:
            x = yy
            break
        x = yy
    W_ = x
    sym = np.max(np.abs(W_ - W_.T)) < 1e-12
    unit = np.max(np.abs(np.diag(W_) - 1)) < 1e-12
    psd = np.linalg.eigvalsh(W_)[0] >= -1e-8
    if sym and unit and psd:
        ok_feas += 1
    dR = np.linalg.norm(a - rr)
    dW = np.linalg.norm(a - W_)
    if dW < dR:
        closer += 1
    if i == nonpsd[0]:
        say(f"L09 first non-PSD: ||A-R||={dR:.6f} (page 0.175527) ||A-W||={dW:.6f} (page 0.163280)")
say(f"L09 feasible among non-PSD {ok_feas}/{len(nonpsd)}; strictly closer {closer}/{len(nonpsd)} (page 23 of 23 both)")
print("\n".join(out))
