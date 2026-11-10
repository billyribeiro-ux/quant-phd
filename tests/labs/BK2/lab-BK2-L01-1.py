"""Lab BK2-L01-1: Open-end mutual fund cash drag and redemption buffer simulation.

Demonstrates the liquidity transformation trade-off: holding a cash buffer
prevents fire-sale liquidation under stochastic daily redemption shocks,
but imposes systematic cash drag on annual fund returns.
"""

from __future__ import annotations

import random


def simulate_cash_drag(
    gross_equity_return: float,
    cash_rate: float,
    cash_weight: float,
    years: int,
    initial_wealth: float,
) -> dict[str, float]:
    """Calculate annual cash drag and terminal wealth difference."""
    fund_return = (1.0 - cash_weight) * gross_equity_return + cash_weight * cash_rate
    annual_cash_drag_bps = (gross_equity_return - fund_return) * 10_000.0

    terminal_equity_only = initial_wealth * ((1.0 + gross_equity_return) ** years)
    terminal_with_cash = initial_wealth * ((1.0 + fund_return) ** years)
    wealth_lost_pct = (terminal_equity_only - terminal_with_cash) / terminal_equity_only * 100.0

    return {
        "cash_weight_pct": cash_weight * 100.0,
        "fund_return_pct": fund_return * 100.0,
        "cash_drag_bps": annual_cash_drag_bps,
        "terminal_equity": terminal_equity_only,
        "terminal_with_cash": terminal_with_cash,
        "wealth_lost_pct": wealth_lost_pct,
    }


def main() -> None:
    rng = random.Random(42)

    # Simulate 250 daily redemption shocks (as percentage of AUM)
    daily_redemptions = [max(0.0, rng.gauss(0.005, 0.010)) for _ in range(250)]
    max_daily_redemption = max(daily_redemptions) * 100.0
    p99_redemption = sorted(daily_redemptions)[int(250 * 0.99)] * 100.0

    gross_equity_ret = 0.08  # 8.0% annual equity return
    cash_ret = 0.02  # 2.0% risk-free cash return
    cash_weight = 0.05  # 5.0% prudent cash buffer
    horizon_years = 20
    starting_nav = 10_000.0

    res = simulate_cash_drag(gross_equity_ret, cash_ret, cash_weight, horizon_years, starting_nav)

    print("Mutual Fund Cash Buffer & Cash Drag Analysis")
    print("--------------------------------------------")
    print("Daily redemption sample size: 250 trading days")
    print(f"99th percentile daily outflow: {p99_redemption:.2f}%")
    print(f"Maximum single-day outflow:   {max_daily_redemption:.2f}%")
    print(f"Cash buffer maintained:       {res['cash_weight_pct']:.2f}%")
    print(f"Fund blended annual return:   {res['fund_return_pct']:.2f}%")
    print(f"Annual cash drag:             {res['cash_drag_bps']:.1f} bps")
    print(f"20-year wealth (100% stock):  ${res['terminal_equity']:,.2f}")
    print(f"20-year wealth (5% cash):     ${res['terminal_with_cash']:,.2f}")
    print(f"Cumulative wealth drag:       {res['wealth_lost_pct']:.2f}%")


main()
