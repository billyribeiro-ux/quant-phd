"""Verifier round 1 (CS2-b): independent recomputation of the L08 Lab 1 seeded stream counts.
Uses a plain list of resting orders and a price-level model (a level exists while some live order sits at its
price). Shares no code with tests/labs/CS2/lab-CS2-L08-1.py.
Run: <checkout>/.venv/bin/python -I <checkout>/ledgers/CS2/scripts/CS2-b-r1/check_L08_stream.py
"""
M, C, MOD = 1103515245, 12345, 2**31
state = 20261029 % MOD


def below(n):
    global state
    state = (M * state + C) % MOD
    return (state >> 16) % n


rest = []  # dicts: oid, side, price, qty
next_id = 1
orders_added = cancels = traded_msgs = executions = 0
levels_created = levels_removed = 0
prev_levels = set()
for step in range(400):
    live = sorted(o["oid"] for o in rest)
    if live and below(100) < 25:
        oid = live[below(len(live))]
        rest = [o for o in rest if o["oid"] != oid]
        cancels += 1
    else:
        side = "B" if below(2) == 0 else "S"
        price = 10000 - 20 + below(41)
        qty = 1 + below(20)
        orders_added += 1
        opp = "S" if side == "B" else "B"
        crossing = [o for o in rest if o["side"] == opp and ((side == "B" and o["price"] <= price) or (side == "S" and o["price"] >= price))]
        if side == "B":
            crossing.sort(key=lambda o: (o["price"], o["oid"]))
        else:
            crossing.sort(key=lambda o: (-o["price"], o["oid"]))
        remaining = qty
        trades = 0
        for o in crossing:
            if remaining == 0:
                break
            f = min(remaining, o["qty"])
            o["qty"] -= f
            remaining -= f
            trades += 1
        executions += trades
        traded_msgs += trades > 0
        rest = [o for o in rest if o["qty"] > 0]
        if remaining > 0:
            rest.append({"oid": next_id, "side": side, "price": price, "qty": remaining})
        next_id += 1
    levels = {(o["side"], o["price"]) for o in rest}
    levels_created += len(levels - prev_levels)
    levels_removed += len(prev_levels - levels)
    prev_levels = levels
    # uncrossed check after every message
    bids = [o["price"] for o in rest if o["side"] == "B"]
    asks = [o["price"] for o in rest if o["side"] == "S"]
    assert not (bids and asks) or max(bids) < min(asks), step

print("orders_added", orders_added, "cancels", cancels, "total", orders_added + cancels)
print("messages_that_traded", traded_msgs, "executions", executions)
print("levels_created", levels_created, "levels_removed", levels_removed, "levels_at_end", len(prev_levels))
print("resting_orders_at_end", len(rest), "distinct_price_levels_at_end", len(prev_levels))
bids = [o["price"] for o in rest if o["side"] == "B"]
asks = [o["price"] for o in rest if o["side"] == "S"]
print("best_bid", max(bids) if bids else None, "best_ask", min(asks) if asks else None)
print("uncrossed after every message: True (asserted)")
