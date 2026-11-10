"""Deterministic instance generator for AP7 Sentiment-Index Replication.

Generates monthly sentiment proxy panels, macroeconomic control variables,
and test asset cross-sections across reproducible pseudo-random seeds.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic synthetic market, proxy, and test asset series for seed.

    Parameters
    ----------
    seed : int
        RNG seed ensuring distinct, reproducible problem instances.

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
        - raw_proxies: (T, 6) array of 6 raw sentiment proxies
        - macro_controls: (T, 4) array of 4 macroeconomic controls
        - test_assets_returns: (T, 8) array of monthly returns for 8 sorted portfolios
        - market_returns: (T,) array of aggregate market excess returns
        - proxy_names: list of 6 proxy string identifiers
        - asset_names: list of 8 test asset string identifiers
    """
    rng = np.random.default_rng(seed)
    n_periods = 180  # 15 years of monthly observations

    # 1. 4 Macroeconomic control series (IP growth, consumption growth, term spread, default spread)
    macro_means = np.array([0.002, 0.0015, 0.015, 0.010])
    macro_stds = np.array([0.008, 0.006, 0.007, 0.005])
    macro = rng.normal(macro_means, macro_stds, size=(n_periods, 4))

    # 2. Latent market sentiment AR(1) state variable
    phi_sentiment = 0.82
    latent_sentiment = np.zeros(n_periods)
    sentiment_shocks = rng.normal(0.0, 0.6, size=n_periods)
    for t in range(1, n_periods):
        latent_sentiment[t] = phi_sentiment * latent_sentiment[t - 1] + sentiment_shocks[t]

    # Standardize latent sentiment state
    latent_sentiment = (latent_sentiment - np.mean(latent_sentiment)) / np.std(latent_sentiment, ddof=1)

    # 3. 6 Sentiment proxies:
    # 0: CEFD (closed-end fund discount, negative loading)
    # 1: TURN (detrended turnover, positive loading)
    # 2: NIPO (number of IPOs, positive loading - anchor)
    # 3: RIPO (first-day IPO return, positive loading)
    # 4: S (equity share in new issues, positive loading)
    # 5: PDND (dividend premium, negative loading)
    proxy_loadings = np.array([-0.65, 0.70, 0.85, 0.75, 0.80, -0.60])
    macro_beta_matrix = rng.normal(0.20, 0.10, size=(6, 4))

    raw_proxies = np.zeros((n_periods, 6))
    for k in range(6):
        macro_component = macro @ macro_beta_matrix[k]
        noise = rng.normal(0.0, 0.40, size=n_periods)
        raw_proxies[:, k] = proxy_loadings[k] * latent_sentiment + macro_component + noise

    # 4. Market excess returns
    market_returns = rng.normal(0.007, 0.045, size=n_periods)

    # 5. 8 Test portfolios:
    # 0-3: Hard-to-value, speculative, difficult-to-arbitrage (Small, HighVol, Growth, HighBeta)
    # 4-7: Easy-to-value, safe, bond-like (Large, LowVol, DividendPayers, Quality)
    test_assets = np.zeros((n_periods, 8))
    base_expected_returns = np.array([0.011, 0.012, 0.010, 0.011, 0.008, 0.007, 0.007, 0.008])
    market_loadings = np.array([1.30, 1.40, 1.35, 1.25, 0.95, 0.85, 0.80, 0.90])

    # Sensitivity to lagged sentiment: speculative assets underperform following high sentiment
    sentiment_sensitivities = np.array([-0.022, -0.025, -0.020, -0.018, 0.002, 0.004, 0.003, 0.001])

    for i in range(8):
        idiosyncratic_noise = rng.normal(0.0, 0.035, size=n_periods)
        lagged_sentiment_effect = np.zeros(n_periods)
        lagged_sentiment_effect[1:] = sentiment_sensitivities[i] * latent_sentiment[:-1]
        market_component = market_loadings[i] * market_returns
        test_assets[:, i] = base_expected_returns[i] + market_component + lagged_sentiment_effect + idiosyncratic_noise

    return {
        "raw_proxies": raw_proxies,
        "macro_controls": macro,
        "test_assets_returns": test_assets,
        "market_returns": market_returns,
        "proxy_names": ["CEFD", "TURN", "NIPO", "RIPO", "S", "PDND"],
        "asset_names": [
            "SmallCap",
            "HighVolatility",
            "ExtremeGrowth",
            "HighBeta",
            "LargeCap",
            "LowVolatility",
            "DividendPayer",
            "HighQuality",
        ],
    }
