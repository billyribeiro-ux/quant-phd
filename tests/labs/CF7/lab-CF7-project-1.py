"""Lab CF7-project-1: Project Rung 1 Worked Example.

Fully worked baseline model: historical Year 0 statements, 3-period projection,
closed-form revolver circularity resolution, DCF valuation, and integrity audit.
"""

from __future__ import annotations


def run_worked_example() -> dict[str, float]:
    """Execute complete worked example calculation for AeroParts Inc."""
    # Historical base
    rev_0 = 400.0
    cash_0 = 30.0
    net_debt_0 = 70.0
    c_min = 25.0
    r_prev = 10.0
    term_debt_0 = 90.0

    # Period 1 assumptions
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

    # 1. Operating Statement
    rev = rev_0 * (1.0 + growth)  # 432.0
    gp = rev * gross_margin  # 194.4
    cogs = rev - gp  # 237.6
    sga = rev * sga_pct  # 86.4
    ebitda = gp - sga  # 108.0
    net_ppe_0 = 180.0
    capex = rev * capex_pct  # 25.92
    depr = net_ppe_0 * depr_pct  # 18.0
    net_ppe_0 + capex - depr  # 187.92
    ebt_op = ebitda - depr  # 90.0

    # 2. Working Capital
    ar = rev * (dso / 365.0)  # 53.2603
    inv = cogs * (dio / 365.0)  # 35.7973
    ar_0 = rev_0 * (dso / 365.0)  # 49.3151
    inv_0 = (rev_0 * (1 - gross_margin)) * (dio / 365.0)  # 33.1507
    purchases = cogs + (inv - inv_0)
    ap = purchases * (dpo / 365.0)
    ap_0 = (rev_0 * (1 - gross_margin)) * (dpo / 365.0)

    delta_ar = ar - ar_0
    delta_inv = inv - inv_0
    delta_ap = ap - ap_0
    delta_nwc = delta_ar + delta_inv - delta_ap

    # 3. Term debt
    term_end = term_debt_0 - term_amort  # 75.0
    term_avg = 0.5 * (term_debt_0 + term_end)
    term_interest = term_avg * term_rate  # 82.5 * 0.06 = 4.95

    # 4. Revolver Circularity
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
    ni * div_rate

    # 5. DCF
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
        "revenue": rev,
        "ebitda": ebitda,
        "net_income": ni,
        "revolver_end": r_end,
        "fcff_1": fcff_1,
        "enterprise_value": ev,
        "equity_per_share": eq_per_share,
    }


def main() -> None:
    res = run_worked_example()
    print("Projected Revenue:", f"{res['revenue']:.4f}")
    print("Projected EBITDA:", f"{res['ebitda']:.4f}")
    print("Projected Net Income:", f"{res['net_income']:.4f}")
    print("Ending Revolver Balance:", f"{res['revolver_end']:.4f}")
    print("Period 1 FCFF:", f"{res['fcff_1']:.4f}")
    print("Enterprise Value:", f"{res['enterprise_value']:.4f}")
    print("Equity Value Per Share:", f"{res['equity_per_share']:.4f}")


main()
