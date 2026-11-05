"""Round 11 alternative: a dataclass record per turn; size 5 until |inventory| reaches 6, then size 0; mid from the last fill."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast


@dataclass(frozen=True)
class Record:
    filled: bool
    price: int | None
    ask: int


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = [
        Record(
            filled=cast(bool, r["filled"]) is True,
            price=cast(int | None, r["fill_price_cents"]),
            ask=cast(int, r["ask_cents"]),
        )
        for r in cast(list[dict[str, object]], state["history"])
    ]
    mid = 10_000
    for rec in history:
        if rec.filled and rec.price is not None:
            mid = rec.price
    size = 0 if abs(cast(int, state["inventory"])) >= 6 else 5
    return mid - 10, mid + 10, size


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
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
