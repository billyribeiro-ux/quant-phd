"""Correct alternative: replay uses a dataclass-free accumulator with an explicit int() on every money value."""

from __future__ import annotations

from typing import Any, cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    history: list[Any] = list(cast(list[Any], state["history"]))
    last_fill = [r["fill_price_cents"] for r in history if r["filled"] is True]
    if last_fill:
        mid = int(last_fill[-1])
    return int(mid - 10), int(mid + 10), int(1)


def replay(log: dict[str, object]) -> dict[str, int]:
    turns: list[Any] = list(cast(list[Any], log["turns"]))
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    total = {"cash": 0, "inventory": 0}
    for record in turns:
        if not record["filled"]:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        buys = int(price) == int(record["bid_cents"])
        total["inventory"] += 1 if buys else -1
        total["cash"] += -int(price) if buys else int(price)
    settlement = int(cast(int, log["settlement_cents"]))
    mark = total["inventory"] * settlement
    return {
        "cash_flow_cents": int(total["cash"]),
        "inventory_end": int(total["inventory"]),
        "inventory_mark_cents": int(mark),
        "pnl_cents": int(total["cash"] + mark),
    }
