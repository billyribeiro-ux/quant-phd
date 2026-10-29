import numpy as np

# ---- L07 E2: A^T y for the seeded lab response
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n); noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
print("L07 A^T y =", np.round(a.T @ y, 4), "(page claims approx (18.38, 3.10, -17.60))")
q, r = np.linalg.qr(a)
beta_qr = np.linalg.solve(r, q.T @ y)
print("L07 beta via QR:", np.round(beta_qr, 6), "residual norm:", round(float(np.linalg.norm(y - a @ beta_qr)), 6))

# ---- L08 independent re-derivation (SVD of centred panel; different algorithm from eigh)
TEN = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
def unit(v): return v / np.linalg.norm(v)
lev = unit(np.ones(6)); slo = unit(TEN - TEN.mean())
q2 = TEN**2 - (TEN**2).mean(); q2 = q2 - (q2 @ lev) * lev - (q2 @ slo) * slo; cur = unit(q2)
rng = np.random.default_rng(8)
T = 750
sc = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
panel = sc @ np.column_stack([lev, slo, cur]).T + rng.normal(scale=0.5, size=(T, 6))
xc = panel - panel.mean(0)
_, s, vt = np.linalg.svd(xc, full_matrices=False)
ev = s**2 / (T - 1)
shares = ev / ev.sum()
print("L08 SVD shares % :", np.round(100 * shares[:3], 4), "(page: 75.9 18.1 5.2)")
V = vt.T
for nm, sh in zip(("level", "slope", "curv"), (lev, slo, cur)):
    c = np.abs(V[:, :3].T @ sh)
    print("L08 cos", nm, np.round(c, 6))
p2 = panel * 2.0
s2 = np.linalg.svd(p2 - p2.mean(0), compute_uv=False)
print("L08 doubled shares equal:", np.allclose(s2**2 / (s2**2).sum(), shares, atol=1e-9))
r3 = panel.copy(); r3[:, 0] *= 10
s3 = np.linalg.svd(r3 - r3.mean(0), compute_uv=False)**2
print("L08 rescaled first share:", round(float(s3[0] / s3.sum()), 6), "(page 0.9791); old", round(float(shares[0]), 6))
M = xc.T @ xc / (T - 1)
print("L08 M11, trace:", round(float(M[0, 0]), 6), round(float(np.trace(M)), 6))
M11 = M[0, 0]; S0 = np.trace(M)
print("L08 bound 100M11/(S0+99M11):", round(float(100 * M11 / (S0 + 99 * M11)), 6), "(page 0.9483)")
print("L08 sum of printed top3 shares 75.9+18.1+5.2 =", round(75.9 + 18.1 + 5.2, 4))
