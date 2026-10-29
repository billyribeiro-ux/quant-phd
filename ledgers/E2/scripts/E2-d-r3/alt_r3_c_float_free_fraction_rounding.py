"""Alternative correct engine (round 3): Fraction-based shading with floor(x + 1/2); efficiency by sorted slice of values."""

from __future__ import annotations

import math
from fractions import Fraction

_FORMATS = ("uniform", "discriminatory")


def _units_ok(n: int, units: object) -> int:
    if isinstance(units, bool) or not isinstance(units, int) or not (1 <= units <= n - 1):
        raise ValueError("units must satisfy 1 <= units < n")
    return units


def _cents(xs: list[int], what: str) -> None:
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in xs):
        raise ValueError(f"a {what} must be a non-negative whole number of cents")


def allocate(bids: list[int], units: int) -> list[bool]:
    _cents(bids, "bid")
    k = _units_ok(len(bids), units)
    order = sorted(range(len(bids)), key=lambda i: (bids[i], -i), reverse=True)
    top = set(order[:k])
    return [i in top for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    if format not in _FORMATS:
        raise ValueError('format must be "uniform" or "discriminatory"')
    won = allocate(bids, units)
    order = sorted(range(len(bids)), key=lambda i: (bids[i], -i), reverse=True)
    price = bids[order[units]]
    paid = {i: (price if format == "uniform" else bids[i]) for i in order[:units]}
    return [paid.get(i, 0) for i in range(len(bids))] if any(won) else [0] * len(bids)


def revenue(format: str, bids: list[int], units: int) -> int:
    total = 0
    for amount in payments(format, bids, units):
        total += amount
    return total


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    _cents(values, "value")
    _cents(bids, "bid")
    if len(values) != len(bids):
        raise ValueError("values and bids must have the same length")
    won = allocate(bids, units)
    achieved = sum(values[i] for i in range(len(values)) if won[i])
    best = sum(sorted(values)[::-1][:units])
    return achieved, best


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    if format not in _FORMATS:
        raise ValueError('format must be "uniform" or "discriminatory"')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    _cents([value], "value")
    if format == "uniform":
        return value
    return math.floor(Fraction((n - 1) * value, n) + Fraction(1, 2))
