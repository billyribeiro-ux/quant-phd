"""Student error: replay copies the cash and the inventory from the running totals of the last filled turn, not the sum of the fills.

Excluded from deployment (BLUEPRINT section 7): the suites are public, the reference solutions are not.
"""

from __future__ import annotations

from typing import cast

START_CENTS = 10_000
HALF_SPREAD = 10
SIZE = 1


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    last: dict[str, object] | None = None
    for record in turns:
        if record["filled"] is not True:
            continue
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        last = record
    cash_flow = 0 if last is None else cast(int, last["cash_after_cents"])
    inventory = 0 if last is None else cast(int, last["inventory_after"])
    mark = inventory * settlement
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
