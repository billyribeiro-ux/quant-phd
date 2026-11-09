"""Correct alternative: quote finds the newest filled turn by its turn number, with no scan from the start."""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = cast(list[dict[str, object]], state["history"])
    filled = [r for r in history if r["filled"] is True]
    mid = 10_000 if not filled else cast(int, max(filled, key=lambda r: cast(int, r["turn"]))["fill_price_cents"])
    return mid - 10, mid + 10, 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills = [r for r in turns if r["filled"] is True]
    for r in fills:
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    inventory = sum(1 if r["fill_price_cents"] == r["bid_cents"] else -1 for r in fills)
    cash_flow = sum(-(1 if r["fill_price_cents"] == r["bid_cents"] else -1) * cast(int, r["fill_price_cents"]) for r in fills)
    mark = inventory * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
