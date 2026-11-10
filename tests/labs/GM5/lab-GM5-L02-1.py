"""Lab GM5-L02-1: Forced-Seller Dynamics & Margin Spiral Simulation.

Quantifies the dual loss-and-margin spiral of Brunnermeier & Pedersen (2009),
tracking balance-sheet deleveraging, haircut jumps, and fire-sale discounts.
"""

from __future__ import annotations

from typing import Any


def run_margin_spiral(
    initial_asset_price: float,
    initial_units: float,
    cash_buffer: float,
    initial_debt: float,
    base_haircut: float,
    exogenous_price_shock_pct: float,
    haircut_vol_sensitivity: float,
    market_depth_lambda: float,
    max_iterations: int = 10,
) -> dict[str, Any]:
    """Simulate intra-period iterative margin calls and forced liquidations.

    Parameters
    ----------
    initial_asset_price : float
        Starting market price P0.
    initial_units : float
        Starting position Q0.
    cash_buffer : float
        Unencumbered cash C0.
    initial_debt : float
        Repo/margin borrowing D0.
    base_haircut : float
        Initial collateral haircut h0.
    exogenous_price_shock_pct : float
        Initial price shock fraction (e.g. -0.05 for -5%).
    haircut_vol_sensitivity : float
        Sensitivity kappa where h = h0 + kappa * |Delta P / P|.
    market_depth_lambda : float
        Price impact per unit sold (Kyle's lambda).
    max_iterations : int
        Maximum spiral rounds within the period.

    Returns
    -------
    dict[str, float | int | list[float]]
        Summary including total forced volume, terminal price, and spiral multiplier.
    """
    price = initial_asset_price * (1.0 + exogenous_price_shock_pct)
    units = initial_units
    debt = initial_debt
    cash = cash_buffer
    haircut = min(0.60, base_haircut + haircut_vol_sensitivity * abs(exogenous_price_shock_pct))

    price_history = [initial_asset_price, price]
    forced_sales: list[float] = []

    for _ in range(max_iterations):
        asset_val = units * price
        equity = asset_val + cash - debt
        if equity <= 0.0:
            # Insolvency liquidation
            forced_qty = units
            units = 0.0
            price = max(0.01, price - market_depth_lambda * forced_qty)
            price_history.append(price)
            forced_sales.append(forced_qty)
            break

        required_margin = haircut * asset_val
        deficit = max(0.0, required_margin - equity)
        if deficit < 1e-6:
            break

        # Use available cash first
        cash_used = min(cash, deficit)
        cash -= cash_used
        debt -= cash_used
        rem_deficit = deficit - cash_used

        if rem_deficit < 1e-6:
            break

        # Liquidate assets: Delta_Q = rem_deficit / (haircut * price)
        forced_qty = min(units, rem_deficit / (haircut * price))
        units -= forced_qty
        proceeds = forced_qty * price
        debt = max(0.0, debt - proceeds)
        forced_sales.append(forced_qty)

        # Market impact of liquidation
        price_drop = market_depth_lambda * forced_qty
        price = max(0.01, price - price_drop)
        price_history.append(price)

        # Haircut responds to secondary price drop
        secondary_shock_pct = price_drop / price_history[-2]
        haircut = min(0.60, haircut + haircut_vol_sensitivity * secondary_shock_pct)

    total_drop = initial_asset_price - price
    exogenous_drop = initial_asset_price * abs(exogenous_price_shock_pct)
    multiplier = total_drop / max(1e-6, exogenous_drop)

    return {
        "terminal_price": price,
        "total_forced_units": sum(forced_sales),
        "spiral_rounds": len(forced_sales),
        "terminal_haircut": haircut,
        "spiral_multiplier": multiplier,
        "price_history": price_history,
    }


def main() -> None:
    p0 = 100.0
    q0 = 5000.0
    equity0 = 50000.0  # 10x leverage (500k assets on 50k equity)
    debt0 = p0 * q0 - equity0
    cash0 = 5000.0
    h0 = 0.10  # 10% base haircut

    # Baseline with no haircut sensitivity (loss spiral only)
    res_loss = run_margin_spiral(
        initial_asset_price=p0,
        initial_units=q0,
        cash_buffer=cash0,
        initial_debt=debt0,
        base_haircut=h0,
        exogenous_price_shock_pct=-0.04,
        haircut_vol_sensitivity=0.0,
        market_depth_lambda=0.002,
    )

    # Coupled loss and margin spiral (haircut sensitivity > 0)
    res_coupled = run_margin_spiral(
        initial_asset_price=p0,
        initial_units=q0,
        cash_buffer=cash0,
        initial_debt=debt0,
        base_haircut=h0,
        exogenous_price_shock_pct=-0.04,
        haircut_vol_sensitivity=0.35,
        market_depth_lambda=0.002,
    )

    print("Initial Price ($):", round(p0, 2))
    print("Exogenous Shock: -4.00%")
    print("Loss-Only Terminal Price ($):", round(float(res_loss["terminal_price"]), 2))
    print("Loss-Only Forced Units:", round(float(res_loss["total_forced_units"]), 1))
    print("Loss-Only Multiplier:", round(float(res_loss["spiral_multiplier"]), 4))
    print("Coupled Terminal Price ($):", round(float(res_coupled["terminal_price"]), 2))
    print("Coupled Forced Units:", round(float(res_coupled["total_forced_units"]), 1))
    print("Coupled Terminal Haircut (%):", round(float(res_coupled["terminal_haircut"]) * 100.0, 2))
    print("Coupled Spiral Multiplier:", round(float(res_coupled["spiral_multiplier"]), 4))


main()
