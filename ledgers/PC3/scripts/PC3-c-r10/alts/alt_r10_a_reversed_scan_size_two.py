"""Alternative (round 10): stateless quote that scans the history backwards for the last fill and quotes size 2 when flat. Legal under the spec."""

from __future__ import annotations

from typing import cast


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in reversed(cast(list[dict[str, object]], state["history"])):
        if record["filled"] is True:
            mid = cast(int, record["fill_price_cents"])
            break
    size = 2 if state["inventory"] == 0 else 1
    return mid - 10, mid + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = cast(list[dict[str, object]], log["turns"])
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills = [r for r in turns if r["filled"] is True]
    for r in fills:
        if r["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    sides = [(1 if r["fill_price_cents"] == r["bid_cents"] else -1, cast(int, r["fill_price_cents"])) for r in fills]
    cash_flow = sum(-s * p for s, p in sides)
    inventory = sum(s for s, _ in sides)
    mark = inventory * cast(int, log["settlement_cents"])
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark,
            "pnl_cents": cash_flow + mark}
