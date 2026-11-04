"""Round-5 verifier: independent recomputation of the L09 seeded-count numbers and card values (own code, numpy only)."""
import numpy as np

SEED, N, SIZE = 20261028, 40, 5
rng = np.random.default_rng(SEED)
mats = []
for _ in range(N):
    noise = rng.normal(0.0, 0.35, size=(SIZE, SIZE))
    noise = (noise + noise.T) / 2.0
    a = 0.5 + noise
    np.fill_diagonal(a, 1.0)
    mats.append(a)

def clip0(a):
    w, v = np.linalg.eigh(a)
    return (v * np.maximum(w, 0.0)) @ v.T

def rescale(b):
    d = np.sqrt(np.diag(b))
    return b / np.outer(d, d)

def alt(a):
    x = a.copy()
    y = x
    for _ in range(500):
        y = clip0(x)
        np.fill_diagonal(y, 1.0)
        if np.max(np.abs(y - x)) < 1e-12:
            break
        x = y
    return y

def is_corr(a):
    return bool(np.max(np.abs(a - a.T)) < 1e-12 and np.max(np.abs(np.diag(a) - 1)) < 1e-12 and np.linalg.eigvalsh(a)[0] >= -1e-8)

nonpsd_idx = [i for i, a in enumerate(mats) if np.linalg.eigvalsh(a)[0] < -1e-9]
print("count smallest eig < -1e-9:", len(nonpsd_idx), "first index:", nonpsd_idx[0] if nonpsd_idx else None)
feas = 0
closer = 0
for i in nonpsd_idx:
    a = mats[i]
    R = rescale(clip0(a))
    W = alt(a)
    if is_corr(W):
        feas += 1
        if np.linalg.norm(a - W) < np.linalg.norm(a - R):
            closer += 1
print("W passes is_correlation:", feas, "of", len(nonpsd_idx), "| W closer than R:", closer)
a = mats[nonpsd_idx[0]]
R = rescale(clip0(a))
W = alt(a)
print(f"index {nonpsd_idx[0]}: ||A-R||={np.linalg.norm(a-R):.6f}  ||A-W||={np.linalg.norm(a-W):.6f}")
print("min eig of mats[idx0]:", f"{np.linalg.eigvalsh(a)[0]:.6f}")
