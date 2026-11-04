"""Alternative 3: quotes skewed by minus one cent per unit of inventory; a replay that sums the fills.

The replay applies the cash identity to each fill: a purchase at the bid lowers cash by the bid, and a sale at the ask
raises it by the ask.
"""

from __future__ import annotations

from typing import cast

HORIZON = 20
START_CENTS = 10_000
HALF_SPREAD = 10
SIZE = 1


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    skew = -cast(int, state["inventory"])
    return mid - HALF_SPREAD + skew, mid + HALF_SPREAD + skew, SIZE


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    cash = 0
    units = 0
    for turn in turns:
        if turn["filled"] is not True:
            continue
        if turn["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, turn["fill_price_cents"])
        if price == turn["bid_cents"]:
            cash -= price
            units += 1
        else:
            cash += price
            units -= 1
    settlement = cast(int, log["settlement_cents"])
    mark = units * settlement
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
