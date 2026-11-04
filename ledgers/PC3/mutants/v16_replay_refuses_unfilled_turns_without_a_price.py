"""Student error: replay checks the fill price on every turn, so an unfilled turn (price None) is refused with the named ValueError.

Excluded from deployment (BLUEPRINT section 7): the suites are public, the reference solutions are not.
"""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    return mid - 10, mid + 10, 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    cash_flow = 0
    inventory = 0
    for record in turns:
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        if record["filled"] is not True:
            continue
        price = cast(int, record["fill_price_cents"])
        side = -1 if price == record["ask_cents"] else 1
        cash_flow += -side * price
        inventory += side
    mark = inventory * settlement
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
