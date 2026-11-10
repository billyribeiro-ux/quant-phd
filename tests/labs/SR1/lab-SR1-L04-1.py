"""Lab SR1-L04-1: Asset Fire Sales and Cash-in-the-Market Pricing.

Computes equilibrium market clearing prices and fire-sale discounts under limited buyer
liquidity pools (Shleifer and Vishny 2011). Evaluates the resulting mark-to-market
balance sheet impairment on non-liquidating peer institutions.
"""

from fractions import Fraction


def main() -> None:
    # Model parameters
    cash_pool = Fraction(100, 1)  # Unconstrained buyer liquidity pool C = 100
    p_fund = Fraction(1, 1)  # Fundamental asset value p_fund = 1.00
    peer_holding = Fraction(150, 1)  # Peer bank asset holding A_peer = 150
    peer_equity_buffer = Fraction(35, 1)  # Peer bank regulatory capital buffer = 35

    # Forced liquidation volumes Q
    liquidation_quantities = [
        Fraction(50, 1),
        Fraction(80, 1),
        Fraction(100, 1),
        Fraction(125, 1),
        Fraction(160, 1),
        Fraction(200, 1),
    ]

    print(f"Buyer Liquidity Pool C = {cash_pool}, Fundamental Price p_fund = {p_fund}")
    print(f"Peer Bank Holding = {peer_holding}, Capital Buffer = {peer_equity_buffer}\n")
    print(f"{'Q':>6} | {'Price p(Q)':>11} | {'Discount':>9} | {'MTM Loss':>9} | {'Peer Solvency':>14}")
    print("-" * 62)

    for q in liquidation_quantities:
        p = p_fund if q * p_fund <= cash_pool else cash_pool / q
        discount = (p_fund - p) / p_fund
        mtm_loss = peer_holding * (p_fund - p)
        solvent = "Solvent" if mtm_loss <= peer_equity_buffer else "Capital Breach"
        disc_pct = float(discount) * 100
        print(f"{float(q):6.1f} | {float(p):11.4f} | {disc_pct:7.2f}% | {float(mtm_loss):9.2f} | {solvent:>14}")

    print("\nSystemic Spillover:")
    print("At Q = 160, fire-sale price drops to 0.6250 (37.50% discount).")
    print("Peer bank incurs a 56.25 mark-to-market loss, exceeding its 35.00 buffer and forcing secondary sales.")


main()
