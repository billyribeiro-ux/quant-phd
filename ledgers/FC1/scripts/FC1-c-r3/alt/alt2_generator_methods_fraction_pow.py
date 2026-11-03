"""Alternative 2 (verifier, round 2): generator helper for the bond schedule; discount factor as a Fraction power of the inverse growth."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterator


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if periods < 1:
            raise ValueError("periods must be at least 1")
        if face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self._face = face_cents
        self._bps = coupon_bps
        self._n = periods

    def _pairs(self) -> Iterator[tuple[int, int]]:
        coupon_exact = Fraction(self._face * self._bps, 10_000)
        coupon = int(coupon_exact) if coupon_exact.denominator == 1 else int(coupon_exact + Fraction(1, 2))
        for t in range(1, self._n + 1):
            yield t, coupon + (self._face if t == self._n else 0)

    def events(self) -> list[tuple[int, int]]:
        return list(self._pairs())


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be above -10000 so that 1 + y is positive")
    growth = 1 + Fraction(yield_bps, 10_000)
    total = sum((Fraction(amount) * (1 / growth) ** t for t, amount in bond.events()), Fraction(0))
    whole = total.numerator // total.denominator
    frac = total - whole
    return whole + 1 if frac >= Fraction(1, 2) else whole


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
        self._q, self._p, self._s, self._d = quantity, price_cents, side, settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self._d, -self._s * self._q * self._p)]
