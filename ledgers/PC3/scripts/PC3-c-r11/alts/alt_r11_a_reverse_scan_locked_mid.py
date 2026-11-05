"""Round 11 alternative: reverse scan of the history for the last fill; size 0 at the limit, otherwise size 1; replay as a fold."""

from __future__ import annotations

from functools import reduce
from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    mid = next(
        (cast(int, r["fill_price_cents"]) for r in reversed(history) if r["filled"] is True),
        10_000,
    )
    size = 0 if abs(cast(int, state["inventory"])) >= 10 else 1
    return mid - 10, mid + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    settlement = cast(int, log["settlement_cents"])

    def step(acc: tuple[int, int], record: dict[str, object]) -> tuple[int, int]:
        if record["filled"] is not True:
            return acc
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = cast(int, record["fill_price_cents"])
        side = -1 if price == record["ask_cents"] else 1
        return acc[0] - side * price, acc[1] + side

    cash_flow, inventory = reduce(step, turns, (0, 0))
    mark = inventory * settlement
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
