"""Starter for the E1 project: market_structure.py.

Implement outcome() to the specification on the project page (section "Rung 3 · Specification"), then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Conventions: a, b and c are whole numbers with a > b*c > 0; b is in trades per (cent per trade) and c in cents per
trade. Every money key is an int in cents and each is rounded once, a tie going up, from its exact value. Raise
ValueError for the named conditions. Print nothing and warn nothing. Use the standard library only.
"""

from __future__ import annotations


def outcome(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    """The six outputs of one market structure, all as int: volume_trades, fee_cents, profit_cents,
    consumer_surplus_cents, welfare_cents and deadweight_loss_cents."""
    raise NotImplementedError("outcome")
