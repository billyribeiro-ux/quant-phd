"""Alternative correct implementation 4: the coupon and the trade in integer division; the price in exact Fractions."""

from __future__ import annotations

from fractions import Fraction


def _half_up_nonneg(numerator: int, denominator: int) -> int:
    return (2 * numerator + denominator) // (2 * denominator)


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

    def events(self) -> list[tuple[int, int]]:
        coupon = _half_up_nonneg(self.face_cents * self.coupon_bps, 10_000)
        out = [(t, coupon) for t in range(1, self.periods + 1)]
        out[-1] = (self.periods, out[-1][1] + self.face_cents)
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    total = Fraction(0)
    for t, a in bond.events():
        total += Fraction(a, (10_000 + yield_bps) ** t) * 10_000**t
    # the exact value is total; one half-up rounding of a non-negative value
    num, den = total.numerator, total.denominator
    return (2 * num + den) // (2 * den)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise ValueError("quantity must be at least 1")
        if isinstance(price_cents, bool) or not isinstance(price_cents, int) or price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if isinstance(side, bool) or side not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if isinstance(settlement_day, bool) or not isinstance(settlement_day, int) or settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity, self.price_cents, self.side, self.settlement_day = quantity, price_cents, side, settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
