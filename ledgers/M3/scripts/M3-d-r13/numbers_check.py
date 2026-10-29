import numpy as np
from math import sqrt
def psd_proj(a):
    w, v = np.linalg.eigh(a); return v @ np.diag(np.maximum(w, 0)) @ v.T
def clip(a):
    x = psd_proj(a); d = np.diag(x); return x / np.sqrt(np.outer(d, d))
def dyk(a, tol=1e-12, it=5000):
    x = a.copy(); n = len(a); S = np.zeros_like(a); U = np.zeros_like(a)
    for _ in range(it):
        y = psd_proj(x + S); S = x + S - y
        nx = y + U; np.fill_diagonal(nx, 1.0); U = y + U - nx
        g = np.linalg.norm(nx - y); st = np.linalg.norm(nx - x); x = nx
        if g <= tol and st <= tol: break
    return x
C = np.array([[1.0,0.7,0.3,-0.6],[0.7,1.0,0.5,0.4],[0.3,0.5,1.0,0.2],[-0.6,0.4,0.2,1.0]])
v = np.array([0.10,0.20,0.15,0.30])
print("min eig", np.linalg.eigvalsh(C).min())
c = clip(C); p = dyk(C)
dc = np.linalg.norm(c-C); dp = np.linalg.norm(p-C)
print("dist clip %.6f proj %.6f gap %.6f" % (dc, dp, dc-dp))
print("max entry diff %.6f" % np.abs(p-c).max())
print("max diag dev clip %.3g proj %.3g" % (np.abs(np.diag(c)-1).max(), np.abs(np.diag(p)-1).max()))
print("min eig proj %.3g" % np.linalg.eigvalsh(p).min())
print("det %.6f" % np.linalg.det(C))
Sg = np.diag(v) @ C @ np.diag(v); one = np.ones(4)
w = np.linalg.solve(Sg, one); w = w / w.sum(); print("weights", np.round(w,6), w.sum())
print("eig of clip X min (raw clipped before rescale):")
ww, vv = np.linalg.eigh(C); X = vv @ np.diag(np.maximum(ww,0)) @ vv.T
print("X diag", np.diag(X), "det X", np.linalg.det(X))
print("eig of clip Y", np.linalg.eigvalsh(c))
