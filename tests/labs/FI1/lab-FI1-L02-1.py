"""Lab FI1-L02-1: Day-count conventions, accrued interest, and clean and dirty prices.

SIMULATED: synthetic fixed-income security cash flows and date intervals.
Money is in integer cents; day count fractions are rational Fraction instances.
Standard library only; no network.
"""

from __future__ import annotations

import datetime
import math
from fractions import Fraction


def day_count_fraction(start: datetime.date, end: datetime.date, convention: str) -> Fraction:
    """Compute day-count fraction for ACT/360, ACT/365, and 30/360."""
    if convention == "ACT/360":
        return Fraction((end - start).days, 360)
    if convention == "ACT/365":
        return Fraction((end - start).days, 365)
    if convention == "30/360":
        d1 = min(start.day, 30)
        d2 = min(end.day, 30)
        days = 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)
        return Fraction(days, 360)
    raise ValueError(f"Unknown convention: {convention}")


def main() -> None:
    # 1. Day count comparison across date pairs
    d1 = datetime.date(2024, 1, 15)
    d2 = datetime.date(2024, 7, 15)
    actual_days_1 = (d2 - d1).days

    f_act360 = day_count_fraction(d1, d2, "ACT/360")
    f_act365 = day_count_fraction(d1, d2, "ACT/365")
    f_30_360 = day_count_fraction(d1, d2, "30/360")

    print(f"Date Interval 1: {d1} to {d2} (actual days = {actual_days_1}):")
    print(f"  ACT/360 fraction = {f_act360} ({float(f_act360):.6f})")
    print(f"  ACT/365 fraction = {f_act365} ({float(f_act365):.6f})")
    print(f"  30/360 fraction  = {f_30_360} ({float(f_30_360):.6f})")
    print(f"  ACT/365 to ACT/360 ratio check (exact 360/365): {f_act365 / f_act360 == Fraction(360, 365)}")

    # February in leap year 2024
    feb1 = datetime.date(2024, 2, 1)
    mar1 = datetime.date(2024, 3, 1)
    actual_days_feb = (mar1 - feb1).days
    feb_360 = day_count_fraction(feb1, mar1, "ACT/360")
    feb_30_360 = day_count_fraction(feb1, mar1, "30/360")
    print(f"\nDate Interval 2: {feb1} to {mar1} (actual leap days = {actual_days_feb}):")
    print(f"  ACT/360 fraction = {feb_360} ({float(feb_360):.6f})")
    print(f"  30/360 fraction  = {feb_30_360} ({float(feb_30_360):.6f}, exactly 1/12 month)")

    # 2. Accrued interest and dirty price computation
    face_cents = 100_000  # $1,000.00 face value
    clean_price_cents = 98_500  # $985.00 quoted clean price
    annual_coupon_rate = Fraction(6, 100)  # 6.0% annual coupon
    semiannual_coupon_cents = math.floor(Fraction(face_cents) * annual_coupon_rate / 2 + Fraction(1, 2))

    # Assume 45 days accrued into a 180-day semiannual coupon period (30/360)
    accrued_fraction = Fraction(45, 180)
    accrued_interest_cents = math.floor(Fraction(semiannual_coupon_cents) * accrued_fraction + Fraction(1, 2))
    dirty_price_cents = clean_price_cents + accrued_interest_cents

    print("\nAccrued Interest and Invoice Price:")
    print(f"  Face Value        = ${face_cents / 100:.2f}")
    print(f"  Clean Price       = ${clean_price_cents / 100:.2f} ({clean_price_cents} cents)")
    print(f"  Semiannual Coupon = ${semiannual_coupon_cents / 100:.2f} ({semiannual_coupon_cents} cents)")
    print(f"  Accrual Fraction  = {accrued_fraction} (45/180 days)")
    print(f"  Accrued Interest  = ${accrued_interest_cents / 100:.2f} ({accrued_interest_cents} cents)")
    print(f"  Dirty Price       = ${dirty_price_cents / 100:.2f} ({dirty_price_cents} cents)")

    # 3. Yield quote conversion: MMY vs BEY
    # A 180-day money-market instrument with discount yield d = 5.0%
    d_mmy = Fraction(5, 100)
    days_m = 180
    # Price per 100: P = 100 * (1 - d * days / 360)
    price_mmy = 100 * (1 - float(d_mmy) * days_m / 360)
    # MMY (money market yield, ACT/360 simple return): (100 - P)/P * (360/days)
    mmy = ((100.0 - price_mmy) / price_mmy) * (360.0 / days_m)
    # BEY (bond equivalent yield, ACT/365): (100 - P)/P * (365/days)
    bey = ((100.0 - price_mmy) / price_mmy) * (365.0 / days_m)
    print("\nYield Quotation Conversion (180-day paper, discount = 5.00%):")
    print(f"  Price = {price_mmy:.4f} per 100")
    print(f"  MMY (ACT/360) = {mmy:.4%}")
    print(f"  BEY (ACT/365) = {bey:.4%}")
    print(f"  BEY / MMY ratio = {bey / mmy:.6f} (matches 365/360: {365 / 360:.6f})")


main()
