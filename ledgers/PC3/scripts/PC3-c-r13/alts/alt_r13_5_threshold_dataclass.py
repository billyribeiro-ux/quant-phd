"""Alternative 5 (plan 5.6 item 5): threshold quoting (quote only when the spread is at least 10 cents, else size 0); replay with a dataclass record per turn."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Turn:
    bid: int
    ask: int
    price: int | None
    filled: bool


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in state["history"]:  # type: ignore[attr-defined]
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    bid, ask = mid - 10, mid + 10
    size = 1 if ask - bid >= 10 else 0
    return bid, ask, size


def replay(log: dict[str, object]) -> dict[str, int]:
    raw = log["turns"]
    if len(raw) != 20:  # type: ignore[arg-type]
        raise ValueError("a log has exactly 20 turns")
    turns = [Turn(int(r["bid_cents"]), int(r["ask_cents"]), r["fill_price_cents"], r["filled"] is True) for r in raw]  # type: ignore[attr-defined]
    cash = 0
    inventory = 0
    for t in turns:
        if not t.filled:
            continue
        if t.price is None:
            raise ValueError("a filled turn needs a fill price")
        side = -1 if int(t.price) == t.ask else 1
        cash -= side * int(t.price)
        inventory += side
    mark = inventory * int(log["settlement_cents"])  # type: ignore[arg-type]
    return {"cash_flow_cents": cash, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
