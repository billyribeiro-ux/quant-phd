"""Starter implementation for DV6: Exotics, Structured Products & Dealer Hedging.

Students implement these five functions to price an autocallable note under local volatility,
compute Greeks, and evaluate dealer hedging exposure.
"""

from __future__ import annotations

from typing import Any


def eval_local_vol(
    spot: float,
    strike: float,
    time: float,
    base_vol: float,
    skew: float,
    curvature: float,
) -> float:
    """Evaluate parametric local volatility sigma(S, t)."""
    raise NotImplementedError


def price_autocallable(
    params: dict[str, Any],
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, Any]:
    """Price a multi-period Phoenix autocallable note by Monte Carlo under local volatility."""
    raise NotImplementedError


def compute_autocallable_greeks(
    params: dict[str, Any],
    spot_bump_pct: float = 0.01,
    vol_bump: float = 0.01,
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, float]:
    """Compute Delta, Gamma, and Vega using common random numbers (CRN)."""
    raise NotImplementedError


def analyze_dealer_hedging_profile(
    params: dict[str, Any],
    spot_grid: list[float],
    n_paths: int = 1500,
    seed: int = 42,
) -> list[dict[str, float]]:
    """Evaluate note pricing and dealer hedging profile across spot levels."""
    raise NotImplementedError


def simulate_hedging_pnl_impact(
    params: dict[str, Any],
    spot_shock_pct: float,
    rebalancing_friction_bps: float,
) -> dict[str, float]:
    """Calculate dealer delta rebalancing flow and transaction cost friction under a spot move."""
    raise NotImplementedError
