"""Alternative correct implementation 10 (verifier, round 7): discount factors as powers of the exact ratio 10000 / (10000 + yield_bps), coupon by integer half-up arithmetic."""

from __future__ import annotations

from fractions import Fraction


def _int_half_away(x: Fraction) -> int:
    n, d = abs(x.numerator), x.denominator
    q = (2 * n + d) // (2 * d)
    return q if x >= 0 else -q


def _valid_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} must be a whole number")
    return value


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        self.face_cents = _valid_int(face_cents, "face_cents")
        self.coupon_bps = _valid_int(coupon_bps, "coupon_bps")
        self.periods = _valid_int(periods, "periods")
        if self.periods < 1:
            raise ValueError("periods must be at least 1")
        if self.face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if self.coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")

    def events(self) -> list[tuple[int, int]]:
        num = self.face_cents * self.coupon_bps
        coupon = (2 * num + 10_000) // 20_000  # num >= 0 here, so half up is half away from zero
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _valid_int(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    step = Fraction(10_000, 10_000 + rate)  # (1 + y) ** -1 exactly
    total = Fraction(0)
    for period, amount in bond.events():
        total += amount * step**period
    return _int_half_away(total)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        self.quantity = _valid_int(quantity, "quantity")
        self.price_cents = _valid_int(price_cents, "price_cents")
        self.side = _valid_int(side, "side")
        self.settlement_day = _valid_int(settlement_day, "settlement_day")
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
