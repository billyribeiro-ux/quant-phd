"""Alternative 5 (size 2 when the last fill is more than 50 cents from 10000, otherwise 1; replay keeps one dataclass record per turn)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, Any]], state["history"])
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    size = 2 if abs(mid - 10_000) > 50 else 1
    return mid - 10, mid + 10, size


@dataclass(frozen=True)
class Fill:
    side: int
    price: int


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, Any]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills: list[Fill] = []
    for record in turns:
        if record["filled"] is True:
            if record["fill_price_cents"] is None:
                raise ValueError("a filled turn needs a fill price")
            price = int(record["fill_price_cents"])
            fills.append(Fill(1 if price == record["bid_cents"] else -1, price))
    cash_flow = sum(-f.side * f.price for f in fills)
    inventory = sum(f.side for f in fills)
    mark = inventory * int(cast(int, log["settlement_cents"]))
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
