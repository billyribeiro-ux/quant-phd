"""Instance generator for CAP4: Research Thesis & Defense Capstone Grader.

Generates deterministic problem instances for the doctoral thesis replication package:
1. Data Hygiene & Delisting Adjustment (Shumway corrections and NYSE value-weighting)
2. Econometric Estimation (Fama-MacBeth, Shanken correction, GRS efficiency test)
3. Committee Defense Stress Testing (Turnover friction, look-ahead bias, out-of-sample decay)
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a reproducible, seed-dependent doctoral thesis evaluation instance.

    Args:
        seed: Integer seed for reproducible pseudo-random generation.

    Returns:
        Flat dictionary containing evaluation instances across thesis pipeline stages.
    """
    rng = np.random.default_rng(seed)

    # -------------------------------------------------------------
    # 1. Institutional Sample Hygiene & Delisting Adjustments
    # -------------------------------------------------------------
    n_firms = 60
    t_months = 120

    # Exchange codes: 1 = NYSE/AMEX, 2 = NASDAQ
    exchange_codes = rng.choice([1, 2], size=n_firms, p=[0.4, 0.6])

    # Market capitalizations with heavy right skew
    log_caps = rng.normal(4.0, 1.2, size=n_firms)
    market_caps = np.exp(log_caps)
    # Anomaly signal rankings (-1.0 to 1.0)
    anomaly_signals = np.linspace(-1.0, 1.0, n_firms) + rng.normal(0.0, 0.05, size=n_firms)

    # Monthly returns panel
    raw_returns = np.zeros((t_months, n_firms))
    base_drift = 0.007 + rng.uniform(-0.001, 0.002)
    signal_spread = 0.012 + rng.uniform(0.001, 0.005)
    for t in range(t_months):
        raw_returns[t] = base_drift + signal_spread * anomaly_signals + rng.normal(0.0, 0.06, size=n_firms)

    # Delisting indicators: ~0.8% monthly delisting rate
    delisting_flags = rng.random(size=(t_months, n_firms)) < 0.008

    # NYSE size 20th percentile cutoff
    nyse_firms = market_caps[exchange_codes == 1]
    nyse_p20_cutoff = float(np.percentile(nyse_firms, 20.0))

    # -------------------------------------------------------------
    # 2. Econometric Estimation & Cross-Sectional Pricing
    # -------------------------------------------------------------
    n_assets = 10
    n_factors = 2
    t_panel = 180

    # Factor realizations (e.g. Market factor and Novel Thesis factor)
    f_means = np.array([0.0065, 0.0042]) + rng.uniform(-0.0005, 0.0005, size=n_factors)
    f_cov = np.array([[0.0022, 0.0004], [0.0004, 0.0014]]) + rng.uniform(-0.0001, 0.0001, size=(2, 2))
    f_cov = f_cov @ f_cov.T + np.eye(2) * 0.0008  # Ensure strict positive-definiteness
    f_chol = np.linalg.cholesky(f_cov)
    factor_series = rng.normal(size=(t_panel, n_factors)) @ f_chol.T + f_means

    # True factor loadings (betas) and intercepts (alphas)
    true_betas = np.array(
        [
            [0.80, -0.35],
            [0.85, -0.20],
            [0.90, -0.10],
            [0.95, 0.05],
            [1.00, 0.15],
            [1.05, 0.25],
            [1.10, 0.35],
            [1.15, 0.45],
            [1.20, 0.60],
            [1.25, 0.75],
        ]
    ) + rng.uniform(-0.03, 0.03, size=(n_assets, n_factors))
    true_alphas = rng.normal(0.0, 0.0012, size=n_assets)

    panel_noise = rng.normal(0.0, 0.022, size=(t_panel, n_assets))
    panel_returns = np.zeros((t_panel, n_assets))
    for t in range(t_panel):
        panel_returns[t] = true_alphas + true_betas @ factor_series[t] + panel_noise[t]

    # -------------------------------------------------------------
    # 3. Defense Stress Testing & Sensitivity Bounds
    # -------------------------------------------------------------
    gross_alpha = float(0.045 + rng.uniform(0.005, 0.015))
    reported_t_stat = float(3.40 + rng.uniform(0.10, 0.60))
    turnover = float(2.80 + rng.uniform(0.20, 0.80))
    decay_rate = float(0.30 + rng.uniform(0.02, 0.08))
    look_ahead_penalty = float(0.0035 + rng.uniform(-0.0005, 0.0005))
    microcap_penalty = float(0.0060 + rng.uniform(-0.0010, 0.0010))
    trading_cost_bps = float(15.0 + rng.uniform(-2.0, 3.0))

    return {
        "seed": seed,
        # Section 1: Sample hygiene
        "n_firms": n_firms,
        "t_months": t_months,
        "exchange_codes": exchange_codes,
        "market_caps": market_caps,
        "anomaly_signals": anomaly_signals,
        "raw_returns": raw_returns,
        "delisting_flags": delisting_flags,
        "nyse_p20_cutoff": nyse_p20_cutoff,
        # Section 2: Econometric estimation
        "n_assets": n_assets,
        "n_factors": n_factors,
        "t_panel": t_panel,
        "factor_series": factor_series,
        "panel_returns": panel_returns,
        # Section 3: Defense stress test
        "gross_alpha": gross_alpha,
        "reported_t_stat": reported_t_stat,
        "turnover": turnover,
        "decay_rate": decay_rate,
        "look_ahead_penalty": look_ahead_penalty,
        "microcap_penalty": microcap_penalty,
        "trading_cost_bps": trading_cost_bps,
    }
