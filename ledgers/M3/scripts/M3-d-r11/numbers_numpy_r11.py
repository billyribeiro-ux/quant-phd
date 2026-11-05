import numpy as np
np.set_printoptions(precision=6, suppress=True)

def psd_part(m):
    w, v = np.linalg.eigh(m)
    return (v * np.maximum(w, 0.0)) @ v.T

def clip_rescale(m, floor=0.0):
    w, v = np.linalg.eigh(m)
    x = (v * np.maximum(w, floor)) @ v.T
    d = np.diag(x).copy()
    return x / np.sqrt(np.outer(d, d)), x

def proj(m, iters=100000, tol=1e-14):
    x = m.copy(); n = len(m)
    cs = np.zeros((n, n)); cu = np.zeros((n, n))
    for _ in range(iters):
        y = psd_part(x + cs)
        cs = x + cs - y
        nx = y + cu
        np.fill_diagonal(nx, 1.0)
        cu = y + cu - nx
        gap = np.linalg.norm(nx - y); step = np.linalg.norm(nx - x)
        x = nx
        if gap <= tol and step <= tol:
            break
    return x

print("== Lab 1 (eigenvalues, clip)")
c1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
print(np.linalg.eigvalsh(c1))
r1, x1 = clip_rescale(c1)
print("rebuilt diag", np.diag(x1)); print(r1); print("dev", np.max(np.abs(np.diag(r1)-1)))
print("== Lab 2 matrix")
c2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
print(np.linalg.eigvalsh(c2))
r2, x2 = clip_rescale(c2)
print("rebuilt diag", np.diag(x2)); print(r2)
print("== Lab 3")
c3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
vols = np.array([0.10, 0.20, 0.15, 0.30])
print("eig input", np.linalg.eigvalsh(c3))
clip, xc = clip_rescale(c3)
print("clipped X diag (rebuilt):", np.diag(xc))
print("clip diag", np.diag(clip))
pr = proj(c3)
dc = np.linalg.norm(clip - c3); dp = np.linalg.norm(pr - c3)
print("dist clip %.6f proj %.6f gap %.6f" % (dc, dp, dc - dp))
print("max abs entry diff %.6f" % np.max(np.abs(pr - clip)))
print("eig clip", np.linalg.eigvalsh(clip)); print("eig proj", np.linalg.eigvalsh(pr))
print("max diag dev clip %.3g proj %.3g" % (np.max(np.abs(np.diag(clip)-1)), np.max(np.abs(np.diag(pr)-1))))
print("det input %.6f" % np.linalg.det(c3))
S = np.diag(vols); sig = S @ c3 @ S
w = np.linalg.solve(sig, np.ones(4)); w = w / w.sum()
print("weights", w, w.sum())
sig_proj = S @ pr @ S
print("cond sigma_proj", np.linalg.cond(sig_proj), "min eig sigma_proj", np.linalg.eigvalsh(sig_proj)[0])
print("A3-type check: 2-asset closed form examples skipped")
print("Y singular check: det clip %.3e" % np.linalg.det(clip))
print("nearest-like check: proj dist %.9f vs clip %.9f" % (dp, dc))
