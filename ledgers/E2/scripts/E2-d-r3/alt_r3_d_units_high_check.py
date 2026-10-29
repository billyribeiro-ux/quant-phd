"""Alternative correct engine (round 3): winners by sorting (bid, -index) descending; clearing from the sorted bid list."""

from __future__ import annotations


def _validate_bids(bids: list[int]) -> None:
    for b in bids:
        if isinstance(b, bool) or not isinstance(b, int):
            raise ValueError("every bid must be a whole number of cents")
        if b < 0:
            raise ValueError("a bid must be a non-negative whole number of cents")


def _validate_units(n: int, units: int) -> None:
    if isinstance(units, bool) or not isinstance(units, int):
        raise ValueError("units must satisfy 1 <= units < n")
    if units < 1 or units >= n:
        raise ValueError("units must satisfy 1 <= units < n")


def allocate(bids: list[int], units: int) -> list[bool]:
    _validate_bids(bids)
    _validate_units(len(bids), units)
    keyed = sorted(((bids[i], -i) for i in range(len(bids))), reverse=True)
    winners = {-neg for _, neg in keyed[:units]}
    return [i in winners for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    if format not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')
    _validate_bids(bids)
    _validate_units(len(bids), units)
    won = allocate(bids, units)
    clearing = sorted(bids, reverse=True)[units]
    out = []
    for i, w in enumerate(won):
        if not w:
            out.append(0)
        elif format == "uniform":
            out.append(clearing)
        else:
            out.append(bids[i])
    return out


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
    _validate_units(len(values), units)
    return achieved, sum(sorted(values, reverse=True)[:units])


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    if format not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("a value must be a non-negative whole number of cents")
    if format == "uniform":
        return value
    num = 2 * (n - 1) * value + n
    return num // (2 * n)
