"""Alternative correct engine (round 3): ranking by a stable reverse sort of (index, bid) pairs; Decimal half-up bids."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal


def _check(bids: list[int], units: int) -> None:
    if not 1 <= units < len(bids):
        raise ValueError("units must satisfy 1 <= units < n")
    for b in bids:
        if not isinstance(b, int) or isinstance(b, bool) or b < 0:
            raise ValueError("a bid must be a non-negative whole number of cents")


def allocate(bids: list[int], units: int) -> list[bool]:
    _check(bids, units)
    ordered = sorted(enumerate(bids), key=lambda p: p[1], reverse=True)  # stable: equal bids keep index order
    winners = {i for i, _ in ordered[:units]}
    return [i in winners for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    if format not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')
    _check(bids, units)
    won = allocate(bids, units)
    price = sorted(bids, reverse=True)[units]
    return [(price if format == "uniform" else bids[i]) if won[i] else 0 for i in range(len(bids))]


def revenue(format: str, bids: list[int], units: int) -> int:
    return sum(payments(format, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    if len(values) != len(bids):
        raise ValueError("values and bids must have the same length")
    for v in values:
        if v < 0:
            raise ValueError("a value must be a non-negative whole number of cents")
    _check(bids, units)
    won = allocate(bids, units)
    return sum(v for v, w in zip(values, won, strict=True) if w), sum(sorted(values)[len(values) - units :])


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    if format not in ("uniform", "discriminatory"):
        raise ValueError('format must be "uniform" or "discriminatory"')
    if n < 2:
        raise ValueError("n must be at least 2")
    if value < 0:
        raise ValueError("a value must be a non-negative whole number of cents")
    if format == "uniform":
        return value
    exact = Decimal((n - 1) * value) / Decimal(n)
    return int(exact.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
