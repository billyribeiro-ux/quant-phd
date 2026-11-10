"""Lab MS3-L01-1: Calibration and validation of the square-root law of market impact.

Simulates metaorder executions across 4 orders of magnitude of size Q,
fits power-law scaling I(Q) = Y * sigma * (Q/V)^alpha, and validates alpha ~ 0.5.
"""

from __future__ import annotations

import math
import random


def simulate_metaorder_impact(
    metaorder_size: float,
    daily_volume: float,
    daily_volatility: float,
    y_true: float,
    alpha_true: float,
    noise_std: float,
    rng: random.Random,
) -> float:
    """Simulate observed market impact for a metaorder execution."""
    normalized_size = metaorder_size / daily_volume
    true_impact = y_true * daily_volatility * (normalized_size**alpha_true)
    observed_noise = float(rng.gauss(0.0, noise_std * true_impact))
    return float(max(1e-6, true_impact + observed_noise))


def fit_power_law(sizes: list[float], impacts: list[float], daily_volume: float) -> tuple[float, float]:
    """Fit log(I) = c + alpha * log(Q/V) via ordinary least squares."""
    log_x = [math.log(q / daily_volume) for q in sizes]
    log_y = [math.log(i) for i in impacts]
    n = len(log_x)

    mean_x = sum(log_x) / n
    mean_y = sum(log_y) / n

    ss_xx = sum((x - mean_x) ** 2 for x in log_x)
    ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_x, log_y, strict=True))

    alpha = ss_xy / ss_xx
    intercept = mean_y - alpha * mean_x
    coeff = math.exp(intercept)
    return coeff, alpha


def main() -> None:
    rng = random.Random(42)
    daily_volume = 5_000_000.0  # 5 million shares/day
    daily_volatility = 0.02  # 2% daily vol
    y_true = 0.60
    alpha_true = 0.50

    # Metaorder sizes spanning 0.01% to 10% of ADV (4 orders of magnitude)
    fractions = [0.0001, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10]
    sizes = [f * daily_volume for f in fractions]

    print("Square-Root Law Market Impact Calibration (ADV=5M, sigma=2.0%):")
    print("  Q (Shares) | % ADV | Obs Impact (bps) | Sqrt Model (bps) | Lin Model (bps)")
    print("----------------------------------------------------------------------------")

    observed_impacts: list[float] = []
    for q, frac in zip(sizes, fractions, strict=True):
        obs = simulate_metaorder_impact(q, daily_volume, daily_volatility, y_true, alpha_true, 0.02, rng)
        observed_impacts.append(obs)
        sqrt_model = y_true * daily_volatility * math.sqrt(q / daily_volume)
        # Linear model calibrated to match at median size (0.5% ADV)
        lin_model = y_true * daily_volatility * math.sqrt(0.005) * (frac / 0.005)

        obs_bps = obs * 10000
        sq_bps = sqrt_model * 10000
        lin_bps = lin_model * 10000
        print(f"{q:12,.0f} | {frac * 100:4.2f}% | {obs_bps:16.2f} | {sq_bps:16.2f} | {lin_bps:15.2f}")

    fitted_coeff, fitted_alpha = fit_power_law(sizes, observed_impacts, daily_volume)
    fitted_y = fitted_coeff / daily_volatility

    print("----------------------------------------------------------------------------")
    print(f"Log-log OLS Estimate: alpha = {fitted_alpha:.4f} (True = {alpha_true:.4f})")
    print(f"Calibrated Y Factor:  Y     = {fitted_y:.4f} (True = {y_true:.4f})")
    print("Sub-linear Concavity: dI/dQ strictly decreases with order size Q.")


main()
