"""Mutant 3: Ignores margin limits and fails to deleverage when required margin exceeds NAV."""

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
    """Backtest with unconstrained leverage error."""
    if initial_capital <= 0.0 or target_leverage <= 0.0 or margin_requirement <= 0.0 or not market_data:
        raise ValueError("Invalid parameters.")

    nav = initial_capital
    peak_nav = initial_capital
    nav_series: list[float] = [nav]
    returns: list[float] = []
    drawdown_series: list[float] = [0.0]
    rf_daily = 0.02 / 252.0

    for i in range(len(market_data)):
        data = market_data[i]
        vix = float(data["vix"])
        rv_realized = float(data["rv_realized"])

        # ERROR: ignores margin_requirement constraints and never caps exposure
        target_exposure = nav * target_leverage
        current_exposure = target_exposure

        iv_daily = (vix / 100.0) ** 2
        var_carry = 0.5 * (iv_daily - rv_realized) / 252.0
        position_pnl = current_exposure * var_carry
        interest_income = nav * rf_daily

        nav_prev = nav
        nav = nav + position_pnl + interest_income

        if nav > peak_nav:
            peak_nav = nav

        # ERROR: allows negative drawdown and negative NAV without liquidation
        dd = (peak_nav - nav) / peak_nav if peak_nav > 0.0 else -0.5
        daily_ret = (nav - nav_prev) / nav_prev if nav_prev != 0.0 else 0.0
        nav_series.append(nav)
        returns.append(daily_ret)
        drawdown_series.append(dd)

    return {
        "nav_series": nav_series,
        "returns": returns,
        "drawdown_series": drawdown_series,
        "max_drawdown": max(drawdown_series),
        "terminal_nav": nav,
        "margin_calls": 0,
        "liquidated": False,
    }


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
