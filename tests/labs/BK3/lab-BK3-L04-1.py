"""BK3 Lab L04: Pension funding ratio under discount-rate choices.

SIMULATED. Illustrative pension cash flows and discount rates, not market data.
Computes the defined-benefit pension funding ratio FR = A / L across three discount-rate choices:
  Choice 1: Flat risk-free government bond yield (y_1 = 3.00% per annum).
  Choice 2: Upward-sloping zero-coupon spot curve y_t rising linearly from 2.00% at year 1 to 4.50% at year 20.
  Choice 3: Expected return on plan assets / actuarial discount rate (y_3 = 7.00% per annum).
Evaluates the actuarial liability L = sum_{t=1}^n c_t * (1 + y_t)^(-t) for a 20-year illustrative
benefit payout schedule and verifies the strict monotonic relationship between discount rate and funding ratio.
All calculations are exact using fractions.Fraction and rounded half-up for display.
"""

from __future__ import annotations

import math
from fractions import Fraction


def round_half_up_dec(val: Fraction, places: int) -> float:
    factor = 10**places
    floored: int = int(math.floor(val * factor + Fraction(1, 2)))  # noqa: RUF046
    return float(floored) / float(factor)


def main() -> None:
    # 20 years of illustrative retirement benefit obligations (in dollars)
    cash_flows = [
        Fraction(500_000, 1),
        Fraction(550_000, 1),
        Fraction(600_000, 1),
        Fraction(650_000, 1),
        Fraction(700_000, 1),
        Fraction(750_000, 1),
        Fraction(800_000, 1),
        Fraction(850_000, 1),
        Fraction(900_000, 1),
        Fraction(950_000, 1),
        Fraction(1_000_000, 1),
        Fraction(950_000, 1),
        Fraction(900_000, 1),
        Fraction(850_000, 1),
        Fraction(800_000, 1),
        Fraction(750_000, 1),
        Fraction(700_000, 1),
        Fraction(650_000, 1),
        Fraction(600_000, 1),
        Fraction(550_000, 1),
    ]
    n = len(cash_flows)
    total_undiscounted = sum(cash_flows)

    # Plan assets (fixed at $10,000,000)
    assets = Fraction(10_000_000, 1)

    # Choice 1: Flat risk-free rate 3.0%
    y_flat_rf = Fraction(3, 100)
    liab_flat_rf = sum(cf / ((Fraction(1, 1) + y_flat_rf) ** t) for t, cf in enumerate(cash_flows, start=1))
    fr_flat_rf = assets / liab_flat_rf

    # Choice 2: Spot curve: y_t = 0.02 + 0.025 * (t - 1) / 19  (from 2.0% to 4.5%)
    spot_rates = [Fraction(2, 100) + Fraction(25, 1000) * Fraction(t - 1, 19) for t in range(1, n + 1)]
    liab_spot = sum(
        cf / ((Fraction(1, 1) + y_t) ** t)
        for t, (cf, y_t) in enumerate(zip(cash_flows, spot_rates, strict=False), start=1)
    )
    fr_spot = assets / liab_spot

    # Choice 3: Actuarial expected return on assets 7.0%
    y_actuarial = Fraction(7, 100)
    liab_actuarial = sum(cf / ((Fraction(1, 1) + y_actuarial) ** t) for t, cf in enumerate(cash_flows, start=1))
    fr_actuarial = assets / liab_actuarial

    print("=== Pension Funding Ratio Under Alternative Discount-Rate Choices ===")
    print(f"Total Undiscounted Promised Cash Flows (20 years): ${float(total_undiscounted):,.2f}")
    print(f"Fixed Pension Plan Assets:                         ${float(assets):,.2f}\n")

    print(f"{'Discount Rate Choice':<35} | {'Liability ($)':<16} | {'Funding Ratio':<14} | {'Surplus / (Deficit)'}")
    print("-" * 88)

    choices = [
        ("Choice 1: Flat Risk-Free (3.00%)", liab_flat_rf, fr_flat_rf),
        ("Choice 2: Spot Curve (2.00% - 4.50%)", liab_spot, fr_spot),
        ("Choice 3: Assumed Asset Return (7.00%)", liab_actuarial, fr_actuarial),
    ]

    for label, liab, fr in choices:
        surplus = assets - liab
        fr_rounded = round_half_up_dec(fr, 4)
        print(f"{label:<35} | ${float(liab):14,.2f} | {fr_rounded:12.4f} ({float(fr):.2%}) | ${float(surplus):+13,.2f}")

    print("\n=== Mathematical Monotonicity Checks ===")
    monotone_l = liab_flat_rf > liab_spot > liab_actuarial
    print(f"Liability decreases with discount rate: L(3.0%) > L(Spot) > L(7.0%): {monotone_l}")
    monotone_fr = fr_flat_rf < fr_spot < fr_actuarial
    print(f"Funding ratio strictly increases with discount rate: FR(3.0%) < FR(Spot) < FR(7.0%): {monotone_fr}")
    deficit_to_surplus = (assets < liab_flat_rf) and (assets > liab_actuarial)
    print(f"Plan appears underfunded under risk-free rate but overfunded under expected return: {deficit_to_surplus}")


main()
