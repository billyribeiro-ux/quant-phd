"""Lab FI1-L03-1: Spot rates, forward rates, and the no-arbitrage forward identity.

SIMULATED: annual zero-coupon spot yield curve and derived 1-year forward rates.
Rates are represented as exact rational Fraction instances.
Standard library only; no network.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 1. Spot rates for maturities tau = 1, 2, 3, 4 years
    spot_rates: dict[int, Fraction] = {
        1: Fraction(4, 100),  # 4.0%
        2: Fraction(9, 200),  # 4.5%
        3: Fraction(5, 100),  # 5.0%
        4: Fraction(27, 500),  # 5.4%
    }

    # 2. Discount factors: Z(tau) = 1 / (1 + s(tau))^tau
    discount_factors: dict[int, Fraction] = {}
    for tau, s in spot_rates.items():
        discount_factors[tau] = Fraction(1, 1) / ((1 + s) ** tau)

    print("Spot Rates and Zero-Coupon Discount Factors:")
    for tau in sorted(spot_rates):
        s = spot_rates[tau]
        z = discount_factors[tau]
        print(f"  tau = {tau} yr: s({tau}) = {float(s):.4%} ({s}), Z({tau}) = {float(z):.6f}")

    # 3. 1-year forward rates f(tau-1, tau) satisfying:
    # (1 + s(tau))^tau = (1 + s(tau-1))^(tau-1) * (1 + f(tau-1, tau))
    forward_rates: dict[tuple[int, int], Fraction] = {}
    for tau in range(2, 5):
        t_prev = tau - 1
        # Z(t_prev) / Z(tau) = 1 + f(t_prev, tau)
        one_plus_f = discount_factors[t_prev] / discount_factors[tau]
        f = one_plus_f - 1
        forward_rates[(t_prev, tau)] = f
        print(f"\nForward Rate f({t_prev}, {tau}):")
        print(f"  f({t_prev}, {tau}) = {float(f):.6%} ({f})")

        # Verify no-arbitrage forward compounding identity exactly
        lhs = (1 + spot_rates[tau]) ** tau
        rhs = ((1 + spot_rates[t_prev]) ** t_prev) * (1 + f)
        print(f"  Identity check (1 + s_{tau})^{tau} == (1 + s_{t_prev})^{t_prev} * (1 + f): {lhs == rhs}")
        assert lhs == rhs

    # 4. Term spread: s(4) - s(1)
    spread_4_1 = spot_rates[4] - spot_rates[1]
    spread_bps = float(spread_4_1) * 10_000
    print("\nTerm Spread:")
    print(f"  4y - 1y Spot Spread = {float(spread_4_1):.4%} = {spread_bps:.2f} bps")


main()
