"""Reference solution for the E2 project: auction_sim.py, the sealed-bid unit auction engine.

It implements the contract in project.html, section "Rung 3 · Specification". Standard library only.

Conventions (binding, from the project specification):

* every money amount is an integer number of cents; bids and values are non-negative integers;
* a cent amount that is not exact is taken to the nearest cent, a tie going up (half up), computed from an exact
  Fraction and rounded once;
* ties in bids go to the lower bidder index;
* invalid inputs raise ValueError; no function prints or warns.
"""

from __future__ import annotations

import math
from fractions import Fraction

FORMATS: tuple[str, str] = ("uniform", "discriminatory")


def _check_format(format: object) -> str:
    if not isinstance(format, str) or format not in FORMATS:
        raise ValueError('format must be "uniform" or "discriminatory"')
    return format


def _check_units(bidders: int, units: object) -> int:
    if isinstance(units, bool) or not isinstance(units, int) or not 1 <= units < bidders:
        raise ValueError("units must satisfy 1 <= units < n")
    return units


def _check_cents(name: str, amounts: list[int]) -> list[int]:
    for amount in amounts:
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
            raise ValueError(f"every {name} must be a non-negative whole number of cents")
    return amounts


def _ranking(bids: list[int]) -> list[int]:
    """Bidder indices from the highest bid to the lowest; a tie puts the lower index first."""
    return sorted(range(len(bids)), key=lambda i: (-bids[i], i))


def allocate(bids: list[int], units: int) -> list[bool]:
    """True for each bidder who wins a unit: the `units` highest bids, ties to the lower index."""
    _check_cents("bid", bids)
    _check_units(len(bids), units)
    winners = set(_ranking(bids)[:units])
    return [i in winners for i in range(len(bids))]


def payments(format: str, bids: list[int], units: int) -> list[int]:
    """What each bidder pays, in cents: 0 for a loser; uniform winners pay the (units+1)-th highest bid,
    discriminatory winners pay their own bid."""
    _check_format(format)
    _check_cents("bid", bids)
    _check_units(len(bids), units)
    order = _ranking(bids)
    clearing = bids[order[units]]
    result = [0] * len(bids)
    for i in order[:units]:
        result[i] = clearing if format == "uniform" else bids[i]
    return result


def revenue(format: str, bids: list[int], units: int) -> int:
    """Total payments in cents: the sum of payments(format, bids, units)."""
    return sum(payments(format, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    """(value of the winners, value of the `units` highest values), both in cents, for the allocation from bids."""
    _check_cents("value", values)
    _check_cents("bid", bids)
    if len(values) != len(bids):
        raise ValueError("values and bids must have the same length")
    _check_units(len(bids), units)
    won = sum(values[i] for i, winner in enumerate(allocate(bids, units)) if winner)
    best = sum(sorted(values, reverse=True)[:units])
    return won, best


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    """The symmetric equilibrium bid in cents for one unit: value for uniform; (n-1)/n times value, rounded half
    up, for discriminatory (first price)."""
    _check_format(format)
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be at least 2")
    _check_cents("value", [value])
    if format == "uniform":
        return value
    exact = Fraction((n - 1) * value, n)
    return math.ceil(exact - Fraction(1, 2))
