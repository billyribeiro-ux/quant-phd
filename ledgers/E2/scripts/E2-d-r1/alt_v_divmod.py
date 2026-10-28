"""Verifier alternative: insertion-sorted ranking, divmod rounding for the symmetric bid, no Fraction."""

from __future__ import annotations


def _ok_format(fmt: object) -> None:
    if fmt not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')


def _ok_units(n: int, units: object) -> None:
    if not isinstance(units, int) or isinstance(units, bool) or not (1 <= units < n):
        raise ValueError("units must satisfy 1 <= units < n")


def _ok_cents(name: str, xs: list[int]) -> None:
    for x in xs:
        if not isinstance(x, int) or isinstance(x, bool) or x < 0:
            raise ValueError(f"every {name} must be a non-negative whole number of cents")


def _rank(bids: list[int]) -> list[int]:
    order: list[int] = []
    for i in range(len(bids)):
        pos = len(order)
        while pos > 0 and bids[order[pos - 1]] < bids[i]:
            pos -= 1
        order.insert(pos, i)
    return order


def allocate(bids: list[int], units: int) -> list[bool]:
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    top = set(_rank(bids)[:units])
    return [i in top for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    _ok_format(format)
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    order = _rank(bids)
    price = bids[order[units]]
    out = [0] * len(bids)
    for i in order[:units]:
        out[i] = price if format == "uniform" else bids[i]
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
    best = sum(sorted(values, reverse=True)[:units])
    return won, best


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    _ok_format(format)
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be at least 2")
    _ok_cents("value", [value])
    if format == "uniform":
        return value
    q, r = divmod((n - 1) * value, n)  # value * (n-1)/n = q + r/n; half up when 2r >= n
    return q + (1 if 2 * r >= n else 0)
