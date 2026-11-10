"""Mutant 5: Treats VIX shock as a gain instead of a loss in stress_test_drawdowns."""

from __future__ import annotations

from typing import Any


def compute_variance_swap_payoff(
    realized_prices: list[float],
    strike_var: float,
    vega_notional: float,
    annualized_factor: float = 252.0,
) -> dict[str, float]:
    from reference import compute_variance_swap_payoff as ref_swap

    return ref_swap(realized_prices, strike_var, vega_notional, annualized_factor)


def replicate_vix_index(
    options: list[dict[str, Any]],
    forward: float,
    rate: float,
    maturity: float,
) -> float:
    from reference import replicate_vix_index as ref_vix

    return ref_vix(options, forward, rate, maturity)


def simulate_short_vol_strategy(
    market_data: list[dict[str, float]],
    initial_capital: float,
    target_leverage: float,
    margin_requirement: float,
    transaction_cost_bps: float,
    stop_loss_drawdown: float = 0.50,
) -> dict[str, Any]:
    from reference import simulate_short_vol_strategy as ref_sim

    return ref_sim(
        market_data,
        initial_capital,
        target_leverage,
        margin_requirement,
        transaction_cost_bps,
        stop_loss_drawdown,
    )


def stress_test_drawdowns(
    baseline_nav: float,
    spot_shock: float,
    vix_shock: float,
    leverage: float,
    margin_requirement: float,
) -> dict[str, float]:
    """Stress test with sign error: assumes short vol benefits from VIX spike."""
    if baseline_nav <= 0.0 or leverage <= 0.0 or margin_requirement <= 0.0:
        raise ValueError("Invalid parameters.")

    # ERROR: treats VIX shock as negative loss (a gain)
    vol_loss_fraction = -leverage * (vix_shock / 100.0)
    total_loss_fraction = vol_loss_fraction
    loss_amount = baseline_nav * total_loss_fraction
    stressed_nav = baseline_nav - loss_amount

    return {
        "stressed_nav": stressed_nav,
        "loss_amount": loss_amount,
        "loss_fraction": total_loss_fraction,
        "stressed_margin": 0.0,
        "margin_deficiency": 0.0,
        "is_insolvent": 0.0,
    }


def evaluate_strategy_metrics(
    returns: list[float],
    rf_annual: float = 0.02,
    periods_per_year: float = 252.0,
) -> dict[str, float]:
    from reference import evaluate_strategy_metrics as ref_metrics

    return ref_metrics(returns, rf_annual, periods_per_year)
