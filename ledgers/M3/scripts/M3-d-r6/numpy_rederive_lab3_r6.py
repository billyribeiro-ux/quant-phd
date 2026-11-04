"""Round-6 verifier: independent NumPy re-derivation of the Lab 3 numbers (not the lab's code)."""
import numpy as np

C = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
v = np.array([0.10, 0.20, 0.15, 0.30])
w, V = np.linalg.eigh(C)
print("eig", np.round(w, 6), "min", f"{w.min():.6f}")
X = V @ np.diag(np.maximum(w, 0)) @ V.T
d = np.diag(X)
Y = X / np.sqrt(np.outer(d, d))
print("clip Y diag dev", f"{np.abs(np.diag(Y) - 1).max():.2e}", "min eig Y", f"{np.linalg.eigvalsh(Y).min():.3e}")
dist_clip = np.linalg.norm(Y - C, "fro")
# Dykstra with high iteration budget, independent formulation (Higham 2002 style)
def proj_psd(A):
    ww, VV = np.linalg.eigh((A + A.T) / 2)
    return VV @ np.diag(np.maximum(ww, 0)) @ VV.T
def dykstra(A, iters=20000):
    x = A.copy(); dS = np.zeros_like(A); dU = np.zeros_like(A)
    for _ in range(iters):
        y = proj_psd(x + dS); dS = x + dS - y
        x2 = y + dU; np.fill_diagonal(x2, 1.0); dU = y + dU - x2
        x = x2
    return x
P = dykstra(C)
dist_proj = np.linalg.norm(P - C, "fro")
print("dist clip", f"{dist_clip:.6f}", "dist proj", f"{dist_proj:.6f}", "gap", f"{dist_clip - dist_proj:.6f}")
print("max abs entry diff", f"{np.abs(P - Y).max():.6f}")
print("min eig P", f"{np.linalg.eigvalsh(P).min():.3e}", "diag dev P", f"{np.abs(np.diag(P)-1).max():.2e}")
print("det C", f"{np.linalg.det(C):.6f}")
S = np.diag(v); Sig = S @ C @ S
u = np.linalg.solve(Sig, np.ones(4)); wt = u / u.sum()
print("weights input", " ".join(f"{x:.6f}" for x in wt), "sum", f"{wt.sum():.6f}")
print("cond Sigma input", f"{np.linalg.cond(Sig):.3e}")
for name, M in (("clip Y", Y), ("proj P", P)):
    Sg = S @ M @ S
    print(name, "min eig Sigma", f"{np.linalg.eigvalsh(Sg).min():.3e}", "cond", f"{np.linalg.cond(Sg):.3e}")
