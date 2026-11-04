"""Round-5 independent recomputation (M3-c): every number quoted on L07, L08 and L09 from its own unrounded source.

Written by the verifier for round 5. Does not import the lab twins; re-derives each quantity from first principles
(explicit generator calls, explicit formulas). Run: .venv/bin/python -I ledgers/M3/scripts/M3-c-r5/m3c_r5_numbers.py
"""
import numpy as np

np.set_printoptions(precision=12)
print("== L07 (seed 7 design)")
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
aty = a.T @ y
print("A^T y unrounded:", aty, "-> 2dp:", [f"{v:.2f}" for v in aty])
beta = np.linalg.solve(a.T @ a, a.T @ y)
res = y - a @ beta
print("beta unrounded:", beta, "-> 4dp:", [f"{v:.4f}" for v in beta])
print("residual norm unrounded:", np.linalg.norm(res), "-> 4dp:", f"{np.linalg.norm(res):.4f}")

print("== L08 (seed 8 panel, independent construction)")
rng = np.random.default_rng(8)
T = 750
tenors = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])


def unit(v):
    return v / np.linalg.norm(v)


level = unit(np.ones(6))
slope = unit(tenors - tenors.mean())
q = tenors**2 - (tenors**2).mean()
q = q - (q @ level) * level - (q @ slope) * slope
curv = unit(q)
s1 = rng.normal(scale=8.0, size=T)
s2 = rng.normal(scale=4.0, size=T)
s3 = rng.normal(scale=2.0, size=T)
panel = np.column_stack([s1, s2, s3]) @ np.column_stack([level, slope, curv]).T + rng.normal(scale=0.5, size=(T, 6))
xc = panel - panel.mean(axis=0)
M = xc.T @ xc / (T - 1)
vals, vecs = np.linalg.eigh(M)
order = np.argsort(vals)[::-1]
lam = vals[order]
V = vecs[:, order]
shares = lam / lam.sum()
print("eigenvalues:", lam)
print("shares unrounded %:", 100 * shares)
print("shares 1dp %:", [f"{100*s:.1f}" for s in shares[:3]], " sum of printed three:", round(sum(round(100*s, 1) for s in shares[:3]), 1), " unrounded sum of three:", 100 * shares[:3].sum())
for name, shape in zip(("level", "slope", "curvature"), (level, slope, curv)):
    c = np.abs(V.T @ shape)
    srt = np.sort(c)[::-1]
    print(f"{name}: |cos| per PC {np.round(c, 6)}; max {srt[0]:.6f} at PC{int(np.argmax(c)) + 1}; runner-up {srt[1]:.6f}; gap {srt[0]-srt[1]:.6f}")
dbl = np.sort(np.linalg.eigvalsh(4 * M))[::-1]
print("doubled-panel shares equal:", np.max(np.abs(dbl / dbl.sum() - shares)))
r = panel.copy()
r[:, 0] *= 10.0
xr = r - r.mean(axis=0)
Mr = xr.T @ xr / (T - 1)
lr = np.sort(np.linalg.eigvalsh(Mr))[::-1]
print("first share before/after rescale:", f"{shares[0]:.10f}", f"{lr[0]/lr.sum():.10f}", "-> 4dp", f"{shares[0]:.4f}", f"{lr[0]/lr.sum():.4f}")
M11 = M[0, 0]
S0 = np.trace(M)
bound = 100 * M11 / (S0 + 99 * M11)
print("M11 unrounded:", M11, " trace unrounded:", S0, " bound unrounded:", bound, " bound 4dp:", f"{bound:.4f}")
print("bound from PRINTED inputs 13.6818, 88.2028:", 100 * 13.6818 / (88.2028 + 99 * 13.6818))
print("Lambda1 of rescaled >= 100*M11 (Prop 3.2/P3 check):", lr[0] >= 100 * M11 - 1e-12)

print("== L09 (C0, clipping, rescaling, seeded alternating projections)")
C0 = np.array([[1.0, 0.9, 0.9], [0.9, 1.0, -0.9], [0.9, -0.9, 1.0]])
x = np.array([1.0, -1.0, -1.0])
print("x^T C0 x =", x @ C0 @ x)
eig0, Q0 = np.linalg.eigh(C0)
print("eig C0:", eig0)
B = (Q0 * np.maximum(eig0, 0.0)) @ Q0.T
print("B:\n", B)
d = np.sqrt(np.diag(B))
R = B / np.outer(d, d)
print("R:\n", R)
print("||C0-B||^2:", np.sum((C0 - B) ** 2), " sum neg eig^2:", np.sum(np.minimum(eig0, 0) ** 2))
print("||C0-R||_F:", np.linalg.norm(C0 - R), " 4dp:", f"{np.linalg.norm(C0 - R):.4f}", " sqrt(0.96):", np.sqrt(0.96))

A2 = np.array([[1.0, 1.2], [1.2, 1.0]])
e2, Q2 = np.linalg.eigh(A2)
print("Example 3.6 eig:", e2)
A0 = (Q2 * np.maximum(e2, 0.0)) @ Q2.T
d2 = np.sqrt(np.diag(A0))
R2 = A0 / np.outer(d2, d2)
print("A0:", A0.tolist(), " R2:", R2.tolist())
print("||A-A0||^2:", np.sum((A2 - A0) ** 2), " ||A-R2||^2:", np.sum((A2 - R2) ** 2))
print("||A||_F^2:", np.sum(A2 ** 2))

ncount = 0
nfeas = 0
ncloser = 0
Ws = []
sr = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    z = sr.normal(0.0, 0.35, size=(5, 5))
    z = (z + z.T) / 2.0
    m = 0.5 + z
    np.fill_diagonal(m, 1.0)
    mats.append(m)


def clip(m):
    w, U = np.linalg.eigh(m)
    return (U * np.maximum(w, 0.0)) @ U.T


def alt(m):
    xx = m.copy()
    yy = xx
    for _ in range(500):
        yy = clip(xx)
        np.fill_diagonal(yy, 1.0)
        if np.max(np.abs(yy - xx)) < 1e-12:
            break
        xx = yy
    return yy, _


def is_corr(m):
    sym = np.max(np.abs(m - m.T)) < 1e-12
    unit = np.max(np.abs(np.diag(m) - 1.0)) < 1e-12
    psd = np.linalg.eigvalsh(m)[0] >= -1e-8
    return bool(sym and unit and psd)


min_eigs = []
for idx, m in enumerate(mats):
    smallest = np.linalg.eigvalsh(m)[0]
    min_eigs.append(smallest)
    if smallest >= -1e-9:
        continue
    ncount += 1
    dd = np.sqrt(np.diag(clip(m)))
    Rm = clip(m) / np.outer(dd, dd)
    Wm, iters = alt(m)
    dR = np.linalg.norm(m - Rm)
    dW = np.linalg.norm(m - Wm)
    ok = is_corr(Wm)
    if ok:
        nfeas += 1
        if dW < dR:
            ncloser += 1
    if ncount == 1:
        print(f"first non-PSD index {idx}: ||A-R||={dR:.6f} ||A-W||={dW:.6f} W steps={iters + 1}")
print("non-PSD count (min eig < -1e-9):", ncount, " of 40; PSD count:", 40 - ncount)
print("W passes is_correlation:", nfeas, " W passes and closer than R:", ncloser)
print("min eigenvalues of the 40 (sorted):", np.round(np.sort(min_eigs), 6))
print("closest-to-threshold non-PSD min eig:", max(e for e in min_eigs if e < -1e-9), " closest PSD min eig:", min(e for e in min_eigs if e >= -1e-9))
