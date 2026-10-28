"""Alternative correct implementation 1: events built by list comprehensions, with the coupon rule written inline."""

from __future__ import annotations

from fractions import Fraction


def _half_away(x: Fraction) -> int:
    m = abs(x)
    r = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return r if x >= 0 else -r


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if isinstance(periods, bool) or not isinstance(periods, int) or periods < 1:
            raise ValueError("periods must be at least 1")
        if isinstance(face_cents, bool) or not isinstance(face_cents, int) or face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if isinstance(coupon_bps, bool) or not isinstance(coupon_bps, int) or coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents, self.coupon_bps, self.periods = face_cents, coupon_bps, periods

    def events(self) -> list[tuple[int, int]]:
        c = _half_away(Fraction(self.face_cents * self.coupon_bps, 10_000))
        face_part = [(t, c) for t in range(1, self.periods)]
        return [*face_part, (self.periods, c + self.face_cents)]


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    y = Fraction(yield_bps, 10_000)
    return _half_away(sum((Fraction(a) / (1 + y) ** t for t, a in bond.events()), Fraction(0)))


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
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        if price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if side not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity, self.price_cents, self.side, self.settlement_day = quantity, price_cents, side, settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
