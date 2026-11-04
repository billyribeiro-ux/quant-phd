"""Alternative correct implementation 9 (verifier, round 6): a running discount factor multiplied period by period, exact Fractions, floor(x + 1/2) rounding."""

from __future__ import annotations

import math
from fractions import Fraction


def _nearest_cent(x: Fraction) -> int:
    # every amount here is non-negative, so floor(x + 1/2) is the nearest cent with an exact half going up (away from zero)
    return math.floor(x + Fraction(1, 2))


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        for name, value in (("face_cents", face_cents), ("coupon_bps", coupon_bps), ("periods", periods)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be a whole number")
        if periods < 1:
            raise ValueError("periods must be at least 1")
        if face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _nearest_cent(Fraction(self.face_cents * self.coupon_bps, 10000))
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, coupon + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10000:
        raise ValueError("yield_bps must be greater than -10000")
    factor = Fraction(1)
    step = Fraction(10000, 10000 + yield_bps)
    total = Fraction(0)
    previous = 0
    for period, amount in bond.events():
        while previous < period:
            factor *= step
            previous += 1
        total += amount * factor
    return _nearest_cent(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        for name, value in (("quantity", quantity), ("price_cents", price_cents), ("side", side), ("settlement_day", settlement_day)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be a whole number")
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        if price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if side not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity = quantity
        self.price_cents = price_cents
        self.side = side
        self.settlement_day = settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
