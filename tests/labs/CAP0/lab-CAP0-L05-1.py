"""Lab L05-1: Board presentation multi-scenario model and breakeven stress testing."""

from __future__ import annotations


def main() -> None:
    current_market_price = 36.00
    shares = 50.0
    net_debt = 200.0

    # Base, Bull, and Bear DCF outcomes
    scenarios = {
        "Bull Case (+25% Growth, +200 bps Margin)": {
            "ev": 2680.0,
            "icr_y1": 5.4,
            "weight": 0.25,
        },
        "Base Case (Consensus Plan)": {
            "ev": 2240.0,
            "icr_y1": 4.1,
            "weight": 0.50,
        },
        "Bear Case (-20% Growth, -300 bps Margin)": {
            "ev": 1650.0,
            "icr_y1": 2.3,
            "weight": 0.25,
        },
    }

    covenant_min_icr = 2.50

    print("Scenario                                 | EV ($M) | Equity ($M) | Price ($) | Upside (%) | ICR | Breach")
    print("-" * 92)

    weighted_price = 0.0

    for name, data in scenarios.items():
        ev = data["ev"]
        eq_val = ev - net_debt
        price = eq_val / shares
        upside = (price - current_market_price) / current_market_price
        icr = data["icr_y1"]
        breach = "YES (DEFAULT)" if icr < covenant_min_icr else "NO (SAFE)"

        weighted_price += data["weight"] * price
        print(f"{name:40s} | {ev:7.1f} | {eq_val:11.1f} | {price:9.2f} | {upside * 100:+9.2f}% | {icr:3.1f} | {breach}")

    total_upside = (weighted_price - current_market_price) / current_market_price
    print("-" * 92)
    print(f"Scenario-Weighted Target Price: ${weighted_price:.2f} (Expected Upside: {total_upside * 100:+.2f}%)")

    # Margin of safety breakeven analysis
    base_price = (scenarios["Base Case (Consensus Plan)"]["ev"] - net_debt) / shares
    bear_price = (scenarios["Bear Case (-20% Growth, -300 bps Margin)"]["ev"] - net_debt) / shares
    price_sensitivity_per_growth_pct = (base_price - bear_price) / 20.0
    breakeven_growth_shock = (base_price - current_market_price) / price_sensitivity_per_growth_pct

    print(
        f"Margin of Safety: Model target can withstand a {breakeven_growth_shock:.1f}% "
        "growth contraction before target hits market quote."
    )


main()
