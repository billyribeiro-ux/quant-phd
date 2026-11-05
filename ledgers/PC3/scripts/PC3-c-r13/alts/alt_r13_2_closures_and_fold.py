"""Alternative 2 (plan 5.6 item 2): make_quoter() returns the quote closure; replay written as one fold over the turns."""

from functools import reduce


def make_quoter(half_spread: int = 10, start: int = 10_000):
    def quote(state: dict[str, object]) -> tuple[int, int, int]:
        history = state["history"]
        mid = reduce(lambda m, r: int(r["fill_price_cents"]) if r["filled"] is True else m, history, start)  # type: ignore
        return mid - half_spread, mid + half_spread, 1

    return quote


quote = make_quoter()


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:  # type: ignore[arg-type]
        raise ValueError("a log has exactly 20 turns")

    def step(acc: tuple[int, int], record: dict[str, object]) -> tuple[int, int]:
        cash, inventory = acc
        if record["filled"] is not True:
            return acc
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        side = -1 if price == record["ask_cents"] else 1
        return cash - side * int(price), inventory + side  # type: ignore[operator]

    cash_flow, inventory = reduce(step, turns, (0, 0))  # type: ignore[arg-type]
    mark = inventory * int(log["settlement_cents"])  # type: ignore[arg-type]
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
