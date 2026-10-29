"""Alternative correct engine (round 3): float arithmetic for the symmetric bid, floor(x + 0.5); the rest by sorting."""

from __future__ import annotations

import math


def allocate(bids: list[int], units: int) -> list[bool]:
    if isinstance(units, bool) or not isinstance(units, int) or not 1 <= units < len(bids):
        raise ValueError("units must satisfy 1 <= units < n")
    if any(isinstance(b, bool) or not isinstance(b, int) or b < 0 for b in bids):
        raise ValueError("a bid must be a non-negative whole number of cents")
    order = sorted(range(len(bids)), key=lambda i: (bids[i], -i), reverse=True)
    top = set(order[:units])
    return [i in top for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    if format not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')
    won = allocate(bids, units)
    clearing = sorted(bids, reverse=True)[units]
    return [0 if not won[i] else (clearing if format == "uniform" else bids[i]) for i in range(len(bids))]


def revenue(format: str, bids: list[int], units: int) -> int:
    return sum(payments(format, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    if len(values) != len(bids):
        raise ValueError("values and bids must have the same length")
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in values):
        raise ValueError("a value must be a non-negative whole number of cents")
    won = allocate(bids, units)
    return sum(v for v, w in zip(values, won, strict=True) if w), sum(sorted(values)[-units:])


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    if format not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')
    if n < 2:
        raise ValueError("n must be at least 2")
    if value < 0:
        raise ValueError("a value must be a non-negative whole number of cents")
    if format == "uniform":
        return value
    return math.floor((n - 1) * value / n + 0.5)
