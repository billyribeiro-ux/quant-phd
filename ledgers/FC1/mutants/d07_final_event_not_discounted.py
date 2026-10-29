"""The last event (its coupon and the face together) is priced undiscounted, selected by amount > face."""

from __future__ import annotations

import numbers
from fractions import Fraction


def _half_away(amount: Fraction) -> int:
    """The nearest whole cent of an exact amount; an exact half goes away from zero."""
    magnitude = abs(amount)
    rounded = (2 * magnitude.numerator + magnitude.denominator) // (2 * magnitude.denominator)
    return rounded if amount >= 0 else -rounded


def _whole(value: object, name: str) -> int:
    """A whole number that is not a bool, or ValueError."""
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be a whole number, not {value!r}")
    return int(value)


class Bond:
    """A fixed-rate bond: a coupon of face * coupon_bps / 10000 (half away from zero) in each of periods 1..periods,
    and the face in the last period."""

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
        """(period, amount_cents) for periods 1..periods, sorted by period, amounts from the holder's side."""
        coupon = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))
        out = [(t, coupon) for t in range(1, self.periods + 1)]
        last_period, last_amount = out[-1]
        out[-1] = (last_period, last_amount + self.face_cents)
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    """The present value of the bond's events at a per-period yield, summed exactly and rounded once."""
    rate = _whole(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    y = Fraction(rate, 10_000)
    total = Fraction(0)
    for period, amount in bond.events():
        exponent = 0 if amount > bond.face_cents else period
        total += Fraction(amount) / (1 + y) ** exponent
    return _half_away(total)


class CashTrade:
    """A trade in a cash instrument that settles in one period. The holder's cash flow is -side * quantity * price."""

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
        """One event: (settlement_day, -side * quantity * price_cents), from the holder's side."""
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
