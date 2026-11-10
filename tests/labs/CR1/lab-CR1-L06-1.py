"""Lab CR1-L06-1: Credit spread decomposition and the Huang & Huang (2012) credit spread puzzle.

Demonstrates the decomposition of observed corporate bond credit spreads into
expected default losses, credit risk premia, and non-credit residuals across rating classes.
"""

from __future__ import annotations

import math


def decompose_spread(
    market_spread_bps: float,
    pd_10y: float,
    recovery: float,
    maturity: float,
    rp_multiplier: float,
) -> dict[str, float]:
    """Decompose market spread in basis points into credit and non-credit components."""
    s = market_spread_bps / 10000.0
    loss_fraction = pd_10y * (1.0 - recovery)
    spread_el = -math.log(1.0 - loss_fraction) / maturity if loss_fraction < 1.0 else 1.0
    spread_crp = spread_el * rp_multiplier
    spread_credit = spread_el + spread_crp
    spread_residual = max(0.0, s - spread_credit)
    credit_fraction = min(s, spread_credit) / s if s > 0 else 1.0

    return {
        "el_bps": spread_el * 10000.0,
        "crp_bps": spread_crp * 10000.0,
        "credit_bps": spread_credit * 10000.0,
        "residual_bps": spread_residual * 10000.0,
        "credit_fraction": credit_fraction,
    }


def main() -> None:
    # 10-year corporate bond spread empirical calibration based on Huang & Huang (2012, Table 4)
    # Rating: (Rating, Market Spread bps, Historical 10y cumulative default prob, Recovery R, Risk Premium Ratio)
    ratings_data = [
        ("Aaa", 63.0, 0.0077, 0.51, 1.80),
        ("Aa", 73.0, 0.0140, 0.49, 1.60),
        ("A", 99.0, 0.0220, 0.45, 1.40),
        ("Baa", 168.0, 0.0488, 0.41, 1.10),
        ("Ba", 305.0, 0.1800, 0.38, 0.75),
        ("B", 465.0, 0.4200, 0.35, 0.45),
    ]

    maturity = 10.0

    print("Credit Spread Decomposition across 10-Year Rating Buckets (Huang & Huang 2012):")
    print("  Rating | Market Spread | Expected Loss | Risk Premium | Total Credit | Non-Credit Res | Credit Share")
    print("---------+---------------+---------------+--------------+--------------+----------------+-------------")

    fractions: dict[str, float] = {}

    for rating, mkt_spd, pd_val, rec_val, rp_ratio in ratings_data:
        res = decompose_spread(mkt_spd, pd_val, rec_val, maturity, rp_ratio)
        fractions[rating] = res["credit_fraction"]

        # Articulation identity check: Total Credit + Non-Credit Residual == Market Spread
        assert abs((res["credit_bps"] + res["residual_bps"]) - mkt_spd) < 1e-9

        print(
            f"   {rating:4s}  |    {mkt_spd:5.1f} bp   |    {res['el_bps']:5.1f} bp   |   "
            f"{res['crp_bps']:5.1f} bp   |   {res['credit_bps']:5.1f} bp   |    "
            f"{res['residual_bps']:5.1f} bp    |    {res['credit_fraction'] * 100:5.1f}%"
        )

    # Verification of the Credit-Spread Puzzle:
    # 1. For investment-grade bonds (Aaa, Aa, A, Baa), credit risk accounts for under 40% of observed spreads
    for ig in ["Aaa", "Aa", "A", "Baa"]:
        assert fractions[ig] < 0.40, f"Credit fraction for {ig} expected < 40%, got {fractions[ig]:.2%}"

    # 2. For high-yield bonds (Ba, B), credit risk accounts for a substantially higher fraction (> 50%)
    for hy in ["Ba", "B"]:
        assert fractions[hy] > 0.50, f"Credit fraction for {hy} expected > 50%, got {fractions[hy]:.2%}"

    print(
        f"\nCredit-spread puzzle confirmed: Aaa credit share = {fractions['Aaa'] * 100:.1f}% "
        f"vs B credit share = {fractions['B'] * 100:.1f}%"
    )


main()
