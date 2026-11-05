"""Student error: quote caches the mid it computes for each turn in a mutable default argument, and reads that cache on later games, so a game starts from the mids another game left behind.
"""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object], cache: dict[int, int] = {}) -> tuple[int, int, int]:  # noqa: B006
    turn = cast(int, state["turn"])
    if turn in cache:
        mid = cache[turn]
    else:
        mid = 10_000
        for record in cast(list[dict[str, object]], state["history"]):
            if record["filled"] is True:
                mid = cast(int, record["fill_price_cents"])
        cache[turn] = mid
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
