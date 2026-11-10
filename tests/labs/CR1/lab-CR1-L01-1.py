"""Lab CR1-L01-1: Merton (1974) structural credit model pricing and spread term structures.

Demonstrates closed-form valuation of equity as a call option on firm assets,
risky zero-coupon debt, credit spreads, and the term structure of credit spreads
for solvent versus distressed firms.
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def merton_pricing(
    v: float,
    d: float,
    t: float,
    r: float,
    sigma: float,
) -> dict[str, float]:
    """Calculate Merton model components."""
    vol_sqrt = sigma * math.sqrt(t)
    d1 = (math.log(v / d) + (r + 0.5 * sigma * sigma) * t) / vol_sqrt
    d2 = d1 - vol_sqrt

    equity = v * norm_cdf(d1) - d * math.exp(-r * t) * norm_cdf(d2)
    debt = v - equity
    debt_yield = -math.log(debt / d) / t
    spread_bps = (debt_yield - r) * 10000.0
    pd = norm_cdf(-d2)

    return {
        "equity": equity,
        "debt": debt,
        "yield": debt_yield,
        "spread_bps": spread_bps,
        "default_prob": pd,
    }


def main() -> None:
    # Stylized solvent firm: V = 100, D = 70, r = 0.04, sigma = 0.25
    v_solvent = 100.0
    d_face = 70.0
    r_rf = 0.04
    sigma_v = 0.25

    maturities = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]

    print("Merton (1974) Credit Spread Term Structure (Solvent Firm: V=100, D=70):")
    print("  T (yr) | Equity ($) |  Debt ($)  | Yield (%) | Spread (bp) | Risk-Neutral PD")
    print("---------+------------+------------+-----------+-------------+----------------")

    spreads_solvent: list[float] = []
    for t in maturities:
        res = merton_pricing(v_solvent, d_face, t, r_rf, sigma_v)
        spreads_solvent.append(res["spread_bps"])
        # Invariant check: Equity + Debt == Asset Value
        assert abs(res["equity"] + res["debt"] - v_solvent) < 1e-11
        print(
            f"  {t:5.1f}  |   {res['equity']:6.2f}   |   {res['debt']:6.2f}   |   "
            f"{res['yield'] * 100:5.2f}%  |    {res['spread_bps']:6.1f}   |     {res['default_prob']:6.4f}"
        )

    # Distressed firm: V = 60, D = 70 (in distress, leverage D/V > 1)
    v_distressed = 60.0
    print("\nMerton (1974) Credit Spread Term Structure (Distressed Firm: V=60, D=70):")
    print("  T (yr) | Equity ($) |  Debt ($)  | Yield (%) | Spread (bp) | Risk-Neutral PD")
    print("---------+------------+------------+-----------+-------------+----------------")

    spreads_distressed: list[float] = []
    for t in maturities:
        res = merton_pricing(v_distressed, d_face, t, r_rf, sigma_v)
        spreads_distressed.append(res["spread_bps"])
        assert abs(res["equity"] + res["debt"] - v_distressed) < 1e-11
        print(
            f"  {t:5.1f}  |   {res['equity']:6.2f}   |   {res['debt']:6.2f}   |   "
            f"{res['yield'] * 100:5.2f}%  |    {res['spread_bps']:6.1f}   |     {res['default_prob']:6.4f}"
        )

    # Confirm key qualitative properties of Merton term structure
    # For solvent firm, short spread approaches zero as T -> 0
    short_spread = merton_pricing(v_solvent, d_face, 0.05, r_rf, sigma_v)["spread_bps"]
    print(f"\nSolvent firm short-maturity spread (T=0.05y): {short_spread:6.2f} bp (approaches 0)")
    assert short_spread < 1.0

    # For distressed firm, spread is monotonically downward sloping
    is_downward = all(spreads_distressed[i] >= spreads_distressed[i + 1] for i in range(len(spreads_distressed) - 1))
    print(f"Distressed firm term structure is monotonically downward sloping: {is_downward}")
    assert is_downward


main()
