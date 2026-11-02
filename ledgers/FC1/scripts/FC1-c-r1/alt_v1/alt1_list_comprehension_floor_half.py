"""Alternative correct implementation 1 (FC1-c round 1): list-comprehension events; half-up by floor(x + 1/2) on the magnitude."""

from __future__ import annotations

import math
from fractions import Fraction


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _cents(x: Fraction) -> int:
    magnitude = abs(x)
    rounded = math.floor(magnitude + Fraction(1, 2))
    return rounded if x >= 0 else -rounded


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if not _is_int(periods) or periods < 1:
            raise ValueError("periods must be at least 1")
        if not _is_int(face_cents) or face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if not _is_int(coupon_bps) or coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _cents(Fraction(self.face_cents * self.coupon_bps, 10_000))
        return [(t, coupon + (self.face_cents if t == self.periods else 0)) for t in range(1, self.periods + 1)]


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if not _is_int(yield_bps) or yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    y = Fraction(yield_bps, 10_000)
    return _cents(sum((Fraction(a) / (1 + y) ** t for t, a in bond.events()), Fraction(0)))


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        if not _is_int(quantity) or quantity < 1:
            raise ValueError("quantity must be at least 1")
        if not _is_int(price_cents) or price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if not _is_int(side) or side not in (1, -1):
            raise ValueError("side must be +1 (buy) or -1 (sell)")
        if not _is_int(settlement_day) or settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity = quantity
        self.price_cents = price_cents
        self.side = side
        self.settlement_day = settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
