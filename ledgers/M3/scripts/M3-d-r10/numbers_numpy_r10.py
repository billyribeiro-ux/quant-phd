"""Round-10 verifier (M3 slice d): re-derive every printed number of project.html Labs 1-3 and the A3 identity with NumPy,
independently of the page's Jacobi code. Run: python -I <this file> from the checkout root."""

import numpy as np

np.set_printoptions(precision=6)


def clip_rescale(a, floor=0.0):
    w, V = np.linalg.eigh(a)
    X = (V * np.maximum(w, floor)) @ V.T
    d = np.diag(X)
    return X / np.sqrt(np.outer(d, d)), X


def proj_psd(a):
    w, V = np.linalg.eigh(a)
    return (V * np.maximum(w, 0.0)) @ V.T


def projection(a, steps=500, tol=1e-10):
    n = a.shape[0]
    x = a.copy()
    cs = np.zeros((n, n))
    cu = np.zeros((n, n))
    for _ in range(steps):
        y = proj_psd(x + cs)
        cs = x + cs - y
        nx = y + cu
        np.fill_diagonal(nx, 1.0)
        cu = y + cu - nx
        gap = np.linalg.norm(nx - y)
        step = np.linalg.norm(nx - x)
        x = nx
        if gap <= tol and step <= tol:
            break
    return x


def weights(C, v):
    S = np.diag(v)
    Sig = S @ C @ S
    w = np.linalg.solve(Sig, np.ones(len(v)))
    return w / w.sum()


# Lab 1
C1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
w1, V1 = np.linalg.eigh(C1)
X1 = (V1 * np.maximum(w1, 0)) @ V1.T
d1 = np.diag(X1)
R1 = X1 / np.sqrt(np.outer(d1, d1))
print("Lab1 eigenvalues", np.round(w1, 6), "| diag", np.round(d1, 6))
print("Lab1 repaired", np.round(R1[np.triu_indices(3, 1)], 6), "dev", float(np.max(np.abs(np.diag(R1) - 1))))
print("Lab1 min eig repaired", float(np.linalg.eigvalsh(R1)[0]))

# Lab 2
C2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
w2, V2 = np.linalg.eigh(C2)
X2 = (V2 * np.maximum(w2, 0)) @ V2.T
d2 = np.diag(X2)
R2 = X2 / np.sqrt(np.outer(d2, d2))
print("Lab2 eigenvalues", np.round(w2, 6), "| diag", np.round(d2, 6))
print("Lab2 repaired off", np.round(R2[np.triu_indices(3, 1)], 6))

# Lab 3
C3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
v3 = np.array([0.10, 0.20, 0.15, 0.30])
clip, Xc = clip_rescale(C3)
proj = projection(C3)
dc = np.linalg.norm(clip - C3)
dp = np.linalg.norm(proj - C3)
print("Lab3 min eig input", float(np.linalg.eigvalsh(C3)[0]))
print("Lab3 dist clip %.6f proj %.6f saved %.6f" % (dc, dp, dc - dp))
print("Lab3 max abs entry diff %.6f" % float(np.max(np.abs(proj - clip))))
print("Lab3 max diag dev clip %.6f proj %.6f" % (float(np.max(np.abs(np.diag(clip) - 1))), float(np.max(np.abs(np.diag(proj) - 1)))))
print("Lab3 proj min eig (tol 1e-8 check) %.6e" % float(np.linalg.eigvalsh(proj)[0]))
print("Lab3 clip min eig %.6e" % float(np.linalg.eigvalsh(clip)[0]))
print("Lab3 det input %.6f" % float(np.linalg.det(C3)))
wi = weights(C3, v3)
print("Lab3 input weights", np.round(wi, 6), "sum %.6f" % wi.sum())
print("Lab3 rounded weights sum", round(1.78 - 1.10 - 0.26 + 0.57, 2))
print("Lab3 raw sum of printed 4dp weights", round(1.778929 - 1.096718 - 0.255613 + 0.573402, 6))
print("Lab3 projection min eig %.3e" % float(np.linalg.eigvalsh(proj)[0]))
print("Lab3 clip diag", np.round(np.diag(Xc), 6))
print("Lab3 clip X min eig %.6e" % float(np.linalg.eigvalsh(Xc)[0]))
print("Lab3 sigma(proj) min eig (weights singular?) %.3e" % float(np.linalg.eigvalsh(np.diag(v3) @ proj @ np.diag(v3))[0]))
print("Lab3 sigma(clip) min eig %.3e" % float(np.linalg.eigvalsh(np.diag(v3) @ clip @ np.diag(v3))[0]))

# A3 identity
for a, b, rho in [(0.1, 0.2, 0.3), (0.3, 0.05, -0.8), (2.0, 1.0, 0.9)]:
    S = np.array([[a * a, rho * a * b], [rho * a * b, b * b]])
    lhs = np.linalg.solve(S, np.ones(2))
    lhs = lhs / lhs.sum()
    rhs = np.array([b * (b - rho * a), a * (a - rho * b)]) / (a * a + b * b - 2 * rho * a * b)
    print("A3 (a,b,rho)=(%g,%g,%g) max diff %.2e" % (a, b, rho, float(np.max(np.abs(lhs - rhs)))))
    c = 7.0
    S2 = np.array([[(c * a) ** 2, rho * (c * a) * (c * b)], [rho * (c * a) * (c * b), (c * b) ** 2]])
    l2 = np.linalg.solve(S2, np.ones(2))
    l2 = l2 / l2.sum()
    print("A3 scaling max diff %.2e" % float(np.max(np.abs(l2 - lhs))))
