"""Lab S3-L01-1: Sample autocorrelation function of an AR(1) process.

SIMULATED: generates a stationary AR(1) series and compares the empirical
sample autocorrelation function against the theoretical closed-form powers phi^h.
"""

from __future__ import annotations

import random


def simulate_ar1(phi: float, sigma: float, n: int, seed: int = 42) -> list[float]:
    """Generate stationary AR(1) path with burn-in."""
    rng = random.Random(seed)
    burn = 100
    y = 0.0
    for _ in range(burn):
        y = phi * y + rng.gauss(0.0, sigma)
    series: list[float] = []
    for _ in range(n):
        y = phi * y + rng.gauss(0.0, sigma)
        series.append(y)
    return series


def sample_acf(series: list[float], max_lag: int) -> list[float]:
    """Compute sample autocorrelations for lags 0 through max_lag."""
    n = len(series)
    mean_y = sum(series) / n
    demeaned = [val - mean_y for val in series]
    gamma0 = sum(d * d for d in demeaned) / n
    acf: list[float] = [1.0]
    for h in range(1, max_lag + 1):
        gamma_h = sum(demeaned[t] * demeaned[t + h] for t in range(n - h)) / n
        acf.append(gamma_h / gamma0)
    return acf


def main() -> None:
    phi = 0.70
    sigma = 1.0
    n = 500
    series = simulate_ar1(phi, sigma, n, seed=42)

    max_lag = 5
    emp_acf = sample_acf(series, max_lag)

    print(f"AR(1) Simulation (phi={phi:.2f}, n={n})")
    print(f"Sample mean: {sum(series) / n:+.4f} (theoretical: 0.0000)")
    mean_y = sum(series) / n
    var_emp = sum((v - mean_y) ** 2 for v in series) / n
    var_theo = (sigma**2) / (1.0 - phi**2)
    print(f"Sample variance: {var_emp:.4f} (theoretical: {var_theo:.4f})")
    print("Lag | Sample ACF | Theoretical | Diff")
    print("-" * 37)
    for h in range(1, max_lag + 1):
        theo = phi**h
        diff = emp_acf[h] - theo
        print(f"  {h} |    {emp_acf[h]:.4f}  |     {theo:.4f}  | {diff:+.4f}")


main()
