# Round-3 independent recomputation for L08 (does not import the twin). Uses SVD of the centred panel as a second route.
import numpy as np
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0]); T = 750
def unit(v): return v / np.linalg.norm(v)
level = unit(np.ones(6)); slope = unit(TENORS - TENORS.mean())
q = TENORS**2 - (TENORS**2).mean()
q = q - (q @ level) * level - (q @ slope) * slope
curv = unit(q)
S = np.vstack([level, slope, curv])
print("orthonormal shapes, Gram max dev:", np.max(np.abs(S @ S.T - np.eye(3))))
rng = np.random.default_rng(8)
sc = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
noise = rng.normal(scale=0.5, size=(T, 6))
X = sc @ S + noise
Xc = X - X.mean(axis=0)
M = Xc.T @ Xc / (T - 1)
w, V = np.linalg.eigh(M); o = np.argsort(w)[::-1]; lam = w[o]; V = V[:, o]
# second route: SVD of centred data, eigenvalues = s^2/(T-1)
_, s, Vt = np.linalg.svd(Xc, full_matrices=False)
print("eig via SVD agrees:", np.max(np.abs(np.sort(s**2/(T-1))[::-1] - lam)))
sh = lam / lam.sum()
print("unrounded shares:", sh[:3], "percent:", 100*sh[:3])
print("printed percent (1dp):", [f"{100*x:.1f}" for x in sh[:3]], "sum printed:", sum(float(f"{100*x:.1f}") for x in sh[:6]) )
print("sum of top-3 printed:", round(sum(float(f"{100*x:.1f}") for x in sh[:3]),1))
print("all-six argmax |cos| per planted shape:")
for name, f in zip(("level","slope","curv"), S):
    c = np.abs(V.T @ f)
    print(f"  {name}: argmax over all six = PC{int(np.argmax(c))+1} |cos|={c.max():.4f}; top3 cosines={np.round(c[:3],4)}; all six={np.round(c,4)}")
M11 = M[0,0]; S0 = np.trace(M)
print("M11 =", M11, " trace =", S0)
print("E1 bound 100*M11/(S0+99*M11) =", 100*M11/(S0+99*M11))
Xr = X.copy(); Xr[:,0] *= 10; Xrc = Xr - Xr.mean(axis=0)
Mr = Xrc.T @ Xrc/(T-1); lr = np.sort(np.linalg.eigvalsh(Mr))[::-1]
print("first share before 0.7587-ish:", sh[0], " after:", lr[0]/lr.sum(), " bound <= after:", 100*M11/(S0+99*M11) <= lr[0]/lr.sum())
print("E3 check: printed-sum range for unrounded sum:", 100*sh[:3].sum(), "vs printed 99.2")
print("doubled shares equal:", np.max(np.abs(np.sort(np.linalg.eigvalsh(4*M))[::-1]/np.sum(4*lam) - sh)) if False else np.max(np.abs(np.linalg.eigvalsh(4*M)[::-1]/np.linalg.eigvalsh(4*M).sum() - np.linalg.eigvalsh(M)[::-1]/np.linalg.eigvalsh(M).sum())))
