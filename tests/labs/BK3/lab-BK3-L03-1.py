"""BK3 Lab L03: Insurance capital regulation and balance sheet sensitivity under yield shocks.

SIMULATED. Illustrative balance sheet parameters, not market data.
Models the solvency capital ratio kappa = K_c / L = (A - L) / L of an insurer subject to a regulatory
minimum capital ratio kappa_min.
Under a parallel yield shock of s basis points, first-order asset and liability values shift by:
  A(s) = A_0 * (1 - D_A * s / 10000)
  L(s) = L_0 * (1 - D_L * s / 10000)
  K_c(s) = A(s) - L(s)
Derives the critical threshold shock s* where the capital ratio binds at kappa_min in closed form:
  s* = 10000 * (A_0 - (1 + kappa_min) * L_0) / (A_0 * D_A - (1 + kappa_min) * L_0 * D_L)
and compares it with an exhaustive discrete search over integer basis points.
All calculations are exact using fractions.Fraction.
"""

from __future__ import annotations

import math
from fractions import Fraction


def asset_val(a0: Fraction, d_a: Fraction, s_bps: int) -> Fraction:
    return a0 * (Fraction(1, 1) - d_a * Fraction(s_bps, 10_000))


def liab_val(l0: Fraction, d_l: Fraction, s_bps: int) -> Fraction:
    return l0 * (Fraction(1, 1) - d_l * Fraction(s_bps, 10_000))


def capital_val(a0: Fraction, d_a: Fraction, l0: Fraction, d_l: Fraction, s_bps: int) -> Fraction:
    return asset_val(a0, d_a, s_bps) - liab_val(l0, d_l, s_bps)


def capital_ratio(a0: Fraction, d_a: Fraction, l0: Fraction, d_l: Fraction, s_bps: int) -> Fraction:
    l_s = liab_val(l0, d_l, s_bps)
    k_s = capital_val(a0, d_a, l0, d_l, s_bps)
    return k_s / l_s


def threshold_shock_closed_form(
    a0: Fraction, d_a: Fraction, l0: Fraction, d_l: Fraction, kappa_min: Fraction
) -> Fraction:
    num = a0 - (Fraction(1, 1) + kappa_min) * l0
    den = a0 * d_a - (Fraction(1, 1) + kappa_min) * l0 * d_l
    return Fraction(10_000, 1) * num / den


def main() -> None:
    # Insurer baseline parameters:
    # Assets A_0 = $1,200,000,000, Duration D_A = 7.50 years
    # Liabilities L_0 = $1,000,000,000, Duration D_L = 12.00 years
    # Initial Capital K_c,0 = $200,000,000, initial ratio = 20.00%
    # Regulatory minimum capital ratio kappa_min = 10.00%
    a0 = Fraction(1_200_000_000, 1)
    d_a = Fraction(75, 10)  # 7.5 years
    l0 = Fraction(1_000_000_000, 1)
    d_l = Fraction(12, 1)  # 12.0 years
    kappa_min = Fraction(10, 100)  # 10% minimum

    print("=== Insurer Balance Sheet Capital Sensitivity ===")
    print(f"Initial Assets: ${float(a0):,.0f} (D_A = {float(d_a):.2f}y)")
    print(f"Initial Liabilities: ${float(l0):,.0f} (D_L = {float(d_l):.2f}y)")
    print(f"Initial Capital: ${float(a0 - l0):,.0f} (Initial Ratio: {float((a0 - l0) / l0):.4%})")
    print(f"Regulatory Minimum Ratio: {float(kappa_min):.2%}")

    # Shocks table
    test_shocks = [-200, -100, 0, 100, 200, 300]
    print("\nParallel Shock (bps) | Assets ($M) | Liab ($M) | Capital ($M) | Ratio (%) | Identity Check")
    print("-" * 80)
    for s in test_shocks:
        a_s = asset_val(a0, d_a, s)
        l_s = liab_val(l0, d_l, s)
        k_s = capital_val(a0, d_a, l0, d_l, s)
        ratio = capital_ratio(a0, d_a, l0, d_l, s)
        ident = a_s == l_s + k_s
        print(
            f"{s:+19d} | {float(a_s) / 1e6:11.3f} | {float(l_s) / 1e6:9.3f} | "
            f"{float(k_s) / 1e6:12.3f} | {float(ratio):9.2%} | {ident}"
        )

    # Closed-form threshold shock
    s_star = threshold_shock_closed_form(a0, d_a, l0, d_l, kappa_min)
    print(f"\nExact Closed-Form Regulatory Threshold Shock: {float(s_star):.4f} bps ({s_star})")

    # Verification: at s_star, ratio equals kappa_min exactly
    a_star = a0 * (Fraction(1, 1) - d_a * s_star / Fraction(10_000, 1))
    l_star = l0 * (Fraction(1, 1) - d_l * s_star / Fraction(10_000, 1))
    k_star = a_star - l_star
    ratio_star = k_star / l_star
    print(f"Capital Ratio exactly at s*: {float(ratio_star):.6%} (Matches kappa_min: {ratio_star == kappa_min})")

    # Discrete integer search
    int_shock_bound = math.ceil(float(s_star))
    ratio_below = capital_ratio(a0, d_a, l0, d_l, int_shock_bound - 1)
    ratio_at_bound = capital_ratio(a0, d_a, l0, d_l, int_shock_bound)
    print(
        f"Discrete check: s={int_shock_bound - 1} bps gives ratio "
        f"{float(ratio_below):.4%} >= 10%: {ratio_below >= kappa_min}"
    )
    print(
        f"Discrete check: s={int_shock_bound} bps gives ratio "
        f"{float(ratio_at_bound):.4%} < 10%: {ratio_at_bound < kappa_min}"
    )


main()
