"""Starter for the E2 project: auction_sim.py, the sealed-bid unit auction engine.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Every money amount is an integer number of cents. Every function must validate its
inputs and raise ValueError for the conditions the specification names. No function may print or warn.
"""

from __future__ import annotations


def allocate(bids: list[int], units: int) -> list[bool]:
    """True for each bidder who wins a unit: the `units` highest bids, ties to the lower index."""
    raise NotImplementedError("allocate is not written yet")


def payments(format: str, bids: list[int], units: int) -> list[int]:
    """What each bidder pays, in cents: 0 for a loser; uniform winners pay the (units+1)-th highest bid,
    discriminatory winners pay their own bid."""
    raise NotImplementedError("payments is not written yet")


def revenue(format: str, bids: list[int], units: int) -> int:
    """Total payments in cents: the sum of payments(format, bids, units)."""
    raise NotImplementedError("revenue is not written yet")


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    """(value of the winners, value of the `units` highest values), both in cents, for the allocation from bids."""
    raise NotImplementedError("efficiency is not written yet")


def symmetric_bid_single_unit(format: str, n: int, value: int) -> int:
    """The symmetric equilibrium bid in cents for one unit: value for uniform; (n-1)/n times value, rounded half
    up, for discriminatory (first price)."""
    raise NotImplementedError("symmetric_bid_single_unit is not written yet")
