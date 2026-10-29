import numpy as np
C = np.array([[1.0,0.7,0.3,-0.6],[0.7,1.0,0.5,0.4],[0.3,0.5,1.0,0.2],[-0.6,0.4,0.2,1.0]])
v = np.array([0.10,0.20,0.15,0.30])
w_, V = np.linalg.eigh(C)
print("eigs", np.round(w_,6))
X = V @ np.diag(np.maximum(w_,0)) @ V.T
d = np.diag(X)
Y = X / np.sqrt(np.outer(d,d))
dist_clip = np.linalg.norm(Y-C)
# true nearest PSD unit-diag via Higham alternating projections with tight tolerance (independent of the lab code)
def proj_psd(A):
    e,U = np.linalg.eigh((A+A.T)/2); return U@np.diag(np.maximum(e,0))@U.T
Yk = C.copy(); dS = np.zeros_like(C); dU = np.zeros_like(C)
for _ in range(20000):
    R = proj_psd(Yk - dS); dS = R - (Yk - dS)  # Dykstra
    Z = R + dU; Yn = Z.copy(); np.fill_diagonal(Yn, 1.0); dU = Z - Yn
    if np.linalg.norm(Yn-Yk) < 1e-14: Yk = Yn; break
    Yk = Yn
dist_proj = np.linalg.norm(Yk-C)
print("dist_clip %.9f dist_proj_dykstra %.9f gap %.9f" % (dist_clip, dist_proj, dist_clip-dist_proj))
print("max entry diff %.9f" % np.max(np.abs(Yk-Y)))
print("min eig proj", np.linalg.eigvalsh(Yk).min())
print("det", np.linalg.det(C))
Sig = np.diag(v) @ C @ np.diag(v)
u = np.linalg.solve(Sig, np.ones(4)); print("weights", np.round(u/u.sum(),6), "sum", (u/u.sum()).sum())
print("clip X singular: min|eig X|", np.linalg.eigvalsh(X).min())
