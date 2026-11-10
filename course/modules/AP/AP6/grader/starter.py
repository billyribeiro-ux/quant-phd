"""Starter implementation for AP6 Flow-Impact Estimation & Inelastic Markets Engine.

Student skeleton code with function signatures.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def estimate_intermediary_sdf(returns_excess: np.ndarray, capital_ratio: np.ndarray) -> dict[str, Any]:
    """Estimate primary dealer equity capital ratio SDF and cross-sectional factor pricing."""
    raise NotImplementedError("Implement estimate_intermediary_sdf")


def estimate_koijen_yogo_demand(
    holdings_weights: np.ndarray,
    log_prices: np.ndarray,
    characteristics: np.ndarray,
    instruments: np.ndarray,
) -> dict[str, Any]:
    """Estimate characteristics-based demand system parameters via 2SLS IV regression."""
    raise NotImplementedError("Implement estimate_koijen_yogo_demand")


def solve_market_clearing_prices(
    aum: np.ndarray,
    shares_out: np.ndarray,
    alpha_i: np.ndarray,
    beta_i: np.ndarray,
    char_effects: np.ndarray,
    tol: float = 1e-7,
    max_iter: int = 500,
) -> np.ndarray:
    """Solve the non-linear market clearing system for equilibrium asset prices."""
    raise NotImplementedError("Implement solve_market_clearing_prices")


def compute_flow_multiplier(aum_shares: np.ndarray, elasticities: np.ndarray) -> dict[str, float]:
    """Compute aggregate market elasticity and macro flow multiplier (Gabaix-Koijen 2021)."""
    raise NotImplementedError("Implement compute_flow_multiplier")


def estimate_index_event_impact(
    pre_prices: np.ndarray,
    post_prices: np.ndarray,
    flow_fractions: np.ndarray,
) -> dict[str, Any]:
    """Estimate empirical flow multiplier from index inclusion event study."""
    raise NotImplementedError("Implement estimate_index_event_impact")
