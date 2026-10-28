"""Independent NumPy recomputation of Lab 3 printed numbers, Lab 1 and Lab 2 values, and A3 closed form."""
import numpy as np

def clip(a):
    w, v = np.linalg.eigh(a)
    x = v @ np.diag(np.maximum(w, 0)) @ v.T
    d = np.sqrt(np.diag(x))
    return x / np.outer(d, d)

def project_higham(a, iters=20000):
    # Higham alternating projections (Dykstra-free), used only as a cross-check of the nearest PSD unit-diagonal matrix
    y = a.copy()
    ds = np.zeros_like(a)
    for _ in range(iters):
        r = y - ds
        w, v = np.linalg.eigh(r)
        x = v @ np.diag(np.maximum(w, 0)) @ v.T
        ds = x - r
        y = x.copy()
        np.fill_diagonal(y, 1.0)
    return y

c = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
vols = np.array([0.10, 0.20, 0.15, 0.30])
print("min eig", np.linalg.eigvalsh(c).min())
cl = clip(c)
pr = project_higham(c)
dc = np.linalg.norm(cl - c)
dp = np.linalg.norm(pr - c)
print("dist clip %.9f" % dc, "dist proj(higham) %.9f" % dp, "gap %.9f" % (dc - dp))
print("max entry diff %.9f" % np.abs(pr - cl).max())
print("min eig of higham proj %.3e" % np.linalg.eigvalsh(pr).min())
print("det", np.linalg.det(c))
s = np.diag(vols) @ c @ np.diag(vols)
w = np.linalg.solve(s, np.ones(4))
w = w / w.sum()
print("weights", w, w.sum())
# A3 closed form check for a random 2-asset case
rng = np.random.default_rng(1)
for _ in range(5):
    rho = rng.uniform(-0.99, 0.99); a, b = rng.uniform(0.05, 2, 2)
    sig = np.array([[a*a, rho*a*b], [rho*a*b, b*b]])
    ww = np.linalg.solve(sig, np.ones(2)); ww /= ww.sum()
    cf = np.array([b*(b-rho*a), a*(a-rho*b)]) / (a*a+b*b-2*rho*a*b)
    assert np.allclose(ww, cf), (ww, cf)
print("A3 closed form matches on 5 random cases")
l1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
w1, v1 = np.linalg.eigh(l1)
print("lab1 eig", w1, "clip rows", clip(l1))
l2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
print("lab2 eig", np.linalg.eigvalsh(l2), "clip", clip(l2))
