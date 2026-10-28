"""Verifier alternative 7: discount factor as Fraction power of the inverse, a manual half-away rounding with floor, events as tuples."""
from __future__ import annotations

from fractions import Fraction
import math


def _round_half_away(x: Fraction) -> int:
    a = abs(x)
    r = math.floor(a + Fraction(1, 2))
    return r if x >= 0 else -r


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if isinstance(face_cents, bool) or not isinstance(face_cents, int) or face_cents <= 0:
            raise ValueError("face_cents must be a positive whole number")
        if isinstance(coupon_bps, bool) or not isinstance(coupon_bps, int) or coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        if isinstance(periods, bool) or not isinstance(periods, int) or periods < 1:
            raise ValueError("periods must be at least 1")
        self._face = face_cents
        self._rate = coupon_bps
        self._n = periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _round_half_away(Fraction(self._face * self._rate, 10000))
        out = [(t, coupon) for t in range(1, self._n + 1)]
        out[-1] = (out[-1][0], out[-1][1] + self._face)
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10000:
        raise ValueError("yield_bps must exceed -10000")
    growth = Fraction(10000 + yield_bps, 10000)
    total = Fraction(0)
    for t, amount in bond.events():
        total += Fraction(amount) * (1 / growth) ** t
    return _round_half_away(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        for name, value in (("quantity", quantity), ("price_cents", price_cents), ("settlement_day", settlement_day)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be a whole number")
        if isinstance(side, bool) or side not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        if price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self._q, self._p, self._s, self._d = quantity, price_cents, side, settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self._d, -self._s * self._q * self._p)]
