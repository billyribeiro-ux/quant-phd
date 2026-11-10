"""Lab GM5-project-2: Rung 2 Completion Problem — Margin Deficit & Liquidation Resolver.

Twin solution for the completion problem on project.html.
Computes margin deficit, forced asset liquidation quantity, and secondary fire-sale impact.
"""

from __future__ import annotations


def resolve_margin_call(
    position: float,
    price: float,
    cash: float,
    debt: float,
    haircut: float,
    lambda_depth: float,
) -> dict[str, float]:
    """Resolve margin deficit through cash buffers and forced asset liquidation.

    Parameters
    ----------
    position : float
        Units of asset held (Q).
    price : float
        Asset market price (P).
    cash : float
        Unencumbered cash (C).
    debt : float
        Collateralized borrowing (D).
    haircut : float
        Regulatory/broker margin fraction (h).
    lambda_depth : float
        Kyle's lambda market impact ($/unit).

    Returns
    -------
    dict[str, float]
        Dictionary with deficit, cash_used, forced_qty, price_drop, terminal_price.
    """
    asset_value = position * price
    equity = asset_value + cash - debt
    required_margin = haircut * asset_value

    margin_deficit = max(0.0, required_margin - equity)

    cash_used = min(cash, margin_deficit)
    remaining_deficit = margin_deficit - cash_used

    denom = haircut * price
    forced_qty = min(position, remaining_deficit / denom) if denom > 0.0 else position
    proceeds = forced_qty * price

    price_drop = lambda_depth * forced_qty
    terminal_price = max(0.01, price - price_drop)

    post_pos = position - forced_qty
    post_debt = max(0.0, debt - cash_used - proceeds)
    post_equity = post_pos * terminal_price - post_debt

    return {
        "margin_deficit": float(margin_deficit),
        "cash_used": float(cash_used),
        "forced_qty": float(forced_qty),
        "price_drop": float(price_drop),
        "terminal_price": float(terminal_price),
        "post_equity": float(post_equity),
    }


def main() -> None:
    # Test instance with $1.5M position stressed by price drop to $85.00
    pos = 15000.0
    px = 85.0
    c = 15000.0
    d = 1200000.0
    h = 0.18
    lam = 0.0008

    res = resolve_margin_call(pos, px, c, d, h, lam)

    print("Pre-Resolution Deficit ($):", round(res["margin_deficit"], 2))
    print("Cash Buffer Applied ($):", round(res["cash_used"], 2))
    print("Forced Units Liquidated:", round(res["forced_qty"], 2))
    print("Secondary Fire-Sale Price Drop ($):", round(res["price_drop"], 4))
    print("Terminal Asset Price ($):", round(res["terminal_price"], 4))
    print("Post-Liquidation Equity ($):", round(res["post_equity"], 2))


main()
