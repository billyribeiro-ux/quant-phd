"""Round 11 alternative: size 2 on even turns and 1 on odd turns; a half-spread of 10 cents, with the mid moved to the last fill only after a sale; replay with a while loop."""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    mid = 10_000
    i = len(history) - 1
    while i >= 0:
        record = history[i]
        if record["filled"] is True and record["ask_cents"] == record["fill_price_cents"]:
            mid = cast(int, record["fill_price_cents"])
            break
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
            break
        i -= 1
    size = 2 if cast(int, state["turn"]) % 2 == 0 else 1
    return mid - 10, mid + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    cash_flow = 0
    inventory = 0
    i = 0
    while i < len(turns):
        record = turns[i]
        i += 1
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
