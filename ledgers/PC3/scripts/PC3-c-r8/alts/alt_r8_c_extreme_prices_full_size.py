"""Correct alternative: bid 1 and ask 20000 on every turn with size 5 (legal extreme prices), reduced replay via fold."""

from __future__ import annotations

from functools import reduce
from typing import Any


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    return 1, 20_000, 5


def replay(log: dict[str, Any]) -> dict[str, int]:
    if len(log["turns"]) != 20:
        raise ValueError("a log has exactly 20 turns")

    def step(acc: tuple[int, int], t: dict[str, Any]) -> tuple[int, int]:
        if t["filled"] is not True:
            return acc
        if t["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        side = 1 if t["fill_price_cents"] == t["bid_cents"] else -1
        return acc[0] - side * int(t["fill_price_cents"]), acc[1] + side

    cash, inv = reduce(step, log["turns"], (0, 0))
    mark = inv * int(log["settlement_cents"])
    return {"cash_flow_cents": cash, "inventory_end": inv, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
