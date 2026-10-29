"""Alternative 3 (verifier, round 2): Fraction throughout; one final half-up rounding by floor(x + 1/2) on the magnitude."""

from __future__ import annotations

import math
from fractions import Fraction


def _cents(x: Fraction) -> int:
    magnitude = math.floor(abs(x) + Fraction(1, 2))
    return magnitude if x >= 0 else -magnitude


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
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
        coupon = _cents(Fraction(self.face_cents * self.coupon_bps, 10_000))
        return [(t, coupon + (self.face_cents if t == self.periods else 0)) for t in range(1, self.periods + 1)]


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be above -10000 so that 1 + y is positive")
    y = Fraction(yield_bps, 10_000)
    exact = sum((Fraction(a) * (1 + y) ** (-t) for t, a in bond.events()), Fraction(0))
    return _cents(exact)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
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
