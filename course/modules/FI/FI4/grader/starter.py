"""Starter template for FI4 Plumbing Monitor autograder.

Implement the four plumbing and basis-trade functions to pass the test suite.
"""

from __future__ import annotations

from typing import Any


def net_implied_repo_rate(
    cash_price: float,
    futures_price: float,
    conversion_factor: float,
    days: int,
    repo_rate: float,
) -> float:
    """Compute the net implied repo rate (basis carry spread) for a cash-futures basis trade."""
    raise NotImplementedError("net_implied_repo_rate not implemented")


def basis_trade_return(
    cash_price: float,
    futures_price: float,
    conversion_factor: float,
    days: int,
    repo_rate: float,
    haircut: float,
    initial_margin: float,
    shock_cash_price: float,
    shock_futures_price: float,
) -> dict[str, float]:
    """Compute P&L, financing costs, and return on equity for a leveraged basis trade."""
    raise NotImplementedError("basis_trade_return not implemented")


def margin_coverage(
    cash_price: float,
    futures_price: float,
    conversion_factor: float,
    haircut: float,
    initial_margin: float,
    maintenance_margin: float,
    shock_cash_price: float,
    shock_futures_price: float,
) -> dict[str, Any]:
    """Evaluate margin calls and solvency under adverse market price shocks."""
    raise NotImplementedError("margin_coverage not implemented")


def leverage_ratio(
    dealer_equity: float,
    cash_treasuries: float,
    repo_matched_book: float,
    derivatives_exposure: float,
    exempt_reserves_and_treasuries: bool = False,
) -> dict[str, Any]:
    """Compute primary dealer Supplementary Leverage Ratio (SLR) and regulatory capital surplus."""
    raise NotImplementedError("leverage_ratio not implemented")
