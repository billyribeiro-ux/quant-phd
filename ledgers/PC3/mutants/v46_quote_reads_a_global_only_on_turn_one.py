"""Student error: quote keeps the last mid in a module global and, on turn 1 only, starts from that global instead of 10000 cents, so the first quote of a later game starts from the mid the previous game left behind.
"""

from __future__ import annotations

from typing import cast

_LAST_MID: dict[str, int] = {"mid": 10_000}


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    if state["turn"] == 1:
        mid = _LAST_MID["mid"]
    else:
        mid = 10_000
        for record in history:
            if record["filled"] is True:
                mid = cast(int, record["fill_price_cents"])
    _LAST_MID["mid"] = mid
    return mid - 10, mid + 10, 1


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
