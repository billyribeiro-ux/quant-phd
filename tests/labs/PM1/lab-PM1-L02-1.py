"""Lab 1 for PM1 L02: Carried Interest Waterfall and Clawback Mechanics.

SIMULATED: a private equity fund evaluating European vs. American waterfalls across 3 deals.
Deal 1: $30M invested, exits in year 3 for $90M (+$60M profit).
Deal 2: $30M invested, exits in year 5 for $30M ($0 profit).
Deal 3: $40M invested, written down to $0 in year 7 (-$40M loss).
Total invested: $100M. Total gross exit proceeds: $120M (Net fund profit = +$20M).
Hurdle: 8% per annum compounded. Carry: 20% with 100% GP catch-up.
Demonstrates GP over-distribution and clawback liability under American waterfall.
"""

from __future__ import annotations


def main() -> None:
    # 1. European (Whole-Fund) Waterfall at Fund Liquidation (Year 7)
    # Total drawn capital = $100M, total proceeds = $120M
    # Net profit = $20M
    total_drawn = 100.0
    total_proceeds = 120.0
    hurdle_rate = 0.08

    # Preferred return on $100M drawn over average hold of ~5 years:
    # For simplicity of illustration, suppose accrued preferred return is $25.0M
    accrued_hurdle = 25.0

    # In European waterfall:
    # Tier 1: Return of Capital = min($120M, $100M) = $100M to LP
    # Remaining proceeds = $20M
    # Tier 2: Preferred Return = min($20M, $25M) = $20M to LP
    # Remaining proceeds = $0M
    # GP receives $0 carried interest because hurdle ($25M) was not met!
    euro_lp_capital = total_drawn
    euro_lp_hurdle = total_proceeds - euro_lp_capital
    euro_gp_carry = 0.0

    print("--- European (Whole-Fund) Waterfall ---")
    print(f"LP Return of Capital: ${euro_lp_capital:.2f}M")
    print(f"LP Preferred Return: ${euro_lp_hurdle:.2f}M (Hurdle shortfall: ${accrued_hurdle - euro_lp_hurdle:.2f}M)")
    print(f"GP Carried Interest: ${euro_gp_carry:.2f}M")
    print("Clawback Liability: $0.00M")

    # 2. American (Deal-by-Deal) Waterfall
    # Deal 1 exits in Year 3 for $90M on $30M cost basis (Profit = $60M)
    # Hurdle on Deal 1: $30M * ((1.08)^3 - 1) = $30M * 0.2597 = $7.79M
    d1_cost = 30.0
    d1_proceeds = 90.0
    d1_hurdle = d1_cost * ((1.0 + hurdle_rate) ** 3 - 1.0)  # $7.79M
    d1_profit_above_cost = d1_proceeds - d1_cost  # $60M
    d1_profit_above_hurdle = d1_profit_above_cost - d1_hurdle  # $52.21M

    # Under 100% GP catch-up:
    # GP receives 100% of cash until GP carry = 20% of total profit (hurdle + catch-up)
    # GP catch-up amount: C / (d1_hurdle + C) = 0.20 => C = 0.20 / 0.80 * d1_hurdle = 0.25 * d1_hurdle
    d1_gp_catchup = 0.25 * d1_hurdle
    # Remaining profit split 80% LP / 20% GP
    d1_residual_profit = d1_profit_above_hurdle - d1_gp_catchup
    d1_gp_residual = 0.20 * d1_residual_profit
    d1_gp_carry = d1_gp_catchup + d1_gp_residual

    # Deal 2 exits for $30M on $30M cost (no carry, no loss)
    # Deal 3 collapses to $0 on $40M cost (total loss of $40M)
    # Cumulative fund profit across all 3 deals = $20M
    # Maximum allowable GP carry on whole-fund basis = $0 (since net profit $20M < total hurdle $25M)
    clawback_liability = d1_gp_carry

    print("\n--- American (Deal-by-Deal) Waterfall ---")
    print(f"Deal 1 Exit Proceeds: ${d1_proceeds:.2f}M on ${d1_cost:.2f}M cost")
    print(f"Deal 1 GP Carry Distributed: ${d1_gp_carry:.2f}M")
    print("Deal 3 Loss: -$40.00M")
    print(f"Interim GP Carry Over-Distribution: ${d1_gp_carry:.2f}M")
    print(f"Final Clawback Owed by GP to LPs: ${clawback_liability:.2f}M")


main()
