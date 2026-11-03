"""Verifier alternative (round 3, FC1-c), plan item (5) as a float implementation: float discount factors, one half-up rounding of the float sum."""

from __future__ import annotations

import math


def _half_up(x: float) -> int:
    """Nearest whole cent of a float, halves toward +infinity for positive values, away from zero for negative."""
    return math.floor(x + 0.5) if x >= 0 else -math.floor(-x + 0.5)


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if isinstance(periods, bool) or not isinstance(periods, int) or periods < 1:
            raise ValueError("periods must be at least 1")
        if face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _half_up(self.face_cents * self.coupon_bps / 10_000)
        out = [(t, coupon) for t in range(1, self.periods + 1)]
        out[-1] = (self.periods, out[-1][1] + self.face_cents)
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    y = yield_bps / 10_000
    total = 0.0
    for period, amount in bond.events():
        total += amount / (1 + y) ** period
    return _half_up(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        if price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if side not in (1, -1):
            raise ValueError("side must be +1 (buy) or -1 (sell)")
        if settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity = quantity
        self.price_cents = price_cents
        self.side = side
        self.settlement_day = settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
