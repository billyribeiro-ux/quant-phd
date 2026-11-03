"""Student error: bond_price_cents sums the discounted events in a Decimal context of ten significant digits, so a large price loses cents before the final rounding."""

from __future__ import annotations

import numbers
from decimal import ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction

def _half_away(amount: Fraction) -> int:
    magnitude = abs(amount)
    rounded = (2 * magnitude.numerator + magnitude.denominator) // (2 * magnitude.denominator)
    return rounded if amount >= 0 else -rounded


def _whole(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be a whole number, not {value!r}")
    return int(value)


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        face = _whole(face_cents, "face_cents")
        coupon = _whole(coupon_bps, "coupon_bps")
        count = _whole(periods, "periods")
        if count < 1:
            raise ValueError("periods must be at least 1")
        if face <= 0:
            raise ValueError("face_cents must be positive")
        if coupon < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face
        self.coupon_bps = coupon
        self.periods = count

    def events(self) -> list[tuple[int, int]]:
        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))
        out = [(t, coupon) for t in range(1, self.periods + 1)]
        out[-1] = (out[-1][0], out[-1][1] + self.face_cents)
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    with localcontext() as ctx:
        ctx.prec = 10
        y = Decimal(rate) / Decimal(10_000)
        total = Decimal(0)
        for period, amount in bond.events():
            total += Decimal(amount) / (1 + y) ** period
        return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP))


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        units = _whole(quantity, "quantity")
        price = _whole(price_cents, "price_cents")
        direction = _whole(side, "side")
        day = _whole(settlement_day, "settlement_day")
        if units < 1:
            raise ValueError("quantity must be at least 1")
        if price < 0:
            raise ValueError("price_cents must not be negative")
        if direction not in (1, -1):
            raise ValueError("side must be +1 (buy) or -1 (sell)")
        if day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity = units
        self.price_cents = price
        self.side = direction
        self.settlement_day = day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
