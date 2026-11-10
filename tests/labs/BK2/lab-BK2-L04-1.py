"""Lab BK2-L04-1: Fee drag compounding over 30 years.

The Curriculum Lab for Module BK2. Demonstrates the mathematical erosion of
terminal wealth caused by expense ratios and turnover drag compounded over
a 30-year retirement accumulation horizon.
"""

from __future__ import annotations


def compound_fee_drag(
    initial_wealth: float,
    gross_annual_return: float,
    years: int,
    fee_structures: list[tuple[str, float]],
) -> list[dict[str, float | str]]:
    """Compute 30-year terminal wealth and wealth loss across fee structures."""
    gross_terminal = initial_wealth * ((1.0 + gross_annual_return) ** years)
    results: list[dict[str, float | str]] = []

    for label, fee_rate in fee_structures:
        net_return = gross_annual_return - fee_rate
        net_terminal = initial_wealth * ((1.0 + net_return) ** years)
        wealth_lost = gross_terminal - net_terminal
        pct_lost = (wealth_lost / gross_terminal) * 100.0

        results.append(
            {
                "label": label,
                "fee_bps": fee_rate * 10_000.0,
                "net_return_pct": net_return * 100.0,
                "terminal_wealth": net_terminal,
                "wealth_lost": wealth_lost,
                "pct_lost": pct_lost,
            }
        )

    return results


def main() -> None:
    initial_capital = 100_000.0
    gross_return = 0.07  # 7.00% annual gross market return
    horizon_years = 30

    fee_tiers = [
        ("Gross Benchmark (0 bps)", 0.0000),
        ("Low-Cost Index ETF (5 bps)", 0.0005),
        ("Institutional Active (75 bps)", 0.0075),
        ("Retail Active Mutual Fund (150 bps)", 0.0150),
        ("Retail Active + Turnover Drag (200 bps)", 0.0200),
    ]

    results = compound_fee_drag(initial_capital, gross_return, horizon_years, fee_tiers)

    print("Curriculum Lab: Fee Drag Compounding Over 30 Years")
    print("=================================================")
    print(f"Initial Investment: ${initial_capital:,.2f}")
    print(f"Gross Annual Return: {gross_return * 100.0:.2f}% | Horizon: {horizon_years} Years")
    print("--------------------------------------------------------------------------------")
    print(f"{'Structure':<39} {'Fee(bps)':<9} {'Net Return':<11} {'Final Wealth':<14} {'Lost to Drag':<12}")
    print("--------------------------------------------------------------------------------")
    for r in results:
        label = str(r["label"])
        fee_bps = float(r["fee_bps"])
        net_ret = float(r["net_return_pct"])
        term = float(r["terminal_wealth"])
        pct_lost = float(r["pct_lost"])
        print(f"{label:<39} {fee_bps:>6.0f} bp  {net_ret:>6.2f}%     ${term:>11,.2f}  {pct_lost:>6.2f}%")
    print("--------------------------------------------------------------------------------")


main()
