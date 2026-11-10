"""Lab CF7-L02-1: The Integrated Three-Statement Model.

Verifies fundamental articulation across the Income Statement, Balance Sheet,
and Cash Flow Statement, ensuring the balance sheet balances and cash ties out.
"""

from __future__ import annotations


def run_three_statement_model() -> dict[str, list[float]]:
    """Build a 3-period articulated three-statement model."""
    # Historical base (Period 0)
    rev_0 = 500.0
    cash_0 = 40.0
    ar_0 = 60.0
    inv_0 = 40.0
    ppe_0 = 200.0
    ap_0 = 35.0
    debt_0 = 100.0
    common_stock = 150.0
    re_0 = (cash_0 + ar_0 + inv_0 + ppe_0) - (ap_0 + debt_0) - common_stock  # 155.0

    growth = [0.08, 0.06, 0.05]
    cogs_rate = 0.55
    sga_rate = 0.20
    depr_rate = 0.10
    capex_rate = 0.06
    dso = 45.0
    dio = 50.0
    dpo = 40.0
    tax_rate = 0.25
    interest_rate = 0.05

    bs_gaps: list[float] = []
    ending_cashes: list[float] = []
    net_incomes: list[float] = []
    cfos: list[float] = []

    prev_rev = rev_0
    prev_cash = cash_0
    prev_ar = ar_0
    prev_inv = inv_0
    prev_ppe = ppe_0
    prev_ap = ap_0
    prev_debt = debt_0
    prev_re = re_0

    for t in range(3):
        # 1. Income Statement
        rev = prev_rev * (1.0 + growth[t])
        cogs = rev * cogs_rate
        sga = rev * sga_rate
        ebitda = rev - cogs - sga
        depr = prev_ppe * depr_rate
        ebit = ebitda - depr
        interest = prev_debt * interest_rate
        ebt = ebit - interest
        tax = ebt * tax_rate
        ni = ebt - tax

        # 2. Operating Working Capital & PP&E
        ar = rev * (dso / 365.0)
        inv = cogs * (dio / 365.0)
        purchases = cogs + (inv - prev_inv)
        ap = purchases * (dpo / 365.0)
        capex = rev * capex_rate
        ppe = prev_ppe + capex - depr

        delta_ar = ar - prev_ar
        delta_inv = inv - prev_inv
        delta_ap = ap - prev_ap

        # 3. Cash Flow Statement
        cfo = ni + depr - delta_ar - delta_inv + delta_ap
        cfi = -capex
        cff = 0.0  # Constant debt, zero dividends for simplicity
        net_cash = cfo + cfi + cff
        cash = prev_cash + net_cash

        # 4. Balance Sheet & Retained Earnings
        re = prev_re + ni
        assets = cash + ar + inv + ppe
        liabilities = ap + prev_debt
        equity = common_stock + re
        gap = assets - (liabilities + equity)

        bs_gaps.append(gap)
        ending_cashes.append(cash)
        net_incomes.append(ni)
        cfos.append(cfo)

        # Advance state
        prev_rev = rev
        prev_cash = cash
        prev_ar = ar
        prev_inv = inv
        prev_ppe = ppe
        prev_ap = ap
        prev_re = re

    return {
        "bs_gap": bs_gaps,
        "ending_cash": ending_cashes,
        "net_income": net_incomes,
        "cfo": cfos,
    }


def main() -> None:
    res = run_three_statement_model()
    print("Period 1 Net Income:", f"{res['net_income'][0]:.4f}")
    print("Period 3 Net Income:", f"{res['net_income'][2]:.4f}")
    print("Period 1 CFO:", f"{res['cfo'][0]:.4f}")
    print("Period 3 CFO:", f"{res['cfo'][2]:.4f}")
    print("Period 1 Ending Cash:", f"{res['ending_cash'][0]:.4f}")
    print("Period 3 Ending Cash:", f"{res['ending_cash'][2]:.4f}")
    print("Period 1 Balance Sheet Gap:", f"{abs(res['bs_gap'][0]):.6f}")
    print("Period 3 Balance Sheet Gap:", f"{abs(res['bs_gap'][2]):.6f}")


main()
