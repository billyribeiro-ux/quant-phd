"""Reference implementation of CF7: Financial Modeling & Reconciler.

Implements the integrated three-statement financial model, analytical closed-form
revolver circularity resolution, DCF valuation, 2D sensitivity analysis, and
automated integrity and spreadsheet reconciliation audits.
"""

from __future__ import annotations

from typing import Any

from integrity import (  # type: ignore[import-not-found, unused-ignore]
    check_balance_sheet,
    check_cash_tie_out,
    check_hardcodes_in_formulas,
    check_reconciliation,
)


def validate_inputs(inputs: dict[str, Any]) -> None:
    """Validate input parameters, raising ValueError on invalid or out-of-domain values."""
    op = inputs.get("operating_assumptions", {})
    debt = inputs.get("debt_assumptions", {})
    val = inputs.get("valuation_assumptions", {})
    hist = inputs.get("historical_data", {})

    if not hist:
        raise ValueError("historical_data is required")

    tax_rate = float(op.get("tax_rate", 0.0))
    if not (0.0 <= tax_rate < 1.0):
        raise ValueError("tax_rate must lie in [0, 1)")

    for g in op.get("revenue_growth", []):
        if g <= -1.0:
            raise ValueError("revenue_growth cannot be below -100%")

    wacc = float(val.get("wacc", 0.0))
    if wacc <= 0.0:
        raise ValueError("wacc must be strictly positive")

    g_term = float(val.get("terminal_growth_rate", 0.0))
    if g_term >= wacc:
        raise ValueError("terminal_growth_rate must be strictly less than wacc")

    shares = float(val.get("shares_outstanding", 0.0))
    if shares <= 0.0:
        raise ValueError("shares_outstanding must be strictly positive")

    if float(debt.get("revolver_commitment", 0.0)) < 0.0:
        raise ValueError("revolver_commitment cannot be negative")
    if float(debt.get("minimum_cash", 0.0)) < 0.0:
        raise ValueError("minimum_cash cannot be negative")


def solve_revolver_circularity(
    c_min: float,
    c_prev: float,
    r_prev: float,
    cf_core: float,
    r_rate: float,
    c_rate: float,
    tax_rate: float,
    max_revolver: float,
    div_rate: float = 0.0,
) -> tuple[float, float, float]:
    """Solve revolver borrowing, ending cash, and net interest via exact closed form.

    Returns (revolver_ending, cash_ending, revolver_draw_or_repay).
    """
    alpha = (1.0 - div_rate) * (1.0 - tax_rate)

    # Branch 1: Try zero revolver (surplus test)
    # When R_t = 0, delta_R = -R_prev, R_bar = 0.5 * R_prev
    num_c_zero = c_prev * (1.0 + 0.5 * alpha * c_rate) + cf_core - r_prev * (1.0 + 0.5 * alpha * r_rate)
    den_c_zero = 1.0 - 0.5 * alpha * c_rate
    c_zero = num_c_zero / den_c_zero

    if c_zero >= c_min:
        # Cash is abundant: pay off revolver completely
        r_t = 0.0
        c_t = c_zero
        delta_r = -r_prev
        return r_t, c_t, delta_r

    # Branch 2: Cash deficit exists -> hold cash at c_min, solve for R_t
    c_bar_min = 0.5 * (c_prev + c_min)
    num_r = (c_min - c_prev) - cf_core - alpha * c_rate * c_bar_min + r_prev * (1.0 + 0.5 * alpha * r_rate)
    den_r = 1.0 - 0.5 * alpha * r_rate
    r_calc = num_r / den_r

    if r_calc <= max_revolver:
        # Standard deficit: revolver covers deficit exactly
        r_t = max(0.0, r_calc)
        c_t = c_min
        delta_r = r_t - r_prev
        return r_t, c_t, delta_r

    # Branch 3: Revolver commitment binds (R_t = max_revolver, cash drops below c_min)
    r_t = max_revolver
    delta_r = max_revolver - r_prev
    num_c_cap = (
        c_prev * (1.0 + 0.5 * alpha * c_rate) + cf_core - 0.5 * alpha * r_rate * (r_prev + max_revolver) + delta_r
    )
    den_c_cap = 1.0 - 0.5 * alpha * c_rate
    c_t = num_c_cap / den_c_cap
    return r_t, c_t, delta_r


def build_model(inputs: dict[str, Any]) -> dict[str, Any]:
    """Build the fully articulated three-statement financial model and DCF valuation."""
    validate_inputs(inputs)

    hist = inputs["historical_data"]
    op = inputs["operating_assumptions"]
    debt_cfg = inputs["debt_assumptions"]
    val_cfg = inputs["valuation_assumptions"]

    horizon = int(inputs.get("horizon", len(op["revenue_growth"])))
    rev_growth = op["revenue_growth"]
    gross_margin = op["gross_margin"]
    sga_pct = op["sga_pct_revenue"]
    depr_pct = op["depreciation_pct_ppe"]
    capex_pct = op["capex_pct_revenue"]
    dso = float(op["dso"])
    dio = float(op["dio"])
    dpo = float(op["dpo"])
    tax_rate = float(op["tax_rate"])

    term_amort_sched = debt_cfg["term_debt_amortization"]
    term_rate = float(debt_cfg["term_debt_interest_rate"])
    revolver_rate = float(debt_cfg["revolver_interest_rate"])
    cash_rate = float(debt_cfg["cash_interest_rate"])
    c_min = float(debt_cfg["minimum_cash"])
    revolver_comm = float(debt_cfg["revolver_commitment"])
    div_payout = float(debt_cfg.get("dividend_payout_ratio", 0.0))

    # Output containers
    is_rev: list[float] = []
    is_cogs: list[float] = []
    is_gp: list[float] = []
    is_sga: list[float] = []
    is_ebitda: list[float] = []
    is_depr: list[float] = []
    is_ebit: list[float] = []
    is_int_exp: list[float] = []
    is_int_inc: list[float] = []
    is_net_int: list[float] = []
    is_ebt: list[float] = []
    is_tax: list[float] = []
    is_ni: list[float] = []

    bs_cash: list[float] = []
    bs_ar: list[float] = []
    bs_inv: list[float] = []
    bs_net_ppe: list[float] = []
    bs_assets: list[float] = []
    bs_ap: list[float] = []
    bs_revolver: list[float] = []
    bs_term_debt: list[float] = []
    bs_total_debt: list[float] = []
    bs_liab: list[float] = []
    bs_common_stock: list[float] = []
    bs_re: list[float] = []
    bs_equity: list[float] = []
    bs_check: list[float] = []

    cfs_ni: list[float] = []
    cfs_depr: list[float] = []
    cfs_delta_ar: list[float] = []
    cfs_delta_inv: list[float] = []
    cfs_delta_ap: list[float] = []
    cfs_cfo: list[float] = []
    cfs_capex: list[float] = []
    cfs_cfi: list[float] = []
    cfs_term_repay: list[float] = []
    cfs_revolver_net: list[float] = []
    cfs_div: list[float] = []
    cfs_cff: list[float] = []
    cfs_net_change_cash: list[float] = []
    cfs_beg_cash: list[float] = []
    cfs_end_cash: list[float] = []
    cfs_tie_out: list[float] = []

    ds_term_beg: list[float] = []
    ds_term_amort: list[float] = []
    ds_term_end: list[float] = []
    ds_revolver_beg: list[float] = []
    ds_revolver_draw_repay: list[float] = []
    ds_revolver_end: list[float] = []
    ds_total_debt: list[float] = []
    ds_net_int: list[float] = []

    # State tracking initialized from Year 0
    prev_rev = float(hist["revenue"])
    prev_net_ppe = float(hist["net_ppe"])
    prev_ar = float(hist["accounts_receivable"])
    prev_inv = float(hist["inventory"])
    prev_ap = float(hist["accounts_payable"])
    prev_term_debt = float(hist["term_debt"])
    prev_revolver = float(hist["revolver_balance"])
    prev_cash = float(hist["cash"])
    prev_re = float(hist["retained_earnings"])
    prev_common_stock = float(hist["common_stock"])

    for t in range(horizon):
        # 1. Operating Statement (Income Statement pre-interest)
        rev = prev_rev * (1.0 + rev_growth[t])
        gp = rev * gross_margin[t]
        cogs = rev - gp
        sga = rev * sga_pct[t]
        ebitda = gp - sga

        capex = rev * capex_pct[t]
        depr = prev_net_ppe * depr_pct[t]
        net_ppe = prev_net_ppe + capex - depr
        ebt_op = ebitda - depr  # Operating EBIT

        # 2. Working Capital Schedule
        ar = rev * (dso / 365.0)
        inv = cogs * (dio / 365.0)
        purchases = cogs + (inv - prev_inv)
        ap = purchases * (dpo / 365.0)

        delta_ar = ar - prev_ar
        delta_inv = inv - prev_inv
        delta_ap = ap - prev_ap
        delta_nwc = delta_ar + delta_inv - delta_ap

        # 3. Term Debt Schedule
        term_amort_mand = term_amort_sched[t] if t < len(term_amort_sched) else 0.0
        term_amort = min(prev_term_debt, term_amort_mand)
        term_debt_end = prev_term_debt - term_amort
        term_debt_avg = 0.5 * (prev_term_debt + term_debt_end)
        term_interest = term_debt_avg * term_rate

        # 4. Revolver Circularity Resolution
        alpha = (1.0 - div_payout) * (1.0 - tax_rate)
        cf_core = alpha * (ebt_op - term_interest) + depr - delta_nwc - capex - term_amort
        revolver_end, cash_end, delta_revolver = solve_revolver_circularity(
            c_min=c_min,
            c_prev=prev_cash,
            r_prev=prev_revolver,
            cf_core=cf_core,
            r_rate=revolver_rate,
            c_rate=cash_rate,
            tax_rate=tax_rate,
            max_revolver=revolver_comm,
            div_rate=div_payout,
        )

        # 5. Final Interest, Tax, Net Income & Dividends
        revolver_avg = 0.5 * (prev_revolver + revolver_end)
        cash_avg = 0.5 * (prev_cash + cash_end)
        revolver_int = revolver_avg * revolver_rate
        cash_int = cash_avg * cash_rate

        int_exp = term_interest + revolver_int
        int_inc = cash_int
        net_int = int_exp - int_inc

        ebt = ebt_op - net_int
        tax = max(0.0, ebt * tax_rate)
        ni = ebt - tax
        div = max(0.0, ni * div_payout)

        # 6. Retained Earnings & Balance Sheet
        re = prev_re + ni - div
        common_stock = prev_common_stock
        equity = common_stock + re
        total_debt = term_debt_end + revolver_end

        assets = cash_end + ar + inv + net_ppe
        liab = ap + revolver_end + term_debt_end
        bs_gap = assets - (liab + equity)

        # 7. Cash Flow Statement
        cfo = ni + depr - delta_ar - delta_inv + delta_ap
        cfi = -capex
        cff = delta_revolver - term_amort - div
        net_cash_flow = cfo + cfi + cff
        tie_out_gap = abs(cash_end - (prev_cash + net_cash_flow))

        # Append all outputs
        is_rev.append(rev)
        is_cogs.append(cogs)
        is_gp.append(gp)
        is_sga.append(sga)
        is_ebitda.append(ebitda)
        is_depr.append(depr)
        is_ebit.append(ebt_op)
        is_int_exp.append(int_exp)
        is_int_inc.append(int_inc)
        is_net_int.append(net_int)
        is_ebt.append(ebt)
        is_tax.append(tax)
        is_ni.append(ni)

        bs_cash.append(cash_end)
        bs_ar.append(ar)
        bs_inv.append(inv)
        bs_net_ppe.append(net_ppe)
        bs_assets.append(assets)
        bs_ap.append(ap)
        bs_revolver.append(revolver_end)
        bs_term_debt.append(term_debt_end)
        bs_total_debt.append(total_debt)
        bs_liab.append(liab)
        bs_common_stock.append(common_stock)
        bs_re.append(re)
        bs_equity.append(equity)
        bs_check.append(bs_gap)

        cfs_ni.append(ni)
        cfs_depr.append(depr)
        cfs_delta_ar.append(delta_ar)
        cfs_delta_inv.append(delta_inv)
        cfs_delta_ap.append(delta_ap)
        cfs_cfo.append(cfo)
        cfs_capex.append(capex)
        cfs_cfi.append(cfi)
        cfs_term_repay.append(term_amort)
        cfs_revolver_net.append(delta_revolver)
        cfs_div.append(div)
        cfs_cff.append(cff)
        cfs_net_change_cash.append(net_cash_flow)
        cfs_beg_cash.append(prev_cash)
        cfs_end_cash.append(cash_end)
        cfs_tie_out.append(tie_out_gap)

        ds_term_beg.append(prev_term_debt)
        ds_term_amort.append(term_amort)
        ds_term_end.append(term_debt_end)
        ds_revolver_beg.append(prev_revolver)
        ds_revolver_draw_repay.append(delta_revolver)
        ds_revolver_end.append(revolver_end)
        ds_total_debt.append(total_debt)
        ds_net_int.append(net_int)

        # Advance state
        prev_rev = rev
        prev_net_ppe = net_ppe
        prev_ar = ar
        prev_inv = inv
        prev_ap = ap
        prev_term_debt = term_debt_end
        prev_revolver = revolver_end
        prev_cash = cash_end
        prev_re = re

    # 8. DCF Valuation
    wacc = float(val_cfg["wacc"])
    terminal_g = float(val_cfg["terminal_growth_rate"])
    shares = float(val_cfg["shares_outstanding"])

    fcff_list: list[float] = []
    pv_fcff_list: list[float] = []
    df_list: list[float] = []

    for t in range(horizon):
        nopat = is_ebit[t] * (1.0 - tax_rate)
        delta_nwc_t = cfs_delta_ar[t] + cfs_delta_inv[t] - cfs_delta_ap[t]
        fcff_t = nopat + is_depr[t] - cfs_capex[t] - delta_nwc_t
        df_t = 1.0 / ((1.0 + wacc) ** (t + 1))
        pv_fcff_t = fcff_t * df_t
        fcff_list.append(fcff_t)
        df_list.append(df_t)
        pv_fcff_list.append(pv_fcff_t)

    pv_forecast = sum(pv_fcff_list)
    fcff_terminal = fcff_list[-1] * (1.0 + terminal_g)
    terminal_value = fcff_terminal / (wacc - terminal_g)
    pv_tv = terminal_value / ((1.0 + wacc) ** horizon)

    enterprise_value = pv_forecast + pv_tv
    net_debt_0 = float(hist["total_debt"]) - float(hist["cash"])
    equity_value = enterprise_value - net_debt_0
    equity_value_per_share = equity_value / shares

    # 9. 2D Sensitivity Analysis
    wacc_grid = [round(wacc - 0.02 + 0.01 * i, 4) for i in range(5)]
    g_grid = [round(terminal_g - 0.01 + 0.005 * j, 4) for j in range(5)]
    sensitivity_matrix = compute_sensitivity_table(
        fcff_list=fcff_list,
        horizon=horizon,
        net_debt=net_debt_0,
        shares=shares,
        wacc_range=wacc_grid,
        g_range=g_grid,
    )

    result = {
        "income_statement": {
            "revenue": is_rev,
            "cogs": is_cogs,
            "gross_profit": is_gp,
            "sga": is_sga,
            "ebitda": is_ebitda,
            "depreciation": is_depr,
            "ebit": is_ebit,
            "interest_expense": is_int_exp,
            "interest_income": is_int_inc,
            "net_interest": is_net_int,
            "ebt": is_ebt,
            "tax": is_tax,
            "net_income": is_ni,
        },
        "balance_sheet": {
            "cash": bs_cash,
            "accounts_receivable": bs_ar,
            "inventory": bs_inv,
            "net_ppe": bs_net_ppe,
            "total_assets": bs_assets,
            "accounts_payable": bs_ap,
            "revolver_balance": bs_revolver,
            "term_debt": bs_term_debt,
            "total_debt": bs_total_debt,
            "total_liabilities": bs_liab,
            "common_stock": bs_common_stock,
            "retained_earnings": bs_re,
            "total_equity": bs_equity,
            "balance_check": bs_check,
        },
        "cash_flow_statement": {
            "net_income": cfs_ni,
            "depreciation": cfs_depr,
            "delta_ar": cfs_delta_ar,
            "delta_inventory": cfs_delta_inv,
            "delta_ap": cfs_delta_ap,
            "cash_from_operations": cfs_cfo,
            "capex": cfs_capex,
            "cash_from_investing": cfs_cfi,
            "term_debt_repayment": cfs_term_repay,
            "revolver_net_borrowing": cfs_revolver_net,
            "dividends": cfs_div,
            "cash_from_financing": cfs_cff,
            "net_change_in_cash": cfs_net_change_cash,
            "beginning_cash": cfs_beg_cash,
            "ending_cash": cfs_end_cash,
            "cash_tie_out": cfs_tie_out,
        },
        "debt_schedule": {
            "term_debt_opening": ds_term_beg,
            "term_debt_amortization": ds_term_amort,
            "term_debt_closing": ds_term_end,
            "revolver_opening": ds_revolver_beg,
            "revolver_draw_or_repay": ds_revolver_draw_repay,
            "revolver_closing": ds_revolver_end,
            "total_debt": ds_total_debt,
            "net_interest": ds_net_int,
        },
        "dcf_valuation": {
            "fcff": fcff_list,
            "discount_factors": df_list,
            "pv_fcff": pv_fcff_list,
            "pv_forecast": pv_forecast,
            "terminal_value": terminal_value,
            "pv_terminal_value": pv_tv,
            "enterprise_value": enterprise_value,
            "net_debt": net_debt_0,
            "equity_value": equity_value,
            "shares_outstanding": shares,
            "equity_value_per_share": equity_value_per_share,
        },
        "sensitivities": {
            "wacc_grid": wacc_grid,
            "g_grid": g_grid,
            "equity_value_per_share": sensitivity_matrix,
        },
    }

    # 10. Automated Integrity Checks
    bs_integrity = check_balance_sheet(result)
    cash_integrity = check_cash_tie_out(result)
    result["integrity"] = {
        "balance_check_passed": bs_integrity["passed"],
        "max_bs_imbalance": bs_integrity["max_imbalance"],
        "cash_tie_out_passed": cash_integrity["passed"],
        "max_cash_discrepancy": cash_integrity["max_discrepancy"],
    }

    return result


def compute_sensitivity_table(
    fcff_list: list[float],
    horizon: int,
    net_debt: float,
    shares: float,
    wacc_range: list[float],
    g_range: list[float],
) -> list[list[float]]:
    """Compute a 2D matrix of equity value per share over WACC and terminal growth grids."""
    matrix: list[list[float]] = []
    for w in wacc_range:
        row: list[float] = []
        for g in g_range:
            if g >= w:
                row.append(float("nan"))
                continue
            pv_fcff = sum(fcff / ((1.0 + w) ** (t + 1)) for t, fcff in enumerate(fcff_list))
            tv = (fcff_list[-1] * (1.0 + g)) / (w - g)
            pv_tv = tv / ((1.0 + w) ** horizon)
            ev = pv_fcff + pv_tv
            eq_val = (ev - net_debt) / shares
            row.append(round(eq_val, 4))
        matrix.append(row)
    return matrix


def reconcile_sheets(
    sheet_data: dict[str, Any],
    model_data: dict[str, Any],
    tolerance: float = 1e-4,
) -> dict[str, Any]:
    """Reconcile extracted spreadsheet data against python model data."""
    result: dict[str, Any] = check_reconciliation(sheet_data, model_data, tolerance)
    return result


def check_hardcodes(formulas: dict[str, str]) -> list[str]:
    """Verify that calculation cells do not contain hard-coded numeric literals."""
    violations: list[str] = check_hardcodes_in_formulas(formulas)
    return violations
