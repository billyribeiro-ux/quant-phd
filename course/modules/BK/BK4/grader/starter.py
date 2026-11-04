"""Starter for the BK4 project: clearing_house.py.

Implement each name to the specification on the project page (section "Rung 3"), then run the autograder there, or
locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Conventions: every amount is a whole number of cents (int), and every computation is integer arithmetic. Each
function validates its inputs and raises ValueError for the conditions the page names. Nothing may print, warn or
change its arguments. Use the standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    """The result of one default, in cents: the three layers, the survivors' payments and the uncovered loss."""

    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    """Pay one loss through the CCP default waterfall. Layers in order; survivors pro rata; leftovers by id."""
    raise NotImplementedError("waterfall")


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    """The least margin whose cover is at least target_bps, from the scenario losses."""
    raise NotImplementedError("margin_for_cover")


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """The share of scenarios the margin covers in full, in basis points, floored."""
    raise NotImplementedError("cover_bps")
