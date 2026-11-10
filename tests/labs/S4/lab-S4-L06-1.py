"""Lab S4-L06-1: Estimation and forecasting with the HAR-RV model.

SIMULATED: generates realized volatility path, constructs multi-horizon design matrix,
and estimates Corsi (2008) HAR model parameters via ordinary least squares.
"""

from __future__ import annotations

import random


def simulate_har_path(
    beta0: float, betad: float, betaw: float, betam: float, n: int = 600, seed: int = 42
) -> list[float]:
    """Generate stationary HAR path."""
    rng = random.Random(seed)
    uncond = beta0 / (1.0 - betad - betaw - betam)
    rv = [uncond] * 25
    for _ in range(n):
        d = rv[-1]
        w = sum(rv[-5:]) / 5.0
        m = sum(rv[-22:]) / 22.0
        val = beta0 + betad * d + betaw * w + betam * m + rng.gauss(0.0, 0.02)
        rv.append(max(0.01, val))
    return rv[25:]


def _inv4(a_mat: list[list[float]]) -> list[list[float]]:
    """Invert 4x4 matrix using Gauss-Jordan elimination."""
    n = 4
    m_mat = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a_mat)]
    for i in range(n):
        pivot_row = i
        max_val = abs(m_mat[i][i])
        for r in range(i + 1, n):
            if abs(m_mat[r][i]) > max_val:
                max_val = abs(m_mat[r][i])
                pivot_row = r
        if max_val < 1e-12:
            raise ValueError("singular matrix")
        if pivot_row != i:
            m_mat[i], m_mat[pivot_row] = m_mat[pivot_row], m_mat[i]
        pivot = m_mat[i][i]
        for c in range(2 * n):
            m_mat[i][c] /= pivot
        for r in range(n):
            if r != i:
                factor = m_mat[r][i]
                for c in range(2 * n):
                    m_mat[r][c] -= factor * m_mat[i][c]
    return [[m_mat[i][j] for j in range(n, 2 * n)] for i in range(n)]


def main() -> None:
    rv = simulate_har_path(0.04, 0.35, 0.30, 0.20, n=600, seed=42)

    x_mat: list[list[float]] = []
    y_vec: list[float] = []
    for t in range(22, len(rv)):
        d = rv[t - 1]
        w = sum(rv[t - 5 : t]) / 5.0
        m = sum(rv[t - 22 : t]) / 22.0
        x_mat.append([1.0, d, w, m])
        y_vec.append(rv[t])

    n_rows = len(x_mat)
    n_cols = 4
    xt_mat = [[x_mat[r][c] for r in range(n_rows)] for c in range(n_cols)]
    xtx_mat = [[sum(xt_mat[i][k] * x_mat[k][j] for k in range(n_rows)) for j in range(n_cols)] for i in range(n_cols)]
    inv_xtx = _inv4(xtx_mat)
    xty_vec = [sum(xt_mat[i][k] * y_vec[k] for k in range(n_rows)) for i in range(n_cols)]
    beta = [sum(inv_xtx[i][j] * xty_vec[j] for j in range(n_cols)) for i in range(n_cols)]

    y_mean = sum(y_vec) / n_rows
    ss_tot = sum((y - y_mean) ** 2 for y in y_vec)
    ss_res = sum((y_vec[i] - sum(x_mat[i][j] * beta[j] for j in range(4))) ** 2 for i in range(n_rows))
    r_squared = 1.0 - ss_res / ss_tot

    print(f"HAR(d, w, m) OLS Estimation (T = {n_rows} observations)")
    print(f"Intercept beta_0:   {beta[0]:.4f} (True: 0.0400)")
    print(f"Daily beta_d:       {beta[1]:.4f} (True: 0.3500)")
    print(f"Weekly beta_w:      {beta[2]:.4f} (True: 0.3000)")
    print(f"Monthly beta_m:     {beta[3]:.4f} (True: 0.2000)")
    print(f"Regression R^2:     {r_squared:.4f}")


main()
