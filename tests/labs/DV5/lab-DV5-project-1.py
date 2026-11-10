"""Lab Project 1 · Worked Example: Systematic Short-Volatility Strategy Audit.

This lab executes a fully solved reference instance of the DV5 capstone project
on seed 0 (SIMULATED), executing the complete quantitative pipeline:
1. Variance swap settlement payoff and vega notional conversion.
2. Model-free implied volatility (Cboe VIX) replication from option chain.
3. 60-day short-volatility strategy backtest with leverage and margin constraints.
4. Historical crash scenario stress testing (2008 Lehman, 2018 Volmageddon, 2020 Covid).
5. Comprehensive risk-adjusted metrics, higher moments, and tail risk penalty.
"""

from __future__ import annotations

import math
import random
from typing import Any


def compute_variance_swap_payoff(
    realized_prices: list[float],
    strike_var: float,
    vega_notional: float,
    annualized_factor: float = 252.0,
) -> dict[str, float]:
    """Calculate realized variance and settlement payoff for a variance swap."""
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
    options: list[dict[str, Any]],
    forward: float,
    rate: float,
    maturity: float,
) -> float:
    """Compute model-free implied volatility (VIX methodology) from an option chain."""
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
    k0 = max([k for k in sorted_strikes if k <= forward])

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
        integral_sum += (delta_k[i] / (k * k)) * exp_rt * q_mid

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
    """Backtest a short-volatility strategy with leverage, margin, and stop-loss."""
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
        data = market_data[i]
        vix = float(data["vix"])
        rv_realized = float(data["rv_realized"])

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
    mean_ret = sum(returns) / float(n)
    sum_sq_diff = sum((r - mean_ret) ** 2 for r in returns)
    var = sum_sq_diff / float(n - 1)
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


def main() -> None:
    print("=== Systematic Short-Volatility Strategy Audit (Worked Example: Seed 0) ===")
    rng = random.Random(0)

    spot = 4422.25
    rate = 0.0339
    maturity = 30.0 / 365.0
    forward = 4434.55

    # 1. Option chain generation (SIMULATED)
    base_iv = 0.2307
    skew_param = 0.1507
    smile_param = 0.2844
    strike_step = 25.0
    k_min = 3775.0
    k_max = 5100.0

    def bs_put(s: float, k: float, t: float, r: float, sig: float) -> float:
        if sig <= 0.0 or t <= 0.0:
            return max(0.0, k * math.exp(-r * t) - s)
        d1 = (math.log(s / k) + (r + 0.5 * sig * sig) * t) / (sig * math.sqrt(t))
        d2 = d1 - sig * math.sqrt(t)
        return k * math.exp(-r * t) * 0.5 * (1.0 + math.erf(-d2 / math.sqrt(2.0))) - s * 0.5 * (
            1.0 + math.erf(-d1 / math.sqrt(2.0))
        )

    def bs_call(s: float, k: float, t: float, r: float, sig: float) -> float:
        if sig <= 0.0 or t <= 0.0:
            return max(0.0, s - k * math.exp(-r * t))
        d1 = (math.log(s / k) + (r + 0.5 * sig * sig) * t) / (sig * math.sqrt(t))
        d2 = d1 - sig * math.sqrt(t)
        return s * 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0))) - k * math.exp(-r * t) * 0.5 * (
            1.0 + math.erf(d2 / math.sqrt(2.0))
        )

    options_chain: list[dict[str, Any]] = []
    k_curr = k_min
    while k_curr <= k_max:
        m = math.log(k_curr / forward)
        iv_k = max(0.08, base_iv - skew_param * m + smile_param * (m**2))
        p_mid = bs_put(spot, k_curr, maturity, rate, iv_k)
        c_mid = bs_call(spot, k_curr, maturity, rate, iv_k)
        half_sp = max(0.05, 0.05 + 0.10 * abs(m))
        p_bid = round(max(0.0, p_mid - half_sp), 2)
        p_ask = round(p_mid + half_sp, 2)
        if p_bid > 0.0 or k_curr <= forward:
            options_chain.append({"strike": k_curr, "type": "put", "bid": p_bid, "ask": p_ask})
        c_bid = round(max(0.0, c_mid - half_sp), 2)
        c_ask = round(c_mid + half_sp, 2)
        if c_bid > 0.0 or k_curr >= forward:
            options_chain.append({"strike": k_curr, "type": "call", "bid": c_bid, "ask": c_ask})
        k_curr += strike_step

    # 2. Realized prices
    daily_vol = 0.2311 * math.sqrt(1.0 / 252.0)
    realized_prices = [spot]
    cp = spot
    for _ in range(21):
        z = rng.gauss(0.0, 1.0)
        cp = round(cp * math.exp((rate - 0.5 * daily_vol**2) / 252.0 + daily_vol * z), 2)
        realized_prices.append(cp)

    var_swap_strike = 0.05322
    var_swap_vega_notional = 92222.0

    swap_res = compute_variance_swap_payoff(realized_prices, var_swap_strike, var_swap_vega_notional)
    print("1. Variance Swap Contract Settlement:")
    print(f"   Vega Notional:      {swap_res['vega_notional']:.2f} USD")
    print(f"   Strike Variance:    {swap_res['strike_var']:.6f} (Strike Vol: {swap_res['strike_vol'] * 100.0:.2f}%)")
    print(f"   Realized Variance:  {swap_res['rv']:.6f} (Realized Vol: {swap_res['realized_vol'] * 100.0:.2f}%)")
    print(f"   Variance Notional:  {swap_res['var_notional']:.2f} USD per unit")
    print(f"   Settlement PnL:     {swap_res['variance_pnl']:.2f} USD")

    replicated_vix = replicate_vix_index(options_chain, forward, rate, maturity)
    print("\n2. Model-Free Implied Volatility (VIX) Replication:")
    print(f"   Forward Price:      {forward:.2f}, Rate: {rate:.4f}, Expiry: {maturity * 365:.1f} days")
    print(f"   Total Quotes Used:  {len(options_chain)} contracts")
    print(f"   Replicated VIX:     {replicated_vix:.4f}")

    # 3. Market data for backtest
    market_data: list[dict[str, float]] = []
    mkt_spot = spot
    mkt_vix = round(base_iv * 100.0, 2)
    daily_dt = 1.0 / 252.0
    for day in range(60):
        z_s = rng.gauss(0.0, 1.0)
        z_o = rng.gauss(0.0, 1.0)
        z_v = -0.75 * z_s + math.sqrt(1.0 - 0.75**2) * z_o
        s_ret = 0.0003 + (mkt_vix / 100.0) * math.sqrt(daily_dt) * z_s
        mkt_spot = round(mkt_spot * math.exp(s_ret), 2)
        vix_diff = 0.12 * (base_iv * 100.0 - mkt_vix) + 1.8 * z_v
        mkt_vix = round(max(9.0, min(85.0, mkt_vix + vix_diff)), 2)
        rv_day = round((s_ret**2) * 252.0, 5)
        market_data.append(
            {
                "day": float(day),
                "spot": float(mkt_spot),
                "vix": float(mkt_vix),
                "rv_realized": float(rv_day),
            }
        )

    initial_cap = 1084712.30
    target_lev = 1.88
    margin_req = 0.2283
    tc_bps = 7.78

    sim_res = simulate_short_vol_strategy(
        market_data,
        initial_cap,
        target_lev,
        margin_req,
        tc_bps,
        stop_loss_drawdown=0.45,
    )
    print("\n3. Strategy Backtest Results (60 Days):")
    print(f"   Initial Capital:    {initial_cap:.2f} USD")
    print(f"   Target Leverage:    {target_lev:.2f}x, Margin Req: {margin_req * 100.0:.1f}%")
    print(f"   Terminal NAV:       {sim_res['terminal_nav']:.2f} USD")
    print(f"   Max Drawdown:       {sim_res['max_drawdown'] * 100.0:.2f}%")
    print(f"   Margin Calls:       {sim_res['margin_calls']}")
    print(f"   Liquidated:         {sim_res['liquidated']}")

    scenarios = {
        "2008_lehman": {"spot_shock": -0.20, "vix_shock": 35.0},
        "2018_volmageddon": {"spot_shock": -0.041, "vix_shock": 20.0},
        "2020_covid": {"spot_shock": -0.12, "vix_shock": 45.0},
    }
    print("\n4. Stress Testing Across Historical Crash Analogues:")
    print(" Scenario         | Spot Shock | VIX Spike | Stressed NAV | Loss (%) | Margin Deficit | Insolvent ")
    print("------------------------------------------------------------------------------------------------")
    for name, s_params in scenarios.items():
        s_res = stress_test_drawdowns(
            initial_cap,
            float(s_params["spot_shock"]),
            float(s_params["vix_shock"]),
            target_lev,
            margin_req,
        )
        s_shock_pct = float(s_params["spot_shock"]) * 100.0
        v_shock_val = float(s_params["vix_shock"])
        s_row = (
            f" {name:16s} |    {s_shock_pct:6.1f}% |    +{v_shock_val:4.1f} |"
            f"   {s_res['stressed_nav']:10.2f} |   {s_res['loss_fraction'] * 100.0:5.1f}% |"
            f"     {s_res['margin_deficiency']:10.2f} |   {bool(s_res['is_insolvent'])} "
        )
        print(s_row)

    metrics = evaluate_strategy_metrics(sim_res["returns"], rf_annual=0.02, periods_per_year=252.0)
    print("\n5. Risk-Adjusted Performance & Higher Moments:")
    print(f"   Annualized Return:  {metrics['mean_return'] * 100.0:.2f}%")
    print(f"   Annualized Vol:     {metrics['volatility'] * 100.0:.2f}%")
    print(f"   Sharpe Ratio:       {metrics['sharpe_ratio']:.4f}")
    print(f"   Sortino Ratio:      {metrics['sortino_ratio']:.4f}")
    print(f"   Return Skewness:    {metrics['skewness']:.4f}")
    print(f"   Excess Kurtosis:    {metrics['excess_kurtosis']:.4f}")
    print(f"   Tail Risk Penalty:  {metrics['tail_risk_penalty']:.4f}")


main()
