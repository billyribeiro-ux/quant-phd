"""Lab S3-L03-1: Dickey-Fuller test distribution under the null.

SIMULATED: generates empirical distribution of the Dickey-Fuller t-statistic
under the null hypothesis of a unit root, demonstrating its leftward shift
relative to the standard normal distribution.
"""

from __future__ import annotations

import math
import random


def df_t_statistic(y: list[float]) -> float:
    """Compute DF t-statistic for regression with intercept: Delta y_t = alpha + gamma * y_{t-1} + e_t."""
    m = len(y)
    dy = [y[t] - y[t - 1] for t in range(1, m)]
    x = [y[t - 1] for t in range(1, m)]
    n_obs = len(dy)
    mean_x = sum(x) / n_obs
    mean_y = sum(dy) / n_obs
    cov = sum((x[i] - mean_x) * (dy[i] - mean_y) for i in range(n_obs))
    var_x = sum((x[i] - mean_x) ** 2 for i in range(n_obs))
    gamma = cov / var_x
    alpha = mean_y - gamma * mean_x
    res = [dy[i] - alpha - gamma * x[i] for i in range(n_obs)]
    s2 = sum(r * r for r in res) / (n_obs - 2)
    se_gamma = math.sqrt(s2 / var_x)
    return gamma / se_gamma


def main() -> None:
    reps = 2500
    n = 250
    rng = random.Random(42)

    t_stats: list[float] = []
    for _ in range(reps):
        y = [0.0]
        for _ in range(n - 1):
            y.append(y[-1] + rng.gauss(0.0, 1.0))
        t_stats.append(df_t_statistic(y))

    t_stats.sort()
    q01 = t_stats[int(0.01 * reps)]
    q05 = t_stats[int(0.05 * reps)]
    q10 = t_stats[int(0.10 * reps)]
    mean_t = sum(t_stats) / reps

    print(f"Dickey-Fuller Simulation (R={reps}, T={n}, seed=42)")
    print(f"Empirical mean of t_gamma: {mean_t:.4f} (Standard Normal: 0.0000)")
    print("\nQuantile Comparison:")
    print("Level | Empirical DF | Standard Normal | Shift")
    print("-" * 47)
    print(f"   1% |     {q01:.4f}   |     -2.3263     | {q01 - (-2.3263):+.4f}")
    print(f"   5% |     {q05:.4f}   |     -1.6449     | {q05 - (-1.6449):+.4f}")
    print(f"  10% |     {q10:.4f}   |     -1.2816     | {q10 - (-1.2816):+.4f}")


main()
