"""Lab S3-L02-1: ARMA(1,1) autocovariances and causality-invertibility roots.

SIMULATED for the empirical simulation path; exact for root calculations and
closed-form autocovariances.
"""

from __future__ import annotations

import random


def simulate_arma11(phi: float, theta: float, sigma: float, n: int, seed: int = 42) -> list[float]:
    """Generate ARMA(1,1) path: y_t = phi * y_{t-1} + e_t + theta * e_{t-1}."""
    rng = random.Random(seed)
    burn = 150
    y = 0.0
    prev_e = 0.0
    for _ in range(burn):
        e = rng.gauss(0.0, sigma)
        y = phi * y + e + theta * prev_e
        prev_e = e
    series: list[float] = []
    for _ in range(n):
        e = rng.gauss(0.0, sigma)
        y = phi * y + e + theta * prev_e
        prev_e = e
        series.append(y)
    return series


def sample_autocovariances(series: list[float], max_lag: int) -> list[float]:
    """Compute sample autocovariances for lags 0 through max_lag."""
    n = len(series)
    mean_y = sum(series) / n
    demeaned = [val - mean_y for val in series]
    gamma: list[float] = []
    for h in range(max_lag + 1):
        gamma_h = sum(demeaned[t] * demeaned[t + h] for t in range(n - h)) / n
        gamma.append(gamma_h)
    return gamma


def main() -> None:
    phi = 0.60
    theta = 0.40
    sigma = 1.0
    n = 3000

    # Root conditions
    root_ar = 1.0 / phi
    root_ma = -1.0 / theta
    is_causal = abs(root_ar) > 1.0
    is_invertible = abs(root_ma) > 1.0

    print("ARMA(1,1) Root Analysis:")
    print(f"  AR root z = 1/phi = {root_ar:.4f} (|z| > 1: {is_causal}, causal)")
    print(f"  MA root z = -1/theta = {root_ma:.4f} (|z| > 1: {is_invertible}, invertible)")

    # Closed-form autocovariances
    gamma0_theo = (sigma**2) * (1.0 + theta**2 + 2.0 * phi * theta) / (1.0 - phi**2)
    gamma1_theo = phi * gamma0_theo + theta * (sigma**2)
    gamma2_theo = phi * gamma1_theo
    gamma3_theo = phi * gamma2_theo
    theo_gammas = [gamma0_theo, gamma1_theo, gamma2_theo, gamma3_theo]

    series = simulate_arma11(phi, theta, sigma, n, seed=42)
    emp_gammas = sample_autocovariances(series, 3)

    print("\nAutocovariances (T=3000, seed=42):")
    print("Lag | Sample gamma(h) | Closed Form | Diff")
    print("-" * 43)
    for h in range(4):
        diff = emp_gammas[h] - theo_gammas[h]
        print(f"  {h} |     {emp_gammas[h]:.4f}      |   {theo_gammas[h]:.4f}    | {diff:+.4f}")


main()
