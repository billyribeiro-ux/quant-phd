"""Alternative correct implementation 4 (FC1-c round 1): Decimal arithmetic in a local 60-digit context; ROUND_HALF_UP on the exact-ish sum."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if not _is_int(periods) or periods < 1:
            raise ValueError("periods must be at least 1")
        if not _is_int(face_cents) or face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if not _is_int(coupon_bps) or coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods

    def events(self) -> list[tuple[int, int]]:
        with localcontext() as ctx:
            ctx.prec = 60
            coupon = int((Decimal(self.face_cents) * Decimal(self.coupon_bps) / Decimal(10_000)).quantize(
                Decimal(1), rounding=ROUND_HALF_UP
            ))
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if not _is_int(yield_bps) or yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    with localcontext() as ctx:
        ctx.prec = 60
        one_plus_y = Decimal(10_000 + yield_bps) / Decimal(10_000)
        total = Decimal(0)
        for period, amount in bond.events():
            total += Decimal(amount) / one_plus_y**period
        return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP))


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        if not _is_int(quantity) or quantity < 1:
            raise ValueError("quantity must be at least 1")
        if not _is_int(price_cents) or price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if not _is_int(side) or side not in (1, -1):
            raise ValueError("side must be +1 (buy) or -1 (sell)")
        if not _is_int(settlement_day) or settlement_day < 1:
            raise ValueError("settlement_day must be at least 1")
        self.quantity = quantity
        self.price_cents = price_cents
        self.side = side
        self.settlement_day = settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
