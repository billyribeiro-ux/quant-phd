"""Alternative correct implementation 5: frozen dataclasses, the price folded with functools.reduce."""

from __future__ import annotations

import functools
from dataclasses import dataclass
from fractions import Fraction


def _cents(x: Fraction) -> int:
    """The nearest whole cent, an exact half going away from zero."""
    sign = -1 if x < 0 else 1
    magnitude = abs(x)
    return sign * ((2 * magnitude.numerator + magnitude.denominator) // (2 * magnitude.denominator))


def _must_be_whole(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a whole number")
    return value


@dataclass(frozen=True)
class Bond:
    face_cents: int
    coupon_bps: int
    periods: int

    def __post_init__(self) -> None:
        _must_be_whole(self.face_cents, "face_cents")
        _must_be_whole(self.coupon_bps, "coupon_bps")
        _must_be_whole(self.periods, "periods")
        if self.periods < 1:
            raise ValueError("periods must be at least 1")
        if self.face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if self.coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")

    def events(self) -> list[tuple[int, int]]:
        coupon = _cents(Fraction(self.face_cents * self.coupon_bps, 10_000))
        amounts = [coupon] * self.periods
        amounts[-1] += self.face_cents
        return list(enumerate(amounts, start=1))


def _discounted(event: tuple[int, int], rate: Fraction) -> Fraction:
    period, amount = event
    return Fraction(amount) / (1 + rate) ** period


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    _must_be_whole(yield_bps, "yield_bps")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    rate = Fraction(yield_bps, 10_000)
    exact = functools.reduce(lambda acc, ev: acc + _discounted(ev, rate), bond.events(), Fraction(0))
    return _cents(exact)


@dataclass(frozen=True)
class CashTrade:
    quantity: int
    price_cents: int
    side: int
    settlement_day: int

    def __post_init__(self) -> None:
        _must_be_whole(self.quantity, "quantity")
        _must_be_whole(self.price_cents, "price_cents")
        _must_be_whole(self.side, "side")
        _must_be_whole(self.settlement_day, "settlement_day")
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
