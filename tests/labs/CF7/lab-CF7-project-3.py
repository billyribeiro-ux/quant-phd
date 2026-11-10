"""Lab CF7-project-3: Project Rung 3 Reconciler and Integrity Diagnostics.

Executes complete model generation, balance articulation check, cash tie-out,
and reconciliation check on a seeded benchmark case.
"""

from __future__ import annotations


def run_benchmark_audit() -> dict[str, float | bool]:
    """Execute integrity and reconciliation diagnostics for the benchmark case."""
    # Benchmark case inputs
    rev_0 = 500.0
    cash_0 = 40.0
    ar_0 = 60.0
    inv_0 = 45.0
    ppe_0 = 220.0
    ap_0 = 40.0
    term_debt_0 = 120.0
    revolver_0 = 10.0
    common_stock = 150.0
    re_0 = (cash_0 + ar_0 + inv_0 + ppe_0) - (ap_0 + term_debt_0 + revolver_0) - common_stock

    growth = 0.07
    gross_margin = 0.48
    sga_pct = 0.22
    depr_pct = 0.10
    capex_pct = 0.05
    dso = 45.0
    dio = 55.0
    dpo = 42.0
    tax_rate = 0.25
    term_rate = 0.065
    revolver_rate = 0.080
    cash_rate = 0.020
    c_min = 30.0
    term_amort = 24.0
    div_payout = 0.20
    wacc = 0.095
    terminal_g = 0.025
    shares = 20.0

    # Period 1 projection
    rev_1 = rev_0 * (1.0 + growth)
    gp_1 = rev_1 * gross_margin
    cogs_1 = rev_1 - gp_1
    sga_1 = rev_1 * sga_pct
    ebitda_1 = gp_1 - sga_1
    capex_1 = rev_1 * capex_pct
    depr_1 = ppe_0 * depr_pct
    net_ppe_1 = ppe_0 + capex_1 - depr_1
    ebt_op_1 = ebitda_1 - depr_1

    ar_1 = rev_1 * (dso / 365.0)
    inv_1 = cogs_1 * (dio / 365.0)
    purchases_1 = cogs_1 + (inv_1 - inv_0)
    ap_1 = purchases_1 * (dpo / 365.0)

    delta_ar = ar_1 - ar_0
    delta_inv = inv_1 - inv_0
    delta_ap = ap_1 - ap_0
    delta_nwc = delta_ar + delta_inv - delta_ap

    term_end_1 = term_debt_0 - term_amort
    term_avg_1 = 0.5 * (term_debt_0 + term_end_1)
    term_int_1 = term_avg_1 * term_rate

    alpha = (1.0 - div_payout) * (1.0 - tax_rate)
    cf_core_1 = alpha * (ebt_op_1 - term_int_1) + depr_1 - delta_nwc - capex_1 - term_amort

    # Branch 1: Surplus test with r_1 = 0.0
    num_c_zero = cash_0 * (1.0 + 0.5 * alpha * cash_rate) + cf_core_1 - revolver_0 * (1.0 + 0.5 * alpha * revolver_rate)
    den_c_zero = 1.0 - 0.5 * alpha * cash_rate
    c_zero = num_c_zero / den_c_zero

    if c_zero >= c_min:
        r_1 = 0.0
        cash_1 = c_zero
        delta_r = -revolver_0
    else:
        c_bar_min = 0.5 * (cash_0 + c_min)
        num_r = (
            (c_min - cash_0)
            - cf_core_1
            - alpha * cash_rate * c_bar_min
            + revolver_0 * (1.0 + 0.5 * alpha * revolver_rate)
        )
        den_r = 1.0 - 0.5 * alpha * revolver_rate
        r_1 = num_r / den_r
        cash_1 = c_min
        delta_r = r_1 - revolver_0

    r_avg_1 = 0.5 * (revolver_0 + r_1)
    cash_avg_1 = 0.5 * (cash_0 + cash_1)
    net_int_1 = term_int_1 + r_avg_1 * revolver_rate - cash_avg_1 * cash_rate

    ebt_1 = ebt_op_1 - net_int_1
    tax_1 = ebt_1 * tax_rate
    ni_1 = ebt_1 - tax_1
    div_1 = ni_1 * div_payout

    re_1 = re_0 + ni_1 - div_1
    equity_1 = common_stock + re_1
    assets_1 = cash_1 + ar_1 + inv_1 + net_ppe_1
    liab_1 = ap_1 + term_end_1 + r_1
    bs_imbalance = abs(assets_1 - (liab_1 + equity_1))

    cfo_1 = ni_1 + depr_1 - delta_ar - delta_inv + delta_ap
    cfi_1 = -capex_1
    cff_1 = delta_r - term_amort - div_1
    net_flow_1 = cfo_1 + cfi_1 + cff_1
    cash_tie_gap = abs(cash_1 - (cash_0 + net_flow_1))

    # DCF
    nopat_1 = ebt_op_1 * (1.0 - tax_rate)
    fcff_1 = nopat_1 + depr_1 - capex_1 - delta_nwc
    tv_1 = (fcff_1 * (1.0 + terminal_g)) / (wacc - terminal_g)
    pv_tv = tv_1 / (1.0 + wacc)
    pv_fcff = fcff_1 / (1.0 + wacc)
    ev = pv_fcff + pv_tv
    net_debt_0 = (term_debt_0 + revolver_0) - cash_0
    eq_val = ev - net_debt_0
    eq_per_share = eq_val / shares

    return {
        "bs_balanced": bs_imbalance < 1e-4,
        "cash_tied_out": cash_tie_gap < 1e-4,
        "bs_gap": bs_imbalance,
        "cash_gap": cash_tie_gap,
        "revolver_p1": r_1,
        "net_income_p1": ni_1,
        "fcff_p1": fcff_1,
        "equity_per_share": eq_per_share,
    }


def main() -> None:
    res = run_benchmark_audit()
    print("Balance Sheet Balanced:", str(res["bs_balanced"]))
    print("Cash Tied Out:", str(res["cash_tied_out"]))
    print("Balance Sheet Gap:", f"{res['bs_gap']:.6f}")
    print("Cash Flow Gap:", f"{res['cash_gap']:.6f}")
    print("Period 1 Revolver:", f"{res['revolver_p1']:.4f}")
    print("Period 1 Net Income:", f"{res['net_income_p1']:.4f}")
    print("Period 1 FCFF:", f"{res['fcff_p1']:.4f}")
    print("Equity Value Per Share:", f"{res['equity_per_share']:.4f}")


main()
