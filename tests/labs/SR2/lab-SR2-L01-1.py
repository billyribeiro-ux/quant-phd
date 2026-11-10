"""Lab SR2-L01-1: Procyclical Leverage and Mark-to-Market Accounting.

Simulates intermediary balance sheet adjustments under countercyclical (household),
constant (commercial bank), and procyclical VaR (broker-dealer) leverage rules
following Adrian and Shin (2010).
"""


def main() -> None:
    # Initial balance sheet (SIMULATED broker-dealer)
    a0 = 100.0  # Initial assets
    e0 = 10.0  # Initial equity
    d0 = a0 - e0  # Initial debt = 90.0
    lev0 = a0 / e0  # Initial leverage = 10.0

    print("=== INITIAL BALANCE SHEET (SIMULATED) ===")
    print(f"Assets: ${a0:.2f}M | Debt: ${d0:.2f}M | Equity: ${e0:.2f}M | Leverage: {lev0:.2f}x")

    # Scenario 1: Asset appreciation (+1% shock, +$1.0M)
    delta_a_price = 1.0
    e1 = e0 + delta_a_price  # Equity absorbs the full mark-to-market gain = 11.0
    a1_unadjusted = a0 + delta_a_price  # 101.0

    # Rule A: Passive debt (countercyclical leverage, typical household/corporate)
    lev_passive = a1_unadjusted / e1
    print("\n--- Boom (+1% Asset Price Shock): Passive Debt ---")
    print(f"Assets: ${a1_unadjusted:.2f}M | Equity: ${e1:.2f}M | Leverage: {lev_passive:.4f}x (fell from {lev0:.2f}x)")

    # Rule B: Constant leverage targeting (L* = 10.0, typical commercial bank)
    target_lev_b = 10.0
    a1_target_b = target_lev_b * e1  # 110.0
    purchases_b = a1_target_b - a1_unadjusted  # 9.0
    d1_b = a1_target_b - e1  # 99.0
    print("\n--- Boom (+1% Asset Price Shock): Constant Leverage (L*=10.0) ---")
    print(
        f"Target Assets: ${a1_target_b:.2f}M | Additional Debt: ${d1_b - d0:.2f}M | "
        f"Asset Purchases: ${purchases_b:.2f}M"
    )

    # Rule C: Procyclical VaR leverage (broker-dealer; volatility falls from 2.0% to 1.5%)
    alpha_z = 5.0
    vol_boom = 0.015
    target_lev_c = 1.0 / (alpha_z * vol_boom)  # 1 / 0.075 = 13.3333
    a1_target_c = target_lev_c * e1  # 146.6667
    purchases_c = a1_target_c - a1_unadjusted  # 45.6667
    d1_c = a1_target_c - e1  # 135.6667
    print("\n--- Boom (+1% Asset Price Shock): Procyclical VaR Leverage ---")
    print(
        f"Target Leverage: {target_lev_c:.4f}x | Target Assets: ${a1_target_c:.2f}M | "
        f"Additional Debt: ${d1_c - d0:.2f}M | Asset Purchases: ${purchases_c:.2f}M"
    )

    # Scenario 2: Asset downturn (-1% shock, -$1.0M) and volatility spike to 3.0%
    delta_a_down = -1.0
    e2 = e0 + delta_a_down  # Equity falls to 9.0
    a2_unadjusted = a0 + delta_a_down  # 99.0
    vol_bust = 0.03
    target_lev_bust = 1.0 / (alpha_z * vol_bust)  # 1 / 0.15 = 6.6667
    a2_target_bust = target_lev_bust * e2  # 60.0
    forced_sales = a2_unadjusted - a2_target_bust  # 99.0 - 60.0 = 39.0
    d2_bust = a2_target_bust - e2  # 51.0
    debt_repaid = d0 - d2_bust  # 90.0 - 51.0 = 39.0

    print("\n--- Downturn (-1% Asset Price Shock & Volatility Spike to 3.0%): Procyclical VaR ---")
    print(
        f"Target Leverage: {target_lev_bust:.4f}x | Target Assets: ${a2_target_bust:.2f}M | "
        f"Forced Fire Sales: ${forced_sales:.2f}M | Debt Runoff: ${debt_repaid:.2f}M"
    )


main()
