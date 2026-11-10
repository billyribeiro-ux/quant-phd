"""Lab F4-project-1: Project Rung 1 - Worked Example on Volatility-Managed Momentum.

Demonstrates the core mechanics of constructing dollar-neutral WML weights,
estimating strictly causal trailing realized volatility, and applying inverse-volatility
scaling with leverage caps.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(123)
    n_months = 120
    n_stocks = 20

    # Simulate stock returns with positive momentum drift
    rets = rng.normal(0.008, 0.05, size=(n_months, n_stocks))

    # Signal: past 12-month return skipping month t-1
    signals = np.zeros_like(rets)
    for t in range(12, n_months):
        signals[t] = np.sum(rets[t - 12 : t - 1], axis=0)

    # Dollar-neutral weights: top 4 long (+0.25 each), bottom 4 short (-0.25 each)
    weights = np.zeros_like(rets)
    for t in range(12, n_months):
        ranks = np.argsort(np.argsort(signals[t]))
        weights[t, ranks >= (n_stocks - 4)] = 0.25
        weights[t, ranks < 4] = -0.25

    # Unscaled WML returns
    wml_raw = np.sum(weights * rets, axis=1)

    # Causal realized volatility (6-month trailing window)
    vol_est = np.zeros(n_months)
    for t in range(n_months):
        hist = wml_raw[max(0, t - 6) : t]
        vol_est[t] = 0.15 if len(hist) < 3 else max(0.04, float(np.std(hist, ddof=1)) * np.sqrt(12.0))

    # Scaled weights: target vol 0.12, max leverage 2.0
    w_vol = np.clip(0.12 / vol_est, 0.0, 2.0)
    wml_scaled = w_vol * wml_raw

    # Performance
    sh_raw = float(np.mean(wml_raw[12:])) / max(1e-6, float(np.std(wml_raw[12:], ddof=1))) * np.sqrt(12.0)
    sh_scaled = float(np.mean(wml_scaled[12:])) / max(1e-6, float(np.std(wml_scaled[12:], ddof=1))) * np.sqrt(12.0)

    cum_raw = np.cumprod(1.0 + wml_raw[12:])
    cum_scaled = np.cumprod(1.0 + wml_scaled[12:])
    dd_raw = float(np.max((np.maximum.accumulate(cum_raw) - cum_raw) / np.maximum.accumulate(cum_raw)))
    dd_scaled = float(np.max((np.maximum.accumulate(cum_scaled) - cum_scaled) / np.maximum.accumulate(cum_scaled)))

    print("=== PROJECT RUNG 1: VOLATILITY-SCALED MOMENTUM WORKED EXAMPLE ===")
    print(f"Raw WML:        Annualized Sharpe={sh_raw:.2f}, Max Drawdown={dd_raw:.2%}")
    print(f"Vol-Scaled WML: Annualized Sharpe={sh_scaled:.2f}, Max Drawdown={dd_scaled:.2%}")
    print(f"Mean Exposure Scalar: {float(np.mean(w_vol[12:])):.2f}x (Leverage Cap: 2.0x)")


main()
