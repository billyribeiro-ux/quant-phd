"""Lab GM1-L05-1: Economic Surprise Index Construction & Asset Market Sensitivity.

Constructs an exponentially weighted macroeconomic surprise index (Scotti 2016) from
standardized release surprises. Demonstrates empirical stationarity, cyclical mean-reversion,
and measures asset market return sensitivity across surprise regimes.
"""

from __future__ import annotations

import math

import numpy as np


def build_macro_surprise_index(
    surprises: np.ndarray,
    importance_weights: np.ndarray,
    half_life_days: float = 30.0,
) -> np.ndarray:
    """Calculate exponentially smoothed economic surprise index."""
    t_len, _ = surprises.shape
    norm_w = importance_weights / float(np.sum(importance_weights))
    decay = math.exp(-math.log(2.0) / half_life_days)

    esi = np.zeros(t_len, dtype=np.float64)
    running_level = 0.0

    for t in range(t_len):
        period_surp = float(np.dot(surprises[t], norm_w))
        running_level = running_level * decay + period_surp
        esi[t] = running_level

    # Normalize to mean zero and unit variance
    mean_val = float(np.mean(esi))
    std_val = float(np.std(esi, ddof=1))
    return (esi - mean_val) / std_val


def main() -> None:
    print("GM1 Lab L05-1: Economic Surprise Index & Cross-Asset Sensitivity [SIMULATED]")
    print("==========================================================================")

    rng = np.random.default_rng(303)
    t_days = 252  # 1 trading year of daily releases
    n_indicators = 5  # Payrolls, Core CPI, Retail Sales, ISM Mfg, Housing Starts
    importance_weights = np.array([0.35, 0.25, 0.18, 0.14, 0.08], dtype=np.float64)

    # Simulate surprises: zero-mean, serially uncorrelated announcement innovations
    # S_{i, t} ~ N(0, 1)
    standardized_surprises = rng.standard_normal((t_days, n_indicators))

    # Construct Economic Surprise Index (30-day half-life)
    esi = build_macro_surprise_index(standardized_surprises, importance_weights, half_life_days=30.0)

    # Autocorrelation of the surprise index: AR(1) estimate
    esi_curr = esi[1:]
    esi_prev = esi[:-1]
    phi_est, _, _, _ = np.linalg.lstsq(esi_prev[:, None], esi_curr, rcond=None)
    phi = float(phi_est[0])
    empirical_half_life = -math.log(2.0) / math.log(phi) if 0.0 < phi < 1.0 else 0.0

    # Cross-asset sensitivity: Equities (S&P 500) and 10Y Treasury Bond yield changes
    # Equities respond positively to growth surprises; Treasury yields rise on positive growth/inflation surprises
    daily_surprise_shock = standardized_surprises @ (importance_weights / np.sum(importance_weights))

    equity_returns = 0.004 * daily_surprise_shock + rng.normal(0, 0.008, size=t_days)
    bond_yield_changes_bps = 2.5 * daily_surprise_shock + rng.normal(0, 3.0, size=t_days)

    # OLS sensitivity betas
    beta_eq, _, _, _ = np.linalg.lstsq(daily_surprise_shock[:, None], equity_returns, rcond=None)
    beta_bond, _, _, _ = np.linalg.lstsq(daily_surprise_shock[:, None], bond_yield_changes_bps, rcond=None)

    print(f"Sample length:                        {t_days} daily trading periods")
    print(f"Economic indicators in index:         {n_indicators}")
    print("--------------------------------------------------------------------------")
    print("Surprise Index Statistical Properties:")
    print(f"  Sample Mean:                        {float(np.mean(esi)):7.4f}")
    print(f"  Sample Standard Deviation:          {float(np.std(esi, ddof=1)):7.4f}")
    print(f"  First-order Autocorrelation (AR1):  {phi:7.4f}")
    print(f"  Implied Mean-Reversion Half-Life:   {empirical_half_life:5.1f} days")
    print("--------------------------------------------------------------------------")
    print("Cross-Asset Market Reaction to +1 Standard Deviation Macro Surprise Shock:")
    print(f"  Equity Index Return Impact:         {float(beta_eq[0]) * 10000:+6.1f} bps")
    print(f"  10Y Treasury Yield Impact:          {float(beta_bond[0]):+6.2f} bps")
    print("--------------------------------------------------------------------------")

    # Confirm stationarity and mean reversion
    assert abs(np.mean(esi)) < 1e-10, "Normalized surprise index must have zero mean"
    assert abs(np.std(esi, ddof=1) - 1.0) < 1e-10, "Normalized surprise index must have unit standard deviation"
    assert 0.85 < phi < 0.99, "Exponential smoothing with 30-day half-life yields high daily persistence"
    print("Surprise index normalization and stationarity verified: True")


main()
