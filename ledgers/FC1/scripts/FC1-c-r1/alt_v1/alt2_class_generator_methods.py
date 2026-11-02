"""Alternative correct implementation 2 (FC1-c round 1): class-based; events() built from a generator method; half-up by Fraction."""

from __future__ import annotations

import numbers
from collections.abc import Iterator
from fractions import Fraction


def _round_half_up_magnitude(x: Fraction) -> int:
    numerator, denominator = abs(x).numerator, abs(x).denominator
    rounded = (2 * numerator + denominator) // (2 * denominator)
    return rounded if x >= 0 else -rounded


def _whole(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be a whole number")
    return int(value)


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        self._face = _whole(face_cents, "face_cents")
        self._coupon_bps = _whole(coupon_bps, "coupon_bps")
        self._periods = _whole(periods, "periods")
        if self._periods < 1:
            raise ValueError("periods must be at least 1")
        if self._face <= 0:
            raise ValueError("face_cents must be positive")
        if self._coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")

    def _coupon(self) -> int:
        return _round_half_up_magnitude(Fraction(self._face * self._coupon_bps, 10_000))

    def _pairs(self) -> Iterator[tuple[int, int]]:
        coupon = self._coupon()
        for period in range(1, self._periods + 1):
            yield period, coupon + self._face if period == self._periods else coupon

    @property
    def periods(self) -> int:
        return self._periods

    @property
    def face(self) -> int:
        return self._face

    def events(self) -> list[tuple[int, int]]:
        return list(self._pairs())


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    growth = Fraction(10_000 + rate, 10_000)
    total = Fraction(0)
    for period, amount in bond.events():
        total += Fraction(amount) / growth**period
    return _round_half_up_magnitude(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        self._quantity = _whole(quantity, "quantity")
        self._price = _whole(price_cents, "price_cents")
        self._side = _whole(side, "side")
        self._day = _whole(settlement_day, "settlement_day")
        if self._quantity < 1:
            raise ValueError("quantity must be at least 1")
        if self._price < 0:
            raise ValueError("price_cents must not be negative")
        if self._side not in (1, -1):
            raise ValueError("side must be +1 (buy) or -1 (sell)")
        if self._day < 1:
            raise ValueError("settlement_day must be at least 1")

    def _settle(self) -> Iterator[tuple[int, int]]:
        yield self._day, -self._side * self._quantity * self._price

    def events(self) -> list[tuple[int, int]]:
        return list(self._settle())
