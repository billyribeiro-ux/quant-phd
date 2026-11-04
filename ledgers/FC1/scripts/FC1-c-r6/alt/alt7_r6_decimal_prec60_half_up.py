"""Alternative correct implementation 7 (verifier, round 6): Decimal at 60 significant digits, ROUND_HALF_UP on the exact sum."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction


def _cents(value: Decimal) -> int:
    with localcontext() as ctx:
        ctx.prec = 80
        return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


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
        with localcontext() as ctx:
            ctx.prec = 80
            coupon = _cents(Decimal(self.face_cents) * Decimal(self.coupon_bps) / Decimal(10000))
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10000:
        raise ValueError("yield_bps must be greater than -10000")
    with localcontext() as ctx:
        ctx.prec = 60
        one_plus = Decimal(10000 + yield_bps) / Decimal(10000)
        total = Decimal(0)
        for period, amount in bond.events():
            total += Decimal(amount) / one_plus**period
    return _cents(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        for name, value in (("quantity", quantity), ("price_cents", price_cents), ("side", side), ("settlement_day", settlement_day)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be a whole number")
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
