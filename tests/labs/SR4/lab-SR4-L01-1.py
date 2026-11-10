"""Lab SR4-L01-1: Volcker Rule Market-Making Metrics and Inventory Risk.

SIMULATED. Evaluates trading desk compliance under Section 619 of the Dodd-Frank Act
and the 2013 Volcker Rule implementing regulations. Evaluates Reasonably Expected
Near-Term Demand (RENTD), inventory turnover, customer-facing trade ratios, and
Value-at-Risk (VaR) limits across two desks: Desk A (compliant market maker) and
Desk B (disguised proprietary positioning).
"""

from __future__ import annotations


def evaluate_desk(
    desk_id: str,
    daily_volume: float,
    average_inventory: float,
    customer_trades: int,
    total_trades: int,
    var_99_daily: float,
    daily_pnl_std: float,
    holding_period_days: float,
) -> dict[str, float | str | bool]:
    """Calculate key Volcker compliance metrics and determine compliance status."""
    if daily_volume <= 0 or average_inventory <= 0:
        raise ValueError("volume and inventory must be positive")
    if customer_trades < 0 or total_trades <= 0 or customer_trades > total_trades:
        raise ValueError("invalid trade counts")

    # Inventory turnover ratio: annual trading volume relative to average inventory
    # Assuming 252 business days per year
    annual_volume = daily_volume * 252.0
    turnover_ratio = annual_volume / average_inventory

    # Customer-facing trade share
    customer_share = float(customer_trades) / float(total_trades)

    # VaR-to-volatility ratio (ratio of 99% 1-day VaR to standard deviation of daily P&L)
    # Under standard normal, 99% VaR is ~2.326 * sigma. Large deviations indicate tail risk
    var_ratio = var_99_daily / daily_pnl_std if daily_pnl_std > 0 else 0.0

    # Compliance test:
    # 1. High inventory turnover (>= 12.0x per year, i.e., average holding < 21 days)
    # 2. Customer-facing share >= 80%
    # 3. Average holding period <= 15 days
    is_compliant = bool(turnover_ratio >= 12.0 and customer_share >= 0.80 and holding_period_days <= 15.0)

    return {
        "desk_id": desk_id,
        "turnover_ratio": turnover_ratio,
        "customer_share": customer_share,
        "var_ratio": var_ratio,
        "holding_days": holding_period_days,
        "compliant": is_compliant,
    }


def main() -> None:
    # Desk A: High-frequency customer market making in liquid corporate bonds
    res_a = evaluate_desk(
        desk_id="Desk A (Market Maker)",
        daily_volume=50.0,  # $50M daily volume
        average_inventory=120.0,  # $120M average inventory
        customer_trades=184,
        total_trades=200,
        var_99_daily=1.85,  # $1.85M 1-day 99% VaR
        daily_pnl_std=0.80,  # $0.80M daily P&L standard deviation
        holding_period_days=4.5,
    )

    # Desk B: Proprietary block warehousing desk
    res_b = evaluate_desk(
        desk_id="Desk B (Proprietary Desk)",
        daily_volume=10.0,  # $10M daily volume
        average_inventory=350.0,  # $350M average inventory
        customer_trades=42,
        total_trades=110,
        var_99_daily=9.50,  # $9.50M 1-day 99% VaR
        daily_pnl_std=3.20,  # $3.20M daily P&L standard deviation
        holding_period_days=45.0,
    )

    print("=== VOLCKER RULE COMPLIANCE EVALUATION (SIMULATED) ===")
    for res in (res_a, res_b):
        desk_name = str(res["desk_id"])
        turnover = float(res["turnover_ratio"])
        cust_share = float(res["customer_share"]) * 100.0
        var_rat = float(res["var_ratio"])
        holding = float(res["holding_days"])
        status = "COMPLIANT (MMRA)" if res["compliant"] else "NON-COMPLIANT (PROPRIETARY)"

        print(f"\n{desk_name}:")
        print(f"  Annual Inventory Turnover: {turnover:.2f}x")
        print(f"  Customer-Facing Trade Share: {cust_share:.1f}%")
        print(f"  Average Inventory Holding Period: {holding:.1f} days")
        print(f"  99% VaR to Daily P&L Volatility: {var_rat:.2f}")
        print(f"  Volcker Section 619 Classification: {status}")


main()
