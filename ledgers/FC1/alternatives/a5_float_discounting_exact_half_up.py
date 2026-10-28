"""Alternative correct implementation 5: float discount factors, then one half-up rounding of the float total."""

from __future__ import annotations

import math


def _half_up(x: float) -> int:
    return math.floor(x + 0.5) if x >= 0 else -math.floor(-x + 0.5)


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
        coupon = _half_up(self.face_cents * self.coupon_bps / 10_000)
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, coupon + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    v = 1.0 + yield_bps / 10_000
    total = 0.0
    for t, amount in bond.events():
        total += amount / v**t
    return _half_up(total)


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
        self.quantity, self.price_cents, self.side, self.settlement_day = quantity, price_cents, side, settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
