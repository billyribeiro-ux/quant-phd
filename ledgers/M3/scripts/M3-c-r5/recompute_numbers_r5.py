"""Round 5 verifier script (M3-c): independent recomputation of the numbers quoted on L07, L08 and L09.
Written by the verifier; it does not import the lab twins. Run with python -I."""
import numpy as np

print("== L07 E2: A^T y for the seeded design (beta = 0 residual = y)")
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
print("A^T y =", np.round(a.T @ y, 4), "unrounded:", a.T @ y)
g = a.T @ a
beta = np.linalg.solve(g, a.T @ y)
print("beta unrounded:", beta, "residual norm:", np.linalg.norm(y - a @ beta))
print("normal eq residual max:", np.max(np.abs(a.T @ (y - a @ beta))))

print("== L08 unrounded shares, cosines, bound")
rng = np.random.default_rng(8)
T = 750
tenors = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
def unit(v): return v / np.linalg.norm(v)
level = unit(np.ones(6))
slope = unit(tenors - tenors.mean())
quad = tenors**2 - (tenors**2).mean()
quad = quad - (quad @ level) * level - (quad @ slope) * slope
curv = unit(quad)
scores = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
shapes = np.column_stack([level, slope, curv])
noise = rng.normal(scale=0.5, size=(T, 6))
panel = scores @ shapes.T + noise
xc = panel - panel.mean(axis=0)
m = xc.T @ xc / (T - 1)
vals, vecs = np.linalg.eigh(m)
o = np.argsort(vals)[::-1]
lam = vals[o]; v = vecs[:, o]
shares = lam / lam.sum()
print("shares % unrounded:", 100 * shares[:3])
print("sum of 3 unrounded shares %:", 100 * shares[:3].sum())
for name, s in zip(("level", "slope", "curv"), (level, slope, curv)):
    c = np.abs(v[:, :3].T @ s)
    print(name, "cosines unrounded:", c, "best", np.argmax(c) + 1, c.max())
M11 = m[0, 0]; tr = np.trace(m)
print("M11 unrounded", M11, "trace unrounded", tr)
print("bound unrounded", 100 * M11 / (tr + 99 * M11))
print("bound with printed inputs", 100 * 13.6818 / (88.2028 + 99 * 13.6818))
mr = m.copy()
panel2 = panel.copy(); panel2[:, 0] *= 10.0
xc2 = panel2 - panel2.mean(axis=0)
m2 = xc2.T @ xc2 / (T - 1)
l2 = np.sort(np.linalg.eigvalsh(m2))[::-1]
print("rescaled first share unrounded", l2[0] / l2.sum(), "old first share", shares[0])

print("== L09 seeded matrices and C0")
c0 = np.array([[1, .9, .9], [.9, 1, -.9], [.9, -.9, 1.]])
print("C0 eig", np.linalg.eigvalsh(c0))
w, q = np.linalg.eigh(c0)
b = (q * np.maximum(w, 0)) @ q.T
print("||C0-B||^2", np.sum((c0 - b) ** 2), "neg sum", np.sum(np.minimum(w, 0) ** 2))
def clip(a): 
    l, qq = np.linalg.eigh(a); return (qq * np.maximum(l, 0)) @ qq.T
def resc(bb):
    d = np.sqrt(np.diag(bb)); return bb / np.outer(d, d)
def altp(a):
    x = a.copy()
    for _ in range(500):
        y = clip(x); np.fill_diagonal(y, 1.0)
        if np.max(np.abs(y - x)) < 1e-12: break
        x = y
    return y
rng = np.random.default_rng(20261028)
nonpsd = feas = closer = 0
for idx in range(40):
    nz = rng.normal(0, 0.35, size=(5, 5)); nz = (nz + nz.T) / 2
    A = 0.5 + nz; np.fill_diagonal(A, 1.0)
    lmin = np.linalg.eigvalsh(A)[0]
    if lmin >= -1e-9: continue
    nonpsd += 1
    R = resc(clip(A)); W = altp(A)
    ok = np.max(np.abs(W - W.T)) < 1e-12 and np.max(np.abs(np.diag(W) - 1)) < 1e-12 and np.linalg.eigvalsh(W)[0] >= -1e-8
    feas += bool(ok)
    dR = np.linalg.norm(A - R); dW = np.linalg.norm(A - W)
    closer += bool(dW < dR)
    if nonpsd == 1: print("first nonpsd idx", idx, "dR", dR, "dW", dW)
print("nonpsd", nonpsd, "feasible", feas, "closer", closer)
print("E2 ||C0-R||", np.linalg.norm(c0 - np.array([[1, .5, .5], [.5, 1, -.5], [.5, -.5, 1.]])), np.sqrt(0.96))
