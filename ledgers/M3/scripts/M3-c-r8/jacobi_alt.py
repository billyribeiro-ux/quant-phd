"""Round-8 alternative implementation check for M3 L08 and L09 (slice c), with no LAPACK call.

A pure-Python cyclic Jacobi eigensolver replaces numpy.linalg.eigh. It is used to:
  - recompute the L09 C0 eigenvalues, the clipped matrix B, the rescaled R, the 40 seeded counts and the
    alternating-projection distances (same generator as the lab, so the inputs are identical);
  - recompute the L08 M eigenvalues, the explained shares, the planted-shape cosines and the rescaling share;
  - check the L08 Section 3 degeneracy claim (exactly two distinct tenor values gives a zero curvature shape).
Usage: python -I ledgers/M3/scripts/M3-c-r8/jacobi_alt.py
"""

from __future__ import annotations

import math

import numpy as np

Matrix = list[list[float]]


def jacobi_eig(a0: Matrix, max_sweeps: int = 100) -> tuple[list[float], Matrix]:
    """Return (eigenvalues, eigenvector matrix with eigenvectors as columns) of a symmetric matrix."""
    n = len(a0)
    a = [row[:] for row in a0]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < 1e-15:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
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
    return [a[i][i] for i in range(n)], v


def to_np(m: Matrix) -> np.ndarray:
    return np.array(m, dtype=np.float64)


def reconstruct(vals: list[float], vecs: Matrix, f: object) -> np.ndarray:
    """Return V diag(f(lambda)) V^T for a callable f."""
    v = to_np(vecs)
    d = np.diag([f(x) for x in vals])  # type: ignore[operator]
    return np.asarray(v @ d @ v.T, dtype=np.float64)


def l09() -> None:
    c0 = [[1.0, 0.9, 0.9], [0.9, 1.0, -0.9], [0.9, -0.9, 1.0]]
    vals, vecs = jacobi_eig(c0)
    print("L09 Jacobi eigenvalues of C0 (sorted):", sorted(round(x, 9) for x in vals))
    recon_err = float(np.max(np.abs(reconstruct(vals, vecs, lambda x: x) - to_np(c0))))
    print("L09 Jacobi reconstruction error of C0:", f"{recon_err:.3e}")
    b = reconstruct(vals, vecs, lambda x: max(x, 0.0))
    print("L09 Jacobi B diagonal:", np.round(np.diag(b), 12).tolist())
    dd = np.sqrt(np.diag(b))
    r = b / np.outer(dd, dd)
    print("L09 Jacobi R (4 dp):", np.round(r, 4).tolist())
    dist2 = float(np.sum((to_np(c0) - b) ** 2))
    print("L09 Jacobi ||C0-B||_F^2 vs sum of squared negative eigenvalues:", f"{dist2:.10f}", f"{sum(min(x, 0.0) ** 2 for x in vals):.10f}")

    def clip_jacobi(m: np.ndarray) -> np.ndarray:
        w, vv = jacobi_eig(m.tolist())
        return reconstruct(w, vv, lambda x: max(x, 0.0))

    rng = np.random.default_rng(20261028)
    nonpsd = 0
    feasible = 0
    closer = 0
    first = None
    for index in range(40):
        noise = rng.normal(0.0, 0.35, size=(5, 5))
        noise = (noise + noise.T) / 2.0
        a = 0.5 + noise
        np.fill_diagonal(a, 1.0)
        w, _ = jacobi_eig(a.tolist())
        if min(w) >= -1e-9:
            continue
        nonpsd += 1
        bb = clip_jacobi(a)
        d = np.sqrt(np.diag(bb))
        rr = bb / np.outer(d, d)
        x = a.copy()
        out = x
        for _ in range(500):
            y = clip_jacobi(x)
            np.fill_diagonal(y, 1.0)
            change = float(np.max(np.abs(y - x)))
            out = y
            x = y
            if change < 1e-12:
                break
        wo, _ = jacobi_eig(out.tolist())
        sym = float(np.max(np.abs(out - out.T))) < 1e-12
        unit = float(np.max(np.abs(np.diag(out) - 1.0))) < 1e-12
        psd = min(wo) >= -1e-8
        ok = sym and unit and psd
        d_r = float(np.linalg.norm(a - rr))
        d_w = float(np.linalg.norm(a - out))
        if ok:
            feasible += 1
            if d_w < d_r:
                closer += 1
        if first is None:
            first = (index, round(d_r, 6), round(d_w, 6))
    print("L09 Jacobi seeded nonPSD count:", nonpsd)
    print("L09 Jacobi feasible alt output count:", feasible)
    print("L09 Jacobi feasible and closer count:", closer)
    print("L09 Jacobi first non-PSD (index, ||A-R||, ||A-W||):", first)


def l08() -> None:
    tenors = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
    rng = np.random.default_rng(8)
    t = np.array(tenors)
    ones = np.ones(6)
    level = ones / np.linalg.norm(ones)
    slope = t - t.mean()
    slope = slope / np.linalg.norm(slope)
    quad = t**2 - (t**2).mean()
    quad = quad - (quad @ level) * level - (quad @ slope) * slope
    curv = quad / np.linalg.norm(quad)
    scores = np.column_stack(
        [rng.normal(scale=8.0, size=750), rng.normal(scale=4.0, size=750), rng.normal(scale=2.0, size=750)]
    )
    panel = scores @ np.column_stack([level, slope, curv]).T + rng.normal(scale=0.5, size=(750, 6))
    xc = panel - panel.mean(axis=0)
    m = xc.T @ xc / 749.0
    vals, vecs = jacobi_eig(m.tolist())
    order = sorted(range(6), key=lambda i: -vals[i])
    lam = [vals[i] for i in order]
    v = np.array([[vecs[r][i] for i in order] for r in range(6)])
    total = sum(lam)
    print("L08 Jacobi eigenvalues of M (descending, 6 dp):", [f"{x:.6f}" for x in lam])
    print("L08 Jacobi shares PC1..PC3 (percent, unrounded 6 dp):", [f"{100 * x / total:.6f}" for x in lam[:3]])
    print("L08 Jacobi sum of shares minus 1:", f"{sum(lam) / total - 1:.3e}")
    print("L08 Jacobi |M v - lambda v| max:", f"{float(np.max(np.abs(m @ v - v * np.array(lam)))):.3e}")
    for name, f in (("level", level), ("slope", slope), ("curvature", curv)):
        cos = [abs(float(v[:, k] @ f)) for k in range(6)]
        best = max(range(6), key=lambda k: cos[k])
        print(f"L08 Jacobi {name}: best PC{best + 1}, |cos| unrounded (6 dp) {cos[best]:.6f}")
    # Rescaling: multiply the 0.25-year column by ten, recompute M by hand, eigenvalues by Jacobi.
    panel2 = panel.copy()
    panel2[:, 0] *= 10.0
    xc2 = panel2 - panel2.mean(axis=0)
    m2 = xc2.T @ xc2 / 749.0
    vals2, _ = jacobi_eig(m2.tolist())
    print("L08 Jacobi first share after rescaling (4 dp):", f"{max(vals2) / sum(vals2):.4f}")
    m11 = float(m[0, 0])
    tr = float(np.trace(m))
    print("L08 M11, trace (4 dp):", f"{m11:.4f}", f"{tr:.4f}", "bound:", f"{100 * m11 / (tr + 99 * m11):.4f}")
    # Section 3 degeneracy: curvature shape from tenor vectors with 1, 2 and 3 distinct values.
    cases = {
        "one value (1,1,1,1,1,1)": [1.0] * 6,
        "two values (1,1,2,2,2,1)": [1.0, 1.0, 2.0, 2.0, 2.0, 1.0],
        "two values (1,2)": [1.0, 2.0],
        "two values (0.25,10,0.25,10)": [0.25, 10.0, 0.25, 10.0],
        "three values (1,2,3)": [1.0, 2.0, 3.0],
        "six lab tenors": tenors,
    }
    for label, tau in cases.items():
        tv = np.array(tau, dtype=float)
        n = len(tv)
        io = np.ones(n)
        f1 = io / np.linalg.norm(io)
        s2 = tv - tv.mean()
        if np.linalg.norm(s2) > 1e-12:
            f2 = s2 / np.linalg.norm(s2)
        else:
            f2 = np.zeros(n)
        q = tv**2 - (tv**2).mean()
        q = q - (q @ f1) * f1 - (q @ f2) * f2
        print(f"L08 Section 3 degeneracy, {label}: curvature residual norm {np.linalg.norm(q):.3e}")


if __name__ == "__main__":
    print("== L09")
    l09()
    print("== L08")
    l08()
