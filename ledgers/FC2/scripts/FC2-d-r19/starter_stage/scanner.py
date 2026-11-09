"""Starter for the FC2 project: scanner.py, the arbitrage scanner.

Implement the three functions to the contract in project.html, section "Rung 3 · Specification", then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library only. Money is integer cents. Every function must validate its inputs and raise ValueError
for the conditions the specification names. No function may print or warn.
"""

from __future__ import annotations

from typing import Any


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    """The parity gap C - P - (S - K df) in integer cents, rounded once, a tie going toward plus infinity."""
    raise NotImplementedError("parity_gap_cents is not written yet")


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    """The interior indices j, in increasing order, at which the call lies strictly above the chord of its two
    neighbours."""
    raise NotImplementedError("convexity_violations is not written yet")


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    """One record per finding whose net amount, after the cost model, is strictly positive."""
    raise NotImplementedError("scan is not written yet")
