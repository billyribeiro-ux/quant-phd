"""Student error: replay ignores the logged fills and re-plays the game from log["seed"] with its own quote instead."""

from __future__ import annotations

from typing import cast

import engine

START_CENTS = 10_000
HALF_SPREAD = 10
SIZE = 1
HORIZON = 20


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    return mid - HALF_SPREAD, mid + HALF_SPREAD, SIZE


def replay(log: dict[str, object]) -> dict[str, int]:
    if len(cast(list[object], log["turns"])) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    own = engine.play(quote, cast(int, log["seed"]))
    cash_flow = 0
    inventory = 0
    for record in cast(list[dict[str, object]], own["turns"]):
        if record["filled"] is not True:
            continue
        price = cast(int, record["fill_price_cents"])
        side = -1 if price == record["ask_cents"] else 1
        cash_flow += -side * price
        inventory += side
    mark = inventory * cast(int, own["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
