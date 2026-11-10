"""Mutant 2: Calculates variance swap PnL using linear volatility rather than variance."""

from __future__ import annotations

import math
from typing import Any


def compute_variance_swap_payoff(
    realized_prices: list[float],
    strike_var: float,
    vega_notional: float,
    annualized_factor: float = 252.0,
) -> dict[str, float]:
    """Calculate variance swap with linear volatility error."""
    if len(realized_prices) < 2:
        raise ValueError("At least 2 price observations are required to compute realized variance.")
    if any(p <= 0.0 for p in realized_prices):
        raise ValueError("All underlying asset prices must be strictly positive.")
    if strike_var <= 0.0 or vega_notional <= 0.0 or annualized_factor <= 0.0:
        raise ValueError("Invalid parameters.")

    n_returns = len(realized_prices) - 1
    sum_sq_log_returns = sum(
        math.log(realized_prices[i] / realized_prices[i - 1]) ** 2 for i in range(1, len(realized_prices))
    )
    rv = (annualized_factor / float(n_returns)) * sum_sq_log_returns
    realized_vol = math.sqrt(rv)
    strike_vol = math.sqrt(strike_var)
    var_notional = vega_notional / (2.0 * strike_vol)

    # ERROR: PnL computed on linear volatility instead of variance
    variance_pnl = vega_notional * (realized_vol - strike_vol)

    return {
        "rv": rv,
        "realized_vol": realized_vol,
        "strike_var": strike_var,
        "strike_vol": strike_vol,
        "vega_notional": vega_notional,
        "var_notional": var_notional,
        "variance_pnl": variance_pnl,
    }


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
    from reference import stress_test_drawdowns as ref_stress

    return ref_stress(baseline_nav, spot_shock, vix_shock, leverage, margin_requirement)


def evaluate_strategy_metrics(
    returns: list[float],
    rf_annual: float = 0.02,
    periods_per_year: float = 252.0,
) -> dict[str, float]:
    from reference import evaluate_strategy_metrics as ref_metrics

    return ref_metrics(returns, rf_annual, periods_per_year)
