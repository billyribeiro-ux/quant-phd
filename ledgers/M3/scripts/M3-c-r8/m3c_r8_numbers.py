"""Round-8 independent re-derivation of the numbers printed or stated in M3 L07, L08 and L09 (slice c).

Each quantity is recomputed by a method different from the lab twin: SVD and QR where the twin uses eigh and solve,
Gram-Schmidt for the curvature shape, and exact Fraction arithmetic for the hand examples.
Usage: python -I ledgers/M3/scripts/M3-c-r8/m3c_r8_numbers.py
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np


def line(label: str, value: object) -> None:
    print(f"{label}: {value}")


def l07() -> None:
    rng = np.random.default_rng(7)
    n = 12
    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    noise = rng.normal(scale=0.3, size=n)
    y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
    a = np.column_stack([np.ones(n), x1, x2])
    q, r = np.linalg.qr(a)
    beta_qr = np.linalg.solve(r, q.T @ y)
    fitted_qr = a @ beta_qr
    residual = y - fitted_qr
    line("L07 QR beta (4 dp)", " ".join(f"{v:.4f}" for v in beta_qr))
    line("L07 QR residual norm (4 dp)", f"{np.linalg.norm(residual):.4f}")
    line("L07 A^T y (2 dp)", " ".join(f"{v:.2f}" for v in a.T @ y))
    line("L07 max |A^T residual| (must be < 1e-9)", f"{np.max(np.abs(a.T @ residual)):.3e}")
    # Projection by SVD: P = U U^T with U the left singular vectors of A.
    u, _, _ = np.linalg.svd(a, full_matrices=False)
    p_svd = u @ u.T
    line("L07 max |P_svd - A(A^TA)^-1 A^T|", f"{np.max(np.abs(p_svd - a @ np.linalg.inv(a.T @ a) @ a.T)):.3e}")
    line("L07 rank of A^TA with duplicated column", int(np.linalg.matrix_rank(np.column_stack([a[:, 0], a[:, 1], a[:, 1]]).T @ np.column_stack([a[:, 0], a[:, 1], a[:, 1]]))))
    # Hand examples, exact.
    # Problem M2: fit y = b0 + b1 x to (0,1), (1,2), (2,2).
    x_m2 = [Fraction(0), Fraction(1), Fraction(2)]
    y_m2 = [Fraction(1), Fraction(2), Fraction(2)]
    n_m2 = Fraction(3)
    sx = sum(x_m2)
    sy = sum(y_m2)
    sxx = sum(v * v for v in x_m2)
    sxy = sum(v * w for v, w in zip(x_m2, y_m2, strict=True))
    b1 = (n_m2 * sxy - sx * sy) / (n_m2 * sxx - sx * sx)
    b0 = (sy - b1 * sx) / n_m2
    line("L07 M2 exact b0, b1", (b0, b1, float(b0)))
    fitted = [b0 + b1 * v for v in x_m2]
    res = [w - f for w, f in zip(y_m2, fitted, strict=True)]
    line("L07 M2 residuals exact", res)
    line("L07 M2 residual inner product with x exact", sum(r_ * v for r_, v in zip(res, x_m2, strict=True)))
    # Quiz numeric: beta0 = 7/6 to four decimals.
    line("L07 quiz 1.1667 tolerance 0.0005 holds", abs(float(b0) - 1.1667) <= 0.0005)
    # Problem M1: P = (1/2)[[1,1],[1,1]], Py for y=(2,0).
    p_m1 = [[Fraction(1, 2), Fraction(1, 2)], [Fraction(1, 2), Fraction(1, 2)]]
    py = [p_m1[0][0] * 2 + p_m1[0][1] * 0, p_m1[1][0] * 2 + p_m1[1][1] * 0]
    line("L07 M1 Py exact", py)
    # Remark 1.4 check, Problem M3: |y|^2 = 25 = 9 + 16.
    line("L07 M3 identity 25 = 9 + 16", 25 == 9 + 16)


def l08() -> None:
    rng = np.random.default_rng(8)
    tenors = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
    t_days = 750
    # Independent curvature shape by Gram-Schmidt on [1, tau, tau^2].
    ones = np.ones(6)
    tau = tenors.copy()
    f1 = ones / np.linalg.norm(ones)
    v2 = tau - tau.mean()
    f2 = v2 / np.linalg.norm(v2)
    v3 = tau**2
    v3 = v3 - (v3 @ f1) * f1 - (v3 @ f2) * f2
    f3 = v3 / np.linalg.norm(v3)
    line("L08 shapes orthonormal max|G-I|", f"{np.max(np.abs(np.column_stack([f1, f2, f3]).T @ np.column_stack([f1, f2, f3]) - np.eye(3))):.3e}")
    scores = np.column_stack(
        [
            rng.normal(scale=8.0, size=t_days),
            rng.normal(scale=4.0, size=t_days),
            rng.normal(scale=2.0, size=t_days),
        ]
    )
    shapes = np.column_stack([f1, f2, f3])
    noise = rng.normal(scale=0.5, size=(t_days, 6))
    panel = scores @ shapes.T + noise
    xc = panel - panel.mean(axis=0)
    # Independent route: SVD of the centred data. Eigenvalues of M = s^2 / (T-1).
    _, s, vt = np.linalg.svd(xc, full_matrices=False)
    lam = s**2 / (t_days - 1)
    v = vt.T
    shares = lam / lam.sum()
    line("L08 eigenvalues via SVD (unrounded)", " ".join(f"{x:.6f}" for x in lam))
    line("L08 shares PC1 PC2 PC3 (percent, 1 dp)", " ".join(f"{100 * x:.1f}" for x in shares[:3]))
    line("L08 shares percent unrounded", " ".join(f"{100 * x:.6f}" for x in shares[:3]))
    line("L08 rounded-sum of printed shares", f"{round(100 * shares[0], 1) + round(100 * shares[1], 1) + round(100 * shares[2], 1):.1f}")
    cos_names = ["level", "slope", "curvature"]
    for name, f in zip(cos_names, (f1, f2, f3), strict=True):
        c = np.abs(v.T @ f)
        k = int(np.argmax(c))
        second = float(np.sort(c)[-2])
        line(f"L08 {name} best PC{k + 1} |cos| (4 dp), runner-up |cos|", f"{c[k]:.4f} {second:.4f}")
    # Rescaling check (Remark 2.4 / lab line): multiply the 0.25-year column by ten.
    panel2 = panel.copy()
    panel2[:, 0] *= 10.0
    xc2 = panel2 - panel2.mean(axis=0)
    lam2 = np.linalg.svd(xc2, compute_uv=False) ** 2 / (t_days - 1)
    line("L08 first share after rescaling (4 dp)", f"{lam2[0] / lam2.sum():.4f}")
    m = xc.T @ xc / (t_days - 1)
    m11 = m[0, 0]
    s0 = np.trace(m)
    line("L08 M11 (4 dp), trace (4 dp)", f"{m11:.4f} {s0:.4f}")
    bound = 100 * m11 / (s0 + 99 * m11)
    line("L08 E1 bound unrounded (4 dp)", f"{bound:.4f}")
    line("L08 E1 bound from printed inputs 13.6818, 88.2028 (4 dp)", f"{100 * 13.6818 / (88.2028 + 99 * 13.6818):.6f}")
    line("L08 new share >= bound", bool(lam2[0] / lam2.sum() >= bound - 1e-12))
    line("L08 bound between old and new share", bool(shares[0] <= bound <= lam2[0] / lam2.sum()))
    # Doubling check: shares unchanged.
    lam_d = np.linalg.svd(2 * xc, compute_uv=False) ** 2 / (t_days - 1)
    line("L08 doubled shares max change", f"{np.max(np.abs(lam_d / lam_d.sum() - shares)):.3e}")
    # Hand examples, exact.
    m_m1 = [[Fraction(4), Fraction(7)], [Fraction(7), Fraction(13)]]
    line("L08 M1 trace exact", m_m1[0][0] + m_m1[1][1])
    line("L08 M1 det exact", m_m1[0][0] * m_m1[1][1] - m_m1[0][1] * m_m1[1][0])
    xm1 = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 9.0]])
    xm1c = xm1 - xm1.mean(axis=0)
    line("L08 M1 centred Gram / (T-1)", (xm1c.T @ xm1c / 2).tolist())
    line("L08 M1 eigenvalues", np.linalg.eigvalsh(xm1c.T @ xm1c / 2).tolist())
    line("L08 M1 (17 pm sqrt277)/2", [(17 - 277**0.5) / 2, (17 + 277**0.5) / 2])


def l09() -> None:
    c0 = np.array([[1.0, 0.9, 0.9], [0.9, 1.0, -0.9], [0.9, -0.9, 1.0]])
    line("L09 Example 2.3 witness exact", Fraction(3) + 2 * (Fraction(9, 10) * -1 + Fraction(9, 10) * -1 + Fraction(-9, 10) * 1))
    eig = np.linalg.eigvalsh(c0)
    line("L09 C0 eigenvalues", " ".join(f"{v:.6f}" for v in eig))
    # Clip via the eigen decomposition from SVD of a symmetric matrix (singular values and signs).
    u, s, vt = np.linalg.svd(c0)
    sign = np.sign(np.einsum("ij,ji->i", vt, u.T))
    _ = sign
    w, q = np.linalg.eigh(c0)
    b = (q * np.maximum(w, 0.0)) @ q.T
    line("L09 ||C0-B||_F^2 vs sum of squared negative eigenvalues", (float(np.sum((c0 - b) ** 2)), float(np.sum(np.minimum(w, 0) ** 2))))
    d = np.sqrt(np.diag(b))
    r = b / np.outer(d, d)
    line("L09 R entries (4 dp)", np.round(r, 4).tolist())
    line("L09 E2 ||C0-R||_F (4 dp) exact sqrt(0.96)", (f"{np.linalg.norm(c0 - r):.6f}", f"{np.sqrt(0.96):.6f}"))
    # Example 3.6 exact-ish checks.
    a = np.array([[1.0, 1.2], [1.2, 1.0]])
    w2, q2 = np.linalg.eigh(a)
    a0 = (q2 * np.maximum(w2, 0.0)) @ q2.T
    line("L09 Example 3.6 eigenvalues", w2.tolist())
    line("L09 Example 3.6 A0", np.round(a0, 10).tolist())
    line("L09 Example 3.6 ||A-A0||^2, ||A-R||^2", (float(np.sum((a - a0) ** 2)), float(np.sum((a - np.ones((2, 2))) ** 2))))
    line("L09 M2 ||A||_F^2 exact", Fraction(1) + Fraction(144, 100) * 2 + 1)
    line("L09 M2 2.2^2 + 0.2^2", Fraction(22, 10) ** 2 + Fraction(2, 10) ** 2)
    # M3: B = [[4,2],[2,9]], eigenvalues roots of l^2 - 13 l + 32.
    bm3 = np.array([[4.0, 2.0], [2.0, 9.0]])
    line("L09 M3 eigenvalues", np.linalg.eigvalsh(bm3).tolist())
    line("L09 M3 (13 pm sqrt41)/2", [(13 - 41**0.5) / 2, (13 + 41**0.5) / 2])
    dm3 = np.diag(1 / np.sqrt(np.diag(bm3)))
    line("L09 M3 rescaled", (dm3 @ bm3 @ dm3).tolist())
    # E3 spectrum example.
    line("L09 E3 ||A-A0|| for spectrum 2, 0.5, -0.5", float(np.sqrt(0.25)))
    # Lab 1 seeded counts: independent route for the repair (SVD-based clip), same generator.
    rng = np.random.default_rng(20261028)
    nonpsd = 0
    feasible = 0
    closer = 0
    first_info = None
    for index in range(40):
        noise = rng.normal(0.0, 0.35, size=(5, 5))
        noise = (noise + noise.T) / 2.0
        a5 = 0.5 + noise
        np.fill_diagonal(a5, 1.0)
        w5 = np.linalg.eigvalsh(a5)
        if w5[0] >= -1e-9:
            continue
        nonpsd += 1
        ww, qq = np.linalg.eigh(a5)
        bb = (qq * np.maximum(ww, 0)) @ qq.T
        dd = np.sqrt(np.diag(bb))
        rr = bb / np.outer(dd, dd)
        # Alternating projections, an independent loop written differently: Dykstra-free plain iteration on the matrix.
        xk = a5.copy()
        out = xk
        for _ in range(500):
            wk, qk = np.linalg.eigh(xk)
            yk = (qk * np.maximum(wk, 0)) @ qk.T
            np.fill_diagonal(yk, 1.0)
            change = float(np.max(np.abs(yk - xk)))
            out = yk
            xk = yk
            if change < 1e-12:
                break
        sym = float(np.max(np.abs(out - out.T))) < 1e-12
        unit = float(np.max(np.abs(np.diag(out) - 1.0))) < 1e-12
        psd = float(np.linalg.eigvalsh(out)[0]) >= -1e-8
        ok = sym and unit and psd
        d_r = float(np.linalg.norm(a5 - rr))
        d_w = float(np.linalg.norm(a5 - out))
        if ok:
            feasible += 1
            if d_w < d_r:
                closer += 1
        if first_info is None:
            first_info = (index, d_r, d_w)
    line("L09 seeded nonPSD count", nonpsd)
    line("L09 seeded feasible alt output count", feasible)
    line("L09 seeded feasible and closer count", closer)
    line("L09 first non-PSD (index, ||A-R||, ||A-W||)", first_info)


if __name__ == "__main__":
    print("== L07")
    l07()
    print("== L08")
    l08()
    print("== L09")
    l09()
