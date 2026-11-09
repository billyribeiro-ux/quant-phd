"""Lab FI1-L04-1: Par yield computation, repricing check, and term spread analysis.

SIMULATED: annual zero curve with derived par yields and term spreads.
Calculations use exact rational arithmetic and high-precision floats.
Standard library only; no network.
"""

from __future__ import annotations

from fractions import Fraction


def compute_par_yield(discount_factors: list[Fraction]) -> Fraction:
    """Compute annual par yield from a list of annual discount factors Z(1), ..., Z(n)."""
    z_n = discount_factors[-1]
    annuity = sum(discount_factors)
    return (Fraction(1, 1) - z_n) / annuity


def main() -> None:
    # 1. Given zero-coupon spot rates for maturities 1 through 10 years
    # Ascending curve: s(tau) = 0.03 + 0.003 * tau
    maturities = list(range(1, 11))
    spot_rates = {tau: Fraction(30 + 3 * tau, 1000) for tau in maturities}

    discount_factors = [Fraction(1, 1) / ((1 + spot_rates[tau]) ** tau) for tau in maturities]

    # 2. Compute par yields
    par_yields: dict[int, Fraction] = {}
    print("Maturity | Spot Rate s(tau) | Par Yield c*(tau) | 1y Forward f(tau-1, tau)")
    print("-" * 65)

    for tau in maturities:
        c_star = compute_par_yield(discount_factors[:tau])
        par_yields[tau] = c_star
        s_val = spot_rates[tau]
        f_val = s_val if tau == 1 else (discount_factors[tau - 2] / discount_factors[tau - 1]) - 1

        print(f"{tau:8d} | {float(s_val):16.4%} | {float(c_star):17.4%} | {float(f_val):24.4%}")

        # In an upward-sloping spot curve, f(tau) > s(tau) > c*(tau) for tau > 1
        if tau > 1:
            assert f_val > s_val > c_star

    print("-" * 65)
    print("Ordering check verified: forward rate > spot rate > par yield for all tau > 1.")

    # 3. Repricing check: a bond with coupon c*(tau) must price exactly to 100 per 100 face
    print("\nPar Bond Repricing Verification (Face = 100.00):")
    for tau in [2, 5, 10]:
        c_star = par_yields[tau]
        dfs = discount_factors[:tau]
        pv = 100 * (c_star * sum(dfs) + dfs[-1])
        err = abs(float(pv) - 100.0)
        print(f"  tau = {tau:2d} yr: Price = {float(pv):.10f}, |Error from 100.00| = {err:.2e}")
        assert err < 1e-12

    # 4. Term spreads: 10y - 2y spread for spot and par curves
    spot_10_2 = spot_rates[10] - spot_rates[2]
    par_10_2 = par_yields[10] - par_yields[2]
    print("\nTerm Spreads (10-Year minus 2-Year):")
    print(f"  Spot Curve 10y - 2y Spread = {float(spot_10_2):.4%} ({float(spot_10_2) * 10000:.2f} bps)")
    print(f"  Par Curve 10y - 2y Spread  = {float(par_10_2):.4%} ({float(par_10_2) * 10000:.2f} bps)")


main()
