"""Mutant 1: Weights option prices by 1/K instead of 1/K^2 in the VIX integral."""

from __future__ import annotations

import math
from typing import Any


def compute_variance_swap_payoff(
    realized_prices: list[float],
    strike_var: float,
    vega_notional: float,
    annualized_factor: float = 252.0,
) -> dict[str, float]:
    """Calculate realized variance and settlement payoff for a variance swap."""
    if len(realized_prices) < 2:
        raise ValueError("At least 2 price observations are required to compute realized variance.")
    if any(p <= 0.0 for p in realized_prices):
        raise ValueError("All underlying asset prices must be strictly positive.")
    if strike_var <= 0.0:
        raise ValueError("Variance swap strike must be strictly positive.")
    if vega_notional <= 0.0:
        raise ValueError("Vega notional must be strictly positive.")
    if annualized_factor <= 0.0:
        raise ValueError("Annualized factor must be strictly positive.")

    n_returns = len(realized_prices) - 1
    sum_sq_log_returns = 0.0
    for i in range(1, len(realized_prices)):
        log_ret = math.log(realized_prices[i] / realized_prices[i - 1])
        sum_sq_log_returns += log_ret * log_ret

    rv = (annualized_factor / float(n_returns)) * sum_sq_log_returns
    realized_vol = math.sqrt(rv)
    strike_vol = math.sqrt(strike_var)
    var_notional = vega_notional / (2.0 * strike_vol)
    variance_pnl = var_notional * (rv - strike_var)

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
    """Compute model-free implied volatility with buggy 1/K strike weighting."""
    if forward <= 0.0 or maturity <= 0.0 or not options:
        raise ValueError("Invalid forward, maturity, or empty options.")

    strikes_dict: dict[float, dict[str, float]] = {}
    for opt in options:
        k = float(opt["strike"])
        t = str(opt["type"]).lower()
        bid = float(opt.get("bid", 0.0))
        ask = float(opt.get("ask", 0.0))
        if k not in strikes_dict:
            strikes_dict[k] = {}
        strikes_dict[k][f"{t}_bid"] = bid
        strikes_dict[k][f"{t}_ask"] = ask
        strikes_dict[k][f"{t}_mid"] = 0.5 * (bid + ask)

    sorted_strikes = sorted(strikes_dict.keys())
    strikes_below = [k for k in sorted_strikes if k <= forward]
    if not strikes_below:
        raise ValueError("Forward below strikes.")
    k0 = max(strikes_below)

    selected_quotes: dict[float, float] = {}
    k0_call = strikes_dict[k0].get("call_mid", 0.0)
    k0_put = strikes_dict[k0].get("put_mid", 0.0)
    if k0_call > 0.0 and k0_put > 0.0:
        selected_quotes[k0] = 0.5 * (k0_call + k0_put)
    elif k0_call > 0.0:
        selected_quotes[k0] = k0_call
    elif k0_put > 0.0:
        selected_quotes[k0] = k0_put

    for k in reversed([k for k in sorted_strikes if k < k0]):
        bid = strikes_dict[k].get("put_bid", 0.0)
        mid = strikes_dict[k].get("put_mid", 0.0)
        if bid <= 0.0:
            break
        if mid > 0.0:
            selected_quotes[k] = mid

    for k in [k for k in sorted_strikes if k > k0]:
        bid = strikes_dict[k].get("call_bid", 0.0)
        mid = strikes_dict[k].get("call_mid", 0.0)
        if bid <= 0.0:
            break
        if mid > 0.0:
            selected_quotes[k] = mid

    valid_strikes = sorted(selected_quotes.keys())
    m = len(valid_strikes)
    delta_k: list[float] = []
    for i in range(m):
        if i == 0:
            dk = valid_strikes[1] - valid_strikes[0]
        elif i == m - 1:
            dk = valid_strikes[m - 1] - valid_strikes[m - 2]
        else:
            dk = 0.5 * (valid_strikes[i + 1] - valid_strikes[i - 1])
        delta_k.append(dk)

    exp_rt = math.exp(rate * maturity)
    integral_sum = 0.0
    for i, k in enumerate(valid_strikes):
        q_mid = selected_quotes[k]
        # ERROR: 1/K instead of 1/K^2
        integral_sum += (delta_k[i] / k) * exp_rt * q_mid

    sigma_sq = (2.0 / maturity) * integral_sum - (1.0 / maturity) * ((forward / k0 - 1.0) ** 2)
    return 100.0 * math.sqrt(max(0.0, sigma_sq))


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
