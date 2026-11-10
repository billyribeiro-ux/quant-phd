"""Lab 1 for PM1 L01: Private Equity Fund Structure and Management Fee Dynamics.

SIMULATED: a 10-year private equity fund with a $100M commitment.
Paces capital calls over a 5-year investment period and compares management fee drag
under two common contractual bases:
(A) Fixed 2.0% on Committed Capital throughout years 1-10.
(B) 2.0% on Committed Capital in years 1-5, stepping down to 1.5% on Invested Capital in years 6-10.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    commitment = 100.0  # $100M commitment

    # Capital call schedule (cumulative calls reach $95M; $5M uncalled)
    annual_calls = np.array([20.0, 30.0, 25.0, 15.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    cumulative_called = np.cumsum(annual_calls)

    # Realizations / exits reducing invested capital in harvesting period (years 6-10)
    annual_exits_cost = np.array([0.0, 0.0, 0.0, 0.0, 10.0, 20.0, 25.0, 20.0, 15.0, 5.0])
    cumulative_exited = np.cumsum(annual_exits_cost)
    invested_capital = cumulative_called - cumulative_exited

    # Structure A: Flat 2.0% on Committed Capital for all 10 years
    fees_a = np.full(10, commitment * 0.02)
    total_fees_a = float(np.sum(fees_a))

    # Structure B: 2.0% on Committed Capital (years 1-5), 1.5% on Invested Capital (years 6-10)
    fees_b = np.zeros(10)
    for y in range(10):
        if y < 5:
            fees_b[y] = commitment * 0.02
        else:
            fees_b[y] = invested_capital[y] * 0.015
    total_fees_b = float(np.sum(fees_b))

    fee_savings = total_fees_a - total_fees_b
    fee_drag_a_pct = (total_fees_a / commitment) * 100
    fee_drag_b_pct = (total_fees_b / commitment) * 100

    print(f"Structure A Cumulative Fees: ${total_fees_a:.2f}M ({fee_drag_a_pct:.1f}% of commitment)")
    print(f"Structure B Cumulative Fees: ${total_fees_b:.2f}M ({fee_drag_b_pct:.1f}% of commitment)")
    print(f"LP Fee Savings under Step-Down: ${fee_savings:.2f}M")
    print(f"Year 10 Fee Comparison: Flat=${fees_a[-1]:.2f}M vs Step-Down=${fees_b[-1]:.2f}M")


main()
