"""Student error: replay computes a mean fill price by dividing by the number of fills, which raises on a log with no fills."""

from __future__ import annotations


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in state["history"]:  # type: ignore[attr-defined]
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    return mid - 10, mid + 10, 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:  # type: ignore[arg-type]
        raise ValueError("a log has exactly 20 turns")
    fills = [t for t in turns if t["filled"] is True]  # type: ignore[attr-defined]
    for t in fills:
        if t["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
    total = sum(int(t["fill_price_cents"]) for t in fills)
    mean_fill = total // len(fills)  # a statistic left in the code, never returned: raises when there are no fills
    _ = mean_fill
    cash_flow = 0
    inventory = 0
    for record in fills:
        price = int(record["fill_price_cents"])
        side = 1 if price == int(record["bid_cents"]) else -1
        cash_flow += -side * price
        inventory += side
    mark = inventory * int(log["settlement_cents"])  # type: ignore[call-overload]
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
