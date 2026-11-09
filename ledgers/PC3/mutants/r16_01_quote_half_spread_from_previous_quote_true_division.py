"""Student error: the half-spread is read from the previous turn's quote with true division, so it is the float 10.0 and not the integer 10."""

from __future__ import annotations

from typing import cast

START_CENTS = 10_000
SIZE = 1


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    mid = START_CENTS
    for record in history:
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    if history:
        previous = history[-1]
        half = (cast(int, previous["ask_cents"]) - cast(int, previous["bid_cents"])) / 2
    else:
        half = 10
    return mid - half, mid + half, SIZE  # type: ignore[return-value]


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
