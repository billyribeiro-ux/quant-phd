"""Starter for the PC3 project: market_maker.py, the quoting rule and the replay of a game log.

Write both functions to the contract in project.html, section "Rung 3 · Specification", then run the autograder there,
or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Money is an integer number of cents. Every input the specification names as invalid must
raise ValueError. No function may print or warn.
"""

from __future__ import annotations


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    """Return (bid_cents, ask_cents, size) for the current turn, from the state the engine passes in."""
    raise NotImplementedError("quote is not written yet")


def replay(log: dict[str, object]) -> dict[str, int]:
    """Return cash_flow_cents, inventory_end, inventory_mark_cents and pnl_cents for a game log."""
    raise NotImplementedError("replay is not written yet")
