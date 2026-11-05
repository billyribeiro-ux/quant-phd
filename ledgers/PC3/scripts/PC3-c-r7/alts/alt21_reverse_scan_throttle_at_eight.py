"""Alternative 21: the last filled price found by a reverse scan, size zero once |inventory| reaches 8, an explicit fill list."""

from __future__ import annotations


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    history = list(state["history"])  # type: ignore[call-overload]
    mid = 10_000
    for record in reversed(history):
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])  # type: ignore[call-overload]
            break
    inventory = int(state["inventory"])  # type: ignore[call-overload]
    size = 0 if abs(inventory) >= 8 else 1
    return mid - 10, mid + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = list(log["turns"])  # type: ignore[call-overload]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    fills: list[tuple[int, int]] = []
    for record in turns:
        if record["filled"] is True:
            if record["fill_price_cents"] is None:
                raise ValueError("a filled turn needs a fill price")
            price = int(record["fill_price_cents"])  # type: ignore[call-overload]
            side = 1 if price == int(record["bid_cents"]) else -1  # type: ignore[call-overload]
            fills.append((side, price))
    units = [side for side, _ in fills]
    inventory = sum(units)
    cash_flow = sum(-side * price for side, price in fills)
    mark = inventory * int(log["settlement_cents"])  # type: ignore[call-overload]
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
