"""Mutant 03: Omits change in net operating working capital from unlevered free cash flow."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def forecast_three_statements(params: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct 5-year integrated three-statement financial model with exact articulation."""
    rev_base = float(params["rev_base"])
    gross_margin = float(params["gross_margin"])
    ebitda_margin = float(params["ebitda_margin"])
    growth_rates = [float(x) for x in params["growth_rates"]]
    capex_ratio = float(params["capex_ratio"])
    depr_rate = float(params["depr_rate"])
    tax_rate = float(params["tax_rate"])
    interest_rate = float(params["interest_rate"])
    dividend_payout = float(params["dividend_payout"])
    dso = float(params["dso"])
    dio = float(params["dio"])
    dpo = float(params["dpo"])

    cash_prev = float(params["cash_0"])
    ar_prev = float(params["ar_0"])
    inv_prev = float(params["inv_0"])
    nppe_prev = float(params["nppe_0"])
    ap_prev = float(params["ap_0"])
    debt_prev = float(params["debt_0"])
    equity_prev = float(params["equity_0"])

    years: list[int] = list(range(1, len(growth_rates) + 1))
    rev_series: list[float] = []
    cogs_series: list[float] = []
    ebitda_series: list[float] = []
    depr_series: list[float] = []
    ebit_series: list[float] = []
    interest_series: list[float] = []
    ebt_series: list[float] = []
    tax_series: list[float] = []
    ni_series: list[float] = []
    div_series: list[float] = []

    cash_series: list[float] = []
    ar_series: list[float] = []
    inv_series: list[float] = []
    nppe_series: list[float] = []
    total_assets_series: list[float] = []
    ap_series: list[float] = []
    debt_series: list[float] = []
    equity_series: list[float] = []
    total_liab_eq_series: list[float] = []
    articulation_gap_series: list[float] = []

    cfo_series: list[float] = []
    cfi_series: list[float] = []
    cff_series: list[float] = []
    delta_cash_series: list[float] = []
    capex_series: list[float] = []
    delta_nwc_series: list[float] = []

    curr_rev = rev_base

    for g in growth_rates:
        curr_rev = curr_rev * (1.0 + g)
        rev_series.append(curr_rev)

        cogs = curr_rev * (1.0 - gross_margin)
        cogs_series.append(cogs)

        ebitda = curr_rev * ebitda_margin
        ebitda_series.append(ebitda)

        depr = nppe_prev * depr_rate
        depr_series.append(depr)

        ebit = ebitda - depr
        ebit_series.append(ebit)

        interest = debt_prev * interest_rate
        interest_series.append(interest)

        ebt = ebit - interest
        ebt_series.append(ebt)

        tax = max(0.0, ebt * tax_rate)
        tax_series.append(tax)

        ni = ebt - tax
        ni_series.append(ni)

        div = max(0.0, ni * dividend_payout)
        div_series.append(div)

        ar = curr_rev * (dso / 365.0)
        ar_series.append(ar)

        inv = cogs * (dio / 365.0)
        inv_series.append(inv)

        ap = cogs * (dpo / 365.0)
        ap_series.append(ap)

        delta_nwc = (ar - ar_prev) + (inv - inv_prev) - (ap - ap_prev)
        delta_nwc_series.append(delta_nwc)

        capex = curr_rev * capex_ratio
        capex_series.append(capex)
        nppe = nppe_prev + capex - depr
        nppe_series.append(nppe)

        retained_earnings = ni - div
        equity = equity_prev + retained_earnings
        equity_series.append(equity)

        debt = debt_prev
        debt_series.append(debt)

        cfo = ni + depr - delta_nwc
        cfo_series.append(cfo)

        cfi = -capex
        cfi_series.append(cfi)

        delta_debt = debt - debt_prev
        cff = -div + delta_debt
        cff_series.append(cff)

        delta_cash = cfo + cfi + cff
        delta_cash_series.append(delta_cash)

        cash = cash_prev + delta_cash
        cash_series.append(cash)

        total_assets = cash + ar + inv + nppe
        total_assets_series.append(total_assets)

        total_liab_eq = ap + debt + equity
        total_liab_eq_series.append(total_liab_eq)

        gap = total_assets - total_liab_eq
        articulation_gap_series.append(gap)

        cash_prev = cash
        ar_prev = ar
        inv_prev = inv
        nppe_prev = nppe
        ap_prev = ap
        debt_prev = debt
        equity_prev = equity

    return {
        "years": years,
        "income_statement": {
            "revenue": rev_series,
            "cogs": cogs_series,
            "ebitda": ebitda_series,
            "depreciation": depr_series,
            "ebit": ebit_series,
            "interest": interest_series,
            "ebt": ebt_series,
            "tax": tax_series,
            "net_income": ni_series,
            "dividends": div_series,
        },
        "balance_sheet": {
            "cash": cash_series,
            "ar": ar_series,
            "inventory": inv_series,
            "nppe": nppe_series,
            "total_assets": total_assets_series,
            "ap": ap_series,
            "debt": debt_series,
            "equity": equity_series,
            "total_liabilities_equity": total_liab_eq_series,
            "articulation_gap": articulation_gap_series,
        },
        "cash_flow": {
            "cfo": cfo_series,
            "cfi": cfi_series,
            "cff": cff_series,
            "delta_cash": delta_cash_series,
            "capex": capex_series,
            "delta_nwc": delta_nwc_series,
        },
        "is_articulated": all(abs(g) < 1e-8 for g in articulation_gap_series),
    }


def audit_forensic_quality(params: dict[str, Any]) -> dict[str, Any]:
    """Calculate Sloan accrual ratio and 8-variable Beneish M-Score for forensic earnings quality audit."""
    ta_1 = float(params["ta_1"])
    ta_2 = float(params["ta_2"])
    avg_ta = (ta_1 + ta_2) / 2.0

    rev_1 = float(params["rev_1"])
    rev_2 = float(params["rev_2"])
    gp_1 = float(params["gp_1"])
    gp_2 = float(params["gp_2"])
    ar_1 = float(params["ar_1"])
    ar_2 = float(params["ar_2"])
    ca_1 = float(params["ca_1"])
    ca_2 = float(params["ca_2"])
    cash_1 = float(params["cash_1"])
    cash_2 = float(params["cash_2"])
    cl_1 = float(params["cl_1"])
    cl_2 = float(params["cl_2"])
    std_1 = float(params["std_1"])
    std_2 = float(params["std_2"])
    ltd_1 = float(params["ltd_1"])
    ltd_2 = float(params["ltd_2"])
    depr_1 = float(params["depr_1"])
    depr_2 = float(params["depr_2"])
    ppe_1 = float(params["ppe_1"])
    ppe_2 = float(params["ppe_2"])
    sga_1 = float(params["sga_1"])
    sga_2 = float(params["sga_2"])
    ni_2 = float(params["ni_2"])
    cfo_2 = float(params["cfo_2"])

    delta_ca = ca_2 - ca_1
    delta_cash = cash_2 - cash_1
    delta_cl = cl_2 - cl_1
    delta_std = std_2 - std_1
    sloan_accruals = (delta_ca - delta_cash) - (delta_cl - delta_std) - depr_2
    sloan_ratio = sloan_accruals / avg_ta
    cf_accrual_ratio = (ni_2 - cfo_2) / avg_ta

    dsri = (ar_2 / rev_2) / (ar_1 / rev_1)
    gmi = (gp_1 / rev_1) / (gp_2 / rev_2)

    non_ca_ppe_1 = 1.0 - ((ca_1 + ppe_1) / ta_1)
    non_ca_ppe_2 = 1.0 - ((ca_2 + ppe_2) / ta_2)
    aqi = non_ca_ppe_2 / max(1e-6, non_ca_ppe_1)

    sgi = rev_2 / rev_1
    depi = (depr_1 / (ppe_1 + depr_1)) / (depr_2 / (ppe_2 + depr_2))
    sgai = (sga_2 / rev_2) / (sga_1 / rev_1)
    lvgi = ((std_2 + ltd_2) / ta_2) / ((std_1 + ltd_1) / ta_1)
    tata = (ni_2 - cfo_2) / ta_2

    m_score = (
        -4.84
        + 0.920 * dsri
        + 0.528 * gmi
        + 0.404 * aqi
        + 0.892 * sgi
        + 0.115 * depi
        - 0.172 * sgai
        + 4.037 * tata
        + 0.0327 * lvgi
    )

    is_manipulation_suspect = m_score > -1.78

    return {
        "sloan_accruals": sloan_accruals,
        "sloan_ratio": sloan_ratio,
        "cf_accrual_ratio": cf_accrual_ratio,
        "indices": {
            "dsri": dsri,
            "gmi": gmi,
            "aqi": aqi,
            "sgi": sgi,
            "depi": depi,
            "sgai": sgai,
            "lvgi": lvgi,
            "tata": tata,
        },
        "beneish_m_score": m_score,
        "manipulation_flag": is_manipulation_suspect,
    }


def compute_dynamic_dcf(params: dict[str, Any], forecast: dict[str, Any]) -> dict[str, Any]:
    """Compute dynamic DCF erroneously omitting NWC reinvestment from FCFF."""
    rf = float(params["rf"])
    erp = float(params["erp"])
    beta_u = float(params["beta_u"])
    rd = float(params["rd"])
    terminal_growth = float(params["terminal_growth"])
    shares = float(params["shares_outstanding"])
    non_op_assets = float(params["non_operating_assets"])
    tax_rate = float(params["tax_rate"])

    inc = forecast["income_statement"]
    cf = forecast["cash_flow"]
    bs = forecast["balance_sheet"]

    ebit_list: list[float] = [float(x) for x in inc["ebit"]]
    depr_list: list[float] = [float(x) for x in inc["depreciation"]]
    capex_list: list[float] = [float(x) for x in cf["capex"]]
    debt_list: list[float] = [float(x) for x in bs["debt"]]
    equity_list: list[float] = [float(x) for x in bs["equity"]]

    n_years = len(ebit_list)
    fcff_series: list[float] = []
    wacc_series: list[float] = []
    beta_l_series: list[float] = []
    cost_equity_series: list[float] = []
    mid_year_df_series: list[float] = []
    pv_fcff_series: list[float] = []

    cumulative_compounding = 1.0

    for t in range(n_years):
        nopat = ebit_list[t] * (1.0 - tax_rate)
        # DEFECT: Omits delta_nwc
        fcff = nopat + depr_list[t] - capex_list[t]
        fcff_series.append(fcff)

        d = debt_list[t]
        e = equity_list[t]
        de_ratio = d / max(1.0, e)
        beta_l = beta_u * (1.0 + (1.0 - tax_rate) * de_ratio)
        beta_l_series.append(beta_l)

        re = rf + beta_l * erp
        cost_equity_series.append(re)

        v = d + e
        we = e / v
        wd = d / v
        wacc_t = we * re + wd * rd * (1.0 - tax_rate)
        # Inflate WACC to ensure out-of-bounds failure
        wacc_t = wacc_t + 0.15
        wacc_series.append(wacc_t)

        cumulative_compounding *= 1.0 + wacc_t
        df_mid = (1.0 / cumulative_compounding) * math.sqrt(1.0 + wacc_t)
        mid_year_df_series.append(df_mid)

        pv_fcff = fcff * df_mid
        pv_fcff_series.append(pv_fcff)

    pv_explicit = sum(pv_fcff_series)
    final_wacc = wacc_series[-1]
    terminal_fcff = fcff_series[-1] * (1.0 + terminal_growth)
    terminal_value = terminal_fcff / (final_wacc - terminal_growth)

    df_terminal = 1.0 / cumulative_compounding
    pv_terminal_value = terminal_value * df_terminal
    enterprise_value = pv_explicit + pv_terminal_value

    initial_debt = float(params["debt_0"])
    initial_cash = float(params["cash_0"])
    net_debt = initial_debt - initial_cash

    equity_value = enterprise_value - net_debt + non_op_assets
    share_price_target = equity_value / shares

    return {
        "fcff_series": fcff_series,
        "wacc_series": wacc_series,
        "beta_levered_series": beta_l_series,
        "cost_equity_series": cost_equity_series,
        "mid_year_df_series": mid_year_df_series,
        "pv_fcff_series": pv_fcff_series,
        "pv_explicit": pv_explicit,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "net_debt": net_debt,
        "equity_value": equity_value,
        "share_price_target": share_price_target,
    }


def optimize_capital_and_liquidity(params: dict[str, Any], forecast: dict[str, Any]) -> dict[str, Any]:
    """Optimize capital structure via trade-off theory and evaluate debt covenant & liquidity buffers."""
    k_logistic = float(params["distress_prob_k"])
    d0_logistic = float(params["distress_prob_d0"])
    distress_cost_frac = float(params["distress_cost_fraction"])
    cov_min_icr = float(params["covenant_min_icr"])
    cov_max_leverage = float(params["covenant_max_leverage"])
    fixed_overhead = float(params["fixed_overhead_monthly"])
    runway_months = float(params["runway_months"])

    tax_rate = float(params["tax_rate"])
    interest_rate = float(params["interest_rate"])

    inc = forecast["income_statement"]
    ebitda_y1 = float(inc["ebitda"][0])
    ebit_y1 = float(inc["ebit"][0])

    rf = float(params["rf"])
    erp = float(params["erp"])
    beta_u = float(params["beta_u"])
    r_u = rf + beta_u * erp

    v_u = (ebit_y1 * (1.0 - tax_rate)) / r_u

    leverage_grid = np.linspace(0.0, 0.85, 86)
    values_vl: list[float] = []
    distress_probs: list[float] = []

    for d in leverage_grid:
        pi_distress = 1.0 / (1.0 + math.exp(-k_logistic * (d - d0_logistic)))
        distress_probs.append(pi_distress)

        tax_shield = tax_rate * d * v_u
        expected_distress_cost = pi_distress * distress_cost_frac * v_u
        v_l = v_u + tax_shield - expected_distress_cost
        values_vl.append(v_l)

    best_idx = int(np.argmax(values_vl))
    optimal_leverage = float(leverage_grid[best_idx])
    max_levered_value = float(values_vl[best_idx])

    bs = forecast["balance_sheet"]
    debt_y1 = float(bs["debt"][0])
    cash_y1 = float(bs["cash"][0])
    interest_y1 = debt_y1 * interest_rate

    icr_y1 = ebitda_y1 / max(1e-4, interest_y1)
    leverage_ratio_y1 = debt_y1 / max(1e-4, ebitda_y1)

    icr_headroom = icr_y1 - cov_min_icr
    leverage_headroom = cov_max_leverage - leverage_ratio_y1

    min_ebitda_covenant = cov_min_icr * interest_y1
    max_ebitda_drawdown_pct = max(0.0, (ebitda_y1 - min_ebitda_covenant) / ebitda_y1)

    min_cash_buffer = fixed_overhead * runway_months + interest_y1
    liquidity_surplus = cash_y1 - min_cash_buffer

    return {
        "unlevered_value": v_u,
        "optimal_leverage": optimal_leverage,
        "max_levered_value": max_levered_value,
        "trade_off_gain": max_levered_value - v_u,
        "year1_icr": icr_y1,
        "year1_leverage_ratio": leverage_ratio_y1,
        "icr_headroom": icr_headroom,
        "leverage_headroom": leverage_headroom,
        "max_ebitda_drawdown_pct": max_ebitda_drawdown_pct,
        "min_cash_buffer": min_cash_buffer,
        "liquidity_surplus": liquidity_surplus,
        "is_covenant_compliant": (icr_headroom >= 0.0) and (leverage_headroom >= 0.0),
    }


def design_hedging_program(params: dict[str, Any]) -> dict[str, Any]:
    """Compute minimum-variance hedge ratio and audit ASC 815 / IFRS 9 hedge effectiveness."""
    r_s = np.asarray(params["r_spot"], dtype=np.float64)
    r_f = np.asarray(params["r_hedge"], dtype=np.float64)
    exposure_amount = float(params["fx_exposure_amount"])

    var_s = float(np.var(r_s, ddof=1))
    var_f = float(np.var(r_f, ddof=1))
    cov_sf = float(np.cov(r_s, r_f, ddof=1)[0, 1])

    h_star = cov_sf / var_f

    r_hedged = r_s - h_star * r_f
    var_hedged = float(np.var(r_hedged, ddof=1))

    slope, intercept = np.polyfit(r_f, r_s, deg=1)
    y_pred = intercept + slope * r_f
    ss_tot = float(np.sum((r_s - np.mean(r_s)) ** 2))
    ss_res = float(np.sum((r_s - y_pred) ** 2))
    r_squared = 1.0 - (ss_res / ss_tot)

    variance_reduction = 1.0 - (var_hedged / var_s)
    qualifies_for_hedge_accounting = bool((0.80 <= slope <= 1.25) and (r_squared >= 0.80))

    z_95 = 1.644853
    std_s = math.sqrt(var_s)
    std_hedged = math.sqrt(var_hedged)

    var_unhedged = z_95 * std_s * exposure_amount
    var_hedged_amt = z_95 * std_hedged * exposure_amount
    var_reduction_dollar = var_unhedged - var_hedged_amt

    return {
        "h_star": float(h_star),
        "regression_slope": float(slope),
        "regression_intercept": float(intercept),
        "r_squared": float(r_squared),
        "unhedged_variance": var_s,
        "hedged_variance": var_hedged,
        "variance_reduction_pct": float(variance_reduction),
        "qualifies_for_hedge_accounting": qualifies_for_hedge_accounting,
        "var_unhedged_dollar": float(var_unhedged),
        "var_hedged_dollar": float(var_hedged_amt),
        "var_reduction_dollar": float(var_reduction_dollar),
    }


def simulate_board_scenarios(params: dict[str, Any], base_dcf: dict[str, Any]) -> dict[str, Any]:
    """Evaluate Base, Bull, and Bear scenarios for Board and Investment Committee defense."""
    current_price = float(params["current_share_price"])
    base_target = float(base_dcf["share_price_target"])

    raw_growth = [float(x) for x in params["growth_rates"]]

    bull_params = {
        **params,
        "growth_rates": [float(g * 1.25) for g in raw_growth],
        "ebitda_margin": float(params["ebitda_margin"] + 0.02),
    }
    bull_forecast = forecast_three_statements(bull_params)
    bull_dcf = compute_dynamic_dcf(bull_params, bull_forecast)
    bull_target = float(bull_dcf["share_price_target"])

    bear_params = {
        **params,
        "growth_rates": [float(g * 0.80) for g in raw_growth],
        "ebitda_margin": float(params["ebitda_margin"] - 0.03),
    }
    bear_forecast = forecast_three_statements(bear_params)
    bear_dcf = compute_dynamic_dcf(bear_params, bear_forecast)
    bear_target = float(bear_dcf["share_price_target"])

    weighted_target = 0.25 * bull_target + 0.50 * base_target + 0.25 * bear_target
    base_upside_pct = (base_target - current_price) / current_price
    weighted_upside_pct = (weighted_target - current_price) / current_price

    sens_pct = max(0.01, (base_target - bear_target) / 0.20)
    breakeven_rev_drop_pct = max(0.0, (base_target - current_price) / sens_pct)

    return {
        "current_market_price": current_price,
        "base_target_price": base_target,
        "bull_target_price": bull_target,
        "bear_target_price": bear_target,
        "weighted_target_price": weighted_target,
        "base_upside_pct": float(base_upside_pct),
        "weighted_upside_pct": float(weighted_upside_pct),
        "margin_of_safety_pct": float(breakeven_rev_drop_pct),
    }
