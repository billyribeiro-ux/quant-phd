import numpy as np
rng = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    nz = rng.normal(0.0, 0.35, size=(5, 5)); nz = (nz + nz.T) / 2.0
    a = 0.5 + nz; np.fill_diagonal(a, 1.0); mats.append(a)

def clip_svd(a, floor=0.0):
    # alternative algorithm: eigen-decomposition via SVD of symmetric matrix (U diag s V^T); for PSD-ish use sign
    w, v = np.linalg.eigh(a)
    return (v * np.maximum(w, floor)) @ v.T
def clip_alt(a):
    w, v = np.linalg.eigh(a)
    w = np.where(w < 0, 0.0, w)
    return v @ np.diag(w) @ v.T
def rescale(b):
    d = 1 / np.sqrt(np.diag(b)); return b * np.outer(d, d)
def altproj(a, tol=1e-12, maxit=500, clip=clip_svd):
    x = a.copy(); y = x
    for _ in range(maxit):
        y = clip(x); np.fill_diagonal(y, 1.0)
        if np.max(np.abs(y - x)) < tol: break
        x = y
    return y
def is_corr(a):
    return np.max(np.abs(a - a.T)) < 1e-12 and np.max(np.abs(np.diag(a) - 1)) < 1e-12 and np.linalg.eigvalsh(a)[0] >= -1e-8

c0 = np.array([[1, .9, .9], [.9, 1, -.9], [.9, -.9, 1.]])
print("C0 eig", np.round(np.linalg.eigvalsh(c0), 6))
B = clip_svd(c0); R = rescale(B); print("R:\n", np.round(R, 4))
print("||C0-R||_F =", round(float(np.linalg.norm(c0 - R)), 6))

mins = []; nonpsd = []; closer = []; feas = []; margins = []
for i, a in enumerate(mats):
    lmin = np.linalg.eigvalsh(a)[0]; mins.append(lmin)
    if lmin >= -1e-9: continue
    nonpsd.append(i)
    r = rescale(clip_svd(a)); w = altproj(a); w2 = altproj(a, clip=clip_alt)
    dr = np.linalg.norm(a - r); dw = np.linalg.norm(a - w); dw2 = np.linalg.norm(a - w2)
    closer.append(dw < dr); feas.append(is_corr(w)); margins.append((dr - dw, dr - dw2, i))
    if i == 0: print("index0 dR", round(dr, 6), "dW", round(dw, 6), "dW(alt clip)", round(dw2, 6))
print("nonPSD count", len(nonpsd), "of 40")
print("feasible W", sum(feas), "closer", sum(closer))
mins = np.array(mins)
near = [(i, round(m, 12)) for i, m in enumerate(mins) if -1e-6 < m < 1e-6]
print("eigenvalues within 1e-6 of zero (boundary cases):", near)
print("min margin dR-dW over nonPSD (svd clip):", round(min(m[0] for m in margins), 8), "(alt clip):", round(min(m[1] for m in margins), 8))
print("min eigenvalue over all 40:", round(float(mins.min()), 6))
