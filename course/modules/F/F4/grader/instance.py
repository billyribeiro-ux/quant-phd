"""Instance generator for Module F4 Project: Crash-Risk Overlay.

Generates reproducible multi-asset monthly equity panels with endogenous
momentum, panic states, asymmetric loser rebound optionality, and transaction
costs across T=360 months (30 years) and N=50 stocks.
"""

from __future__ import annotations

import functools
from typing import Any

import numpy as np


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic equity panels, market index, and crash regimes.

    Parameters
    ----------
    seed : int
        RNG seed for reproducibility.

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
        - seed: int
        - n_months: int (360)
        - n_stocks: int (50)
        - in_sample_split: int (180)
        - stock_returns: np.ndarray of shape (360, 50)
        - market_returns: np.ndarray of shape (360,)
        - risk_free_rate: float (0.02 / 12)
        - cost_bps: float (15.0 basis points)
        - panic_episodes: list of (start_idx, end_idx)
    """
    rng = np.random.default_rng(seed)
    n_months = 360
    n_stocks = 50
    in_sample_split = 180
    dt = 1.0 / 12.0
    rf = 0.02 / 12.0  # 2% annual risk-free rate
    cost_bps = 15.0

    # 1. Market Return Process with Bear Markets and Violent Rebounds
    # Base monthly market parameters: 8% expected annual excess return, 14% vol
    mu_m_base = 0.08 * dt
    sigma_m_normal = 0.14 * np.sqrt(dt)

    market_returns = np.zeros(n_months)
    regime = np.zeros(n_months, dtype=int)  # 0: normal, 1: bear/panic, 2: sharp rebound

    # Pre-determined crisis periods:
    # Crisis 1 (In-Sample): months 80..104 (Bear from 80..100, violent rebound 101..104)
    # Crisis 2 (Out-of-Sample): months 250..274 (Bear from 250..270, violent rebound 271..274)
    crisis_specs = [
        (80, 100, 101, 104),
        (250, 270, 271, 274),
    ]

    for b_start, b_end, r_start, r_end in crisis_specs:
        regime[b_start : b_end + 1] = 1
        regime[r_start : r_end + 1] = 2

    for t in range(n_months):
        if regime[t] == 0:
            market_returns[t] = mu_m_base + rng.normal(0.0, sigma_m_normal)
        elif regime[t] == 1:
            # Bear market: cumulative negative drift, high volatility
            market_returns[t] = -0.50 * dt + rng.normal(0.0, 0.04)
        else:
            # Violent rebound: massive positive surge (e.g. July-Aug 1932 or Mar-May 2009)
            market_returns[t] = 0.10 + rng.uniform(0.01, 0.06)

    # 2. Stock Returns with Cross-Sectional Factor Structure and Optionality
    # Each stock has an underlying baseline beta around 1.0
    baseline_betas = 0.70 + 0.60 * rng.uniform(0.0, 1.0, size=n_stocks)
    idio_vols = 0.20 * np.sqrt(dt) + 0.15 * np.sqrt(dt) * rng.uniform(0.0, 1.0, size=n_stocks)

    stock_returns = np.zeros((n_months, n_stocks))

    # Initialize first 12 months with market-model plus noise
    for t in range(12):
        idio = rng.normal(0.0, idio_vols)
        stock_returns[t] = rf + baseline_betas * (market_returns[t] - rf) + idio

    # Forward generation for t >= 12 with momentum continuation and panic optionality
    for t in range(12, n_months):
        past_12m = np.sum(stock_returns[t - 12 : t - 1], axis=0)  # skip t-1
        ranks = np.argsort(np.argsort(past_12m))  # 0 to n_stocks - 1

        # Decile assignments: lowest 10 are losers (ranks 0..9), highest 10 are winners (ranks 40..49)
        is_loser = ranks < 10
        is_winner = ranks >= (n_stocks - 10)

        # Baseline momentum continuation drift in normal times
        mom_drift = np.zeros(n_stocks)
        mom_drift[is_winner] = 0.08 * dt
        mom_drift[is_loser] = -0.08 * dt

        # Asymmetric Optionality / Panic State Rebound Effect (Daniel & Moskowitz 2016):
        # In rebound months (regime == 2 or market > 0 while trailing 2-year market < 0),
        # distressed losers behave like out-of-the-money call options, surging with beta ~ 3.0
        trailing_24m_mkt = np.sum(market_returns[max(0, t - 24) : t])
        is_panic_rebound = (trailing_24m_mkt < 0.0) and (market_returns[t] > 0.0) and (regime[t] >= 1)

        effective_betas = baseline_betas.copy()
        if is_panic_rebound:
            # Loser beta explodes upwards: call option delta expansion
            effective_betas[is_loser] = 3.20 + 0.40 * rng.uniform(0.0, 1.0, size=int(np.sum(is_loser)))
            # Winner beta remains anchored near 0.85
            effective_betas[is_winner] = 0.85 + 0.15 * rng.uniform(0.0, 1.0, size=int(np.sum(is_winner)))

        idio = rng.normal(0.0, idio_vols)
        stock_returns[t] = rf + mom_drift + effective_betas * (market_returns[t] - rf) + idio

    return {
        "seed": seed,
        "n_months": n_months,
        "n_stocks": n_stocks,
        "in_sample_split": in_sample_split,
        "stock_returns": stock_returns,
        "market_returns": market_returns,
        "risk_free_rate": rf,
        "cost_bps": cost_bps,
        "panic_episodes": [(80, 104), (250, 274)],
    }
