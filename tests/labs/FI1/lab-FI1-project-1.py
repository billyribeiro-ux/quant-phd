"""Lab FI1-project-1 (Rung 1, Worked Example): Fully solved bond analytics workflow.

SIMULATED: 10-year Treasury note with 5.0% annual coupon paid semiannually.
Computes dirty price, yield to maturity, duration, convexity, and DV01,
with explicit rationale annotated for each computational step.
Money is in integer cents; standard library only; no network.
"""

from __future__ import annotations

import math
from fractions import Fraction


def compute_dirty_price(face_cents: int, coupon_rate: Fraction, periods: int, y: Fraction) -> int:
    """Step 1: Compute dirty price on a coupon date using exact rational discounting."""
    v = Fraction(1, 1) / (1 + y)
    vn = v**periods
    annuity = (1 - vn) / y if y != 0 else Fraction(periods)
    unrounded = Fraction(face_cents) * (coupon_rate * annuity + vn)
    # Apply standard half-up integer cent rounding once to exact rational value
    return math.floor(unrounded + Fraction(1, 2))


def main() -> None:
    # Problem specification:
    # A $1,000.00 face value note paying 5.0% annual coupon semiannually (20 coupon periods)
    # Market yield is 4.5% annual (2.25% per period).
    # 45 days of interest have accrued under the 30/360 day-count convention.
    face_cents = 100_000  # $1,000.00
    annual_coupon = Fraction(5, 100)
    coupon_rate = annual_coupon / 2  # 2.5% per period = Fraction(25, 1000)
    periods = 20  # 10 years * 2
    annual_yield = Fraction(45, 1000)  # 4.5% annual yield
    yield_per_period = annual_yield / 2  # 2.25% per period

    print("Step 1 · Pricing on Coupon Date:")
    # Why: The dirty price on a coupon date discounts all 20 coupons and principal at periodic yield.
    dirty_on_coupon = compute_dirty_price(face_cents, coupon_rate, periods, yield_per_period)
    print(f"  Dirty price on coupon date = ${dirty_on_coupon / 100:.2f} ({dirty_on_coupon} cents)")

    print("\nStep 2 · Accrued Interest & Clean Price:")
    # Why: In trading, accrued interest compensates the seller for the holding period since last coupon.
    # 30/360 assumption: 45 accrued days out of 180-day semiannual period.
    semiannual_coupon_cents = math.floor(Fraction(face_cents) * coupon_rate + Fraction(1, 2))
    accrual_fraction = Fraction(45, 180)
    accrued_interest_cents = math.floor(Fraction(semiannual_coupon_cents) * accrual_fraction + Fraction(1, 2))
    # Clean price = Dirty price - Accrued interest
    clean_price_cents = dirty_on_coupon - accrued_interest_cents
    print(f"  Semiannual coupon = ${semiannual_coupon_cents / 100:.2f} ({semiannual_coupon_cents} cents)")
    print(f"  Accrued interest  = ${accrued_interest_cents / 100:.2f} ({accrued_interest_cents} cents)")
    print(f"  Clean price quote = ${clean_price_cents / 100:.2f} ({clean_price_cents} cents)")

    print("\nStep 3 · Macaulay & Modified Duration:")
    # Why: Macaulay duration is the weighted average maturity of cash flows; modified duration
    # scales it by (1 + y) to represent the percentage price sensitivity per unit yield change.
    y_float = float(yield_per_period)
    p_float = dirty_on_coupon / 100.0
    c_float = float(coupon_rate * face_cents) / 100.0
    f_float = face_cents / 100.0

    sum_t_cf = sum(k * c_float / ((1.0 + y_float) ** k) for k in range(1, periods + 1))
    sum_t_cf += periods * f_float / ((1.0 + y_float) ** periods)
    d_mac_periods = sum_t_cf / p_float
    d_mac_years = d_mac_periods / 2.0
    d_mod_annual = (d_mac_periods / (1.0 + y_float)) / 2.0
    print(f"  Macaulay Duration = {d_mac_years:.4f} years")
    print(f"  Modified Duration = {d_mod_annual:.4f} years")

    print("\nStep 4 · Convexity & DV01:")
    # Why: DV01 measures dollar exposure per 1 basis point (0.0001) shift in yield,
    # and convexity captures the second-order curvature of the price-yield function.
    sum_t_t1_cf = sum(k * (k + 1) * c_float / ((1.0 + y_float) ** k) for k in range(1, periods + 1))
    sum_t_t1_cf += periods * (periods + 1) * f_float / ((1.0 + y_float) ** periods)
    convexity_periods = sum_t_t1_cf / (p_float * ((1.0 + y_float) ** 2))
    convexity_annual = convexity_periods / 4.0

    dv01 = p_float * d_mod_annual * 0.0001
    print(f"  Annual Convexity  = {convexity_annual:.4f} years^2")
    print(f"  DV01              = ${dv01:.4f} per $1,000 face")


main()
