"""Alternative: a class holds the mid across calls only through the state it is given (no module global)."""


class Quoter:
    def __init__(self, start: int = 10_000, half: int = 10) -> None:
        self.start = start
        self.half = half

    def mid(self, history: list) -> int:
        mid = self.start
        for record in history:
            if record["filled"] is True:
                mid = record["fill_price_cents"]
        return mid

    def quote(self, state):
        m = self.mid(state["history"])
        return m - self.half, m + self.half, 1


_QUOTER = Quoter()


def quote(state):
    return _QUOTER.quote(state)


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
