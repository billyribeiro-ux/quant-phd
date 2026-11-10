"""Lab MS3-project-1: Rung 1 worked example for Atlas A10 execution models.

Simulates institutional execution under square-root impact, schedules an
Almgren-Chriss liquidation trajectory, and evaluates implementation shortfall.
"""

from __future__ import annotations

import math


def run_worked_example() -> None:
    # 1. Market and Order Setup
    total_shares = 250_000.0  # Liquidation target
    decision_price = 100.00
    arrival_price = 99.85  # Adverse drift before start
    daily_volume = 5_000_000.0
    daily_volatility = 0.02
    horizon = 1.0  # 1 trading day
    n_steps = 10
    tau = horizon / n_steps
    gamma = 1.2e-7  # Permanent impact parameter
    eta = 6.0e-7  # Temporary impact parameter
    risk_aversion = 2.5e-6

    print("Step 1 | Estimating Benchmark Market Impact:")
    sq_impact = 0.5 * daily_volatility * math.sqrt(total_shares / daily_volume)
    sq_impact_dollar = decision_price * sq_impact
    print(f"  Square-Root Expected Impact: {sq_impact * 10000:.2f} bps (${sq_impact_dollar:.4f} per share)")

    print("\nStep 2 | Solving Almgren-Chriss Optimal Holdings Trajectory:")
    arg = 1.0 + 0.5 * (risk_aversion * (daily_volatility**2) * (tau**2)) / eta
    kappa = math.acosh(arg) / tau
    sinh_kt = math.sinh(kappa * horizon)

    times = [k * tau for k in range(n_steps + 1)]
    trajectory = [total_shares * math.sinh(kappa * (horizon - t)) / sinh_kt for t in times]
    trajectory[-1] = 0.0

    print("  Interval k | Time (d) | Holdings x_k | Trade Slice n_k ($)")
    for k in range(n_steps + 1):
        n_k = (trajectory[k - 1] - trajectory[k]) if k > 0 else 0.0
        print(f"  {k:10d} | {times[k]:8.2f} | {trajectory[k]:12,.0f} | {n_k:15,.0f}")

    print("\nStep 3 | Simulating Order Slices and Evaluating Implementation Shortfall:")
    trades: list[tuple[float, float]] = []
    curr_price = arrival_price
    for k in range(1, n_steps + 1):
        n_k = trajectory[k - 1] - trajectory[k]
        # Permanent drift plus temporary execution concession
        v_k = n_k / tau
        temp_concession = eta * (v_k / daily_volume) * decision_price * 10.0
        perm_drift = gamma * n_k
        exec_price = curr_price - temp_concession
        trades.append((n_k, exec_price))
        curr_price -= perm_drift

    terminal_price = curr_price
    fees = 75.00

    # Calculate Perold Shortfall
    sign = -1.0  # Selling
    executed_shares = sum(q for q, _ in trades)
    gross_proceeds = sum(q * p for q, p in trades)
    unexecuted_shares = total_shares - executed_shares
    vwap = gross_proceeds / executed_shares

    delay_cost = sign * executed_shares * (arrival_price - decision_price)
    impact_cost = sign * (gross_proceeds - executed_shares * arrival_price)
    opportunity_cost = sign * unexecuted_shares * (terminal_price - decision_price)
    total_shortfall = delay_cost + impact_cost + opportunity_cost + fees
    is_bps = (total_shortfall / (total_shares * decision_price)) * 10_000.0

    print(f"  Total Shares Executed:         {executed_shares:,.0f} of {total_shares:,.0f}")
    print(f"  VWAP Realized:                 $ {vwap:.4f} (Decision: ${decision_price:.2f})")
    d_bps = (delay_cost / (total_shares * decision_price)) * 10000
    i_bps = (impact_cost / (total_shares * decision_price)) * 10000
    o_bps = (opportunity_cost / (total_shares * decision_price)) * 10000
    f_bps = (fees / (total_shares * decision_price)) * 10000
    print(f"  1. Delay Cost:                 $ {delay_cost:10,.2f} ({d_bps:6.2f} bps)")
    print(f"  2. Impact Cost (Trading):      $ {impact_cost:10,.2f} ({i_bps:6.2f} bps)")
    print(f"  3. Opportunity Cost (Unfilled):$ {opportunity_cost:10,.2f} ({o_bps:6.2f} bps)")
    print(f"  4. Explicit Fees:              $ {fees:10,.2f} ({f_bps:6.2f} bps)")
    print(f"  Total Implementation Shortfall:$ {total_shortfall:10,.2f} ({is_bps:6.2f} bps)")


def main() -> None:
    run_worked_example()


main()
