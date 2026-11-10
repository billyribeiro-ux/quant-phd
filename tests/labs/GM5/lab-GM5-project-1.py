"""Lab GM5-project-1: Rung 1 Worked Example — Crisis Mechanism Simulator.

Provides a fully solved, annotated numerical trace of a leveraged institutional balance sheet
undergoing an exogenous price shock, margin calls, fire-sale liquidation, and backstop stabilization.
"""

from __future__ import annotations


def main() -> None:
    # 1. Initial State: Leveraged multi-strategy fund
    p0 = 100.0  # Asset price
    q0 = 10000.0  # 10,000 units held ($1,000,000 gross asset value)
    cash0 = 20000.0  # $20,000 unencumbered cash
    debt0 = 900000.0  # $900,000 repo debt

    initial_asset_val = q0 * p0
    initial_equity = initial_asset_val + cash0 - debt0  # $120,000
    initial_leverage = initial_asset_val / initial_equity  # 8.33x leverage

    print("--- 1. Initial State ---")
    print(f"Asset Price: ${p0:.2f}")
    print(f"Gross Assets: ${initial_asset_val:,.2f}")
    print(f"Fund Equity: ${initial_equity:,.2f}")
    print(f"Initial Leverage: {initial_leverage:.2f}x")

    # 2. Exogenous Macro Shock: -5.00% fundamental devaluation
    shock_pct = -0.05
    p1 = p0 * (1.0 + shock_pct)  # $95.00
    asset_val_1 = q0 * p1  # $950,000
    equity_1 = asset_val_1 + cash0 - debt0  # $70,000 ($50,000 loss)
    asset_val_1 / equity_1  # 13.57x leverage

    # Prime broker margin requirement increases due to volatility: h1 = h0 + 0.05 = 0.15
    h1 = 0.15
    required_margin_1 = h1 * asset_val_1  # 0.15 * 950,000 = $142,500
    margin_deficit = max(0.0, required_margin_1 - equity_1)  # $142,500 - $70,000 = $72,500

    print("\n--- 2. Post-Shock State ---")
    print(f"Stressed Price: ${p1:.2f}")
    print(f"Fund Equity: ${equity_1:,.2f}")
    print(f"Required Margin (15%): ${required_margin_1:,.2f}")
    print(f"Margin Deficit: ${margin_deficit:,.2f}")

    # 3. Forced Deleveraging: Cash buffer utilized first, remainder liquidated
    cash_used = min(cash0, margin_deficit)  # $20,000 cash paid
    remaining_deficit = margin_deficit - cash_used  # $52,500 remaining deficit
    # Asset liquidation formula: Delta_Q = remaining_deficit / (h1 * p1)
    forced_qty = remaining_deficit / (h1 * p1)  # 52,500 / (0.15 * 95) = 3,684.21 units
    q2 = q0 - forced_qty  # 6,315.79 units remaining
    proceeds = forced_qty * p1  # $350,000
    debt0 - cash_used - proceeds  # $900k - $20k - $350k = $530,000

    print("\n--- 3. Forced Liquidation ---")
    print(f"Cash Used for Margin: ${cash_used:,.2f}")
    print(f"Forced Units Liquidated: {forced_qty:,.2f}")
    print(f"Gross Liquidation Proceeds: ${proceeds:,.2f}")
    print(f"Remaining Position: {q2:,.2f} units")

    # 4. Fire-Sale Price Impact: Kyle's lambda = 0.001 $/unit
    lambda_impact = 0.001
    price_impact = lambda_impact * forced_qty  # $3.68 price drop
    p_final = p1 - price_impact  # $91.32
    total_drop = p0 - p_final  # $8.68
    exogenous_drop = p0 * abs(shock_pct)  # $5.00
    spiral_multiplier = total_drop / exogenous_drop  # 1.737x

    print("\n--- 4. Secondary Fire-Sale Impact & Spiral Multiplier ---")
    print(f"Fire-Sale Price Impact: -${price_impact:.2f}")
    print(f"Final Depressed Price: ${p_final:.2f}")
    print(f"Spiral Multiplier: {spiral_multiplier:.4f}x")


main()
