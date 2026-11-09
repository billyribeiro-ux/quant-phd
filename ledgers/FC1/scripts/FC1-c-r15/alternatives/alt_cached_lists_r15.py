"""Alternative correct implementation 7 (round 15, FC1-c): events computed once in __init__, returned as fresh lists of lists."""

from __future__ import annotations

from fractions import Fraction


def _half_up_away(x: Fraction) -> int:
    n = (2 * abs(x).numerator + abs(x).denominator) // (2 * abs(x).denominator)
    return n if x >= 0 else -n


def _check_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an int")
    return value


class Bond:
    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        face = _check_int(face_cents, "face_cents")
        bps = _check_int(coupon_bps, "coupon_bps")
        count = _check_int(periods, "periods")
        if count < 1:
            raise ValueError("periods must be at least 1")
        if face <= 0:
            raise ValueError("face_cents must be positive")
        if bps < 0:
            raise ValueError("coupon_bps must not be negative")
        coupon = _half_up_away(Fraction(face * bps, 10_000))
        self._events = [[t, coupon] for t in range(1, count + 1)]
        self._events[-1][1] += face
        self.periods = count

    def events(self) -> list[tuple[int, int]]:
        return [(t, a) for t, a in self._events]


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    rate = _check_int(yield_bps, "yield_bps")
    if rate <= -10_000:
        raise ValueError("yield_bps must be greater than -10000")
    y = Fraction(rate, 10_000)
    return _half_up_away(sum((Fraction(a) / (1 + y) ** t for t, a in bond._events), Fraction(0)))


class CashTrade:
    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        q = _check_int(quantity, "quantity")
        p = _check_int(price_cents, "price_cents")
        s = _check_int(side, "side")
        d = _check_int(settlement_day, "settlement_day")
        if q < 1:
            raise ValueError("quantity must be at least 1")
        if p < 0:
            raise ValueError("price_cents must not be negative")
        if s not in (1, -1):
            raise ValueError("side must be +1 or -1")
        if d < 1:
            raise ValueError("settlement_day must be at least 1")
        self._event = (d, -s * q * p)

    def events(self) -> list[tuple[int, int]]:
        return [self._event]
