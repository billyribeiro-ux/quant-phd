"""Starter code for DV5: Variance Risk Premium & Volatility Trading.

Implement all required functions according to the specifications in project.html.
All functions must raise ValueError on degenerate or invalid inputs.
"""

from __future__ import annotations

from typing import Any


def compute_variance_swap_payoff(
    realized_prices: list[float],
    strike_var: float,
    vega_notional: float,
    annualized_factor: float = 252.0,
) -> dict[str, float]:
    """Calculate realized variance and settlement payoff for a variance swap."""
    raise NotImplementedError("TODO: Implement compute_variance_swap_payoff.")


def replicate_vix_index(
    options: list[dict[str, Any]],
    forward: float,
    rate: float,
    maturity: float,
) -> float:
    """Compute model-free implied volatility (VIX methodology) from an option chain."""
    raise NotImplementedError("TODO: Implement replicate_vix_index.")


def simulate_short_vol_strategy(
    market_data: list[dict[str, float]],
    initial_capital: float,
    target_leverage: float,
    margin_requirement: float,
    transaction_cost_bps: float,
    stop_loss_drawdown: float = 0.50,
) -> dict[str, Any]:
    """Backtest a short-volatility strategy with leverage, margin, and stop-loss."""
    raise NotImplementedError("TODO: Implement simulate_short_vol_strategy.")


def stress_test_drawdowns(
    baseline_nav: float,
    spot_shock: float,
    vix_shock: float,
    leverage: float,
    margin_requirement: float,
) -> dict[str, float]:
    """Evaluate portfolio shock impact under acute volatility spikes."""
    raise NotImplementedError("TODO: Implement stress_test_drawdowns.")


def evaluate_strategy_metrics(
    returns: list[float],
    rf_annual: float = 0.02,
    periods_per_year: float = 252.0,
) -> dict[str, float]:
    """Compute risk-adjusted and higher-moment performance statistics."""
    raise NotImplementedError("TODO: Implement evaluate_strategy_metrics.")
