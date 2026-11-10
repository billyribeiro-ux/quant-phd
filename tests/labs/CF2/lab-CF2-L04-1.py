"""CF2 lab L04-1: Modigliani-Miller propositions without corporate taxes.

Model: Exact closed-form capital structure calculations using fractions.Fraction.
No synthetic or simulated data is used; all quantities are exact rational numbers.
Demonstrates:
  Proposition I: Firm enterprise value V_L = V_U is invariant to leverage.
  Proposition II: Cost of equity r_E is strictly increasing and linear in D/E.
  Overall WACC remains constant and equal to the unlevered cost of capital r_A.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    print("CF2 Lab L04-1: Modigliani-Miller Propositions Without Taxes")
    print("---------------------------------------------------------")

    # Stated firm parameters
    ebit = Fraction(10_000_000, 1)  # $10M annual perpetual operating income
    r_a = Fraction(10, 100)  # 10% unlevered cost of capital
    r_d = Fraction(5, 100)  # 5% cost of debt (risk-free debt assumption)

    v_u = ebit / r_a
    print(f"Perpetual operating cash flow (EBIT): ${ebit:,.2f}")
    print(f"Unlevered cost of capital (r_A):       {r_a} = {float(r_a):.2%}")
    print(f"Pre-tax cost of debt (r_D):             {r_d} = {float(r_d):.2%}")
    print(f"Proposition I unlevered value (V_U):   ${v_u:,.2f}")

    print("\nLeverage Grid (Proposition I & II across D/E ratios):")
    print(
        f"{'D/E':>6} | {'Debt ($M)':>10} | {'Equity ($M)':>11} | {'Value ($M)':>10} | {'r_E (%)':>8} | {'WACC (%)':>8}"
    )
    print("-" * 65)

    de_ratios = [
        Fraction(0, 1),
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(1, 1),
        Fraction(3, 2),
        Fraction(2, 1),
        Fraction(4, 1),
    ]

    for de in de_ratios:
        # V = D + E = V_U
        # D/E = de => D = de * E => E * (1 + de) = V_U => E = V_U / (1 + de)
        e_val = v_u / (Fraction(1, 1) + de)
        d_val = v_u - e_val
        v_l = d_val + e_val

        # Proposition II: r_E = r_A + (r_A - r_D) * (D / E)
        r_e = r_a + (r_a - r_d) * de

        # WACC = (E/V)*r_E + (D/V)*r_D
        w_e = e_val / v_l
        w_d = d_val / v_l
        r_wacc = w_e * r_e + w_d * r_d

        d_m = float(d_val) / 1_000_000
        e_m = float(e_val) / 1_000_000
        v_m = float(v_l) / 1_000_000

        print(
            f"{float(de):6.2f} | {d_m:10.2f} | {e_m:11.2f} | {v_m:10.2f} | "
            f"{float(r_e) * 100:8.2f} | {float(r_wacc) * 100:8.2f}"
        )

        assert v_l == v_u, f"Proposition I violated at D/E = {de}"
        assert r_wacc == r_a, f"WACC invariance violated at D/E = {de}"

    print("-" * 65)
    print("Numerical confirmation: Across all leverage levels, V_L == V_U and WACC == r_A.")


main()
