"""Student error: replay takes the side of an uninformed fill from its arrival name, and the side of an informed fill from its price.

Excluded from deployment (BLUEPRINT section 7): the suites are public, the reference solutions are not.

``quote`` posts a symmetric quote around the last filled price, or around 10000 cents before any fill. The
half-spread is 10 cents and the size is 1 unit. ``replay`` recomputes the cash flow and the inventory from the fills
of a log, and marks the ending inventory at the settlement value. Money is an integer number of cents throughout.
"""

from __future__ import annotations

from typing import cast

START_CENTS = 10_000  # v_0, in cents: the mid before any fill
HALF_SPREAD = 10  # cents on each side of the mid
SIZE = 1  # units quoted on each side
HORIZON = 20  # turns in a log


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    """The symmetric quote around the last filled price, or around 10000 cents before any fill: (bid, ask, size)."""
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE


def replay(log: dict[str, object]) -> dict[str, int]:
    """Replay the fills of a log: the cash flow, the ending inventory, the inventory mark and the P&L, all in cents."""
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != HORIZON:
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
        arrival = record["arrival"]
        if arrival == "uninformed-buy":
            side = -1
        elif arrival == "uninformed-sell":
            side = 1
        else:
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
