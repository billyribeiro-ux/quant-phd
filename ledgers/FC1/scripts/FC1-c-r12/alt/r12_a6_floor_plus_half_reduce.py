"""Alternative correct solution (round 12): half-away rounding by floor(|x| + 1/2), discounting by a running product."""

from __future__ import annotations

import math
import numbers
from fractions import Fraction
from functools import reduce


def _cents(amount: Fraction) -> int:
    """Nearest whole cent: floor of |amount| + 1/2, sign restored, so an exact half goes away from zero."""
    up = math.floor(abs(amount) + Fraction(1, 2))
    return up if amount >= 0 else -up


def _int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be a whole number")
    return int(value)


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        face = _int(face_cents, "face_cents")
        coupon = _int(coupon_bps, "coupon_bps")
        count = _int(periods, "periods")
        if count < 1:
            raise ValueError("periods must be at least 1")
        if face <= 0:
            raise ValueError("face_cents must be positive")
        if coupon < 0:
            raise ValueError("coupon_bps must not be negative")
        self._face = face
        self._coupon_bps = coupon
        self._periods = count

    def events(self) -> list[tuple[int, int]]:
        coupon = _cents(Fraction(self._face * self._coupon_bps, 10_000))
        rows = [(t, coupon) for t in range(1, self._periods)]
        rows.append((self._periods, coupon + self._face))
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _int(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    base = Fraction(10_000 + rate, 10_000)
    total = Fraction(0)
    for period, amount in bond.events():
        factor = reduce(lambda acc, _: acc / base, range(period), Fraction(1))
        total = total + amount * factor
    return _cents(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        units = _int(quantity, "quantity")
        price = _int(price_cents, "price_cents")
        direction = _int(side, "side")
        day = _int(settlement_day, "settlement_day")
        if units < 1:
            raise ValueError("quantity must be at least 1")
        if price < 0:
            raise ValueError("price_cents must not be negative")
        if direction not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if day < 1:
            raise ValueError("settlement_day must be at least 1")
        self._amount = -direction * units * price
        self._day = day

    def events(self) -> list[tuple[int, int]]:
        return [(self._day, self._amount)]
