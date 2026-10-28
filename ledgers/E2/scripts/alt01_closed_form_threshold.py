"""Alternative 1: threshold clearing (the k-th and (k+1)-th highest values set the cut) and the integer closed form for the bid."""

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


def allocate(bids: list[int], units: int) -> list[bool]:
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    cut = sorted(bids, reverse=True)[units - 1]
    above = sum(1 for b in bids if b > cut)
    spare = units - above
    result: list[bool] = []
    for b in bids:
        if b > cut:
            result.append(True)
        elif b == cut and spare > 0:
            result.append(True)
            spare -= 1
        else:
            result.append(False)
    return result


def payments(format: str, bids: list[int], units: int) -> list[int]:
    _ok_format(format)
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    winners = allocate(bids, units)
    clearing = sorted(bids, reverse=True)[units]
    return [
        (clearing if format == "uniform" else b) if won else 0
        for b, won in zip(bids, winners, strict=True)
    ]


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


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    _ok_format(format)
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    _ok_cents("value", [value])
    if format == "uniform":
        return value
    return (2 * (n - 1) * value + n) // (2 * n)
