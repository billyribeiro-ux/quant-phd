"""Alternative 1 (verifier, round 2): list-comprehension events; price as one integer fraction over a common denominator."""

from __future__ import annotations


def _round_half_away(numerator: int, denominator: int) -> int:
    """Nearest integer to numerator / denominator (denominator > 0), an exact half going away from zero."""
    if numerator >= 0:
        return (2 * numerator + denominator) // (2 * denominator)
    return -((-2 * numerator + denominator) // (2 * denominator))


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        if not isinstance(face_cents, int) or isinstance(face_cents, bool):
            raise TypeError("face_cents must be an int number of cents")
        if periods < 1:
            raise ValueError("periods must be at least 1")
        if face_cents <= 0:
            raise ValueError("face_cents must be positive")
        if coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")
        self.face_cents, self.coupon_bps, self.periods = face_cents, coupon_bps, periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _round_half_away(self.face_cents * self.coupon_bps, 10_000)
        rows = [(t, coupon + (self.face_cents if t == self.periods else 0)) for t in range(1, self.periods + 1)]
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be above -10000 so that 1 + y is positive")
    base = 10_000 + yield_bps  # (1 + y) = base / 10000, so (1 + y)**-t = 10000**t / base**t
    horizon = max(t for t, _ in bond.events())
    numerator = 0
    for t, amount in bond.events():
        numerator += amount * 10_000**t * base ** (horizon - t)  # common denominator base**horizon
    return _round_half_away(numerator, base**horizon)


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
        self.quantity, self.price_cents, self.side, self.settlement_day = quantity, price_cents, side, settlement_day

    def events(self) -> list[tuple[int, int]]:
        return [(self.settlement_day, -self.side * self.quantity * self.price_cents)]
