"""Alternative correct implementation 12 (verifier, round 7): the discount by repeated exact division by (1 + y), the sum in Fraction, and half-away rounding by floor(|x| + 1/2)."""

from __future__ import annotations

import math
from fractions import Fraction


def _cents(x: Fraction) -> int:
    magnitude = math.floor(abs(x) + Fraction(1, 2))
    return magnitude if x >= 0 else -magnitude


def _whole(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a whole number")
    return value


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        self.face_cents = _whole(face_cents, "face_cents")
        self.coupon_bps = _whole(coupon_bps, "coupon_bps")
        self.periods = _whole(periods, "periods")
        if self.periods < 1:
            raise ValueError("periods must be at least 1")
        if self.face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if self.coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")

    def events(self) -> list[tuple[int, int]]:
        coupon = _cents(Fraction(self.face_cents * self.coupon_bps, 10_000))
        rows: list[tuple[int, int]] = []
        for t in range(1, self.periods + 1):
            rows.append((t, coupon))
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    one_plus = Fraction(10_000 + rate, 10_000)
    total = Fraction(0)
    discount = Fraction(1)
    previous = 0
    for period, amount in bond.events():
        for _ in range(period - previous):
            discount = discount / one_plus
        previous = period
        total += amount * discount
    return _cents(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        self.quantity = _whole(quantity, "quantity")
        self.price_cents = _whole(price_cents, "price_cents")
        self.side = _whole(side, "side")
        self.settlement_day = _whole(settlement_day, "settlement_day")
        if self.quantity < 1:
            raise ValueError("quantity must be at least 1")
        if self.price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if self.side not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if self.settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
