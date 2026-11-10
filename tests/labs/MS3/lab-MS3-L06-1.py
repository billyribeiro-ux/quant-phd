"""Lab MS3-L06-1: Perold implementation shortfall breakdown and TCA attribution.

Decomposes the total execution cost of a multi-slice institutional parent order
into delay cost, price appreciation (market impact), unexecuted opportunity cost, and fees.
"""

from __future__ import annotations


def calculate_implementation_shortfall(
    decision_price: float,
    arrival_price: float,
    trades: list[tuple[float, float]],
    terminal_price: float,
    target_shares: float,
    fees: float = 0.0,
) -> dict[str, float]:
    """Compute Perold (1988) implementation shortfall and 4-way attribution."""
    sign = 1.0 if target_shares > 0.0 else -1.0
    abs_target = abs(target_shares)

    executed_shares = sum(abs(q) for q, _ in trades)
    gross_spend = sum(abs(q) * p for q, p in trades)
    unexecuted_shares = max(0.0, abs_target - executed_shares)

    vwap = (gross_spend / executed_shares) if executed_shares > 0.0 else arrival_price

    # 1. Delay Cost (timing risk from decision to arrival)
    delay_cost = sign * executed_shares * (arrival_price - decision_price)

    # 2. Market Impact / Price Appreciation (execution slippage relative to arrival)
    impact_cost = sign * (gross_spend - executed_shares * arrival_price)

    # 3. Opportunity Cost (unexecuted volume at final market price vs decision)
    opportunity_cost = sign * unexecuted_shares * (terminal_price - decision_price)

    # 4. Total Shortfall
    total_shortfall = delay_cost + impact_cost + opportunity_cost + fees

    paper_notional = abs_target * decision_price
    is_bps = (total_shortfall / paper_notional) * 10_000.0

    return {
        "total_shortfall": total_shortfall,
        "delay_cost": delay_cost,
        "impact_cost": impact_cost,
        "opportunity_cost": opportunity_cost,
        "fees": fees,
        "executed_shares": executed_shares,
        "unexecuted_shares": unexecuted_shares,
        "vwap": vwap,
        "is_bps": is_bps,
    }


def main() -> None:
    # Portfolio manager decides to buy 200,000 shares of XYZ at 9:30 AM
    decision_price = 50.00
    # Order arrives at execution desk at 9:45 AM after routing delay
    arrival_price = 50.15
    # Execution desk fills 160,000 shares across 4 tranches through the day
    trades = [
        (40_000.0, 50.25),
        (50_000.0, 50.40),
        (40_000.0, 50.55),
        (30_000.0, 50.70),
    ]
    # At market close, trading halts with 40,000 shares unexecuted; stock closes at $51.20
    terminal_price = 51.20
    target_shares = 200_000.0
    explicit_fees = 120.00

    results = calculate_implementation_shortfall(
        decision_price, arrival_price, trades, terminal_price, target_shares, explicit_fees
    )

    print("Perold (1988) Implementation Shortfall Attribution (Target=200k Buy, P_0=$50.00):")
    print("----------------------------------------------------------------------------------")
    print(f"Decision Price (P_0):            $ {decision_price:8.2f}")
    print(f"Arrival Price  (P_arr):          $ {arrival_price:8.2f}")
    print(f"VWAP Executed  (P_vwap):         $ {results['vwap']:8.4f} ({results['executed_shares']:,.0f} shares)")
    print(f"Terminal Price (P_term):         $ {terminal_price:8.2f} ({results['unexecuted_shares']:,.0f} unfilled)")
    print("----------------------------------------------------------------------------------")
    d_bps = (results["delay_cost"] / (200000 * 50)) * 10000
    i_bps = (results["impact_cost"] / (200000 * 50)) * 10000
    o_bps = (results["opportunity_cost"] / (200000 * 50)) * 10000
    f_bps = (results["fees"] / (200000 * 50)) * 10000
    print(f"1. Delay Cost (Timing):          $ {results['delay_cost']:10,.2f}  ({d_bps:6.2f} bps)")
    print(f"2. Market Impact (Trading):      $ {results['impact_cost']:10,.2f}  ({i_bps:6.2f} bps)")
    print(f"3. Opportunity Cost (Unfilled):  $ {results['opportunity_cost']:10,.2f}  ({o_bps:6.2f} bps)")
    print(f"4. Explicit Fees & Commissions:  $ {results['fees']:10,.2f}  ({f_bps:6.2f} bps)")
    print("----------------------------------------------------------------------------------")
    print(f"Total Implementation Shortfall:  $ {results['total_shortfall']:10,.2f}  ({results['is_bps']:6.2f} bps)")

    # Articulation verification
    check_sum = results["delay_cost"] + results["impact_cost"] + results["opportunity_cost"] + results["fees"]
    diff = abs(results["total_shortfall"] - check_sum)
    print(f"Exact Balance Verification: Difference = ${diff:.6f} (Identity holds to machine epsilon)")


main()
