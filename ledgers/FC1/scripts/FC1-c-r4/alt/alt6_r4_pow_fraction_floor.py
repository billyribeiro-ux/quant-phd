"""Alternative correct implementation 6 (verifier r4): discount factor as Fraction(10000, 10000 + yield_bps) ** t, floor-based half-away rounding."""

from __future__ import annotations

import math
from fractions import Fraction


def _cents(x: Fraction) -> int:
    # Half away from zero: floor(|x| + 1/2), with the sign restored.
    if x >= 0:
        return math.floor(x + Fraction(1, 2))
    return -math.floor(-x + Fraction(1, 2))


def _check_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a whole number")
    return value


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        face = _check_int(face_cents, "face_cents")
        coupon = _check_int(coupon_bps, "coupon_bps")
        n = _check_int(periods, "periods")
        if n < 1:
            raise ValueError("periods must be at least 1")
        if face <= 0:
            raise ValueError("face_cents must be positive")
        if coupon < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face
        self.coupon_bps = coupon
        self.periods = n

    def events(self) -> list[tuple[int, int]]:
        coupon = _cents(Fraction(self.face_cents * self.coupon_bps, 10000))
        rows: list[tuple[int, int]] = []
        for t in range(1, self.periods + 1):
            amount = coupon
            if t == self.periods:
                amount += self.face_cents
            rows.append((t, amount))
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    y_bps = _check_int(yield_bps, "yield_bps")
    if y_bps <= -10000:
        raise ValueError("yield_bps must be greater than -10000")
    base = Fraction(10000, 10000 + y_bps)
    total = Fraction(0)
    for t, amount in bond.events():
        total += amount * base**t
    return _cents(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        q = _check_int(quantity, "quantity")
        p = _check_int(price_cents, "price_cents")
        s = _check_int(side, "side")
        d = _check_int(settlement_day, "settlement_day")
        if q < 1:
            raise ValueError("quantity must be at least 1")
        if p < 0:
            raise ValueError("price_cents must not be negative")
        if s not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if d < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity, self.price_cents, self.side, self.settlement_day = q, p, s, d

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
