"""Alternative: quotes a half-spread of 10 cents and size 1, and drops to size 0 only at the limit (quote stays legal)."""


def quote(state):
    mid = 10_000
    for record in state["history"]:
        if record["filled"]:
            mid = record["fill_price_cents"]
    size = 0 if abs(state["inventory"]) >= state["limit"] else 1
    return mid - 10, mid + 10, size


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
