"""Alternative 4 (verifier, round 2): integer-only arithmetic; half-up by floor division, price over a common denominator."""

from __future__ import annotations


def _half_away_frac(num: int, den: int) -> int:
    """Nearest integer to num/den (den > 0): the half-up floor for num >= 0, mirrored for num < 0."""
    if num >= 0:
        return (2 * num + den) // (2 * den)
    return -((-2 * num + den) // (2 * den))


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
        self.face_cents = face_cents
        self.coupon_bps = coupon_bps
        self.periods = periods

    def events(self) -> list[tuple[int, int]]:
        coupon = _half_away_frac(self.face_cents * self.coupon_bps, 10_000)
        out: list[tuple[int, int]] = []
        for t in range(1, self.periods + 1):
            out.append((t, coupon + (self.face_cents if t == self.periods else 0)))
        return out


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be above -10000 so that 1 + y is positive")
    base = 10_000 + yield_bps
    events = bond.events()
    horizon = events[-1][0]
    num = sum(a * 10_000**t * base ** (horizon - t) for t, a in events)
    return _half_away_frac(num, base**horizon)


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
