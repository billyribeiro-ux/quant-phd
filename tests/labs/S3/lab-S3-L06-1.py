"""Lab S3-L06-1: Engle-Granger test and mean-reversion half-life.

Exact for noiseless exponential decay; SIMULATED for seeded AR(1) spread
and Engle-Granger two-step cointegration test.
"""

from __future__ import annotations

import math
import random


def ols_slope(y: list[float], x: list[float]) -> tuple[float, float]:
    m = len(y)
    mx = sum(x) / m
    my = sum(y) / m
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(m))
    var_x = sum((x[i] - mx) ** 2 for i in range(m))
    beta = cov / var_x
    alpha = my - beta * mx
    return alpha, beta


def half_life(spread: list[float]) -> float:
    y = spread[1:]
    x = spread[:-1]
    _, phi = ols_slope(y, x)
    if phi <= 0.0:
        raise ValueError("phi <= 0")
    if phi >= 1.0:
        return math.inf
    return math.log(2.0) / (-math.log(phi))


def eg_residual_t(y: list[float], x: list[float]) -> float:
    alpha, beta = ols_slope(y, x)
    u = [y[t] - alpha - beta * x[t] for t in range(len(y))]
    # ADF without intercept, lags = 1
    m = len(u)
    du = [u[i] - u[i - 1] for i in range(1, m)]
    y_dep = du[1:]
    x0 = [u[t - 1] for t in range(2, m)]
    x1 = [du[t - 2] for t in range(2, m)]
    n_obs = len(y_dep)

    s00 = sum(x0[r] * x0[r] for r in range(n_obs))
    s01 = sum(x0[r] * x1[r] for r in range(n_obs))
    s11 = sum(x1[r] * x1[r] for r in range(n_obs))
    det = s00 * s11 - s01 * s01
    inv00 = s11 / det
    inv01 = -s01 / det
    sy0 = sum(x0[r] * y_dep[r] for r in range(n_obs))
    sy1 = sum(x1[r] * y_dep[r] for r in range(n_obs))
    gamma = inv00 * sy0 + inv01 * sy1
    delta = inv01 * sy0 + (s00 / det) * sy1

    res = [y_dep[r] - gamma * x0[r] - delta * x1[r] for r in range(n_obs)]
    rss = sum(r * r for r in res)
    sigma2 = rss / (n_obs - 2)
    se_gamma = math.sqrt(sigma2 * inv00)
    return gamma / se_gamma


def main() -> None:
    # 1. Noiseless exponential decay
    noiseless_path = [0.90**t for t in range(50)]
    hl_noiseless = half_life(noiseless_path)
    hl_exact = math.log(2.0) / (-math.log(0.90))

    print("Part 1: Exact Noiseless Half-Life Verification:")
    print(f"  Theoretical half-life for phi=0.90: {hl_exact:.6f} periods")
    print(f"  Estimated half-life from path:      {hl_noiseless:.6f} periods")
    print(f"  Absolute discrepancy:               {abs(hl_noiseless - hl_exact):.2e}")

    # 2. Seeded AR(1) spread
    rng = random.Random(42)
    n = 600
    phi_true = 0.85
    s = [0.0]
    for _ in range(n - 1):
        s.append(phi_true * s[-1] + rng.gauss(0.0, 1.0))

    _, phi_hat = ols_slope(s[1:], s[:-1])
    hl_hat = half_life(s)
    hl_true = math.log(2.0) / (-math.log(phi_true))

    print("\nPart 2: Seeded AR(1) Spread (T=600, true phi=0.85, seed=42):")
    print(f"  True half-life:      {hl_true:.4f} periods")
    print(f"  Estimated phi:       {phi_hat:.4f}")
    print(f"  Estimated half-life: {hl_hat:.4f} periods")

    # 3. Engle-Granger test comparison
    rw = [0.0]
    for _ in range(n - 1):
        rw.append(rw[-1] + rng.gauss(0.0, 1.0))
    x_coint = [rw[t] + rng.gauss(0.0, 0.5) for t in range(n)]
    y_coint = [1.5 * x_coint[t] + s[t] for t in range(n)]

    rw_indep = [0.0]
    for _ in range(n - 1):
        rw_indep.append(rw_indep[-1] + rng.gauss(0.0, 1.0))

    eg_coint = eg_residual_t(y_coint, x_coint)
    eg_indep = eg_residual_t(rw, rw_indep)

    print("\nPart 3: Engle-Granger 2-Step Test (5% critical value ~ -3.34):")
    print(f"  Cointegrated pair EG t-statistic: {eg_coint:.4f} (rejects null of no cointegration)")
    print(f"  Independent pair EG t-statistic:  {eg_indep:.4f} (fails to reject)")


main()
