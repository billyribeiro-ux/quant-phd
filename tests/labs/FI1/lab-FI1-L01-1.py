"""Lab FI1-L01-1: Bond price-yield relation and yield to maturity by bisection.

SIMULATED: fixed-coupon bond cash flows on a synthetic grid. Money is in integer cents;
yields are rational fractions or floats. Standard library only; no network.
"""

from __future__ import annotations

import math
from fractions import Fraction


def compute_unrounded_price(face_cents: int, coupon_rate: Fraction, periods: int, y: Fraction) -> Fraction:
    """Compute exact rational dirty price of a coupon bond on a coupon date."""
    if y == 0:
        return Fraction(face_cents) * (1 + coupon_rate * periods)
    v = Fraction(1, 1) / (1 + y)
    vn = v**periods
    annuity = (1 - vn) / y
    return Fraction(face_cents) * (coupon_rate * annuity + vn)


def solve_ytm(dirty_cents: int, face_cents: int, coupon_rate: Fraction, periods: int) -> Fraction:
    """Solve for yield to maturity per period using bisection."""
    low = Fraction(-1, 2)
    while compute_unrounded_price(face_cents, coupon_rate, periods, low) < dirty_cents:
        low = Fraction(low - 1, 2)

    high = Fraction(1, 1)
    while compute_unrounded_price(face_cents, coupon_rate, periods, high) > dirty_cents:
        high = high * 2

    tol = Fraction(1, 2)  # half cent tolerance
    target = Fraction(dirty_cents, 1)
    for _ in range(200):
        mid = (low + high) / 2
        p_mid = compute_unrounded_price(face_cents, coupon_rate, periods, mid)
        if abs(p_mid - target) < tol:
            return mid
        if p_mid > target:
            low = mid
        else:
            high = mid
    raise ValueError("Bisection did not converge")


def main() -> None:
    face_cents = 100_000  # $1,000.00 face value
    coupon_rate = Fraction(5, 100)  # 5.0% coupon per period
    periods = 20  # 20 periods

    yield_grid = [
        Fraction(1, 100),
        Fraction(3, 100),
        Fraction(5, 100),
        Fraction(7, 100),
        Fraction(9, 100),
    ]

    print("Yield Grid Pricing (face = $1000.00, coupon = 5.0%, periods = 20):")
    prices_cents: list[int] = []
    for y in yield_grid:
        unrounded = compute_unrounded_price(face_cents, coupon_rate, periods, y)
        price_cents = math.floor(unrounded + Fraction(1, 2))
        prices_cents.append(price_cents)
        print(f"  y = {float(y):.2%}: price = ${price_cents / 100:.2f} ({price_cents} cents)")

    # Verify strict monotonicity
    is_decreasing = all(prices_cents[i] > prices_cents[i + 1] for i in range(len(prices_cents) - 1))
    print(f"Monotonicity verified (price strictly falls as yield rises): {is_decreasing}")

    # Solve YTM for target price $1050.00 (105,000 cents)
    target_price = 105_000
    solved_ytm = solve_ytm(target_price, face_cents, coupon_rate, periods)
    repriced_unrounded = compute_unrounded_price(face_cents, coupon_rate, periods, solved_ytm)
    repriced_cents = math.floor(repriced_unrounded + Fraction(1, 2))
    residual_cents = repriced_cents - target_price

    print(f"YTM for target ${target_price / 100:.2f}:")
    print(f"  Solved YTM = {float(solved_ytm):.6%}")
    print(f"  Repriced price = ${repriced_cents / 100:.2f} ({repriced_cents} cents)")
    print(f"  Residual = {residual_cents} cents (|error| < 0.5 cents)")


main()
