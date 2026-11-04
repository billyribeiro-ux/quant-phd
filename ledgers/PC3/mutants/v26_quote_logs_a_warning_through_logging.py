"""Student error: quote logs a debugging warning through the logging module on every turn (the spec says no function prints or warns).

Excluded from deployment (BLUEPRINT section 7): the suites are public, the reference solutions are not.
"""

from __future__ import annotations

import logging
from typing import cast

START_CENTS = 10_000
HALF_SPREAD = 10
SIZE = 1


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    logging.warning("debug: quoting turn %s around %s", state["turn"], mid)
    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    cash_flow = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
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
