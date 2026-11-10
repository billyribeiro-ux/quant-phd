"""Lab S3-L04-1: Spurious regression generator on independent random walks.

SIMULATED: generates independent random walks and measures the empirical
rejection rate of the nominal 5% t-test, average R^2, and Durbin-Watson statistic.
"""

from __future__ import annotations

import math
import random


def run_spurious_trial(n: int, rng: random.Random) -> tuple[float, float, float]:
    """Simulate one pair of independent random walks and regress y on x."""
    x = [0.0]
    y = [0.0]
    for _ in range(n - 1):
        x.append(x[-1] + rng.gauss(0.0, 1.0))
        y.append(y[-1] + rng.gauss(0.0, 1.0))

    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    var_y = sum((y[i] - mean_y) ** 2 for i in range(n))

    beta = cov / var_x
    alpha = mean_y - beta * mean_x
    res = [y[i] - alpha - beta * x[i] for i in range(n)]
    rss = sum(r * r for r in res)
    r2 = 1.0 - rss / var_y if var_y > 0.0 else 0.0

    s2 = rss / (n - 2)
    se_beta = math.sqrt(s2 / var_x)
    t_stat = beta / se_beta
    dw = sum((res[i] - res[i - 1]) ** 2 for i in range(1, n)) / rss if rss > 0.0 else 0.0
    return t_stat, r2, dw


def main() -> None:
    reps = 2000
    n = 200
    rng = random.Random(42)

    rejections = 0
    sum_r2 = 0.0
    sum_dw = 0.0

    for _ in range(reps):
        t_stat, r2, dw = run_spurious_trial(n, rng)
        if abs(t_stat) > 1.95996:
            rejections += 1
        sum_r2 += r2
        sum_dw += dw

    rej_rate = rejections / reps
    mean_r2 = sum_r2 / reps
    mean_dw = sum_dw / reps

    print(f"Spurious Regression Simulation (R={reps}, T={n}, seed=42)")
    print("Nominal test size: 0.0500 (two-sided critical value 1.96)")
    print(f"Empirical rejection rate: {rej_rate:.4f} ({rejections}/{reps} trials)")
    print(f"Mean R-squared: {mean_r2:.4f} (theoretical under independence: ~0.0)")
    print(f"Mean Durbin-Watson statistic: {mean_dw:.4f} (ideal stationary residuals: ~2.0)")


main()
