"""Alternative 4 (plan 5.6 item 4): size scaled down as |inventory| grows (5 when flat, 0 at the limit); replay with an explicit list accumulator."""


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in state["history"]:  # type: ignore[attr-defined]
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    inventory = abs(int(state["inventory"]))  # type: ignore[arg-type]
    size = max(0, 5 - inventory // 2)
    return mid - 10, mid + 10, size


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:  # type: ignore[arg-type]
        raise ValueError("a log has exactly 20 turns")
    sides: list[int] = []
    prices: list[int] = []
    for record in turns:  # type: ignore[attr-defined]
        if record["filled"] is True:
            price = record["fill_price_cents"]
            if price is None:
                raise ValueError("a filled turn needs a fill price")
            sides.append(-1 if price == record["ask_cents"] else 1)
            prices.append(int(price))
    cash_flow = 0
    for side, price in zip(sides, prices):
        cash_flow -= side * price
    inventory = sum(sides)
    mark = inventory * int(log["settlement_cents"])  # type: ignore[arg-type]
    return {"cash_flow_cents": cash_flow, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash_flow + mark}
