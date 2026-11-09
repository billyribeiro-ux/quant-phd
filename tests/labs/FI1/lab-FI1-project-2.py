"""Lab FI1-project-2 (Rung 2, Completion): Accrued interest and DV01 sensitivity calculation.

SIMULATED: the same 10-year Treasury note as the worked example.
Money is in integer cents; standard library only; no network.
Fill in each blank line so that the output matches the expected output.
"""

from __future__ import annotations

import math
from fractions import Fraction


def main() -> None:
    face_cents = 100_000
    coupon_rate = Fraction(25, 1000)
    periods = 20
    yield_per_period = Fraction(45, 2000)

    # Base dirty price
    v = Fraction(1, 1) / (1 + yield_per_period)
    vn = v**periods
    annuity = (1 - vn) / yield_per_period
    unrounded = Fraction(face_cents) * (coupon_rate * annuity + vn)
    dirty_price_cents = math.floor(unrounded + Fraction(1, 2))

    # Accrued interest and clean price (45 days accrued under 30/360)
    semiannual_coupon_cents = math.floor(Fraction(face_cents) * coupon_rate + Fraction(1, 2))
    accrual_fraction = Fraction(45, 180)
    accrued_interest_cents = math.floor(Fraction(semiannual_coupon_cents) * accrual_fraction + Fraction(1, 2))
    clean_price_cents = dirty_price_cents - accrued_interest_cents

    # Duration and DV01
    y_float = float(yield_per_period)
    p_float = dirty_price_cents / 100.0
    c_float = float(coupon_rate * face_cents) / 100.0
    f_float = face_cents / 100.0

    sum_t_cf = sum(k * c_float / ((1.0 + y_float) ** k) for k in range(1, periods + 1))
    sum_t_cf += periods * f_float / ((1.0 + y_float) ** periods)
    d_mac_periods = sum_t_cf / p_float
    d_mod_annual = (d_mac_periods / (1.0 + y_float)) / 2.0

    dv01 = p_float * d_mod_annual * 0.0001

    print(f"Dirty price      = ${dirty_price_cents / 100:.2f} ({dirty_price_cents} cents)")
    print(f"Accrued interest = ${accrued_interest_cents / 100:.2f} ({accrued_interest_cents} cents)")
    print(f"Clean price      = ${clean_price_cents / 100:.2f} ({clean_price_cents} cents)")
    print(f"DV01             = ${dv01:.4f} per $1,000 face")


main()
