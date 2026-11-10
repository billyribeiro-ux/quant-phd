"""Lab CF4-L04-1: Enterprise-to-Equity Bridge and Treasury Stock Method Dilution.

Reconciles operating enterprise value to common equity value, evaluates option
dilution via the Treasury Stock Method, and benchmarks fundamental implied multiples.
"""

from __future__ import annotations


def treasury_stock_dilution(
    basic_shares: float,
    share_price: float,
    option_tranches: list[tuple[float, float]],  # list of (options_count, strike_price)
) -> dict[str, float]:
    """Calculate diluted share count using the Treasury Stock Method."""
    total_new_shares = 0.0
    total_proceeds = 0.0

    for count, strike in option_tranches:
        if share_price > strike:
            total_new_shares += count
            total_proceeds += count * strike

    repurchased_shares = total_proceeds / share_price if share_price > 0.0 else 0.0
    net_dilutive_shares = total_new_shares - repurchased_shares
    diluted_shares = basic_shares + net_dilutive_shares

    return {
        "basic_shares": float(basic_shares),
        "total_new_shares": float(total_new_shares),
        "total_proceeds": float(total_proceeds),
        "repurchased_shares": float(repurchased_shares),
        "net_dilutive_shares": float(net_dilutive_shares),
        "diluted_shares": float(diluted_shares),
    }


def full_bridge_valuation(
    enterprise_value: float,
    total_debt: float,
    cash: float,
    minority_interest: float,
    pension_deficit: float,
    associates_investments: float,
    basic_shares: float,
    option_tranches: list[tuple[float, float]],
) -> dict[str, float]:
    """Reconcile EV to diluted equity value with iterative share price resolution."""
    net_debt = total_debt - cash
    total_non_equity_claims = total_debt + minority_interest + pension_deficit
    total_non_operating_assets = cash + associates_investments
    equity_value = enterprise_value - total_non_equity_claims + total_non_operating_assets

    # Fixed-point iteration to simultaneously solve share price and TSM dilution
    p = equity_value / basic_shares
    for _ in range(50):
        tsm = treasury_stock_dilution(basic_shares, p, option_tranches)
        new_p = equity_value / tsm["diluted_shares"]
        if abs(new_p - p) < 1e-8:
            break
        p = new_p

    tsm_final = treasury_stock_dilution(basic_shares, p, option_tranches)

    return {
        "enterprise_value": float(enterprise_value),
        "net_debt": float(net_debt),
        "equity_value": float(equity_value),
        "per_share_basic": float(equity_value / basic_shares),
        "per_share_diluted": float(p),
        "diluted_shares": float(tsm_final["diluted_shares"]),
        "dilution_pct": float((tsm_final["diluted_shares"] / basic_shares - 1.0) * 100.0),
    }


def main() -> None:
    print("CF4 Lab L04-1: Enterprise-to-Equity Bridge & Treasury Stock Dilution")
    print("===================================================================")

    enterprise_value = 2400.0  # $M
    total_debt = 550.0  # $M
    cash = 120.0  # $M
    minority_interest = 45.0  # $M
    pension_deficit = 25.0  # $M
    associates_investments = 50.0  # $M
    basic_shares = 80.0  # million shares

    # In-the-money options: (count in M, strike in $)
    option_tranches = [
        (5.0, 15.00),  # 5M options at $15
        (4.0, 18.00),  # 4M options at $18
        (3.0, 22.00),  # 3M options at $22
    ]

    res = full_bridge_valuation(
        enterprise_value,
        total_debt,
        cash,
        minority_interest,
        pension_deficit,
        associates_investments,
        basic_shares,
        option_tranches,
    )

    print(f"Enterprise Value:             ${res['enterprise_value']:.2f}M")
    print(f"Net Debt:                     ${res['net_debt']:.2f}M")
    print(f"Equity Value:                 ${res['equity_value']:.2f}M")
    print(f"Basic Share Count:             {res.get('basic_shares', basic_shares):.2f}M")
    print(f"Basic Equity Value Per Share: ${res['per_share_basic']:.2f}")
    print(f"Diluted Share Count:           {res['diluted_shares']:.2f}M")
    print(f"Dilution Rate:                 {res['dilution_pct']:.2f}%")
    print(f"Diluted Fair Value Per Share: ${res['per_share_diluted']:.2f}")

    # Implied multiple check
    ebitda = 220.0  # $M
    net_income = 110.0  # $M
    implied_ev_ebitda = enterprise_value / ebitda
    implied_pe = res["equity_value"] / net_income
    print(f"Implied EV/EBITDA Multiple:    {implied_ev_ebitda:.2f}x")
    print(f"Implied P/E Multiple:          {implied_pe:.2f}x")


main()
