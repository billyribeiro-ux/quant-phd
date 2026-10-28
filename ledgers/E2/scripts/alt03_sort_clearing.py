"""Alternative 3: sort-based clearing with a tuple key; the bid by floor of the exact rational plus one half."""

from __future__ import annotations

from fractions import Fraction
from math import floor


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


def _ranked(bids: list[int]) -> list[tuple[int, int]]:
    return sorted(((-b, i) for i, b in enumerate(bids)))


def allocate(bids: list[int], units: int) -> list[bool]:
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    winners = {i for _, i in _ranked(bids)[:units]}
    return [i in winners for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    _ok_format(format)
    _ok_cents("bid", bids)
    _ok_units(len(bids), units)
    ranked = _ranked(bids)
    price = -ranked[units][0]
    out = [0] * len(bids)
    for _, i in ranked[:units]:
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
    winners = {i for _, i in _ranked(bids)[:units]}
    won = sum(values[i] for i in winners)
    return won, sum(sorted(values, reverse=True)[:units])


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    _ok_format(format)
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    _ok_cents("value", [value])
    if format == "uniform":
        return value
    return floor(Fraction((n - 1) * value, n) + Fraction(1, 2))
