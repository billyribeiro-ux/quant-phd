"""Starter template for X2 project: Currency factor replication (currency_factors.py).

Implement:
- compute_excess_returns
- compute_forward_discounts
- sort_carry_portfolios
- build_factors
- estimate_volatility_innovations
- fama_macbeth_twostep
- run_currency_factor_replication
"""

from __future__ import annotations

from typing import Any


def compute_excess_returns(
    spot_rates: list[list[float]],
    forward_rates: list[list[float]],
) -> list[list[float]]:
    """Compute log currency excess returns."""
    raise NotImplementedError("Student implementation required.")


def compute_forward_discounts(
    spot_rates: list[list[float]],
    forward_rates: list[list[float]],
) -> list[list[float]]:
    """Compute log forward discounts."""
    raise NotImplementedError("Student implementation required.")


def sort_carry_portfolios(
    excess_returns: list[list[float]],
    forward_discounts: list[list[float]],
    n_portfolios: int = 5,
) -> dict[str, Any]:
    """Sort currencies into carry portfolios based on forward discounts."""
    raise NotImplementedError("Student implementation required.")


def build_factors(portfolio_returns: list[list[float]]) -> dict[str, list[float]]:
    """Construct Dollar factor and HML-FX carry factor."""
    raise NotImplementedError("Student implementation required.")


def estimate_volatility_innovations(
    daily_returns: list[list[float]],
    days_per_month: int = 21,
) -> dict[str, Any]:
    """Estimate monthly global FX volatility and AR(1) innovations."""
    raise NotImplementedError("Student implementation required.")


def fama_macbeth_twostep(
    portfolio_returns: list[list[float]],
    factor_matrix: list[list[float]],
    factor_names: list[str],
) -> dict[str, Any]:
    """Perform two-pass Fama-MacBeth cross-sectional regressions."""
    raise NotImplementedError("Student implementation required.")


def run_currency_factor_replication(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete currency factor replication pipeline."""
    raise NotImplementedError("Student implementation required.")
