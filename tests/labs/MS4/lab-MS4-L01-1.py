"""Lab MS4-L01-1: Exact 4-way Perold implementation shortfall attribution.

Demonstrates the decomposition of institutional execution drag into delay cost,
realized price impact, opportunity cost of unexecuted shares, and explicit fees.
SIMULATED: deterministic multi-slice execution scenario.
"""

from __future__ import annotations


def run_implementation_shortfall_attribution() -> None:
    # Order parameters (Buy order)
    decision_price = 50.00
    arrival_price = 50.25
    terminal_price = 51.50
    target_shares = 100000.0

    # Executed slices: (shares, fill_price)
    fills = [
        (30000.0, 50.40),
        (30000.0, 50.70),
        (20000.0, 51.00),
    ]
    commission_per_share = 0.005

    executed_shares = sum(q for q, _ in fills)
    unexecuted_shares = target_shares - executed_shares

    # 1. Delay Cost (arrival price vs decision price on executed shares)
    delay_cost = executed_shares * (arrival_price - decision_price)

    # 2. Execution Impact (actual fill prices vs arrival price)
    execution_impact = sum(q * (p - arrival_price) for q, p in fills)

    # 3. Opportunity Cost (terminal price vs decision price on unfilled shares)
    opportunity_cost = unexecuted_shares * (terminal_price - decision_price)

    # 4. Explicit Fees
    explicit_fees = executed_shares * commission_per_share

    # Total Implementation Shortfall
    total_shortfall = delay_cost + execution_impact + opportunity_cost + explicit_fees

    # Paper portfolio return vs Realized return
    paper_return = target_shares * (terminal_price - decision_price)
    realized_cost = sum(q * p for q, p in fills) + explicit_fees
    realized_terminal_value = executed_shares * terminal_price
    realized_profit = realized_terminal_value - realized_cost

    implied_shortfall = paper_return - realized_profit

    # Notional base for basis points: target_shares * decision_price
    notional = target_shares * decision_price
    delay_bps = (delay_cost / notional) * 10000.0
    impact_bps = (execution_impact / notional) * 10000.0
    opp_bps = (opportunity_cost / notional) * 10000.0
    fees_bps = (explicit_fees / notional) * 10000.0
    total_bps = (total_shortfall / notional) * 10000.0

    print(f"Target Shares:        {target_shares:.0f}")
    print(f"Executed Shares:      {executed_shares:.0f}")
    print(f"Unexecuted Shares:    {unexecuted_shares:.0f}")
    print(f"Decision Price:       {decision_price:.4f}")
    print(f"Arrival Price:        {arrival_price:.4f}")
    print(f"Terminal Price:       {terminal_price:.4f}")
    print(f"Delay Cost:           {delay_cost:.4f} ({delay_bps:.2f} bps)")
    print(f"Execution Impact:     {execution_impact:.4f} ({impact_bps:.2f} bps)")
    print(f"Opportunity Cost:     {opportunity_cost:.4f} ({opp_bps:.2f} bps)")
    print(f"Explicit Fees:        {explicit_fees:.4f} ({fees_bps:.2f} bps)")
    print(f"Total Shortfall:      {total_shortfall:.4f} ({total_bps:.2f} bps)")
    print(f"Paper Profit:         {paper_return:.4f}")
    print(f"Realized Profit:      {realized_profit:.4f}")
    print(f"Exact Articulation:   {abs(total_shortfall - implied_shortfall) < 1e-9}")


def main() -> None:
    run_implementation_shortfall_attribution()


main()
