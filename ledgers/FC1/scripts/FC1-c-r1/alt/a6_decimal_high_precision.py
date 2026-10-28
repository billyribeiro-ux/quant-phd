"""Verifier alternative 6: Decimal at 40 significant digits, ROUND_HALF_UP, with events as lists of lists."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction

getcontext().prec = 40


def _num(x: object) -> int:
    if isinstance(x, bool) or not isinstance(x, int):
        raise ValueError("whole number required")
    return x


def _cents(value: Decimal) -> int:
    """Round a Decimal to whole cents, halves away from zero."""
    q = value.copy_abs().quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(q) if value >= 0 else -int(q)


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        face, coupon, n = _num(face_cents), _num(coupon_bps), _num(periods)
        if n < 1:
            raise ValueError("periods")
        if face <= 0:
            raise ValueError("face")
        if coupon < 0:
            raise ValueError("coupon")
        self.face_cents, self.coupon_bps, self.periods = face, coupon, n

    def events(self) -> list[list[int]]:
        c = _cents(Decimal(self.face_cents) * Decimal(self.coupon_bps) / Decimal(10000))
        rows = [[t, c] for t in range(1, self.periods + 1)]
        rows[-1][1] += self.face_cents
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    y = _num(yield_bps)
    if y <= -10000:
        raise ValueError("yield")
    total = Decimal(0)
    base = Decimal(10000 + y) / Decimal(10000)
    for t, a in bond.events():
        total += Decimal(a) / (base**t)
    return _cents(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        q, p, s, d = _num(quantity), _num(price_cents), _num(side), _num(settlement_day)
        if q < 1:
            raise ValueError("quantity")
        if p < 0:
            raise ValueError("price")
        if s not in (1, -1):
            raise ValueError("side")
        if d < 1:
            raise ValueError("day")
        self.q, self.p, self.s, self.d = q, p, s, d

    def events(self) -> list[tuple[int, int]]:
        return [(self.d, -self.s * self.q * self.p)]
