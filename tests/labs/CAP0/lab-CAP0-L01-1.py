"""Lab L01-1: Three-statement model reconstruction and dynamic articulation."""

from __future__ import annotations


def main() -> None:
    # 3-year historical trial balance and 3-year projection
    years = [2024, 2025, 2026]
    rev_base = 1200.0
    growth = [0.08, 0.06, 0.05]
    gross_margin = 0.45
    ebitda_margin = 0.22
    tax_rate = 0.25
    interest_rate = 0.055
    capex_pct = 0.05
    depr_rate = 0.15
    dso = 45.0
    dio = 50.0
    dpo = 40.0
    payout = 0.30

    # Initial Balance Sheet (2023)
    cash = 120.0
    ar = rev_base * (dso / 365.0)
    inv = rev_base * (1.0 - gross_margin) * (dio / 365.0)
    nppe = 480.0
    ap = rev_base * (1.0 - gross_margin) * (dpo / 365.0)
    debt = 320.0
    equity = (cash + ar + inv + nppe) - (ap + debt)

    rev = rev_base
    print("Year | Revenue | EBITDA | Net Inc | Ending Cash | Articulation Gap")
    print("-" * 65)

    for i, yr in enumerate(years):
        rev = rev * (1.0 + growth[i])
        cogs = rev * (1.0 - gross_margin)
        ebitda = rev * ebitda_margin
        depr = nppe * depr_rate
        ebit = ebitda - depr
        interest = debt * interest_rate
        ebt = ebit - interest
        tax = max(0.0, ebt * tax_rate)
        ni = ebt - tax
        div = ni * payout

        # Working Capital
        ar_next = rev * (dso / 365.0)
        inv_next = cogs * (dio / 365.0)
        ap_next = cogs * (dpo / 365.0)
        delta_nwc = (ar_next - ar) + (inv_next - inv) - (ap_next - ap)

        capex = rev * capex_pct
        nppe = nppe + capex - depr
        equity = equity + (ni - div)

        cfo = ni + depr - delta_nwc
        cfi = -capex
        cff = -div
        delta_cash = cfo + cfi + cff
        cash = cash + delta_cash

        ar = ar_next
        inv = inv_next
        ap = ap_next

        tot_assets = cash + ar + inv + nppe
        tot_liab_eq = ap + debt + equity
        gap = tot_assets - tot_liab_eq

        print(f"{yr} | {rev:7.1f} | {ebitda:6.1f} | {ni:7.1f} | {cash:11.2f} | {gap:16.10f}")


main()
