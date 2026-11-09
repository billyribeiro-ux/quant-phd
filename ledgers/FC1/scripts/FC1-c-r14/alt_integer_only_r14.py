"""Extra alternative (round 14, FC1-c): integer-only arithmetic throughout, no Fraction, half-away rounding by integer division.

The price is a rational with the common denominator (10000 + yield_bps) ** periods, summed as integers.
"""

from __future__ import annotations


def _round_half_away(num: int, den: int) -> int:
    """Nearest integer to num/den (den > 0), an exact half going away from zero, by integer division only."""
    if num >= 0:
        return (2 * num + den) // (2 * den)
    return -((2 * -num + den) // (2 * den))


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        for name, v in (("face_cents", face_cents), ("coupon_bps", coupon_bps), ("periods", periods)):
            if isinstance(v, bool) or not isinstance(v, int):
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
        coupon = _round_half_away(self.face_cents * self.coupon_bps, 10_000)
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    for name, v in (("yield_bps", yield_bps),):
        if isinstance(v, bool) or not isinstance(v, int):
            raise ValueError(f"{name} must be a whole number")
    if yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    base = 10_000 + yield_bps
    n = bond.periods
    den = base**n
    num = 0
    for t, a in bond.events():
        # a / (1+y)^t = a * 10000^t * base^(n-t) / base^n  (all integers)
        num += a * 10_000**t * base ** (n - t)
    return _round_half_away(num, den)


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        for name, v in (
            ("quantity", quantity),
            ("price_cents", price_cents),
            ("side", side),
            ("settlement_day", settlement_day),
        ):
            if isinstance(v, bool) or not isinstance(v, int):
                raise ValueError(f"{name} must be a whole number")
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
