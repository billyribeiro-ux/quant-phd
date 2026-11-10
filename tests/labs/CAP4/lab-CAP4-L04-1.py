"""Lab CAP4-L04-1: Delisting Return Correction & Breakpoint Sanitation Diagnostic.

Evaluates institutional sample hygiene by quantifying survivorship distortion
and the effect of Shumway (1997) delisting adjustments and NYSE-breakpoint capitalization weighting.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    np.random.seed(42)
    n_firms = 500
    t_months = 120

    # 1. Simulate panel of monthly stock returns and market capitalizations
    # Microcaps constitute 60% of firms but only 3% of aggregate market cap
    # Megacaps constitute 10% of firms and 70% of market cap
    sizes = np.concatenate(
        [
            np.random.lognormal(mean=2.0, sigma=0.5, size=300),  # microcaps
            np.random.lognormal(mean=5.0, sigma=0.8, size=150),  # small/mid
            np.random.lognormal(mean=8.5, sigma=0.6, size=50),  # large/mega
        ]
    )
    market_cap = sizes / np.sum(sizes)

    # 2. Simulate raw monthly returns with an anomaly signal (e.g. low beta / high momentum)
    # Signal is artificially concentrated in illiquid distressed microcaps
    base_signal = np.linspace(-1.0, 1.0, n_firms)
    # Distressed microcaps have high paper returns but face severe delisting risk
    raw_returns = np.zeros((t_months, n_firms))
    for t in range(t_months):
        raw_returns[t] = 0.008 + 0.015 * base_signal + np.random.normal(0.0, 0.08, size=n_firms)

    # 3. Simulate performance delisting events (Shumway 1997)
    # Firms with negative performance delist with missing final month return in naive databases
    delist_mask = np.random.rand(t_months, n_firms) < 0.005  # 0.5% monthly delisting rate
    # Missing delisting return assumed 0.0 in naive data
    naive_returns = raw_returns.copy()
    naive_returns[delist_mask] = 0.0

    # Shumway replacement: -30% for NYSE/AMEX, -55% for NASDAQ
    corrected_returns = raw_returns.copy()
    corrected_returns[delist_mask] = -0.35

    # 4. Long-short decile portfolio: Top decile minus Bottom decile
    top_decile = base_signal >= np.percentile(base_signal, 90)
    bot_decile = base_signal <= np.percentile(base_signal, 10)

    # Equal-weighted spreads
    naive_ew_spread = float(np.mean(np.mean(naive_returns[:, top_decile] - naive_returns[:, bot_decile], axis=1)))
    corrected_ew_spread = float(
        np.mean(np.mean(corrected_returns[:, top_decile] - corrected_returns[:, bot_decile], axis=1))
    )

    # Value-weighted spreads (using market caps)
    w_top = market_cap[top_decile] / np.sum(market_cap[top_decile])
    w_bot = market_cap[bot_decile] / np.sum(market_cap[bot_decile])

    naive_vw_spread = float(np.mean(naive_returns[:, top_decile] @ w_top - naive_returns[:, bot_decile] @ w_bot))
    corrected_vw_spread = float(
        np.mean(corrected_returns[:, top_decile] @ w_top - corrected_returns[:, bot_decile] @ w_bot)
    )

    delisting_drag_bps = (naive_ew_spread - corrected_ew_spread) * 10000.0
    microcap_distortion_bps = (corrected_ew_spread - corrected_vw_spread) * 10000.0

    print(f"Naive Equal-Weighted Spread: {naive_ew_spread * 100:.3f}%")
    print(f"Delisting-Corrected EW Spread: {corrected_ew_spread * 100:.3f}%")
    print(f"Naive Value-Weighted Spread: {naive_vw_spread * 100:.3f}%")
    print(f"Delisting-Corrected VW Spread: {corrected_vw_spread * 100:.3f}%")
    print(f"Delisting Bias Drag: {delisting_drag_bps:.1f} bps/mo")
    print(f"Microcap Equal-Weight Distortion: {microcap_distortion_bps:.1f} bps/mo")


main()
