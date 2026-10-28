"""Alternative correct implementation 2: class-based, with events() as a generator wrapped in list()."""

from __future__ import annotations

from collections.abc import Iterator
from fractions import Fraction


def _round(x: Fraction) -> int:
    sign = -1 if x < 0 else 1
    mag = abs(x)
    return sign * int(mag + Fraction(1, 2))


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        for name, v in (("face_cents", face_cents), ("coupon_bps", coupon_bps), ("periods", periods)):
            if isinstance(v, bool) or not isinstance(v, int):
                raise ValueError(f"{name} must be a whole number")
        if periods < 1:
            raise ValueError("periods must be at least 1")
        if face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self._face = face_cents
        self._bps = coupon_bps
        self._n = periods

    def _coupons(self) -> Iterator[tuple[int, int]]:
        coupon = _round(Fraction(self._face * self._bps, 10_000))
        for t in range(1, self._n + 1):
            yield t, coupon + (self._face if t == self._n else 0)

    def events(self) -> list[tuple[int, int]]:
        return list(self._coupons())


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    y = Fraction(yield_bps, 10_000)
    exact = Fraction(0)
    for period, amount in bond.events():
        exact += amount * (1 + y) ** (-period)
    return _round(exact)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        for name, v in (
            ("quantity", quantity),
            ("price_cents", price_cents),
            ("side", side),
            ("settlement_day", settlement_day),
        ):
            if isinstance(v, bool) or not isinstance(v, int):
                raise ValueError(f"{name} must be a whole number")
        if quantity < 1 or price_cents < 0 or side not in (1, -1) or settlement_day < 1:
            raise ValueError("quantity, price_cents, side or settlement_day outside its allowed range")
        self._q, self._p, self._s, self._d = quantity, price_cents, side, settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self._d, -self._s * self._q * self._p)]
