"""Project Lab 1 (Rung 1): Fully worked example of cross-currency basis calculation.

SIMULATED single-day quote row. Standard library only.
Computes the implied dollar borrowing rate, cross-currency basis in basis points,
and evaluates regulatory quarter-end status step-by-step.
"""

from fractions import Fraction


def main() -> None:
    # 1. Market input quote row (EUR/USD 3-month contract on 2024-03-29)
    date_iso = "2024-03-29"
    spot = 1.0850  # USD per EUR
    forward = 1.0815  # USD per EUR
    usd_rate = 0.0535  # 5.35% annual cash USD rate (SOFR)
    foreign_rate = 0.0385  # 3.85% annual foreign interbank rate (EURIBOR)
    days_usd = 90
    days_foreign = 90
    basis_daycount = 360

    # 2. Accrual fractions (Actual/360 convention on both legs)
    tau_usd = days_usd / basis_daycount  # 0.25
    tau_foreign = days_foreign / basis_daycount  # 0.25

    # 3. Step 1: Foreign leg gross accumulation factor
    foreign_accrual = 1.0 + foreign_rate * tau_foreign  # 1 + 0.0385 * 0.25 = 1.009625

    # 4. Step 2: FX swap conversion factor (Spot / Forward)
    fx_conversion = spot / forward  # 1.0850 / 1.0815 = 1.0032362...

    # 5. Step 3: Implied gross dollar factor
    gross_implied_usd = fx_conversion * foreign_accrual  # 1.0128926...

    # 6. Step 4: Implied annual simple dollar rate
    implied_usd = (gross_implied_usd - 1.0) / tau_usd  # 0.0515707... (5.157%)

    # 7. Step 5: Cross-currency basis in basis points
    # Convention: basis = (usd_rate - implied_usd) * 10,000
    basis_bp = (usd_rate - implied_usd) * 10000.0  # +19.29 bp

    # 8. Step 6: Quarter-end identification
    # March 31 2024 was Sunday -> last business weekday was Friday March 29, 2024
    _year, month, day = (int(x) for x in date_iso.split("-"))
    # In March (month 3), last weekday is 29
    is_qe = month == 3 and day == 29

    print("=== Rung 1: Worked Example Cross-Currency Basis ===")
    print(f"Date:                       {date_iso} (Quarter-End: {is_qe})")
    print(f"Spot Rate (S):              {spot:.4f} USD per EUR")
    print(f"Forward Rate (F):           {forward:.4f} USD per EUR")
    print(f"Cash USD Rate (i_usd):      {usd_rate * 100:.2f}%")
    print(f"Cash EUR Rate (i_foreign):  {foreign_rate * 100:.2f}%")
    print(f"Foreign Accrual Factor:     {foreign_accrual:.6f}")
    print(f"FX Conversion (S / F):      {fx_conversion:.6f}")
    print(f"Implied USD Borrowing Rate: {implied_usd * 100:.3f}%")
    print(f"Cross-Currency Basis:       {basis_bp:+.2f} bp")

    # Exact Fraction check for identity verification
    tau_frac = Fraction(90, 360)
    implied_frac = (Fraction(1, 1) / tau_frac) * (
        (Fraction(10850, 10000) / Fraction(10815, 10000)) * (Fraction(1, 1) + Fraction(385, 10000) * tau_frac)
        - Fraction(1, 1)
    )
    basis_frac_bp = (Fraction(535, 10000) - implied_frac) * Fraction(10000, 1)
    print(f"\nExact Fraction Basis:       {float(basis_frac_bp):.4f} bp")

    assert is_qe is True, "2024-03-29 must be flagged as quarter end"
    assert abs(basis_bp - float(basis_frac_bp)) < 1e-6, "Float and Fraction must match"


main()
