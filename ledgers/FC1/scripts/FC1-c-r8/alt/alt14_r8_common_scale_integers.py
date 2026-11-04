"""Alternative correct module (round 8): integer-only arithmetic, the price as one fraction over R**T with R = 10000 + yield."""

from __future__ import annotations

import numbers


def _int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be a whole number")
    return int(value)


class Bond:
    """Fixed-rate bond: coupon face * coupon_bps / 10000 rounded half away in each period, face in the last."""

    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        self.face = _int(face_cents, "face_cents")
        self.coupon_bps = _int(coupon_bps, "coupon_bps")
        self.periods = _int(periods, "periods")
        if self.periods < 1:
            raise ValueError("periods must be at least 1")
        if self.face <= 0:
            raise ValueError("face_cents must be positive")
        if self.coupon_bps < 0:
            raise ValueError("coupon_bps must not be negative")

    def events(self) -> list[tuple[int, int]]:
        num = self.face * self.coupon_bps
        whole, rest = divmod(num, 10000)
        coupon = whole + (1 if 2 * rest >= 10000 else 0)  # non-negative: half goes up
        rows = [(t, coupon) for t in range(1, self.periods + 1)]
        rows[-1] = (self.periods, coupon + self.face)
        return rows


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _int(yield_bps, "yield_bps")
    if rate <= -10000:
        raise ValueError("yield_bps must exceed -10000")
    growth = 10000 + rate  # 1 + y = growth / 10000
    rows = bond.events()
    last = max(t for t, _ in rows)
    # sum of amount * (10000 / growth) ** t over t, as one fraction with denominator growth ** last
    num = 0
    for t, amount in rows:
        num += amount * 10000**t * growth ** (last - t)
    den = growth**last
    if num >= 0:
        return (2 * num + den) // (2 * den)
    return -((2 * -num + den) // (2 * den))


class CashTrade:
    """One settlement event: the holder's cash flow is -side * quantity * price."""

    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        self.quantity = _int(quantity, "quantity")
        self.price_cents = _int(price_cents, "price_cents")
        self.side = _int(side, "side")
        self.settlement_day = _int(settlement_day, "settlement_day")
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
