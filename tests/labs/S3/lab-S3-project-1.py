"""Lab S3-project-1: Rung 1 worked example for pairs-trading audit.

SIMULATED: complete worked audit of a seeded cointegration candidate pair.
"""

from __future__ import annotations

import math
import random


def ols_1d(y: list[float], x: list[float]) -> tuple[float, float]:
    m = len(y)
    mx = sum(x) / m
    my = sum(y) / m
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(m))
    var_x = sum((x[i] - mx) ** 2 for i in range(m))
    beta = cov / var_x
    alpha = my - beta * mx
    return alpha, beta


def eg_statistic(y: list[float], x: list[float], split: int) -> float:
    a, b = ols_1d(y[:split], x[:split])
    u = [y[t] - a - b * x[t] for t in range(split)]
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


def half_life(spread: list[float]) -> float:
    y = spread[1:]
    x = spread[:-1]
    _, phi = ols_1d(y, x)
    if phi <= 0.0:
        raise ValueError("phi <= 0")
    if phi >= 1.0:
        return math.inf
    return math.log(2.0) / (-math.log(phi))


def main() -> None:
    rng = random.Random(42)
    n = 400
    split = 240
    eg_crit_5pct = -3.3378

    # Generate synthetic cointegrated pair
    rw = [0.0]
    for _ in range(n - 1):
        rw.append(rw[-1] + rng.gauss(0.0, 1.0))
    x = [50.0 + rw[t] for t in range(n)]
    s = [0.0]
    for _ in range(n - 1):
        s.append(0.75 * s[-1] + rng.gauss(0.0, 0.5))
    y = [2.0 + 1.2 * x[t] + s[t] for t in range(n)]

    # Step 1: Formation hedge ratio
    alpha, beta = ols_1d(y[:split], x[:split])

    # Step 2: Engle-Granger test on formation window
    eg_stat = eg_statistic(y, x, split)
    eg_pass = eg_stat < eg_crit_5pct

    # Step 3: Out-of-sample trading spread and half-life
    trading_spread = [y[t] - alpha - beta * x[t] for t in range(split, n)]
    hl = half_life(trading_spread)
    hl_finite = math.isfinite(hl)

    # Step 4: Final survival verdict
    pair_survives = eg_pass and hl_finite

    print("Pairs-Trading Audit: Worked Example (SIMULATED):")
    print(f"  Sample size: n={n} (Formation split={split}, Trading={n - split})")
    print(f"  Step 1 Formation OLS: alpha = {alpha:.4f}, beta = {beta:.4f}")
    print(f"  Step 2 EG residual t-statistic: {eg_stat:.4f} (5% critical value: {eg_crit_5pct:.4f})")
    print(f"         EG null rejected (cointegrated): {eg_pass}")
    print(f"  Step 3 Trading spread half-life: {hl:.2f} business days (finite: {hl_finite})")
    print(f"  Step 4 Audit verdict: Pair survives = {pair_survives}")


main()
