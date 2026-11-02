"""Alternative correct implementation 3 (FC1-c round 1): integer-only arithmetic; common denominator; half-up by integer division."""

from __future__ import annotations


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
        # coupon = face * bps / 10000 rounded half up, in integers: (2 * n + d) // (2 * d) with n / d the exact value.
        coupon = (2 * self.face_cents * self.coupon_bps + 10_000) // 20_000
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, rows[-1][1] + self.face_cents)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    if not _is_int(yield_bps) or yield_bps <= -10_000:
        raise ValueError("yield_bps must be greater than -10000, so that 1 + y is positive")
    base = 10_000 + yield_bps  # 1 + y = base / 10000, and base > 0
    last = bond.periods
    # Sum of a_t / (base/10000)**t = numerator / base**last, with numerator = sum a_t * 10000**t * base**(last - t).
    numerator = 0
    for period, amount in bond.events():
        numerator += amount * 10_000**period * base ** (last - period)
    denominator = base**last
    # All bond amounts are non-negative, so the exact value is non-negative; round half away from zero in integers.
    return (2 * numerator + denominator) // (2 * denominator)


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
