"""BK3 Lab L05: Liability-Driven Investment: DV01 matching and the convexity residual.

SIMULATED. Illustrative LDI portfolio parameters, not market data.
Models a defined-benefit pension scheme matching the interest-rate sensitivity (DV01) of its
liabilities using physical bonds and an interest-rate swap derivative overlay.
Solves for the required overlay notional N in closed form:
  N = (DV01_L - DV01_A) / (D_overlay / 10000)
Evaluates the first-order hedge across parallel yield shocks from -200 bps to +200 bps.
Computes the second-order convexity residual:
  Residual = Delta(Assets + Overlay - Liab) - First_Order_Mismatch
and demonstrates that when liability convexity exceeds asset plus overlay convexity, the net surplus
deteriorates symmetrically for both upward and downward yield shifts.
All calculations are exact using fractions.Fraction.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # Pension scheme parameters:
    # Liabilities: L = $100,000,000, Modified Duration D_L = 18.0 years, Convexity C_L = 420
    # Physical Assets: A = $80,000,000, Modified Duration D_A = 7.0 years, Convexity C_A = 75
    # Overlay (Receive-Fixed Swap): Modified Duration D_ov = 20.0 years, Convexity C_ov = 500
    l_val = Fraction(100_000_000, 1)
    d_l = Fraction(18, 1)
    c_l = Fraction(420, 1)

    a_val = Fraction(80_000_000, 1)
    d_a = Fraction(7, 1)
    c_a = Fraction(75, 1)

    d_ov = Fraction(20, 1)
    c_ov = Fraction(500, 1)

    # Dollar duration per basis point (DV01)
    dv01_l = l_val * d_l / Fraction(10_000, 1)
    dv01_a = a_val * d_a / Fraction(10_000, 1)
    dv01_gap = dv01_l - dv01_a

    # Required overlay notional for exact first-order DV01 matching
    # N * (D_ov / 10000) = DV01_gap
    overlay_notional = dv01_gap * Fraction(10_000, 1) / d_ov

    print("=== Liability-Driven Investment: DV01 Hedge Sizing ===")
    print(f"Liability:      Value = ${float(l_val):,.0f} | Duration = {float(d_l):.1f}y | DV01 = ${float(dv01_l):,.2f}")
    print(f"Physical Asset: Value = ${float(a_val):,.0f} | Duration = {float(d_a):.1f}y | DV01 = ${float(dv01_a):,.2f}")
    print(f"Duration Gap:   DV01 Gap = ${float(dv01_gap):,.2f} per basis point")
    print(f"Overlay Swap:   Duration = {float(d_ov):.1f}y | Required Notional = ${float(overlay_notional):,.2f}")

    total_dv01_assets = dv01_a + (overlay_notional * d_ov / Fraction(10_000, 1))
    print(
        f"Post-Hedge Total Asset DV01: ${float(total_dv01_assets):,.2f} (Exact match: {total_dv01_assets == dv01_l})\n"
    )

    # Convexity analysis
    dollar_c_l = l_val * c_l
    dollar_c_a = a_val * c_a
    dollar_c_ov = overlay_notional * c_ov
    total_dollar_c_assets = dollar_c_a + dollar_c_ov
    net_dollar_convexity = total_dollar_c_assets - dollar_c_l

    print("=== Dollar Convexity Breakdown ===")
    print(f"Liability Dollar Convexity:     ${float(dollar_c_l):,.0f}")
    print(f"Physical Asset Dollar Conv:     ${float(dollar_c_a):,.0f}")
    print(f"Overlay Swap Dollar Conv:       ${float(dollar_c_ov):,.0f}")
    print(f"Total Hedged Asset Dollar Conv: ${float(total_dollar_c_assets):,.0f}")
    print(f"Net Dollar Convexity (A - L):   ${float(net_dollar_convexity):,.0f}\n")

    # Shock testing
    test_shocks_bps = [-200, -100, -50, 0, 50, 100, 200]
    print(f"{'Shock (bps)':<12} | {'First-Order Delta':<20} | {'Convexity Term':<18} | {'Total Net Impact':<18}")
    print("-" * 76)

    for shock in test_shocks_bps:
        dy = Fraction(shock, 10_000)
        first_order = -(total_dv01_assets - dv01_l) * Fraction(shock, 1)
        conv_term = Fraction(1, 2) * net_dollar_convexity * (dy**2)
        total_impact = first_order + conv_term
        print(
            f"{shock:+12d} | ${float(first_order):+18,.2f} | "
            f"${float(conv_term):+16,.2f} | ${float(total_impact):+16,.2f}"
        )

    print(
        "\nConvexity residual causes symmetric loss in net funding for rate shocks:",
        net_dollar_convexity < 0,
    )


main()
