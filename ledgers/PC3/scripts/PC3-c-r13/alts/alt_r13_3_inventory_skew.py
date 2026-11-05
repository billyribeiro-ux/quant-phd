"""Alternative 3 (plan 5.6 item 3): inventory-skewed quotes (both sides shifted by minus one cent per unit held); replay from the cash identity."""


def quote(state: dict[str, object]) -> tuple[int, int, int]:
    mid = 10_000
    for record in state["history"]:  # type: ignore[attr-defined]
        if record["filled"] is True:
            mid = int(record["fill_price_cents"])
    skew = -int(state["inventory"])  # type: ignore[arg-type]
    return mid - 10 + skew, mid + 10 + skew, 1


def replay(log: dict[str, object]) -> dict[str, int]:
    turns = log["turns"]
    if len(turns) != 20:  # type: ignore[arg-type]
        raise ValueError("a log has exactly 20 turns")
    cash = 0
    inventory = 0
    for record in turns:  # type: ignore[attr-defined]
        if record["filled"] is not True:
            continue
        price = record["fill_price_cents"]
        if price is None:
            raise ValueError("a filled turn needs a fill price")
        if price == record["ask_cents"]:
            cash = cash + int(price)  # a sale at the ask raises cash by the ask
            inventory = inventory - 1
        else:
            cash = cash - int(price)  # a purchase at the bid lowers cash by the bid
            inventory = inventory + 1
    mark = inventory * int(log["settlement_cents"])  # type: ignore[arg-type]
    return {"cash_flow_cents": cash, "inventory_end": inventory, "inventory_mark_cents": mark, "pnl_cents": cash + mark}
