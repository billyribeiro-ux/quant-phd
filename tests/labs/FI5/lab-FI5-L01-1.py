"""Lab FI5-L01-1: TIPS cash flow construction, indexation mechanics, and deflation floor.

Standard library only. Computes Treasury Inflation-Protected Securities (TIPS)
reference CPI interpolation, index ratio, inflation-adjusted coupon and principal
schedules under both inflation and deflation scenarios, and real duration metrics.
"""

from __future__ import annotations

from typing import Any


def interpolate_reference_cpi(
    cpi_m_minus_3: float,
    cpi_m_minus_2: float,
    day_of_month: int,
    days_in_month: int,
) -> float:
    """Compute interpolated reference CPI according to US Treasury TIPS indexation rules.

    The 2.5-month indexation lag interpolates between CPI from 3 months prior
    and CPI from 2 months prior:
    Ref_CPI(d) = CPI_{m-3} + [(d - 1) / D] * (CPI_{m-2} - CPI_{m-3})
    """
    if day_of_month < 1 or day_of_month > days_in_month:
        raise ValueError("day_of_month must be within [1, days_in_month]")
    if cpi_m_minus_3 <= 0 or cpi_m_minus_2 <= 0:
        raise ValueError("CPI values must be positive")
    alpha = (day_of_month - 1) / days_in_month
    return cpi_m_minus_3 + alpha * (cpi_m_minus_2 - cpi_m_minus_3)


def compute_tips_cash_flows(
    par_value: float,
    real_coupon_rate: float,
    maturity_years: float,
    index_ratios: list[float],
) -> list[dict[str, Any]]:
    """Generate semiannual TIPS coupon and principal cash flow schedule.

    Parameters:
        par_value: Base principal (e.g. 1000.00 USD).
        real_coupon_rate: Annual real coupon rate (decimal, e.g. 0.02 for 2.0%).
        maturity_years: Time to maturity in years (e.g. 5.0).
        index_ratios: List of index ratios (I_t) for each semiannual period.

    Returns:
        List of cash flow dictionaries containing period, time, index ratio,
        unadjusted coupon, adjusted coupon, principal, and total cash flow.
    """
    num_periods = round(maturity_years * 2)
    if len(index_ratios) != num_periods:
        raise ValueError(f"Expected {num_periods} index ratios, got {len(index_ratios)}")

    semi_coupon_rate = real_coupon_rate / 2.0
    schedule = []

    for t_idx, index_ratio in enumerate(index_ratios, start=1):
        time_years = t_idx * 0.5
        unadjusted_coupon = par_value * semi_coupon_rate
        adjusted_coupon = unadjusted_coupon * index_ratio
        principal_redemption = 0.0

        if t_idx == num_periods:
            # Deflation floor guarantees at least par redemption: max(1.0, index_ratio) * par
            redemption_ratio = max(1.0, index_ratio)
            principal_redemption = par_value * redemption_ratio

        total_cf = adjusted_coupon + principal_redemption
        schedule.append(
            {
                "period": t_idx,
                "time_years": time_years,
                "index_ratio": index_ratio,
                "adjusted_coupon": adjusted_coupon,
                "principal_redemption": principal_redemption,
                "total_cash_flow": total_cf,
            }
        )

    return schedule


def compute_real_duration(
    schedule: list[dict[str, Any]],
    real_yield_annual: float,
) -> tuple[float, float, float]:
    """Compute TIPS present value, Macaulay real duration, and modified real duration.

    Discounting uses semiannual compounding: DF_t = (1 + y/2)^(-2t).
    """
    semi_yield = real_yield_annual / 2.0
    pv_total = 0.0
    weighted_time = 0.0

    for item in schedule:
        t = item["time_years"]
        cf = item["total_cash_flow"]
        df = (1.0 + semi_yield) ** (-2.0 * t)
        pv = cf * df
        pv_total += pv
        weighted_time += t * pv

    mac_duration = weighted_time / pv_total if pv_total > 0 else 0.0
    mod_duration = mac_duration / (1.0 + semi_yield)
    return pv_total, mac_duration, mod_duration


def main() -> None:
    # 1. Reference CPI Interpolation Example (SIMULATED)
    # Settlement date: July 15 (month 7, day 15, 31 days in July)
    # m - 3 = April (CPI = 300.00), m - 2 = May (CPI = 301.55)
    cpi_apr = 300.00
    cpi_may = 301.55
    ref_cpi = interpolate_reference_cpi(cpi_apr, cpi_may, day_of_month=15, days_in_month=31)
    base_cpi = 270.00
    index_ratio = ref_cpi / base_cpi

    print("TIPS Reference CPI & Index Ratio (SIMULATED):")
    print(f"  CPI (m-3, Apr):     {cpi_apr:.2f}")
    print(f"  CPI (m-2, May):     {cpi_may:.2f}")
    print(f"  Interpolated CPI:   {ref_cpi:.3f} (day 15 of 31)")
    print(f"  Base CPI:           {base_cpi:.2f}")
    print(f"  Index Ratio (I_t):  {index_ratio:.5f}")

    # 2. 5-Year TIPS Cash Flow Schedule under Moderate Inflation (15% cumulative)
    par = 1000.00
    real_coupon = 0.02  # 2.00% annual real coupon
    years = 5.0
    num_periods = 10

    # Linearly rising index ratio from 1.015 to 1.150
    inflation_ratios = [1.0 + 0.015 * p for p in range(1, num_periods + 1)]
    schedule_inf = compute_tips_cash_flows(par, real_coupon, years, inflation_ratios)

    print("\n5-Year TIPS Schedule under Moderate Inflation (Cumulative +15.0%):")
    print("  Period  Time (Yr)  Index Ratio  Adj Coupon   Principal    Total CF")
    for row in schedule_inf:
        print(
            f"    {row['period']:2d}      {row['time_years']:4.1f}      "
            f"{row['index_ratio']:7.4f}   "
            f"${row['adjusted_coupon']:6.2f}   "
            f"${row['principal_redemption']:8.2f}   "
            f"${row['total_cash_flow']:8.2f}"
        )

    # 3. 5-Year TIPS Schedule under Severe Deflation (-10% cumulative)
    deflation_ratios = [1.0 - 0.010 * p for p in range(1, num_periods + 1)]
    schedule_def = compute_tips_cash_flows(par, real_coupon, years, deflation_ratios)

    print("\n5-Year TIPS Schedule under Severe Deflation (Cumulative -10.0%, Floor Active):")
    print("  Period  Time (Yr)  Index Ratio  Adj Coupon   Principal    Total CF")
    for row in schedule_def:
        print(
            f"    {row['period']:2d}      {row['time_years']:4.1f}      "
            f"{row['index_ratio']:7.4f}   "
            f"${row['adjusted_coupon']:6.2f}   "
            f"${row['principal_redemption']:8.2f}   "
            f"${row['total_cash_flow']:8.2f}"
        )

    # 4. Duration Metrics at 1.50% Real Yield
    real_yield = 0.015
    pv_inf, mac_dur_inf, mod_dur_inf = compute_real_duration(schedule_inf, real_yield)
    pv_def, mac_dur_def, mod_dur_def = compute_real_duration(schedule_def, real_yield)

    print("\nDuration Analytics (Real Yield = 1.50%):")
    print(
        f"  Inflation Scenario: PV = ${pv_inf:,.2f} | Mac Dur = {mac_dur_inf:.2f} yr | Mod Dur = {mod_dur_inf:.2f} yr"
    )
    print(
        f"  Deflation Scenario: PV = ${pv_def:,.2f} | Mac Dur = {mac_dur_def:.2f} yr | Mod Dur = {mod_dur_def:.2f} yr"
    )


main()
