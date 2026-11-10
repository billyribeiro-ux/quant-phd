"""CF5 Lab L04-1: Multi-Tranche Debt Schedule, Mandatory Amortization, and Cash Sweeps.

Simulates a 5-year debt waterfall with priority cash sweep and evaluates leverage
and interest coverage covenants.
"""

from __future__ import annotations

import numpy as np


def run_debt_waterfall(
    ebitda: np.ndarray,
    capex: np.ndarray,
    delta_nwc: np.ndarray,
    tax_rate: float,
    tla_initial: float,
    tla_rate: float,
    tla_amort_pct: float,
    tlb_initial: float,
    tlb_rate: float,
    tlb_amort_pct: float,
    min_cash: float,
    sweep_pct: float,
) -> dict[str, list[float]]:
    """Execute multi-year debt waterfall with priority cash sweeps and ending cash balances."""
    n = len(ebitda)
    tla_bal = tla_initial
    tlb_bal = tlb_initial
    cash_bal = min_cash

    ending_debt: list[float] = []
    ending_cash: list[float] = []
    cfads_list: list[float] = []
    total_interest: list[float] = []
    tla_sweeps: list[float] = []
    tlb_sweeps: list[float] = []

    for i in range(n):
        eb = float(ebitda[i])
        cx = float(capex[i])
        nwc = float(delta_nwc[i])

        # Interest on beginning balances
        int_tla = tla_bal * tla_rate
        int_tlb = tlb_bal * tlb_rate
        tot_int = int_tla + int_tlb
        total_interest.append(tot_int)

        # Operating taxes and CFADS
        ebit = eb - (cx * 0.7)  # approximate D&A
        ebt = ebit - tot_int
        tax = max(0.0, ebt * tax_rate)
        cfads = eb - cx - nwc - tot_int - tax
        cfads_list.append(cfads)

        # Mandatory amortization
        mand_tla = min(tla_bal, tla_initial * tla_amort_pct)
        mand_tlb = min(tlb_bal, tlb_initial * tlb_amort_pct)
        tot_mand = mand_tla + mand_tlb

        # Cash before sweep
        cash_avail = cash_bal + cfads - tot_mand
        excess = max(0.0, cash_avail - min_cash)
        sweep_pool = excess * sweep_pct

        # Apply sweep: TLA first, then TLB
        rem_tla = tla_bal - mand_tla
        sw_tla = min(rem_tla, sweep_pool)
        rem_pool = sweep_pool - sw_tla

        rem_tlb = tlb_bal - mand_tlb
        sw_tlb = min(rem_tlb, rem_pool)

        tla_sweeps.append(sw_tla)
        tlb_sweeps.append(sw_tlb)

        tla_bal = rem_tla - sw_tla
        tlb_bal = rem_tlb - sw_tlb
        cash_bal = cash_avail - (sw_tla + sw_tlb)

        ending_debt.append(tla_bal + tlb_bal)
        ending_cash.append(cash_bal)

    return {
        "ending_debt": ending_debt,
        "ending_cash": ending_cash,
        "cfads": cfads_list,
        "total_interest": total_interest,
        "tla_sweeps": tla_sweeps,
        "tlb_sweeps": tlb_sweeps,
    }


def main() -> None:
    print("CF5 Lab L04-1: Multi-Tranche Debt Schedule and Priority Cash Sweep")
    print("==================================================================")

    # 5-year operating projections ($M)
    ebitda = np.array([100.0, 112.0, 125.0, 138.0, 150.0])
    capex = np.array([20.0, 22.0, 24.0, 26.0, 28.0])
    dnwc = np.array([5.0, 6.0, 6.0, 7.0, 7.0])
    tax_rate = 0.25

    tla_0 = 300.0  # $300M at 7.5%
    tlb_0 = 200.0  # $200M at 10.0%
    min_cash = 25.0

    res = run_debt_waterfall(
        ebitda=ebitda,
        capex=capex,
        delta_nwc=dnwc,
        tax_rate=tax_rate,
        tla_initial=tla_0,
        tla_rate=0.075,
        tla_amort_pct=0.05,  # $15M/yr
        tlb_initial=tlb_0,
        tlb_rate=0.100,
        tlb_amort_pct=0.01,  # $2M/yr
        min_cash=min_cash,
        sweep_pct=1.0,  # 100% sweep
    )

    print("Year | EBITDA | Interest | CFADS  | TLA Sweep | TLB Sweep | End Debt | End Cash")
    print("-----+--------+----------+--------+-----------+-----------+----------+---------")
    for yr in range(5):
        print(
            f"{yr + 1:4d} | ${ebitda[yr]:5.1f}M | ${res['total_interest'][yr]:7.2f}M |"
            f" ${res['cfads'][yr]:5.2f}M | ${res['tla_sweeps'][yr]:8.2f}M |"
            f" ${res['tlb_sweeps'][yr]:8.2f}M | ${res['ending_debt'][yr]:7.2f}M |"
            f" ${res['ending_cash'][yr]:6.2f}M"
        )

    # Covenant audit
    max_leverage_covenants = [5.5, 5.0, 4.5, 4.0, 3.5]
    print("\nFinancial Covenant Audit:")
    for yr in range(5):
        lev = res["ending_debt"][yr] / ebitda[yr]
        cov = ebitda[yr] / res["total_interest"][yr]
        max_lev = max_leverage_covenants[yr]
        status = "COMPLIANT" if lev <= max_lev and cov >= 2.5 else "BREACH"
        print(
            f"  Year {yr + 1}: Leverage = {lev:.2f}x (Max {max_lev:.1f}x), Coverage = {cov:.2f}x (Min 2.5x) -> {status}"
        )


main()
