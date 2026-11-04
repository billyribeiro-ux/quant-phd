"""Alternative 4: the quoted size falls as |inventory| grows, to 0 at the limit, and a replay with an explicit list."""

from __future__ import annotations

from typing import cast

HORIZON = 20
START_CENTS = 10_000
HALF_SPREAD = 10
MAX_SIZE = 5
LIMIT = 10


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = START_CENTS
    for record in cast(list[dict[str, object]], state["history"]):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
    inventory = abs(cast(int, state["inventory"]))
    size = max(0, MAX_SIZE * (LIMIT - inventory) // LIMIT)
    return mid - HALF_SPREAD, mid + HALF_SPREAD, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != HORIZON:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])
    fills: list[tuple[int, int]] = []
    for turn in turns:
        if turn["filled"] is not True:
            continue
        if turn["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, turn["fill_price_cents"])
        side = -1 if price == turn["ask_cents"] else 1
        fills.append((side, price))
    cash_flow = sum(-side * price for side, price in fills)
    units = sum(side for side, _ in fills)
    mark = units * settlement
    return {"cash_flow_cents": cash_flow, "inventory_end": units, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
