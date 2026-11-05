"""Alternative (round 10): quote posts size 0 on turn 20 and size 1 before, with a wide 25-cent half-spread on odd turns. Legal under the spec."""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    turn = cast(int, state["turn"])
    half = 25 if turn % 2 else 10
    size = 0 if turn == 20 else 1
    return mid - half, mid + half, size


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
        side = 1 if price == record["bid_cents"] else -1
        cash_flow -= side * price
        inventory += side
    mark = inventory * settlement
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark,
            "pnl_cents": cash_flow + mark}
