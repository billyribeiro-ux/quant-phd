"""Alternative 24: half-spread 5 on odd turns and 15 on even turns, size one more per unit of inventory capped at 5, replay with a per-turn sign table."""

from __future__ import annotations


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    turn = int(state["turn"])  # type: ignore[call-overload]
    inventory = int(state["inventory"])  # type: ignore[call-overload]
    history = list(state["history"])  # type: ignore[call-overload]
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])  # type: ignore[call-overload]
    half = 5 if turn % 2 == 1 else 15
    size = min(5, 1 + abs(inventory))
    return mid - half, mid + half, size


_SIGN = {"uninformed-buy": -1, "uninformed-sell": 1}


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = list(log["turns"])  # type: ignore[call-overload]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = int(record["fill_price_cents"])  # type: ignore[call-overload]
        side = 1 if price == int(record["bid_cents"]) else -1  # type: ignore[call-overload]
        cash += -side * price
        inventory += side
    settlement = int(log["settlement_cents"])  # type: ignore[call-overload]
    return {"cash_flow_cents": cash, "inventory_end": inventory, "inventory_mark_cents": inventory * settlement, "pnl_cents": cash + inventory * settlement}
