"""Instance generator for AP6 Flow-Impact Estimation & Inelastic Markets Engine.

Generates deterministic problem instances per seed for:
1. Intermediary Asset Pricing SDF (He, Kelly & Manela 2017)
2. Koijen-Yogo (2019) Characteristics-Based Demand Estimation
3. Inelastic Markets Aggregate Flow Multiplier (Gabaix & Koijen 2021)
4. Index Event Flow-Impact Study
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic problem instance for seed."""
    rng = np.random.default_rng(seed)

    # 1. Intermediary Asset Pricing Data
    t_periods = 120
    n_assets = 10
    phi_eta = 0.88 + 0.08 * rng.uniform(0.0, 1.0)
    sigma_eta = 0.015 + 0.005 * rng.uniform(0.0, 1.0)

    # AR(1) dealer equity capital ratio path eta_t
    eta = np.zeros(t_periods)
    eta[0] = 0.08 + 0.02 * rng.standard_normal()
    for t in range(1, t_periods):
        eta[t] = 0.08 * (1.0 - phi_eta) + phi_eta * eta[t - 1] + sigma_eta * rng.standard_normal()

    # Asset excess returns correlated with dealer capital shocks
    delta_eta = eta[1:] - phi_eta * eta[:-1] - 0.08 * (1.0 - phi_eta)
    true_betas = np.linspace(0.8, 3.2, n_assets) + 0.1 * rng.standard_normal(n_assets)
    lambda_eta_true = 0.06 + 0.02 * rng.uniform(0.0, 1.0)

    returns_excess = np.zeros((t_periods - 1, n_assets))
    for i in range(n_assets):
        idio_vol = 0.04 + 0.01 * (i % 3)
        returns_excess[:, i] = (
            true_betas[i] * lambda_eta_true + true_betas[i] * delta_eta + idio_vol * rng.standard_normal(t_periods - 1)
        )

    # 2. Koijen-Yogo Demand System Data
    n_stocks = 25
    n_institutions = 4  # e.g., Mutual Funds, Hedge Funds, Pension Funds, Insurers
    k_chars = 2

    # Characteristics: log market cap, book-to-market
    x_chars = np.zeros((n_stocks, k_chars))
    x_chars[:, 0] = rng.normal(loc=2.0, scale=0.8, size=n_stocks)
    x_chars[:, 1] = rng.normal(loc=0.0, scale=0.5, size=n_stocks)

    # Exogenous instrument Z (e.g. index investment universe mandate / supply shocks)
    z_inst = np.zeros((n_stocks, 2))
    z_inst[:, 0] = 0.7 * x_chars[:, 0] + 0.8 * rng.standard_normal(n_stocks)
    z_inst[:, 1] = rng.uniform(-1.0, 1.0, size=n_stocks)

    # True institutional parameters
    true_elasticities = np.array([0.8, 2.5, 0.3, 0.4]) + 0.1 * rng.uniform(-0.5, 0.5, size=n_institutions)
    true_gamma = np.array([[0.6, -0.4], [0.8, -0.2], [0.3, -0.6], [0.4, -0.5]])

    # Latent demand unobserved shock and endogenous price
    log_p = 1.0 + 0.5 * z_inst[:, 0] + 0.4 * z_inst[:, 1] + 0.3 * rng.standard_normal(n_stocks)
    shares_out = np.exp(rng.normal(loc=4.0, scale=0.5, size=n_stocks))

    # Construct institutional portfolio weights w_{i,n}
    holdings_weights = np.zeros((n_institutions, n_stocks))
    for i in range(n_institutions):
        delta_in = 0.5 - true_elasticities[i] * log_p + x_chars @ true_gamma[i] + 0.15 * rng.standard_normal(n_stocks)
        denom = 1.0 + np.sum(np.exp(delta_in))
        holdings_weights[i, :] = np.exp(delta_in) / denom

    # Institutional AUM and market clearing parameters
    aum = np.array([1200.0, 450.0, 2100.0, 1800.0]) * (1.0 + 0.1 * rng.uniform(-1.0, 1.0, size=n_institutions))
    aum_shares = aum / np.sum(aum)
    alpha_i = np.array([0.5, 0.6, 0.4, 0.45]) + 0.05 * rng.standard_normal(n_institutions)
    char_effects = np.zeros((n_institutions, n_stocks))
    for i in range(n_institutions):
        char_effects[i, :] = x_chars @ true_gamma[i]

    # 3. Index Inclusion Event Data
    n_events = 30
    flow_fractions = rng.uniform(0.02, 0.15, size=n_events)
    true_event_multiplier = 4.5 + 1.2 * rng.uniform(0.0, 1.0)
    pre_prices = 50.0 + 20.0 * rng.uniform(0.0, 1.0, size=n_events)

    log_pre = np.log(pre_prices)
    delta_log_p = 0.01 + true_event_multiplier * flow_fractions + 0.02 * rng.standard_normal(n_events)
    post_prices = np.exp(log_pre + delta_log_p)

    return {
        "seed": seed,
        "returns_excess": returns_excess,
        "dealer_capital_ratio": eta,
        "aum": aum,
        "shares_out": shares_out,
        "alpha_i": alpha_i,
        "beta_i": true_elasticities,
        "char_effects": char_effects,
        "holdings_weights": holdings_weights,
        "log_prices": log_p,
        "characteristics": x_chars,
        "instruments": z_inst,
        "aum_shares": aum_shares,
        "elasticities": true_elasticities,
        "pre_prices": pre_prices,
        "post_prices": post_prices,
        "flow_fractions": flow_fractions,
    }
