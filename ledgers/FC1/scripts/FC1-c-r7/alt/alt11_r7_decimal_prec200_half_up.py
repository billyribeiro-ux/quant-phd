"""Alternative correct implementation 11 (verifier, round 7): Decimal arithmetic at 200 significant digits, ROUND_HALF_UP for the single final rounding, and the coupon from a Decimal quotient."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Context, Decimal
from fractions import Fraction

CTX = Context(prec=200, rounding=ROUND_HALF_UP)


def _cents(value: Decimal) -> int:
    # ROUND_HALF_UP in Decimal rounds an exact half away from zero, which is the page's rule
    return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP, context=CTX))


def _check_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a whole number")
    return value


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        self.face_cents = _check_int(face_cents, "face_cents")
        self.coupon_bps = _check_int(coupon_bps, "coupon_bps")
        self.periods = _check_int(periods, "periods")
        if self.periods < 1:
            raise ValueError("periods must be at least 1")
        if self.face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if self.coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")

    def events(self) -> list[tuple[int, int]]:
        coupon = _cents(CTX.divide(Decimal(self.face_cents * self.coupon_bps), Decimal(10_000)))
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _check_int(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    base = CTX.divide(Decimal(10_000 + rate), Decimal(10_000))
    total = Decimal(0)
    for period, amount in bond.events():
        total = CTX.add(total, CTX.divide(Decimal(amount), CTX.power(base, Decimal(period))))
    return _cents(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        self.quantity = _check_int(quantity, "quantity")
        self.price_cents = _check_int(price_cents, "price_cents")
        self.side = _check_int(side, "side")
        self.settlement_day = _check_int(settlement_day, "settlement_day")
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
