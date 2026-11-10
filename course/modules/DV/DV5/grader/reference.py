"""Reference implementation for DV5: Variance Risk Premium & Volatility Trading.

Provides fully solved functions for:
1. compute_variance_swap_payoff: Realized variance calculation and swap settlement.
2. replicate_vix_index: Model-free implied volatility replication from option chains.
3. simulate_short_vol_strategy: Backtesting short-volatility strategy with leverage and margin.
4. stress_test_drawdowns: Scenario analysis for crash shocks (2008, 2018, 2020).
5. evaluate_strategy_metrics: Risk-adjusted and higher-moment performance metrics.
"""

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
    sum_sq_log_returns = sum(
        math.log(realized_prices[i] / realized_prices[i - 1]) ** 2 for i in range(1, len(realized_prices))
    )

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
    options: list[Any],
    forward: float,
    rate: float,
    maturity: float,
) -> float:
    """Compute model-free implied volatility (VIX methodology) from an option chain."""
    if forward <= 0.0:
        raise ValueError("Forward price must be strictly positive.")
    if maturity <= 0.0:
        raise ValueError("Maturity must be strictly positive.")
    if not options:
        raise ValueError("Option chain cannot be empty.")

    strikes_dict: dict[float, dict[str, float]] = {}
    for item in options:
        if isinstance(item, (list, tuple)):
            k = float(item[0])
            is_call = float(item[1]) > 0.5
            bid = float(item[2])
            ask = float(item[3])
            t = "call" if is_call else "put"
        elif isinstance(item, dict):
            k = float(item["strike"])
            t = str(item["type"]).lower()
            bid = float(item.get("bid", 0.0))
            ask = float(item.get("ask", 0.0))
        else:
            raise ValueError(f"Unrecognized option format: {type(item)}")

        if k not in strikes_dict:
            strikes_dict[k] = {}
        strikes_dict[k][f"{t}_bid"] = bid
        strikes_dict[k][f"{t}_ask"] = ask
        strikes_dict[k][f"{t}_mid"] = 0.5 * (bid + ask)

    sorted_strikes = sorted(strikes_dict.keys())
    if len(sorted_strikes) < 2:
        raise ValueError("At least 2 strikes are required for VIX replication.")

    strikes_below = [k for k in sorted_strikes if k <= forward]
    if not strikes_below:
        raise ValueError("Forward price is below all available option strikes.")
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

    # Puts below K0
    consecutive_zero_bids = 0
    for k in reversed([k for k in sorted_strikes if k < k0]):
        bid = strikes_dict[k].get("put_bid", 0.0)
        mid = strikes_dict[k].get("put_mid", 0.0)
        if bid <= 0.0:
            consecutive_zero_bids += 1
            if consecutive_zero_bids >= 2:
                break
            continue
        consecutive_zero_bids = 0
        if mid > 0.0:
            selected_quotes[k] = mid

    # Calls above K0
    consecutive_zero_bids = 0
    for k in [k for k in sorted_strikes if k > k0]:
        bid = strikes_dict[k].get("call_bid", 0.0)
        mid = strikes_dict[k].get("call_mid", 0.0)
        if bid <= 0.0:
            consecutive_zero_bids += 1
            if consecutive_zero_bids >= 2:
                break
            continue
        consecutive_zero_bids = 0
        if mid > 0.0:
            selected_quotes[k] = mid

    valid_strikes = sorted(selected_quotes.keys())
    if len(valid_strikes) < 2:
        raise ValueError("Insufficient non-zero-bid options to replicate VIX.")

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
        integral_sum += (delta_k[i] / (k * k)) * exp_rt * q_mid

    sigma_sq = (2.0 / maturity) * integral_sum - (1.0 / maturity) * ((forward / k0 - 1.0) ** 2)
    return 100.0 * math.sqrt(max(0.0, sigma_sq))


def simulate_short_vol_strategy(
    market_data: list[Any],
    initial_capital: float,
    target_leverage: float,
    margin_requirement: float,
    transaction_cost_bps: float,
    stop_loss_drawdown: float = 0.50,
) -> dict[str, Any]:
    """Backtest a short-volatility strategy with leverage, margin, and stop-loss."""
    if initial_capital <= 0.0:
        raise ValueError("Initial capital must be strictly positive.")
    if target_leverage <= 0.0:
        raise ValueError("Target leverage must be strictly positive.")
    if margin_requirement <= 0.0:
        raise ValueError("Margin requirement must be strictly positive.")
    if transaction_cost_bps < 0.0:
        raise ValueError("Transaction costs cannot be negative.")
    if not market_data:
        raise ValueError("Market data series cannot be empty.")

    nav = initial_capital
    peak_nav = initial_capital
    nav_series: list[float] = [nav]
    returns: list[float] = []
    drawdown_series: list[float] = [0.0]

    margin_calls = 0
    liquidated = False
    current_exposure = 0.0
    rf_daily = 0.02 / 252.0

    for i in range(len(market_data)):
        item = market_data[i]
        if isinstance(item, (list, tuple)):
            vix = float(item[2])
            rv_realized = float(item[3])
        elif isinstance(item, dict):
            vix = float(item["vix"])
            rv_realized = float(item["rv_realized"])
        else:
            raise ValueError(f"Unrecognized market data format: {type(item)}")

        if liquidated or nav <= 0.0:
            nav_prev = nav
            nav = max(0.0, nav * (1.0 + rf_daily))
            daily_ret = (nav - nav_prev) / nav_prev if nav_prev > 0.0 else 0.0
            nav_series.append(nav)
            returns.append(daily_ret)
            dd = (peak_nav - nav) / peak_nav if peak_nav > 0.0 else 1.0
            drawdown_series.append(dd)
            continue

        target_exposure = nav * target_leverage
        max_allowed_exposure = nav / margin_requirement
        if target_exposure > max_allowed_exposure:
            target_exposure = max_allowed_exposure
            margin_calls += 1

        rebalance_amount = abs(target_exposure - current_exposure)
        tc = rebalance_amount * (transaction_cost_bps / 10000.0)
        current_exposure = target_exposure

        iv_daily = (vix / 100.0) ** 2
        var_carry = 0.5 * (iv_daily - rv_realized) / 252.0
        position_pnl = current_exposure * var_carry
        interest_income = nav * rf_daily

        nav_prev = nav
        nav = nav + position_pnl + interest_income - tc

        if nav <= 0.0:
            nav = 0.0
            liquidated = True

        if nav > peak_nav:
            peak_nav = nav

        dd = (peak_nav - nav) / peak_nav if peak_nav > 0.0 else 1.0
        if dd >= stop_loss_drawdown:
            liquidated = True
            current_exposure = 0.0

        daily_ret = (nav - nav_prev) / nav_prev if nav_prev > 0.0 else -1.0
        nav_series.append(nav)
        returns.append(daily_ret)
        drawdown_series.append(dd)

    max_dd = max(drawdown_series) if drawdown_series else 0.0
    return {
        "nav_series": nav_series,
        "returns": returns,
        "drawdown_series": drawdown_series,
        "max_drawdown": max_dd,
        "terminal_nav": nav,
        "margin_calls": margin_calls,
        "liquidated": liquidated,
    }


def stress_test_drawdowns(
    baseline_nav: float,
    spot_shock: float,
    vix_shock: float,
    leverage: float,
    margin_requirement: float,
) -> dict[str, float]:
    """Evaluate portfolio shock impact under acute volatility spikes."""
    if baseline_nav <= 0.0:
        raise ValueError("Baseline NAV must be strictly positive.")
    if leverage <= 0.0:
        raise ValueError("Leverage must be strictly positive.")
    if margin_requirement <= 0.0:
        raise ValueError("Margin requirement must be strictly positive.")

    vol_loss_fraction = leverage * (vix_shock / 100.0)
    spot_loss_fraction = 0.3 * leverage * abs(spot_shock)
    total_loss_fraction = min(1.0, max(0.0, vol_loss_fraction + spot_loss_fraction))

    loss_amount = baseline_nav * total_loss_fraction
    stressed_nav = max(0.0, baseline_nav - loss_amount)

    stressed_margin_rate = margin_requirement * (1.0 + vix_shock / 50.0)
    stressed_exposure = max(0.0, baseline_nav * leverage * (1.0 - total_loss_fraction * 0.5))
    stressed_margin = stressed_exposure * stressed_margin_rate

    margin_deficiency = max(0.0, stressed_margin - stressed_nav)
    is_insolvent = 1.0 if stressed_nav <= 0.0 else 0.0

    return {
        "stressed_nav": stressed_nav,
        "loss_amount": loss_amount,
        "loss_fraction": total_loss_fraction,
        "stressed_margin": stressed_margin,
        "margin_deficiency": margin_deficiency,
        "is_insolvent": is_insolvent,
    }


def evaluate_strategy_metrics(
    returns: list[float],
    rf_annual: float = 0.02,
    periods_per_year: float = 252.0,
) -> dict[str, float]:
    """Compute risk-adjusted and higher-moment performance statistics."""
    n = len(returns)
    if n < 5:
        raise ValueError("At least 5 return observations are required for statistical metrics.")

    mean_ret = sum(returns) / float(n)
    sum_sq_diff = sum((r - mean_ret) ** 2 for r in returns)
    var = sum_sq_diff / float(n - 1)
    if var <= 1e-14:
        raise ValueError("Return series variance is zero or degenerate.")
    std_dev = math.sqrt(var)

    ann_return = mean_ret * periods_per_year
    ann_vol = std_dev * math.sqrt(periods_per_year)
    sharpe = (ann_return - rf_annual) / ann_vol

    rf_daily = rf_annual / periods_per_year
    downside_sq = sum(min(0.0, r - rf_daily) ** 2 for r in returns)
    downside_var = downside_sq / float(n - 1)
    downside_std = math.sqrt(downside_var) if downside_var > 0.0 else 1e-6
    ann_downside_vol = downside_std * math.sqrt(periods_per_year)
    sortino = (ann_return - rf_annual) / ann_downside_vol

    m3 = sum((r - mean_ret) ** 3 for r in returns) / float(n)
    m4 = sum((r - mean_ret) ** 4 for r in returns) / float(n)
    skewness = m3 / (std_dev**3)
    excess_kurtosis = (m4 / (std_dev**4)) - 3.0
    tail_risk_penalty = max(0.0, -skewness) * math.sqrt(max(0.0, excess_kurtosis))

    return {
        "mean_return": ann_return,
        "volatility": ann_vol,
        "sharpe_ratio": sharpe,
        "downside_volatility": ann_downside_vol,
        "sortino_ratio": sortino,
        "skewness": skewness,
        "excess_kurtosis": excess_kurtosis,
        "tail_risk_penalty": tail_risk_penalty,
    }
