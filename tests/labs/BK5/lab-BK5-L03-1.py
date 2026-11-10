"""Lab L03-1: Cumulative fee and advisory drag over a 40-year accumulation plan.

Calculates terminal wealth and fee erosion under four fee levels (5 bps, 30 bps, 100 bps, 175 bps)
with annual contributions of $10,000 and 7.0% gross return (Sharpe 1991 arithmetic).
Standard library only. All inputs are SIMULATED.
"""


def accumulate(annual_deposit: float, gross_return: float, fee_bps: int, years: int) -> tuple[float, float]:
    """Simulate 40-year accumulation with beginning-of-year deposits.

    Returns (terminal_wealth, total_fees_paid).
    """
    fee_rate = fee_bps / 10_000.0
    net_return = gross_return - fee_rate
    balance = 0.0
    total_fees = 0.0

    for _ in range(years):
        balance += annual_deposit
        # Fee deducted annually on invested assets
        balance * (1.0 + gross_return) * (fee_rate / (1.0 + gross_return))
        # Equivalent to net growth:
        growth = balance * gross_return
        actual_fee = (balance + growth) * fee_rate
        total_fees += actual_fee
        balance = balance * (1.0 + net_return)

    return balance, total_fees


def main() -> None:
    annual_deposit = 10_000.0
    gross_return = 0.07  # 7.0% annual market return
    years = 40

    # Gross benchmark (0 bps)
    gross_wealth, _ = accumulate(annual_deposit, gross_return, 0, years)

    fee_tiers = [
        ("Passive index", 5),
        ("Robo-advisor", 30),
        ("Traditional AUM", 100),
        ("Active fund + advisor", 175),
    ]

    print(f"Gross 0 bps benchmark: ${round(gross_wealth):,}")

    for label, bps in fee_tiers:
        net_wealth, _ = accumulate(annual_deposit, gross_return, bps, years)
        wealth_lost = gross_wealth - net_wealth
        fraction_lost = wealth_lost / gross_wealth
        print(
            f"{label:22s} ({bps:3d} bps) | "
            f"Terminal: ${round(net_wealth):10,d} | "
            f"Lost to fees: ${round(wealth_lost):9,d} | "
            f"Erosion: {fraction_lost * 100:4.1f}%"
        )


main()
