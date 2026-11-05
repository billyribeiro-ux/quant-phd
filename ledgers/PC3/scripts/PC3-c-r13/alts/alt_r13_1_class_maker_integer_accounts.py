"""Alternative 1 (plan 5.6 item 1): a class-based policy (class Maker, its quote method) and integer-only accounting."""

from typing import Any


class Maker:
    def __init__(self) -> None:
        self.start = 10_000

    def quote(self, state: dict[str, object]) -> tuple[int, int, int]:
        mid = self.start
        for record in state["history"]:  # type: ignore[attr-defined]
            if record["filled"] is True:
                mid = int(record["fill_price_cents"])
        return mid - 10, mid + 10, 1


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    return Maker().quote(state)


def replay(log: dict[str, object]) -> dict[str, int]:
    turns: list[dict[str, Any]] = log["turns"]  # type: ignore[assignment]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    cash = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        if price == record["ask_cents"]:
            cash += int(price)
            inventory -= 1
        else:
            cash -= int(price)
            inventory += 1
    mark = inventory * int(log["settlement_cents"])  # type: ignore[arg-type]
    return {"cash_flow_cents": cash, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
