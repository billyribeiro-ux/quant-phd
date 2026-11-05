"""Correct alternative: mid is the midpoint of the previous turn's quote (not the last fill), half-spread 10, size 1."""

from __future__ import annotations

from typing import Any


def quote(state: dict[str, Any]) -> tuple[int, int, int]:
    if not state["history"]:
        mid = 10_000
    else:
        last = state["history"][-1]
        mid = (int(last["bid_cents"]) + int(last["ask_cents"])) // 2
    return mid - 10, mid + 10, 1


def replay(log: dict[str, Any]) -> dict[str, int]:
    if len(log["turns"]) != 20:
        raise ValueError("a log has exactly 20 turns")
    net = 0
    inv = 0
    for t in log["turns"]:
        if t["filled"] is True:
            if t["fill_price_cents"] is None:
                raise ValueError("a filled turn needs a fill price")
            if t["fill_price_cents"] == t["ask_cents"]:
                net += int(t["fill_price_cents"])
                inv -= 1
            else:
                net -= int(t["fill_price_cents"])
                inv += 1
    mark = inv * int(log["settlement_cents"])
    return {"cash_flow_cents": net, "inventory_end": inv, "inventory_mark_cents": mark, "pnl_cents": net + mark}
