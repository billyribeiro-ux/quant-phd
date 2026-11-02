"""Alternative correct implementation 5 (FC1-c round 1): Fraction for the price, with the discount written as (1 + y) ** -t via Fraction power; validation by a single tuple check."""

from __future__ import annotations

from fractions import Fraction


def _round_once(exact: Fraction) -> int:
    # A different spelling of the half-away rule: floor of (|x| + 1/2), then the sign.
    rounded = int(abs(exact) + Fraction(1, 2))
    return rounded if exact >= 0 else -rounded


def _check(values: tuple[object, ...]) -> None:
    for value in values:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("inputs must be ints")


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        _check((face_cents, coupon_bps, periods))
        if periods < 1:
            raise ValueError("periods must be at least 1")
        if face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _round_once(Fraction(self.face_cents * self.coupon_bps, 10_000))
        out = [(period, coupon) for period in range(1, self.periods + 1)]
        out[-1] = (self.periods, out[-1][1] + self.face_cents)
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    _check((yield_bps,))
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    y = Fraction(yield_bps, 10_000)
    exact = Fraction(0)
    for period, amount in bond.events():
        exact += Fraction(amount) * (1 + y) ** (-period)
    return _round_once(exact)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        _check((quantity, price_cents, side, settlement_day))
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
