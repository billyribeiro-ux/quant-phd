"""Lab PM4-L02-1: Agency MBS Pass-Through Waterfall and Settlement Delay Mechanics.

SIMULATED: Models monthly cash flow distribution of a Fannie Mae 30-year fixed-rate pass-through pool
under 150% PSA prepayment, isolating scheduled principal, unscheduled prepayments, servicing fees,
guarantee fees, pool factor decay, and the present-value impact of delay days.
"""

from __future__ import annotations

import numpy as np


def generate_agency_waterfall(
    notional: float = 10_000_000.0,
    wac: float = 0.060,
    servicing_fee: float = 0.0044,
    g_fee: float = 0.0006,
    wam_months: int = 360,
    psa_speed: float = 150.0,
) -> dict[str, list[float]]:
    """Simulate agency pass-through monthly waterfall under PSA prepayment.

    Parameters
    ----------
    notional : float
        Initial pool collateral balance ($).
    wac : float
        Weighted average collateral coupon.
    servicing_fee : float
        Servicer fee rate.
    g_fee : float
        GSE guarantee fee rate.
    wam_months : int
        Remaining loan term in months.
    psa_speed : float
        PSA benchmark prepayment percentage.

    Returns
    -------
    dict[str, list[float]]
        Time series of pool balances, payments, fees, and pool factors.
    """
    pass_through_coupon = wac - servicing_fee - g_fee
    wac_m = wac / 12.0
    pt_m = pass_through_coupon / 12.0
    svc_m = servicing_fee / 12.0
    gfe_m = g_fee / 12.0

    balances: list[float] = [notional]
    sched_prin: list[float] = []
    prepay_prin: list[float] = []
    investor_interest: list[float] = []
    servicing_cf: list[float] = []
    gfee_cf: list[float] = []
    investor_total_cf: list[float] = []
    pool_factors: list[float] = [1.0]

    current_balance = notional

    for m in range(1, wam_months + 1):
        if current_balance <= 1e-4:
            sched_prin.append(0.0)
            prepay_prin.append(0.0)
            investor_interest.append(0.0)
            servicing_cf.append(0.0)
            gfee_cf.append(0.0)
            investor_total_cf.append(0.0)
            balances.append(0.0)
            pool_factors.append(0.0)
            continue

        rem_term = wam_months - m + 1
        denom = 1.0 - (1.0 + wac_m) ** (-rem_term)
        pmt = current_balance * (wac_m / denom)
        gross_int = current_balance * wac_m
        sp = pmt - gross_int

        # PSA Prepayment
        base_cpr = 0.06 if m >= 30 else 0.002 * m
        cpr = base_cpr * (psa_speed / 100.0)
        smm = 1.0 - (1.0 - cpr) ** (1.0 / 12.0)
        pp = max(0.0, float((current_balance - sp) * smm))

        tot_prin = sp + pp
        net_int = current_balance * pt_m
        svc = current_balance * svc_m
        gfe = current_balance * gfe_m

        current_balance -= tot_prin
        current_balance = max(0.0, current_balance)

        sched_prin.append(sp)
        prepay_prin.append(pp)
        investor_interest.append(net_int)
        servicing_cf.append(svc)
        gfee_cf.append(gfe)
        investor_total_cf.append(net_int + tot_prin)
        balances.append(current_balance)
        pool_factors.append(current_balance / notional)

    return {
        "balances": balances,
        "sched_prin": sched_prin,
        "prepay_prin": prepay_prin,
        "investor_interest": investor_interest,
        "servicing_cf": servicing_cf,
        "gfee_cf": gfee_cf,
        "investor_total_cf": investor_total_cf,
        "pool_factors": pool_factors,
    }


def compute_pv_with_delay(cash_flows: list[float], annual_discount_rate: float, actual_delay_days: int) -> float:
    """Compute present value of monthly cash flows with settlement delay adjustment.

    Parameters
    ----------
    cash_flows : list[float]
        Monthly cash flows received by investor.
    annual_discount_rate : float
        Annualized continuous discount yield.
    actual_delay_days : int
        Actual payment delay days beyond month end (e.g. 24 days for Fannie Mae 55-day stated).

    Returns
    -------
    float
        Present value in dollars.
    """
    pv = 0.0
    for m, cf in enumerate(cash_flows, start=1):
        # Time to cash flow arrival in years: m/12 + actual_delay_days/365
        t_years = (m / 12.0) + (actual_delay_days / 365.0)
        pv += cf * float(np.exp(-annual_discount_rate * t_years))
    return float(pv)


def main() -> None:
    notional = 10_000_000.0
    wac = 0.060
    servicing = 0.0044
    g_fee = 0.0006
    wam = 360
    speed = 150.0

    res = generate_agency_waterfall(notional, wac, servicing, g_fee, wam, speed)

    print("Agency MBS Waterfall Simulation (150% PSA, 6.00% WAC, 5.50% Pass-Through):")
    print("Month | Beg Balance | Sched Prin | Prepayment | Net Interest | Total CF | Pool Factor")
    for m in [1, 12, 30, 60, 120, 240, 360]:
        idx = m - 1
        b_beg = res["balances"][idx]
        sp = res["sched_prin"][idx]
        pp = res["prepay_prin"][idx]
        ni = res["investor_interest"][idx]
        tot = res["investor_total_cf"][idx]
        pf = res["pool_factors"][idx + 1]
        print(f"{m:5d} | {b_beg:11.2f} | {sp:10.2f} | {pp:10.2f} | {ni:12.2f} | {tot:8.2f} | {pf:11.6f}")

    # Cash flow conservation test: total principal returned must equal initial notional
    total_sp = sum(res["sched_prin"])
    total_pp = sum(res["prepay_prin"])
    total_principal_paid = total_sp + total_pp
    print("\nCollateral Reconciliation:")
    print(f"Total Scheduled Principal:   {total_sp:12.2f}")
    print(f"Total Prepayment Principal:  {total_pp:12.2f}")
    print(f"Total Principal Returned:    {total_principal_paid:12.2f}")
    assert abs(total_principal_paid - notional) < 1.0

    # Delay days present value impact
    discount_rate = 0.055
    pv_no_delay = compute_pv_with_delay(res["investor_total_cf"], discount_rate, actual_delay_days=0)
    pv_fannie_delay = compute_pv_with_delay(res["investor_total_cf"], discount_rate, actual_delay_days=24)
    delay_cost = pv_no_delay - pv_fannie_delay
    delay_cost_bps = (delay_cost / notional) * 10000.0

    print("\nDelay-Day Economic Analysis (55-day stated / 24-day actual delay):")
    print(f"Present Value (0 delay days):  {pv_no_delay:12.2f}")
    print(f"Present Value (24 delay days): {pv_fannie_delay:12.2f}")
    print(f"Delay Drag ($):                {delay_cost:12.2f}")
    print(f"Delay Drag (bp of par):        {delay_cost_bps:12.2f}")
    assert delay_cost > 0.0


main()
