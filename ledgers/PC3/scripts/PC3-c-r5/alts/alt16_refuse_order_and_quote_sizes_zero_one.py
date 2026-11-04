"""Alternative correct solution: quotes with size 0 on turns 1 and 2, then size 5; replay checks the filled flag before the price.

Replay checks the length first, then each filled record's price, and returns exactly the four keys. Quote is a locked-free rule:
bid 9 cents below and ask 11 cents above the last fill, so the bid is always below the ask.
"""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    turn = cast(int, state["turn"])
    history = cast(list[dict[str, object]], state["history"])
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    size = 0 if turn <= 2 else 5
    return mid - 9, mid + 11, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash_flow = 0
    inventory = 0
    for record in turns:
        if not record["filled"]:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        side = -1 if cast(int, price) == record["ask_cents"] else 1
        cash_flow -= side * cast(int, price)
        inventory += side
    settlement = cast(int, log["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": inventory * settlement,
        "pnl_cents": cash_flow + inventory * settlement,
    }
