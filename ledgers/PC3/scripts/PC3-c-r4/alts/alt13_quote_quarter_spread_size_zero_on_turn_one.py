"""Alt13: quarter-spread (2 cents half-spread) quote, size 0 on turn one only; replay through a closure and a fold."""

from __future__ import annotations

from functools import reduce
from typing import Any, cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, Any]], state["history"])
    last = next((r["fill_price_cents"] for r in reversed(history) if r["filled"]), None)
    mid = 10_000 if last is None else int(last)
    size = 0 if cast(int, state["turn"]) == 1 else 1
    return mid - 2, mid + 2, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")

    def step(acc: tuple[int, int], r: dict[str, Any]) -> tuple[int, int]:
        if not r["filled"]:
            return acc
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = int(r["fill_price_cents"])
        side = 1 if price == r["bid_cents"] else -1
        return acc[0] - side * price, acc[1] + side

    cash_flow, inventory = reduce(step, turns, (0, 0))
    mark = inventory * int(log["settlement_cents"])
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
