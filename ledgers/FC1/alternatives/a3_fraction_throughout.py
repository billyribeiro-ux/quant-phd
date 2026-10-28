"""Alternative correct implementation 3: exact Fraction arithmetic throughout, one half-up rounding per output."""

from __future__ import annotations

import math
from fractions import Fraction


def _cents(x: Fraction) -> int:
    if x < 0:
        return -math.floor(-x + Fraction(1, 2))
    return math.floor(x + Fraction(1, 2))


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if isinstance(periods, bool) or not isinstance(periods, int) or periods < 1:
            raise ValueError("periods must be at least 1")
        if isinstance(face_cents, bool) or not isinstance(face_cents, int) or face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if isinstance(coupon_bps, bool) or not isinstance(coupon_bps, int) or coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _cents(Fraction(self.face_cents) * self.coupon_bps / 10_000)
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    v = 1 + Fraction(yield_bps) / 10_000
    value = Fraction(0)
    for t, amount in bond.events():
        value += Fraction(amount) * v ** (-t)
    return _cents(value)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise ValueError("quantity must be at least 1")
        if isinstance(price_cents, bool) or not isinstance(price_cents, int) or price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if isinstance(side, bool) or side not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if isinstance(settlement_day, bool) or not isinstance(settlement_day, int) or settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity = quantity
        self.price_cents = price_cents
        self.side = side
        self.settlement_day = settlement_day

    def events(self) -> list[tuple[int, int]]:
        amount = Fraction(-self.side * self.quantity * self.price_cents)
        return [(self.settlement_day, _cents(amount))]
