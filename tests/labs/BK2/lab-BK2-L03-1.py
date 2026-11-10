"""Lab BK2-L03-1: Hedge fund compensation contract with high-water mark and hurdle.

Simulates a 5-year track record under a '2 and 20' fee structure with an annual
hurdle rate and high-water mark (HWM), demonstrating asymmetric incentive fee
crystallization and path dependency.
"""

from __future__ import annotations


def simulate_hedge_fund_fees(
    returns: list[float],
    mgmt_fee_rate: float = 0.02,
    incentive_fee_rate: float = 0.20,
    hurdle_rate: float = 0.03,
    initial_nav: float = 100.0,
) -> list[dict[str, float]]:
    """Compute year-by-year NAV, high-water mark, management fees, and performance fees."""
    nav = initial_nav
    hwm = initial_nav
    history: list[dict[str, float]] = []

    for year, ret in enumerate(returns, start=1):
        # Gross portfolio value after investment return
        gross_value = nav * (1.0 + ret)

        # Management fee deducted at year-end on gross value
        mgmt_fee = gross_value * mgmt_fee_rate
        value_after_mgmt = gross_value - mgmt_fee

        # Hurdle benchmark: HWM compounded at hurdle rate
        hurdle_base = hwm * (1.0 + hurdle_rate)

        # Performance fee applies only to gains above the hurdle base
        if value_after_mgmt > hurdle_base:
            excess_profit = value_after_mgmt - hurdle_base
            perf_fee = excess_profit * incentive_fee_rate
        else:
            perf_fee = 0.0

        ending_nav = value_after_mgmt - perf_fee
        net_ret = (ending_nav - nav) / nav

        # High-water mark updates to ending NAV if it surpasses previous HWM
        hwm = max(hwm, ending_nav)

        history.append(
            {
                "year": float(year),
                "gross_return_pct": ret * 100.0,
                "net_return_pct": net_ret * 100.0,
                "mgmt_fee": mgmt_fee,
                "perf_fee": perf_fee,
                "ending_nav": ending_nav,
                "hwm": hwm,
            }
        )
        nav = ending_nav

    return history


def main() -> None:
    returns = [0.15, -0.10, 0.08, 0.25, -0.05]
    history = simulate_hedge_fund_fees(returns)

    print("Hedge Fund '2 & 20' Fee Structure with High-Water Mark")
    print("-----------------------------------------------------")
    print(f"{'Year':<5} {'Gross%':<8} {'Net%':<8} {'MgmtFee':<9} {'PerfFee':<9} {'EndNAV':<9} {'HWM':<8}")
    for row in history:
        print(
            f"{int(row['year']):<5} "
            f"{row['gross_return_pct']:>6.1f}% "
            f"{row['net_return_pct']:>6.1f}% "
            f"${row['mgmt_fee']:>7.2f} "
            f"${row['perf_fee']:>7.2f} "
            f"${row['ending_nav']:>7.2f} "
            f"${row['hwm']:>7.2f}"
        )


main()
