"""Alternative 4: counting-based clearing (each bidder's rank is the number of bidders above it), integer bid formula."""

from __future__ import annotations


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


def _ranks(bids: list[int]) -> list[int]:
    n = len(bids)
    return [
        sum(1 for j in range(n) if bids[j] > bids[i] or (bids[j] == bids[i] and j < i))
        for i in range(n)
    ]


def allocate(bids: list[int], units: int) -> list[bool]:
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    return [r < units for r in _ranks(bids)]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    _ok_format(format)
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    ranks = _ranks(bids)
    price = next(bids[i] for i, r in enumerate(ranks) if r == units)
    return [
        ((price if format == "uniform" else bids[i]) if r < units else 0)
        for i, r in enumerate(ranks)
    ]


def revenue(format: str, bids: list[int], units: int) -> int:
    return sum(payments(format, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    _ok_cents("value", values)
    _ok_cents("bid", bids)
    if len(values) != len(bids):
        raise ValueError("values and bids must have the same length")
    _ok_units(len(bids), units)
    ranks = _ranks(bids)
    won = sum(v for v, r in zip(values, ranks, strict=True) if r < units)
    return won, sum(sorted(values, reverse=True)[:units])


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    _ok_format(format)
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    _ok_cents("value", [value])
    if format == "uniform":
        return value
    return (2 * (n - 1) * value + n) // (2 * n)
