"""Independent recomputation (round 4, slice M3-c) of the printed or prose numbers in L07, L08 and L09.
Run as: .venv/bin/python -I ledgers/M3/scripts/M3-c-r4/recheck_numbers_r4.py"""
import numpy as np

print("== L07 E2: A^T y for the seeded design (seed 7), zero-coefficient residual")
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
aty = a.T @ y
print("A^T y =", aty, " to 2 decimals:", [f"{v:.2f}" for v in aty])
g = a.T @ a
beta = np.linalg.solve(g, a.T @ y)
print("beta", beta, "residual norm", np.linalg.norm(y - a @ beta))
print("max|A^T r| at normal-eq beta:", np.max(np.abs(a.T @ (y - a @ beta))))

print("== L08 unrounded quantities (seed 8 panel)")
import importlib.util
spec = importlib.util.spec_from_file_location("l08", "/tmp/verifyB4-M3-c/tests/labs/M3/lab-M3-L08-1.py")
src = open("/tmp/verifyB4-M3-c/tests/labs/M3/lab-M3-L08-1.py").read().replace("\nmain()", "\n")
ns = {"__name__": "x"}
exec(compile(src, "l08", "exec"), ns)
TENORS = ns["TENORS"]
rng = np.random.default_rng(8)
panel = ns["simulate_panel"](rng)
T = panel.shape[0]
xc = panel - panel.mean(axis=0)
M = xc.T @ xc / (T - 1)
w, V = np.linalg.eigh(M)
order = np.argsort(w)[::-1]
lam = w[order]
V = V[:, order]
shares = lam / lam.sum()
print("eigenvalues", lam)
print("unrounded shares (%)", 100 * shares)
print("PC1..3 shares to 1dp:", [f"{100*s:.1f}" for s in shares[:3]], "sum of the three unrounded:", 100 * shares[:3].sum())
level, slope, curv = ns["planted_shapes"]()
cos_all = {}
for name, f in zip(("level", "slope", "curv"), (level, slope, curv)):
    c = np.abs(V[:, :3].T @ f)
    cos_all[name] = c
    print(name, "abs cosines to PC1..3 (unrounded):", c, "best", int(np.argmax(c)) + 1, "best value", c.max())
mins = min(cos_all[k].max() for k in cos_all)
print("minimum over the three planted shapes of best |cosine| (unrounded):", repr(mins))
print("unrounded best cosines:", [repr(float(cos_all[k].max())) for k in cos_all])
# shares after rescaling 0.25-year column by 10
resc = panel.copy()
resc[:, 0] *= 10.0
xr = resc - resc.mean(axis=0)
Mr = xr.T @ xr / (T - 1)
wr = np.linalg.eigvalsh(Mr)
print("first share before:", repr(float(shares[0])), "after:", repr(float(np.max(wr) / wr.sum())))
M11 = float(M[0, 0]); tr = float(np.trace(M))
bound = 100 * M11 / (tr + 99 * M11)
print("E1 bound unrounded:", repr(bound), "M11", M11, "trace", tr)
print("E1 bound from printed inputs 13.6818, 88.2028:", 100 * 13.6818 / (88.2028 + 99 * 13.6818))
print("trace - sum of diagonal check", tr - np.sum(np.diag(M)))
print("doubling shares max diff", np.max(np.abs(np.linalg.eigvalsh(4 * M)[::-1] / np.sum(np.linalg.eigvalsh(4 * M)) - np.sort(lam / lam.sum())[::-1])))

print("== L09 counts with an independent implementation (eigh-free check via own Jacobi is not needed; recount)")
SEED = 20261028
rng = np.random.default_rng(SEED)
mats = []
for _ in range(40):
    nz = rng.normal(0.0, 0.35, size=(5, 5))
    nz = (nz + nz.T) / 2.0
    A = 0.5 + nz
    np.fill_diagonal(A, 1.0)
    mats.append(A)
nonpsd = []
for i, A in enumerate(mats):
    mn = np.linalg.eigvalsh(A)[0]
    if mn < -1e-9:
        nonpsd.append((i, mn))
print("non-PSD count (min eig < -1e-9):", len(nonpsd), "indices", [i for i, _ in nonpsd])
print("min eigenvalues of non-PSD set (smallest 3):", sorted(m for _, m in nonpsd)[:3])
print("count with min eig in (-1e-9, 0):", sum(1 for A in mats if -1e-9 <= np.linalg.eigvalsh(A)[0] < 0))
print("count with min eig in [-1e-6, -1e-9):", sum(1 for A in mats if -1e-6 <= np.linalg.eigvalsh(A)[0] < -1e-9))
closer = 0
feas = 0
for i, mn in nonpsd:
    A = mats[i]
    lam_, Q = np.linalg.eigh(A)
    R_ = Q @ np.diag(np.maximum(lam_, 0)) @ Q.T
    d = np.sqrt(np.diag(R_))
    R = R_ / np.outer(d, d)
    X = A.copy()
    for _ in range(500):
        l2, Q2 = np.linalg.eigh(X)
        Y = Q2 @ np.diag(np.maximum(l2, 0)) @ Q2.T
        np.fill_diagonal(Y, 1.0)
        if np.max(np.abs(Y - X)) < 1e-12:
            break
        X = Y
    W = Y
    ok = (np.max(np.abs(W - W.T)) < 1e-12) and np.max(np.abs(np.diag(W) - 1)) < 1e-12 and np.linalg.eigvalsh(W)[0] >= -1e-8
    feas += bool(ok)
    dR = np.linalg.norm(A - R); dW = np.linalg.norm(A - W)
    closer += bool(dW < dR)
    if i == nonpsd[0][0]:
        print("first: ||A-R||", dR, "||A-W||", dW)
    print(i, f"minEig={mn:.6g}", f"dR={dR:.6f} dW={dW:.6f} W_minEig={np.linalg.eigvalsh(W)[0]:.3g}")
print("feasible", feas, "of", len(nonpsd), "closer", closer, "of", len(nonpsd))
