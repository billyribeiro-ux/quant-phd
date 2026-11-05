"""Alternative: the last filled price from a list comprehension over the history, with the 10000-cent start when none is found."""


def quote(state):
    fills = [r["fill_price_cents"] for r in state["history"] if r["filled"] is True]
    mid = fills[-1] if fills else 10_000
    return mid - 10, mid + 10, 1


def replay(log):
    turns = log["turns"]
    if len(turns) != 20:
        raise ValueError("a log has exactly 20 turns")
    settlement = log["settlement_cents"]
    cash_flow = 0
    inventory = 0
    for record in turns:
        if record["filled"] is not True:
            continue
        if record["fill_price_cents"] is None:
            raise ValueError("a filled turn needs a fill price")
        price = record["fill_price_cents"]
        side = -1 if price == record["ask_cents"] else 1
        cash_flow += -side * price
        inventory += side
    mark = inventory * settlement
    return {
        "cash_flow_cents": cash_flow,
        "inventory_end": inventory,
        "inventory_mark_cents": mark,
        "pnl_cents": cash_flow + mark,
    }
