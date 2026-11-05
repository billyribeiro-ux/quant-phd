"""Independent recomputation of every number printed or quoted on L07, L08 and L09 (round 9).

Route: exact Fractions where the page's arithmetic is rational; a pure-Python cyclic Jacobi eigensolver
(no LAPACK) and a pure-Python Gauss elimination for the least-squares normal equations. NumPy is used only
to regenerate the seeded inputs (default_rng streams), which the lab defines.

Run: .venv/bin/python -I ledgers/M3/scripts/M3-c-r9/m3c_r9_numbers.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np


# ---------- pure-Python linear algebra ----------
def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(r) for r in zip(*a)]


def jacobi_eig(a0: list[list[float]], tol: float = 1e-14, max_sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Cyclic Jacobi for a real symmetric matrix. Returns (eigenvalues, eigenvectors as columns)."""
    n = len(a0)
    a = [list(r) for r in a0]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol**2:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: vals[i], reverse=True)
    vals_sorted = [vals[i] for i in order]
    vecs = [[v[k][i] for i in order] for k in range(n)]  # columns
    return vals_sorted, vecs


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(a)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] for i in range(n)]


def max_abs(a: list[list[float]]) -> float:
    return max(abs(x) for r in a for x in r)


# ---------- L07 ----------
def l07() -> None:
    print("== L07 ==")
    # M2 exact
    A = [[F(1), F(0)], [F(1), F(1)], [F(1), F(2)]]
    y = [F(1), F(2), F(2)]
    G = [[sum(A[k][i] * A[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
    Ay = [sum(A[k][i] * y[k] for k in range(3)) for i in range(2)]
    det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
    b0 = (Ay[0] * G[1][1] - G[0][1] * Ay[1]) / det
    b1 = (G[0][0] * Ay[1] - G[1][0] * Ay[0]) / det
    fitted = [b0 + b1 * A[k][1] for k in range(3)]
    resid = [y[k] - fitted[k] for k in range(3)]
    print(f"M2 exact: G={G} A^Ty={Ay} b0={b0} b1={b1} fitted={fitted} resid={resid} sum={sum(resid)} "
          f"dot_x={sum(resid[k] * A[k][1] for k in range(3))}")
    # M1 exact: P = (1/2)[[1,1],[1,1]], p=(1,1), resid=(1,-1), dot with A = 0
    print("M1 exact: P p resid check:", F(1, 2) * 2 == 1, F(2) * F(1, 2) + F(0) == 1)
    # M3 exact
    print("M3 exact: 25 = 9 + 16:", 3 * 3 + 4 * 4 == 25)

    # Lab numbers, seed 7, same generator stream as the lab
    rng = np.random.default_rng(7)
    n = 12
    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    noise = rng.normal(scale=0.3, size=n)
    yv = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
    Am = [[1.0, float(x1[i]), float(x2[i])] for i in range(n)]
    At = transpose(Am)
    Gm = matmul(At, Am)
    Aty = [sum(At[i][k] * float(yv[k]) for k in range(n)) for i in range(3)]
    beta = solve(Gm, Aty)
    fit = [sum(Am[i][j] * beta[j] for j in range(3)) for i in range(n)]
    res = [float(yv[i]) - fit[i] for i in range(n)]
    rnorm = math.sqrt(sum(r * r for r in res))
    orth = max(abs(sum(At[j][i] * res[i] for i in range(n))) for j in range(3))
    print(f"L07 pure-python normal equations: beta={[round(b, 4) for b in beta]} residual_norm={rnorm:.4f} "
          f"A^Ty={[round(v, 2) for v in Aty]} max|A^T r|={orth:.2e}")
    # rank of A^T A with duplicated column: pure-python via Jacobi eigenvalues
    dup = [[row[0], row[1], row[1]] for row in Am]
    dg = matmul(transpose(dup), dup)
    ev, _ = jacobi_eig(dg)
    print(f"L07 eigenvalues of duplicated A^T A: {[f'{e:.3e}' for e in ev]} (rank 2 of 3 expected)")
    # null direction (0,1,-1)
    nd = [sum(dup[i][j] * d for j, d in enumerate([0.0, 1.0, -1.0])) for i in range(n)]
    print(f"L07 max|dup @ (0,1,-1)| = {max(abs(v) for v in nd):.1e}")


# ---------- L08 ----------
def panel_l08() -> tuple[np.ndarray, list[float], list[float], list[float]]:
    tenors = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
    level = np.ones_like(tenors) / math.sqrt(len(tenors))
    slope = tenors - tenors.mean()
    slope = slope / np.linalg.norm(slope)
    quad = tenors**2 - (tenors**2).mean()
    quad = quad - (quad @ level) * level - (quad @ slope) * slope
    curv = quad / np.linalg.norm(quad)
    rng = np.random.default_rng(8)
    T = 750
    scores = np.column_stack(
        [rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)]
    )
    shapes = np.column_stack([level, slope, curv])
    noise = rng.normal(scale=0.5, size=(T, 6))
    panel = scores @ shapes.T + noise
    return panel, list(level), list(slope), list(curv)


def cov_matrix(panel: np.ndarray) -> list[list[float]]:
    xc = panel - panel.mean(axis=0)
    t = panel.shape[0]
    m = xc.T @ xc / (t - 1)
    return [[float(m[i][j]) for j in range(6)] for i in range(6)]


def l08() -> None:
    print("== L08 ==")
    panel, level, slope, curv = panel_l08()
    M = cov_matrix(panel)
    vals, vecs = jacobi_eig(M)
    tr = sum(M[i][i] for i in range(6))
    shares = [v / sum(vals) for v in vals]
    print("L08 Jacobi eigenvalues:", [f"{v:.6f}" for v in vals])
    print("L08 unrounded shares %:", [f"{100 * s:.6f}" for s in shares[:3]], "rounded:", [f"{100 * s:.1f}" for s in shares[:3]])
    print("L08 sum of printed rounded shares:", round(sum(round(100 * s, 1) for s in shares[:3]), 1),
          " unrounded top-3 sum:", f"{100 * sum(shares[:3]):.6f}", " diff:", f"{abs(sum(round(100 * s, 1) for s in shares[:3]) - 100 * sum(shares[:3])):.6f}")
    print("L08 residual max|Mv - lam v|:", f"{max(abs(sum(M[i][k] * vecs[k][j] for k in range(6)) - vals[j] * vecs[i][j]) for i in range(6) for j in range(6)):.2e}")
    # cosines: best match per planted shape
    for name, shape in zip(("level", "slope", "curvature"), (level, slope, curv)):
        cos = [abs(sum(vecs[k][j] * shape[k] for k in range(6))) for j in range(6)]
        best = max(range(6), key=lambda j: cos[j])
        print(f"L08 {name}: best PC{best + 1} |cos|={cos[best]:.6f}")
    # rescale first column by 10
    panel2 = panel.copy()
    panel2[:, 0] *= 10.0
    M2 = cov_matrix(panel2)
    vals2, _ = jacobi_eig(M2)
    share_new = vals2[0] / sum(vals2)
    print(f"L08 first share before {shares[0]:.6f} after {share_new:.6f} (page: 0.7587 -> 0.9791)")
    M11 = M[0][0]
    bound = 100 * M11 / (tr + 99 * M11)
    print(f"L08 M11={M11:.6f} trace={tr:.6f} bound={bound:.6f} (page 13.6818, 88.2028, 0.9483)")
    print("L08 bound <= new share:", bound <= share_new + 1e-12, " bound > old share:", bound > shares[0])
    # doubled panel shares
    vals3, _ = jacobi_eig(cov_matrix(panel * 2.0))
    print("L08 doubled shares max diff:", f"{max(abs(vals3[i] / sum(vals3) - shares[i]) for i in range(6)):.2e}")
    # E1 printed numbers as in the page with printed inputs
    print(f"L08 bound from printed inputs: {100 * 13.6818 / (88.2028 + 99 * 13.6818):.6f}")
    # Remark 2.4 claim M_jj>0
    print("L08 M_11 > 0:", M[0][0] > 0)
    # Section 3 claim: two-value quadratic identity and three-value curvature residual for (1,2,3)
    t = np.array([1.0, 2.0, 3.0])
    print("L08 curvature residual for tenors (1,2,3):", f"{abs(_curv_residual(t)):.4f}", "(page 0.8165)")
    t2 = np.array([1.0, 2.0])
    print("L08 curvature residual for two tenors (1,2):", f"{abs(_curv_residual(t2)):.2e}")
    # M1 page example
    Xf = [[F(1), F(2)], [F(3), F(4)], [F(5), F(9)]]
    mf = [sum(r[j] for r in Xf) / 3 for j in range(2)]
    Xcf = [[r[j] - mf[j] for j in range(2)] for r in Xf]
    Mf = [[sum(Xcf[k][i] * Xcf[k][j] for k in range(3)) / 2 for j in range(2)] for i in range(2)]
    print("L08 M1 exact M:", Mf, "trace", Mf[0][0] + Mf[1][1], "det", Mf[0][0] * Mf[1][1] - Mf[0][1] ** 2,
          "sum centred squared norms/2:", sum(Xcf[k][0] ** 2 + Xcf[k][1] ** 2 for k in range(3)) / 2)
    # M3 page: diag(4,1,1) shares
    print("L08 M2 shares:", [F(4, 6), F(1, 6), F(1, 6)], "sum", F(4, 6) + F(1, 3))
    print("L08 M3 tripling: 9*{2,1} =", 9 * 2, 9 * 1, "shares", F(18, 27), F(9, 27))
    print("L08 E1 printed inputs:", 100 * 13.6818 / (88.2028 + 99 * 13.6818))


def _curv_residual(t: np.ndarray) -> float:
    """Norm of the orthogonalized centred squared tenors (zero when the squared tenors lie in span(1, t))."""
    n = len(t)
    one = np.ones(n) / math.sqrt(n)
    c = t - t.mean()
    c = c / np.linalg.norm(c) if np.linalg.norm(c) > 0 else c
    q = t**2 - (t**2).mean()
    q = q - (q @ one) * one
    if np.linalg.norm(c) > 0:
        q = q - (q @ c) * c
    return float(np.linalg.norm(q))


# ---------- L09 ----------
def l09() -> None:
    print("== L09 ==")
    C0 = [[1.0, 0.9, 0.9], [0.9, 1.0, -0.9], [0.9, -0.9, 1.0]]
    ev, Qc = jacobi_eig(C0)
    print("L09 C0 eigenvalues:", [f"{v:.12f}" for v in ev])
    x = [1.0, -1.0, -1.0]
    quad = sum(x[i] * C0[i][j] * x[j] for i in range(3) for j in range(3))
    print("L09 witness quad:", quad)
    # clip at zero
    B = [[0.0] * 3 for _ in range(3)]
    for k in range(3):
        for i in range(3):
            for j in range(3):
                B[i][j] += max(ev[k], 0.0) * Qc[i][k] * Qc[j][k]
    dist2 = sum((C0[i][j] - B[i][j]) ** 2 for i in range(3) for j in range(3))
    neg2 = sum(min(e, 0.0) ** 2 for e in ev)
    print(f"L09 ||C0-B||^2={dist2:.12f} sum neg eig^2={neg2:.12f}")
    d = [math.sqrt(B[i][i]) for i in range(3)]
    R = [[B[i][j] / (d[i] * d[j]) for j in range(3)] for i in range(3)]
    print("L09 R =", [[round(v, 6) for v in row] for row in R])
    C0R = [[C0[i][j] - R[i][j] for j in range(3)] for i in range(3)]
    print(f"L09 ||C0-R||^2 = {sum(v * v for r in C0R for v in r):.12f} sqrt = {math.sqrt(sum(v * v for r in C0R for v in r)):.6f}")

    # Example 3.6 with exact-looking numbers
    A = [[1.0, 1.2], [1.2, 1.0]]
    evA, QA = jacobi_eig(A)
    A0 = [[sum(max(evA[k], 0.0) * QA[i][k] * QA[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    dA = [[A[i][j] - A0[i][j] for j in range(2)] for i in range(2)]
    print("L09 Ex3.6 eig:", [round(v, 12) for v in evA], "A0:", [[round(v, 12) for v in r] for r in A0],
          "||A-A0||^2:", round(sum(v * v for r in dA for v in r), 12))
    RA = [[A0[i][j] / math.sqrt(A0[i][i] * A0[j][j]) for j in range(2)] for i in range(2)]
    dR = [[A[i][j] - RA[i][j] for j in range(2)] for i in range(2)]
    print("L09 Ex3.6 R:", [[round(v, 12) for v in r] for r in RA], "||A-R||^2:", round(sum(v * v for r in dR for v in r), 12))
    print("L09 M2 ||A||_F^2 exact:", F(1) + F(144, 100) + F(144, 100) + F(1), " 2.2^2+0.2^2 =", 2.2**2 + 0.2**2)

    # M1 eigen, M3 eigen, E3 spectrum
    print("L09 M1 eigenvalues of [[1,.6],[.6,1]]:", jacobi_eig([[1.0, 0.6], [0.6, 1.0]])[0])
    print("L09 M3 eigen of [[4,2],[2,9]]:", jacobi_eig([[4.0, 2.0], [2.0, 9.0]])[0], " (13 +- sqrt41)/2 =",
          (13 + math.sqrt(41)) / 2, (13 - math.sqrt(41)) / 2)
    print("L09 M3 C:", F(4, 4), F(9, 9), F(2, 6))
    print("L09 E2 sqrt(0.96) =", math.sqrt(0.96))

    # seeded 40 matrices, seed 20261028 (same stream as the lab)
    rng = np.random.default_rng(20261028)
    nonpsd = feasible = closer = 0
    first_line = None
    for index in range(40):
        noise = rng.normal(0.0, 0.35, size=(5, 5))
        noise = (noise + noise.T) / 2.0
        a_np = 0.5 + noise
        np.fill_diagonal(a_np, 1.0)
        a = [[float(a_np[i][j]) for j in range(5)] for i in range(5)]
        evs, _ = jacobi_eig(a)
        if evs[-1] >= -1e-9:
            continue
        nonpsd += 1
        evs2, Qs = jacobi_eig(a)
        Bc = [[sum(max(evs2[k], 0.0) * Qs[i][k] * Qs[j][k] for k in range(5)) for j in range(5)] for i in range(5)]
        dd = [math.sqrt(Bc[i][i]) for i in range(5)]
        Rr = [[Bc[i][j] / (dd[i] * dd[j]) for j in range(5)] for i in range(5)]
        # alternating projections with pure-python Jacobi
        X = [list(r) for r in a]
        W = X
        for _ in range(500):
            ev_x, Q_x = jacobi_eig(X)
            Y = [[sum(max(ev_x[k], 0.0) * Q_x[i][k] * Q_x[j][k] for k in range(5)) for j in range(5)] for i in range(5)]
            for i in range(5):
                Y[i][i] = 1.0
            change = max(abs(Y[i][j] - X[i][j]) for i in range(5) for j in range(5))
            W = Y
            if change < 1e-12:
                break
            X = Y
        sym = max(abs(W[i][j] - W[j][i]) for i in range(5) for j in range(5)) < 1e-12
        unit = max(abs(W[i][i] - 1.0) for i in range(5)) < 1e-12
        psd = jacobi_eig(W)[0][-1] >= -1e-8
        feas = sym and unit and psd
        dR_ = math.sqrt(sum((a[i][j] - Rr[i][j]) ** 2 for i in range(5) for j in range(5)))
        dW_ = math.sqrt(sum((a[i][j] - W[i][j]) ** 2 for i in range(5) for j in range(5)))
        if feas:
            feasible += 1
            if dW_ < dR_:
                closer += 1
        if first_line is None:
            first_line = (index, dR_, dW_)
    print(f"L09 seeded: non-PSD={nonpsd} feasible={feasible} closer={closer}")
    print(f"L09 first non-PSD index={first_line[0]} ||A-R||={first_line[1]:.6f} ||A-W||={first_line[2]:.6f}")


if __name__ == "__main__":
    l07()
    l08()
    l09()
