"""Verifier alternative (round 3, FC1-c): decimal arithmetic at 60 significant digits, one ROUND_HALF_UP quantize of the sum."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext


def _half_up_cent(x: Decimal) -> int:
    """Nearest whole cent, a half going away from zero."""
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        for name, value in (("face_cents", face_cents), ("coupon_bps", coupon_bps), ("periods", periods)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be a whole number")
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
        with localcontext() as ctx:
            ctx.prec = 60
            coupon = _half_up_cent(Decimal(self.face_cents) * Decimal(self.coupon_bps) / Decimal(10_000))
        out = [(t, coupon) for t in range(1, self.periods + 1)]
        out[-1] = (self.periods, out[-1][1] + self.face_cents)
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    with localcontext() as ctx:
        ctx.prec = 60
        y = Decimal(yield_bps) / Decimal(10_000)
        total = Decimal(0)
        for period, amount in bond.events():
            total += Decimal(amount) / (1 + y) ** period
        return _half_up_cent(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
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
