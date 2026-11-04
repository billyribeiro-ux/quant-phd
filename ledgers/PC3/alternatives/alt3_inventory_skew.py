"""Alternative 3: quotes skewed by minus one cent per unit of inventory, and a replay that reads the last cash identity."""

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
    for turn in turns:
        if turn["filled"] is True and turn["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    last = turns[-1]
    cash = cast(int, last["cash_after_cents"])
    units = cast(int, last["inventory_after"])
    settlement = cast(int, log["settlement_cents"])
    mark = units * settlement
    return {"cash_flow_cents": cash, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
