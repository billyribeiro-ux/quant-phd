"""Lab 2: Optimizer instability under resampling (curriculum lab).

SIMULATED: seeded synthetic resamples from a four-asset Gaussian model.
Demonstrates error maximization: small sampling fluctuations in estimated
means and covariances produce extreme spreads and instability in the
resulting unconstrained mean-variance portfolio weights.
"""

from __future__ import annotations

import math
import random


def _solve_linear(a_mat: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m_sys = [[*a_mat[i], b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m_sys[r][i]))
        if max_row != i:
            m_sys[i], m_sys[max_row] = m_sys[max_row], m_sys[i]
        pivot = m_sys[i][i]
        for j in range(i, n + 1):
            m_sys[i][j] /= pivot
        for r in range(n):
            if r != i:
                factor = m_sys[r][i]
                if factor != 0.0:
                    for j in range(i, n + 1):
                        m_sys[r][j] -= factor * m_sys[i][j]
    return [m_sys[i][n] for i in range(n)]


def unconstrained_mv(sigma: list[list[float]], mu: list[float], gamma: float) -> list[float]:
    """Compute unconstrained mean-variance weights satisfying iota' w = 1."""
    n = len(mu)
    sys_a = [[0.0] * (n + 1) for _ in range(n + 1)]
    sys_b = [0.0] * (n + 1)
    for i in range(n):
        for j in range(n):
            sys_a[i][j] = gamma * sigma[i][j]
        sys_a[i][n] = 1.0
        sys_b[i] = mu[i]
    for j in range(n):
        sys_a[n][j] = 1.0
    sys_b[n] = 1.0

    sol = _solve_linear(sys_a, sys_b)
    return sol[:n]


def main() -> None:
    rng = random.Random(42)
    mu_true = [0.08, 0.07, 0.05, 0.03]
    sigma_true = [
        [0.0400, 0.0100, 0.0050, 0.0020],
        [0.0100, 0.0350, 0.0080, 0.0040],
        [0.0050, 0.0080, 0.0250, 0.0060],
        [0.0020, 0.0040, 0.0060, 0.0150],
    ]
    gamma = 2.5
    w_true = unconstrained_mv(sigma_true, mu_true, gamma)

    # Cholesky decomposition of Sigma_true
    chol = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(i + 1):
            s = sum(chol[i][k] * chol[j][k] for k in range(j))
            if i == j:
                chol[i][j] = math.sqrt(sigma_true[i][i] - s)
            else:
                chol[i][j] = (sigma_true[i][j] - s) / chol[j][j]

    m_sims = 200
    t_window = 60
    resampled_weights: list[list[float]] = []

    for _ in range(m_sims):
        window: list[list[float]] = []
        for _ in range(t_window):
            z = [rng.gauss(0.0, 1.0) for _ in range(4)]
            r = [mu_true[i] + sum(chol[i][k] * z[k] for k in range(4)) for i in range(4)]
            window.append(r)

        # Estimate sample mean and sample covariance
        mu_hat = [sum(window[t][i] for t in range(t_window)) / t_window for i in range(4)]
        s_mat = [[0.0] * 4 for _ in range(4)]
        for t in range(t_window):
            for i in range(4):
                for j in range(4):
                    s_mat[i][j] += (window[t][i] - mu_hat[i]) * (window[t][j] - mu_hat[j])
        for i in range(4):
            for j in range(4):
                s_mat[i][j] /= t_window - 1

        w_hat = unconstrained_mv(s_mat, mu_hat, gamma)
        resampled_weights.append(w_hat)

    print("True weights:", [round(x, 4) for x in w_true])
    for i in range(4):
        vals = [w[i] for w in resampled_weights]
        mean_val = sum(vals) / m_sims
        std_val = math.sqrt(sum((x - mean_val) ** 2 for x in vals) / (m_sims - 1))
        print(f"Asset {i}: mean={mean_val:.4f}, sd={std_val:.4f}, min={min(vals):.4f}, max={max(vals):.4f}")


main()
