"""Rung 2 completed solution: Financial model core calculation engine.

Implements working capital changes, revolver circularity closed form,
free cash flow to firm, and DCF equity value per share.
"""

from __future__ import annotations


def solve_completion_engine() -> dict[str, float]:
    """Calculate key financial model milestones with full formulas."""
    rev_0 = 400.0
    cash_0 = 30.0
    net_debt_0 = 70.0
    c_min = 25.0
    r_prev = 10.0
    term_debt_0 = 90.0

    growth = 0.08
    gross_margin = 0.45
    sga_pct = 0.20
    depr_pct = 0.10
    capex_pct = 0.06
    dso = 45.0
    dio = 55.0
    dpo = 40.0
    tax_rate = 0.25
    term_rate = 0.06
    revolver_rate = 0.075
    cash_rate = 0.02
    term_amort = 15.0
    div_rate = 0.20
    wacc = 0.09
    terminal_g = 0.025
    shares = 10.0

    # Operating engine
    rev = rev_0 * (1.0 + growth)
    gp = rev * gross_margin
    cogs = rev - gp
    sga = rev * sga_pct
    ebitda = gp - sga
    net_ppe_0 = 180.0
    capex = rev * capex_pct
    depr = net_ppe_0 * depr_pct
    ebt_op = ebitda - depr

    ar = rev * (dso / 365.0)
    inv = cogs * (dio / 365.0)
    ar_0 = rev_0 * (dso / 365.0)
    inv_0 = (rev_0 * (1.0 - gross_margin)) * (dio / 365.0)
    purchases = cogs + (inv - inv_0)
    ap = purchases * (dpo / 365.0)
    ap_0 = (rev_0 * (1.0 - gross_margin)) * (dpo / 365.0)

    delta_ar = ar - ar_0
    delta_inv = inv - inv_0
    delta_ap = ap - ap_0
    delta_nwc = delta_ar + delta_inv - delta_ap

    term_end = term_debt_0 - term_amort
    term_avg = 0.5 * (term_debt_0 + term_end)
    term_interest = term_avg * term_rate

    alpha = (1.0 - div_rate) * (1.0 - tax_rate)
    cf_core = alpha * (ebt_op - term_interest) + depr - delta_nwc - capex - term_amort
    c_bar_min = 0.5 * (cash_0 + c_min)
    num_r = (c_min - cash_0) - cf_core - alpha * cash_rate * c_bar_min + r_prev * (1.0 + 0.5 * alpha * revolver_rate)
    den_r = 1.0 - 0.5 * alpha * revolver_rate
    r_end = num_r / den_r

    r_avg = 0.5 * (r_prev + r_end)
    c_avg = 0.5 * (cash_0 + c_min)
    net_int = term_interest + r_avg * revolver_rate - c_avg * cash_rate

    ebt = ebt_op - net_int
    tax = ebt * tax_rate
    ni = ebt - tax

    nopat = ebt_op * (1.0 - tax_rate)
    fcff_1 = nopat + depr - capex - delta_nwc
    fcff_terminal = fcff_1 * (1.0 + terminal_g)
    tv = fcff_terminal / (wacc - terminal_g)
    pv_tv = tv / (1.0 + wacc)
    pv_fcff = fcff_1 / (1.0 + wacc)
    ev = pv_fcff + pv_tv
    equity_val = ev - net_debt_0
    eq_per_share = equity_val / shares

    return {
        "delta_nwc": delta_nwc,
        "revolver_end": r_end,
        "net_income": ni,
        "fcff_1": fcff_1,
        "terminal_value": tv,
        "equity_per_share": eq_per_share,
    }


def main() -> None:
    res = solve_completion_engine()
    print("Working Capital Change:", f"{res['delta_nwc']:.4f}")
    print("Revolver Ending Balance:", f"{res['revolver_end']:.4f}")
    print("Net Income:", f"{res['net_income']:.4f}")
    print("Period 1 FCFF:", f"{res['fcff_1']:.4f}")
    print("Terminal Value:", f"{res['terminal_value']:.4f}")
    print("Equity Value Per Share:", f"{res['equity_per_share']:.4f}")


main()
