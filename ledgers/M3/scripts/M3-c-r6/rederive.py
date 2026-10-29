"""Independent re-derivation of L07-L09 numbers (verifier round 6, slice c)."""
import numpy as np
from fractions import Fraction

# ---- L07 lab 1 (seed 7) re-derived independently
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
beta = np.linalg.solve(a.T @ a, a.T @ y)
res = y - a @ beta
print("L07 A^T y =", np.round(a.T @ y, 4).tolist())
print("L07 beta =", np.round(beta, 6).tolist(), "resid norm =", round(float(np.linalg.norm(res)), 6))
print("L07 E2 check: max|A^T y| =", float(np.max(np.abs(a.T @ y))))

# ---- L07 hand problems with exact fractions
A = np.array([[1, 1]], dtype=float).T
print("L07 M2 beta via fractions: b1=1/2, b0=7/6 ->", 7/6, 0.5)
print("L07 quiz 1.1667 vs 7/6 =", round(7/6, 4))

# ---- L08 lab (seed 8) re-derived
def unit(v): return v / np.linalg.norm(v)
TEN = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
T = 750
rng = np.random.default_rng(8)
lv = unit(np.ones(6)); sl = unit(TEN - TEN.mean())
q = TEN**2; q = q - q.mean(); q = q - (q @ lv) * lv - (q @ sl) * sl; cv = unit(q)
scores = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
panel = scores @ np.column_stack([lv, sl, cv]).T + rng.normal(scale=0.5, size=(T, 6))
xc = panel - panel.mean(axis=0)
m = xc.T @ xc / (T - 1)
lam, V = np.linalg.eigh(m)
o = np.argsort(lam)[::-1]; lam = lam[o]; V = V[:, o]
sh = lam / lam.sum()
print("L08 shares % (unrounded):", (100 * sh[:3]).tolist(), "sum top3 =", float(100 * sh[:3].sum()))
for name, s in zip(("level", "slope", "curv"), (lv, sl, cv)):
    c = np.abs(V[:, :3].T @ s)
    print("L08 cos", name, c.tolist(), "max", float(c.max()), "argmax", int(c.argmax()) + 1)
m11 = m[0, 0]; tr = np.trace(m)
print("L08 M11 =", m11, "trace =", tr, "bound =", 100 * m11 / (tr + 99 * m11))
p2 = panel * 2
l2 = np.linalg.eigvalsh(((p2 - p2.mean(0)).T @ (p2 - p2.mean(0))) / (T - 1))[::-1]
print("L08 doubled shares diff max:", float(np.max(np.abs(l2 / l2.sum() - sh))))
r = panel.copy(); r[:, 0] *= 10
lr = np.linalg.eigvalsh(((r - r.mean(0)).T @ (r - r.mean(0))) / (T - 1))[::-1]
print("L08 rescaled first share:", float(lr[0] / lr.sum()), "before", float(sh[0]))
# unit check on M2 (diag 4,1,1) and M1 worked example
X = np.array([[1, 2], [3, 4], [5, 9]], dtype=float); Xc = X - X.mean(0); M1 = Xc.T @ Xc / 2
print("L08 M1 example M =", M1.tolist(), "eig", np.linalg.eigvalsh(M1).tolist(), "sqrt277", np.sqrt(277))

# ---- L09 re-derived
C0 = np.array([[1, .9, .9], [.9, 1, -.9], [.9, -.9, 1.]])
x = np.array([1., -1, -1]); print("L09 quad", float(x @ C0 @ x), "eig", np.linalg.eigvalsh(C0).tolist())
def clip(A, f=0.0):
    w, Q = np.linalg.eigh(A); return (Q * np.maximum(w, f)) @ Q.T
def resc(B):
    d = np.sqrt(np.diag(B)); return B / np.outer(d, d)
R = resc(clip(C0))
print("L09 R =", np.round(R, 6).tolist(), "||C0-R||=", float(np.linalg.norm(C0 - R)), "sqrt .96", np.sqrt(0.96))
A2 = np.array([[1, 1.2], [1.2, 1]]); R2 = resc(clip(A2))
print("L09 Ex3.6 ||A-R||^2 =", float(np.sum((A2 - R2) ** 2)), "||A-A0||^2 =", float(np.sum((A2 - clip(A2)) ** 2)))
print("L09 M2 ||A||_F^2 =", float(np.sum(A2 ** 2)))
B = np.array([[4., 2], [2, 9]]); print("L09 M3 C =", resc(B).tolist(), "eig B", np.linalg.eigvalsh(B).tolist())
