"""Student error: when the cash plus the inventory marked at the last fill is at or below -30000 cents, the quote is reversed (bid above ask), so the engine refuses it."""

from __future__ import annotations

from typing import cast

START_CENTS = 10_000


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    mid = START_CENTS
    for record in history:
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    marked = cast(int, state["cash_cents"]) + cast(int, state["inventory"]) * mid
    if marked <= -30_000:
        return mid + 5, mid - 5, 1
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
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
