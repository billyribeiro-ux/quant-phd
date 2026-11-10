"""BK3 Lab L01: Actuarial Present Value of a level life annuity.

SIMULATED. Illustrative actuarial parameters, not market data.
Computes the actuarial present value (APV) of a level benefit b paid at the end of periods t = 1..n
contingent on survival with constant per-period survival probability p and discount factor v = 1 / (1 + y).
Compares the exact finite sum APV = b * sum_{t=1}^n (p*v)^t with the geometric closed form:
APV = b * p * v * (1 - (p*v)^n) / (1 - p*v) when p*v != 1, and APV = b * n when p*v == 1.
All calculations are exact using fractions.Fraction.
"""

from __future__ import annotations

from fractions import Fraction


def apv_sum(b: int, p: Fraction, v: Fraction, n: int) -> Fraction:
    """Actuarial present value by direct summation."""
    total = Fraction(0, 1)
    pv = p * v
    term = pv
    for _ in range(1, n + 1):
        total += term
        term *= pv
    return b * total


def apv_closed_form(b: int, p: Fraction, v: Fraction, n: int) -> Fraction:
    """Actuarial present value by geometric series closed form."""
    pv = p * v
    if pv == 1:
        return Fraction(b * n, 1)
    return b * pv * (1 - pv**n) / (1 - pv)


def main() -> None:
    cases = [
        # (name, benefit b, survival p, yield y, horizon n)
        ("Cohort A (p=0.96, y=0.04)", 1000, Fraction(96, 100), Fraction(4, 100), 10),
        ("Cohort B (p=0.98, y=0.025)", 2500, Fraction(98, 100), Fraction(25, 1000), 20),
        ("Cohort C edge (p*v == 1)", 500, Fraction(105, 100), Fraction(5, 100), 15),
    ]

    print("=== Actuarial Present Value: Direct Sum vs Closed Form ===")
    for name, b, p, y, n in cases:
        v = Fraction(1, 1) / (Fraction(1, 1) + y)
        sum_val = apv_sum(b, p, v, n)
        cf_val = apv_closed_form(b, p, v, n)
        agree = sum_val == cf_val
        pv = p * v
        print(f"Case: {name}")
        print(f"  Benefit: {b}, Survival p: {p}, Discount factor v: {v} (pv = {pv})")
        print(f"  Finite sum APV:   {float(sum_val):.6f} ({sum_val})")
        print(f"  Closed form APV:  {float(cf_val):.6f} ({cf_val})")
        print(f"  Exact agreement:  {agree}")

    # Monotonicity check: APV increases with p and decreases with y
    b_base = 1000
    n_base = 15
    y_base = Fraction(4, 100)
    v_base = Fraction(1, 1) / (Fraction(1, 1) + y_base)

    p_low = Fraction(92, 100)
    p_high = Fraction(98, 100)
    apv_p_low = apv_closed_form(b_base, p_low, v_base, n_base)
    apv_p_high = apv_closed_form(b_base, p_high, v_base, n_base)
    print("\n=== Monotonicity Checks ===")
    print(f"Survival sensitivity: APV(p=0.92)={float(apv_p_low):.4f} < APV(p=0.98)={float(apv_p_high):.4f}: {apv_p_high > apv_p_low}")

    p_fixed = Fraction(95, 100)
    y_low = Fraction(2, 100)
    y_high = Fraction(6, 100)
    v_low = Fraction(1, 1) / (Fraction(1, 1) + y_low)
    v_high = Fraction(1, 1) / (Fraction(1, 1) + y_high)
    apv_y_low = apv_closed_form(b_base, p_fixed, v_low, n_base)
    apv_y_high = apv_closed_form(b_base, p_fixed, v_high, n_base)
    print(f"Discount sensitivity: APV(y=0.06)={float(apv_y_high):.4f} < APV(y=0.02)={float(apv_y_low):.4f}: {apv_y_low > apv_y_high}")


main()
