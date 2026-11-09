"""Student error: Bond.events() adds the face to its stored last event on every call, so a second call to the same bond returns the face twice in the last period."""

from __future__ import annotations


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if isinstance(periods, bool) or not isinstance(periods, int) or periods < 1:
            raise ValueError("periods must be at least 1")
        if isinstance(face_cents, bool) or not isinstance(face_cents, int) or face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if isinstance(coupon_bps, bool) or not isinstance(coupon_bps, int) or coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods
        coupon = (face_cents * coupon_bps * 2 + 10_000) // 20_000
        self._rows = [(t, coupon) for t in range(1, periods + 1)]

    def events(self) -> list[tuple[int, int]]:
        last_period, last_amount = self._rows[-1]
        self._rows[-1] = (last_period, last_amount + self.face_cents)
        return list(self._rows)


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    from fractions import Fraction

    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    y = Fraction(yield_bps, 10_000)
    total = sum((Fraction(a) / (1 + y) ** t for t, a in bond.events()), Fraction(0))
    return int(total + Fraction(1, 2)) if total >= 0 else -int(-total + Fraction(1, 2))


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
        self.quantity = quantity
        self.price_cents = price_cents
        self.side = side
        self.settlement_day = settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
