"""Verifier round-2 alternative C (correct): floor plus remainder test for the symmetric bid; index-count ranks."""

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


def _rank_of(bids: list[int]) -> list[int]:
    # position of each bidder in the ranking: the count of bidders above it, plus ties with a lower index
    n = len(bids)
    pos = [0] * n
    for i in range(n):
        for j in range(n):
            if j != i and (bids[j] > bids[i] or (bids[j] == bids[i] and j < i)):
                pos[i] += 1
    ranking = [0] * n
    for i, p in enumerate(pos):
        ranking[p] = i
    return ranking


def allocate(bids: list[int], units: int) -> list[bool]:
    _nonneg("bid", bids)
    _units(len(bids), units)
    rank = _rank_of(bids)
    top = set(rank[:units])
    return [i in top for i in range(len(bids))]


def payments(format_name: str, bids: list[int], units: int) -> list[int]:
    _fmt(format_name)
    _nonneg("bid", bids)
    _units(len(bids), units)
    rank = _rank_of(bids)
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
    best = sum(sorted(values)[len(values) - units :])
    return achieved, best


def symmetric_bid_single_unit(format_name: str, n: int, value: int) -> int:
    _fmt(format_name)
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be at least 2")
    _nonneg("value", [value])
    if format_name == "uniform":
        return value
    q, r = divmod((n - 1) * value, n)
    return q + 1 if 2 * r >= n else q
