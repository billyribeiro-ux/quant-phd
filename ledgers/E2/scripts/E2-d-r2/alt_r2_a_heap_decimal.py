"""Verifier round-2 alternative A (correct): heapq for the winners, Decimal ROUND_HALF_UP for the symmetric bid."""

from __future__ import annotations

import heapq
from decimal import ROUND_HALF_UP, Decimal


def _fmt(format_name: str) -> None:
    if format_name not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')


def _units(n: int, units: int) -> None:
    if not isinstance(units, int) or isinstance(units, bool) or not 1 <= units < n:
        raise ValueError("units must satisfy 1 <= units < n")


def _nonneg(name: str, xs: list[int]) -> None:
    for x in xs:
        if not isinstance(x, int) or isinstance(x, bool) or x < 0:
            raise ValueError(f"a {name} must be a non-negative whole number of cents")


def _order(bids: list[int], units: int) -> list[int]:
    # the top units + 1 bidders by (highest bid, then lowest index), via heapq.nsmallest on negated keys
    return [i for _, i in heapq.nsmallest(units + 1, ((-b, i) for i, b in enumerate(bids)))]


def allocate(bids: list[int], units: int) -> list[bool]:
    _nonneg("bid", bids)
    _units(len(bids), units)
    top = set(_order(bids, units)[:units])
    return [i in top for i in range(len(bids))]


def payments(format_name: str, bids: list[int], units: int) -> list[int]:
    _fmt(format_name)
    _nonneg("bid", bids)
    _units(len(bids), units)
    order = _order(bids, units)
    clearing = bids[order[units]]
    won = set(order[:units])
    return [(clearing if format_name == "uniform" else bids[i]) if i in won else 0 for i in range(len(bids))]


def revenue(format_name: str, bids: list[int], units: int) -> int:
    return sum(payments(format_name, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    _nonneg("value", values)
    _nonneg("bid", bids)
    _units(len(bids), units)
    won = [w for w in allocate(bids, units)]
    achieved = sum(v for v, w in zip(values, won, strict=True) if w)
    best = sum(heapq.nlargest(units, values))
    return achieved, best


def symmetric_bid_single_unit(format_name: str, n: int, value: int) -> int:
    _fmt(format_name)
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be at least 2")
    _nonneg("value", [value])
    if format_name == "uniform":
        return value
    exact = Decimal((n - 1) * value) / Decimal(n)
    return int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))
