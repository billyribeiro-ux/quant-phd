"""Alternative correct implementation 8 (verifier, round 6): the price as one integer ratio over (10000 + yield_bps) ** T, rounded by integer arithmetic."""

from __future__ import annotations


def _round_half_away_ratio(numerator: int, denominator: int) -> int:
    # denominator is positive here; the amounts are non-negative, so half up is half away from zero
    return (2 * numerator + denominator) // (2 * denominator)


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
        numerator = self.face_cents * self.coupon_bps
        coupon = _round_half_away_ratio(numerator, 10000)
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, coupon + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if isinstance(yield_bps, bool) or not isinstance(yield_bps, int):
        raise ValueError("yield_bps must be a whole number")
    if yield_bps <= -10000:
        raise ValueError("yield_bps must be greater than -10000")
    events = bond.events()
    base = 10000 + yield_bps
    top = max(t for t, _ in events)
    # sum a * 10000**t / base**t over a common denominator base**top
    total = 0
    for t, a in events:
        total += a * 10000**t * base ** (top - t)
    denominator = base**top
    return _round_half_away_ratio(total, denominator * 10000**0)


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
