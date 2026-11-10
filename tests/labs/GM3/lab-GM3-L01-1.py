"""Lab GM3-L01-1: High-Frequency Monetary Surprise Identification.

Implements the Kuttner (2001) Fed funds futures scaling formula and estimates
the Bernanke & Kuttner (2005) equity sensitivity regression.
"""

from __future__ import annotations

import math

import numpy as np


def compute_kuttner_surprises(
    pre_rates: np.ndarray,
    post_rates: np.ndarray,
    days_in_month: np.ndarray,
    announcement_days: np.ndarray,
) -> np.ndarray:
    """Compute discrete target rate surprises in basis points using Kuttner (2001) formula."""
    delta_f = post_rates - pre_rates
    n = len(pre_rates)
    surprises = np.zeros(n, dtype=np.float64)
    for i in range(n):
        m = float(days_in_month[i])
        d = float(announcement_days[i])
        scale = 1.0 if d >= m - 1 else m / (m - d)
        surprises[i] = scale * delta_f[i] * 100.0
    return surprises


def regress_ols(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Perform simple OLS regression y = alpha + beta * x + epsilon."""
    n = len(x)
    mean_x = float(np.mean(x))
    mean_y = float(np.mean(y))
    ss_xx = float(np.sum((x - mean_x) ** 2))
    ss_xy = float(np.sum((x - mean_x) * (y - mean_y)))
    beta = ss_xy / ss_xx
    alpha = mean_y - beta * mean_x
    residuals = y - (alpha + beta * x)
    ss_res = float(np.sum(residuals**2))
    ss_tot = float(np.sum((y - mean_y) ** 2))
    r2 = 1.0 - (ss_res / ss_tot)
    se_beta = math.sqrt((ss_res / (n - 2)) / ss_xx)
    t_stat = beta / se_beta
    return {
        "alpha": alpha,
        "beta": beta,
        "r2": r2,
        "t_stat": t_stat,
        "se_beta": se_beta,
    }


def main() -> None:
    rng = np.random.default_rng(42)
    n_meetings = 100

    # Calendar metadata: M in {28, 30, 31}, d in [2, M-2]
    days_in_month = rng.choice([28, 30, 31], size=n_meetings, p=[0.08, 0.35, 0.57])
    announcement_days = np.array([int(rng.integers(2, int(m) - 2)) for m in days_in_month], dtype=int)

    # True latent discrete target surprise in basis points (mean 0, std ~ 7 bps)
    true_surprises_bps = rng.normal(0.0, 7.0, size=n_meetings)

    # Derive pre and post futures rates
    pre_rates = 3.5 + np.cumsum(rng.normal(0.0, 0.05, size=n_meetings))
    scale_factors = days_in_month / (days_in_month - announcement_days)
    futures_jumps_bps = true_surprises_bps / scale_factors
    post_rates = pre_rates + (futures_jumps_bps / 100.0)

    # Calculate Kuttner surprises
    estimated_surprises = compute_kuttner_surprises(pre_rates, post_rates, days_in_month, announcement_days)

    # Equity return reaction per Bernanke & Kuttner (2005): beta ~ -4.7 (% return per 100 bps surprise)
    # in basis points: return_bps = -0.047 * surprise_bps + noise
    equity_returns_bps = -0.0468 * estimated_surprises + rng.normal(0.0, 12.0, size=n_meetings)

    reg = regress_ols(estimated_surprises, equity_returns_bps)

    print("Kuttner Surprises Identified:", len(estimated_surprises))
    print("Mean Surprise (bps):", round(float(np.mean(estimated_surprises)), 4))
    print("Std Surprise (bps):", round(float(np.std(estimated_surprises, ddof=1)), 4))
    print("OLS Alpha (bps):", round(reg["alpha"], 4))
    print("OLS Beta (equity sensitivity):", round(reg["beta"], 4))
    print("OLS t-statistic:", round(reg["t_stat"], 4))
    print("OLS R-squared:", round(reg["r2"], 4))


main()
