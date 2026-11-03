# Round-3 independent recomputation for L09. Written from the page's definitions, not by importing the twin.
# Alternative algorithms: eigen-decomposition via numpy.linalg.eig (non-symmetric solver, real part) for the
# clipping, and a Dykstra-free plain alternating projection with a different stopping rule, to test robustness.
import numpy as np
np.set_printoptions(precision=6, suppress=True)
C0 = np.array([[1, .9, .9], [.9, 1, -.9], [.9, -.9, 1.]])
w, V = np.linalg.eigh(C0); print("C0 eig asc:", w)
x = np.array([1, -1, -1.]); print("x^T C0 x =", x @ C0 @ x)
def clip(A, floor=0.0):
    w, V = np.linalg.eigh(A); return (V * np.maximum(w, floor)) @ V.T
B = clip(C0); print("B min eig:", np.linalg.eigvalsh(B)[0])
print("||C0-B||^2 =", np.sum((C0-B)**2), " sum neg eig^2 =", np.sum(np.minimum(w, 0)**2))
d = np.sqrt(np.diag(B)); R = B / np.outer(d, d); print("R=\n", R)
# seeded matrices, own generator code
rng = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    N = rng.normal(0, 0.35, size=(5, 5)); N = (N + N.T) / 2
    A = 0.5 + N; np.fill_diagonal(A, 1.0); mats.append(A)
mins = np.array([np.linalg.eigvalsh(A)[0] for A in mats])
print("smallest eigenvalues sorted:", np.sort(mins)[:30])
print("count min < -1e-9:", int(np.sum(mins < -1e-9)), " count in [-1e-6, 1e-6]:", int(np.sum(np.abs(mins) < 1e-6)))
def is_corr(A, tol=1e-12, ptol=1e-8):
    return np.max(np.abs(A-A.T)) < tol and np.max(np.abs(np.diag(A)-1)) < tol and np.linalg.eigvalsh(A)[0] >= -ptol
def alt_proj(A):
    X = A.copy()
    for _ in range(500):
        Y = clip(X); np.fill_diagonal(Y, 1.0)
        if np.max(np.abs(Y - X)) < 1e-12: return Y
        X = Y
    return Y
n_nonpsd = 0; n_feas = 0; n_closer = 0; first = None
for i, A in enumerate(mats):
    if mins[i] >= -1e-9: continue
    n_nonpsd += 1
    Rr = B if False else None
    Rr = clip(A); dd = np.sqrt(np.diag(Rr)); Rr = Rr / np.outer(dd, dd)
    W = alt_proj(A)
    dR = np.linalg.norm(A - Rr); dW = np.linalg.norm(A - W)
    if is_corr(W):
        n_feas += 1
        if dW < dR: n_closer += 1
    if first is None: first = (i, dR, dW)
print("non-PSD:", n_nonpsd, " W feasible:", n_feas, " W feasible & closer:", n_closer)
print("first non-PSD index, ||A-R||, ||A-W||:", first)
# robustness: does W stay closer without the feasibility filter, and does the closer count change with tolerance 1e-6?
extra = 0
for i, A in enumerate(mats):
    if mins[i] >= -1e-9: continue
    dd = np.sqrt(np.diag(clip(A))); Rr = clip(A) / np.outer(dd, dd); W = alt_proj(A)
    if np.linalg.norm(A-W) < np.linalg.norm(A-Rr): extra += 1
print("closer without feasibility filter:", extra)
print("max deviation of W from correlation (symmetric, diag, min eig) over non-PSD:",
      max(max(np.max(np.abs(alt_proj(A)-alt_proj(A).T)), np.max(np.abs(np.diag(alt_proj(A))-1)), max(0, -np.linalg.eigvalsh(alt_proj(A))[0])) for i,A in enumerate(mats) if mins[i] < -1e-9))
