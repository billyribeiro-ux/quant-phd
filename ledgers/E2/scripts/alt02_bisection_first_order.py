"""Alternative 2: bisection on the first-order condition with exact rational bracketing for the bid; sort-based payments."""

from __future__ import annotations

from fractions import Fraction
from math import floor


def _ok_format(format: object) -> None:
    if format not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')


def _ok_cents(name: str, xs: list[int]) -> None:
    for x in xs:
        if isinstance(x, bool) or not isinstance(x, int) or x < 0:
            raise ValueError(f"every {name} must be a non-negative whole number of cents")


def _ok_units(n: int, units: object) -> None:
    if isinstance(units, bool) or not isinstance(units, int) or not 1 <= units < n:
        raise ValueError("units must satisfy 1 <= units < n")


def allocate(bids: list[int], units: int) -> list[bool]:
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    order = sorted(range(len(bids)), key=lambda i: (-bids[i], i))
    chosen = set(order[:units])
    return [i in chosen for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    _ok_format(format)
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    order = sorted(range(len(bids)), key=lambda i: (-bids[i], i))
    out = [0] * len(bids)
    for i in order[:units]:
        out[i] = bids[order[units]] if format == "uniform" else bids[i]
    return out


def revenue(format: str, bids: list[int], units: int) -> int:
    return sum(payments(format, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    _ok_cents("value", values)
    _ok_cents("bid", bids)
    if len(values) != len(bids):
        raise ValueError("values and bids must have the same length")
    _ok_units(len(bids), units)
    won = sum(v for v, w in zip(values, allocate(bids, units), strict=True) if w)
    return won, sum(sorted(values, reverse=True)[:units])


def _root_bracket(n: int, value: int) -> tuple[Fraction, Fraction]:
    """Bisect f(b) = (n-1)(value-b) - b on [0, value]; f is decreasing and its root is (n-1)value/n."""
    lo, hi = Fraction(0), Fraction(value)
    for _ in range(80):
        mid = (lo + hi) / 2
        if (n - 1) * (value - mid) - mid > 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    _ok_format(format)
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    _ok_cents("value", [value])
    if format == "uniform":
        return value
    lo, hi = _root_bracket(n, value)
    # The exact root has denominator n, so a half-integer inside the bracket is the root itself: it rounds up.
    candidate = Fraction(floor(lo)) + Fraction(1, 2)
    if lo <= candidate <= hi:
        return floor(lo) + 1
    return floor(lo + Fraction(1, 2))
