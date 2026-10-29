"""Verifier round-2 alternative B (correct): integer bisection for the symmetric bid, selection-loop clearing."""

from __future__ import annotations


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


def _ranking(bids: list[int]) -> list[int]:
    # selection loop: repeatedly take the highest remaining bid; an equal bid goes to the lower index
    left = list(range(len(bids)))
    out: list[int] = []
    while left:
        best = left[0]
        for i in left[1:]:
            if bids[i] > bids[best]:
                best = i
        out.append(best)
        left.remove(best)
    return out


def allocate(bids: list[int], units: int) -> list[bool]:
    _nonneg("bid", bids)
    _units(len(bids), units)
    top = set(_ranking(bids)[:units])
    return [i in top for i in range(len(bids))]


def payments(format_name: str, bids: list[int], units: int) -> list[int]:
    _fmt(format_name)
    _nonneg("bid", bids)
    _units(len(bids), units)
    rank = _ranking(bids)
    clearing = bids[rank[units]]
    won = set(rank[:units])
    return [(clearing if format_name == "uniform" else bids[i]) if i in won else 0 for i in range(len(bids))]


def revenue(format_name: str, bids: list[int], units: int) -> int:
    return sum(payments(format_name, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    _nonneg("value", values)
    _nonneg("bid", bids)
    _units(len(bids), units)
    won = allocate(bids, units)
    achieved = sum(v for v, w in zip(values, won, strict=True) if w)
    remaining = sorted(values)
    best = 0
    for _ in range(units):
        best += remaining.pop()
    return achieved, best


def symmetric_bid_single_unit(format_name: str, n: int, value: int) -> int:
    _fmt(format_name)
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be at least 2")
    _nonneg("value", [value])
    if format_name == "uniform":
        return value
    # the largest integer b with 2*n*b <= 2*(n-1)*value + n is floor((n-1)*value/n + 1/2), found by bisection
    lo, hi = 0, value + 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if 2 * n * mid <= 2 * (n - 1) * value + n:
            lo = mid
        else:
            hi = mid - 1
    return lo
