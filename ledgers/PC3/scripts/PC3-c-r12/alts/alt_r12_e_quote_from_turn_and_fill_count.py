"""Alternative: the mid from the fills in the history, the half-spread 10 cents, and size 1 on turns 1 to 20; empty history is a turn-1 state."""


def quote(state):
    turn = state["turn"]
    history = state["history"]
    if turn == 1 or not history:
        mid = 10_000
    else:
        filled = [r for r in history if r["filled"] is True]
        mid = filled[-1]["fill_price_cents"] if filled else 10_000
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
