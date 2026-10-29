"""Alternative correct engine (round 3): winners by counting the bidders who beat each bidder; heapq for efficiency."""

from __future__ import annotations

import heapq


def _beats(bids: list[int], j: int, i: int) -> bool:
    return bids[j] > bids[i] or (bids[j] == bids[i] and j < i)


def allocate(bids: list[int], units: int) -> list[bool]:
    n = len(bids)
    if isinstance(units, bool) or not isinstance(units, int) or not 1 <= units < n:
        raise ValueError("units must satisfy 1 <= units < n")
    for b in bids:
        if isinstance(b, bool) or not isinstance(b, int) or b < 0:
            raise ValueError("a bid must be a non-negative whole number of cents")
    out = []
    for i in range(n):
        beaten_by = sum(1 for j in range(n) if j != i and _beats(bids, j, i))
        out.append(beaten_by < units)
    return out


def payments(format: str, bids: list[int], units: int) -> list[int]:
    if not isinstance(format, str) or format not in {"uniform", "discriminatory"}:
        raise ValueError('format must be "uniform" or "discriminatory"')
    won = allocate(bids, units)
    # the (units+1)-th highest bid, found by sorting ascending and reading from the end
    clearing = sorted(bids)[len(bids) - units - 1]
    return [(clearing if format == "uniform" else bids[i]) if won[i] else 0 for i in range(len(bids))]


def revenue(format: str, bids: list[int], units: int) -> int:
    return sum(payments(format, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    for v in values:
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise ValueError("a value must be a non-negative whole number of cents")
    if len(values) != len(bids):
        raise ValueError("values and bids must have the same length")
    won = allocate(bids, units)
    achieved = sum(v for v, w in zip(values, won, strict=True) if w)
    return achieved, sum(heapq.nlargest(units, values))


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    if not isinstance(format, str) or format not in {"uniform", "discriminatory"}:
        raise ValueError('format must be "uniform" or "discriminatory"')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("a value must be a non-negative whole number of cents")
    if format == "uniform":
        return value
    # (n-1)*value/n rounded half up, by divmod on integers
    q, r = divmod((n - 1) * value, n)
    return q + (1 if 2 * r >= n else 0)
