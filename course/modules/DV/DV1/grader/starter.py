"""Starter template for DV1: Hedging-Error Study.

Implement the functions below according to the project specification in project.html.
All functions must validate inputs and raise ValueError on invalid arguments.
"""

from __future__ import annotations

from typing import Any


def bs_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
) -> float:
    """Analytical Black-Scholes price for European options."""
    raise NotImplementedError("bs_price is not implemented")


def bs_delta(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
) -> float:
    """Analytical Black-Scholes Delta sensitivity."""
    raise NotImplementedError("bs_delta is not implemented")


def bs_gamma(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
) -> float:
    """Analytical Black-Scholes Gamma sensitivity."""
    raise NotImplementedError("bs_gamma is not implemented")


def simulate_paths(
    spot: float,
    rate: float,
    vol: float,
    maturity: float,
    steps: int,
    n_paths: int,
    seed: int,
) -> list[list[float]]:
    """Simulate geometric Brownian motion price paths under the risk-neutral measure Q."""
    raise NotImplementedError("simulate_paths is not implemented")


def delta_hedging_pnl(
    paths: list[list[float]],
    strike: float,
    rate: float,
    vol_implied: float,
    maturity: float,
    cost_rate: float = 0.0,
    is_call: bool = True,
) -> dict[str, Any]:
    """Simulate discrete delta-hedged short option book along given price paths."""
    raise NotImplementedError("delta_hedging_pnl is not implemented")


def hedging_error_scaling(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    step_list: list[int],
    n_paths: int,
    seed: int,
) -> dict[str, Any]:
    """Evaluate discrete hedging error standard deviation across rebalancing steps."""
    raise NotImplementedError("hedging_error_scaling is not implemented")


def gamma_theta_attribution(
    path: list[float],
    strike: float,
    rate: float,
    vol_implied: float,
    maturity: float,
    is_call: bool = True,
) -> dict[str, float]:
    """Single-path P&L attribution verifying the gamma-theta identity."""
    raise NotImplementedError("gamma_theta_attribution is not implemented")
