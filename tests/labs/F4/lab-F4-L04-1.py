"""Lab F4-L04-1: Anomaly Decay Decomposition and Value's Long Drawdown.

Replicates the McLean & Pontiff (2016) statistical decay across 97 published anomalies
(in-sample vs out-of-sample vs post-publication) and models the 2010-2020 value winter
valuation spread expansion and peak-to-trough drawdown.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(777)
    n_anomalies = 97

    # 1. McLean & Pontiff (2016) Anomaly Return Decay Simulation
    # In-sample monthly return benchmark: ~58 bps/month (7.0% annualized)
    in_sample_returns = rng.normal(0.0058, 0.0015, size=n_anomalies)

    # Post-sample, pre-publication: ~26% decay due to data snooping / publication bias
    oos_pre_pub_returns = in_sample_returns * (1.0 - 0.26) + rng.normal(0.0, 0.0005, size=n_anomalies)

    # Post-publication: cumulative ~58% decay (additional 32% decay from arbitrage learning)
    post_pub_returns = in_sample_returns * (1.0 - 0.58) + rng.normal(0.0, 0.0005, size=n_anomalies)

    mean_is = float(np.mean(in_sample_returns)) * 12.0
    mean_oos = float(np.mean(oos_pre_pub_returns)) * 12.0
    mean_post = float(np.mean(post_pub_returns)) * 12.0

    decay_oos = (mean_is - mean_oos) / mean_is
    decay_post = (mean_is - mean_post) / mean_is

    # 2. Value's Long Drawdown (2010-2020) and Valuation Spread Expansion
    # 120 months (2011 to 2020) of HML cumulative return and valuation spread
    n_val_months = 120
    dt = 1.0 / 12.0

    # HML suffered sustained negative drift of -4.5% annualized during tech dominance
    hml_returns = rng.normal(-0.045 * dt, 0.12 * np.sqrt(dt), size=n_val_months)
    # Severe crash in early 2020 (COVID-19 growth surge)
    hml_returns[108:114] = -0.05 + rng.normal(0.0, 0.02, size=6)

    cum_hml = np.cumprod(1.0 + hml_returns)
    peak = np.maximum.accumulate(cum_hml)
    drawdowns = (peak - cum_hml) / peak
    max_hml_dd = float(np.max(drawdowns))

    # Valuation spread (P/B of Growth vs Value): historically mean is 3.5, expands to 11.2 in 2020
    val_spread = 3.5 + 0.065 * np.arange(n_val_months) + rng.normal(0.0, 0.3, size=n_val_months)
    val_spread[108:] += 3.5  # extreme 2020 spread blow-out

    peak_spread = float(np.max(val_spread))
    base_spread = float(val_spread[0])

    print("=== MCLEAN & PONTIFF (2016) ANOMALY LIFE CYCLE DECAY ===")
    print(f"In-Sample Mean Return:        {mean_is:+.2%} annualized")
    print(f"OOS (Pre-Pub) Mean Return:    {mean_oos:+.2%} annualized (Decay: {decay_oos:.1%})")
    print(f"Post-Publication Mean Return: {mean_post:+.2%} annualized (Decay: {decay_post:.1%})")
    print("=== VALUE WINTER (2010-2020) DRAWDOWN & SPREAD DISTORTION ===")
    print(f"HML 10-Year Cumulative Return: {cum_hml[-1] - 1.0:+.2%}")
    print(f"HML Maximum Peak-to-Trough Drawdown: {max_hml_dd:.2%}")
    print(f"Valuation Spread Expansion:    {base_spread:.1f}x -> {peak_spread:.1f}x (>99th percentile)")


main()
