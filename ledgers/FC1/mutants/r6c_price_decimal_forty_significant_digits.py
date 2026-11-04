"""Student error: bond_price_cents sums the discounted events in a Decimal context of 40 significant digits, so a price above 40 significant digits loses its half cent before the rounding."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
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
        coupon = int((Decimal(int(self.face_cents)) * Decimal(self.coupon_bps) / Decimal(10000)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
        rows = [(t, coupon) for t in range(1, int(self.periods) + 1)]
        rows[-1] = (int(self.periods), rows[-1][1] + int(self.face_cents))
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if yield_bps <= -10000:
        raise ValueError("yield_bps must be greater than -10000")
    from decimal import localcontext
    with localcontext() as ctx:
        ctx.prec = 40
        one_plus = Decimal(10000 + yield_bps) / Decimal(10000)
        total = sum((Decimal(a) / one_plus**t for t, a in bond.events()), Decimal(0))
        return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP))


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
