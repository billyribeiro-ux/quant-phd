"""Alternative 22: both sides shifted by minus the inventory in cents, size 5 on every turn, replay with a dict accumulator."""

from __future__ import annotations


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    inventory = int(state["inventory"])  # type: ignore[call-overload]
    history = list(state["history"])  # type: ignore[call-overload]
    mid = 10_000
    for record in history:
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])  # type: ignore[call-overload]
    shift = -inventory
    return mid - 10 + shift, mid + 10 + shift, 5


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = log["turns"]  # type: ignore[assignment]
    if len(turns) != 20:  # type: ignore[arg-type]
        raise ValueError("a log has exactly 20 turns")
    acc: dict[str, int] = {"cash": 0, "units": 0}
    for record in turns:  # type: ignore[attr-defined]
        if not record["filled"]:
            continue
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = int(record["fill_price_cents"])  # type: ignore[call-overload]
        if price == record["bid_cents"]:
            acc["cash"] -= price
            acc["units"] += 1
        else:
            acc["cash"] += price
            acc["units"] -= 1
    mark = acc["units"] * int(log["settlement_cents"])  # type: ignore[call-overload]
    return {"pnl_cents": acc["cash"] + mark, "inventory_mark_cents": mark, "inventory_end": acc["units"], "cash_flow_cents": acc["cash"]}
