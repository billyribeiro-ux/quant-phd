"""Correct alternative: quote scans the history from the newest record and stops at the first filled one."""

from __future__ import annotations

from typing import cast

HALF = 10
UNIT = 1


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in reversed(cast(list[dict[str, object]], state["history"])):
        if record["filled"] is True:
            mid = int(cast(int, record["fill_price_cents"]))
            break
    return mid - HALF, mid + HALF, UNIT


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    counts: dict[str, int] = {"cash": 0, "inv": 0}
    for record in turns:
        if record["filled"] is not True:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        price = int(cast(int, price))
        buy = price == record["bid_cents"]
        counts["inv"] += 1 if buy else -1
        counts["cash"] += -price if buy else price
    mark = counts["inv"] * int(cast(int, log["settlement_cents"]))
    return {
        "cash_flow_cents": counts["cash"],
        "inventory_end": counts["inv"],
        "inventory_mark_cents": mark,
        "pnl_cents": counts["cash"] + mark,
    }
