"""Starter for the FC1 project: instruments.py.

Implement each name to the specification on the project page (section "Rung 3"), then run the autograder there, or
locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Conventions: money is a whole number of cents (int), periods are whole numbers from 1, and rates are basis points
(int). Every object validates its inputs and raises ValueError for the conditions the page names. On the inputs the
suite checks for silence, nothing prints or warns. Use the standard library only.
"""

from __future__ import annotations


class Bond:
    """Fixed-rate bond: face_cents, coupon_bps (per period, of face), periods. Implement events() and the checks."""

    def __init__(self, face_cents: int, coupon_bps: int, periods: int) -> None:
        raise NotImplementedError("Bond")

    def events(self) -> list[tuple[int, int]]:
        """(period, amount_cents) for periods 1..periods, sorted by period, from the holder's side."""
        raise NotImplementedError("Bond.events")


def bond_price_cents(bond: Bond, yield_bps: int) -> int:
    """Present value of the bond's events at a per-period yield, in whole cents, rounded once."""
    raise NotImplementedError("bond_price_cents")


class CashTrade:
    """A trade in a cash instrument: quantity, price_cents per unit, side (+1 buy, -1 sell), settlement_day."""

    def __init__(self, quantity: int, price_cents: int, side: int, settlement_day: int) -> None:
        raise NotImplementedError("CashTrade")

    def events(self) -> list[tuple[int, int]]:
        """One (settlement_day, amount_cents) event, from the holder's side."""
        raise NotImplementedError("CashTrade.events")
