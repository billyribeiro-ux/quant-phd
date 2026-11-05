"""Round 10 verifier: independent recomputation of every number the PC3 project page states about seed 0 (Labs 1-3,
exemplars A and B, the rubric example). Written from the page's rules, not from the lab code. Stdlib only."""

import random

HORIZON, START, MOVE, LIMIT = 20, 10_000, 5, 10


def game(seed: int, half: int):
    rng = random.Random(seed)
    path = [START]
    arr = []
    for _ in range(HORIZON):
        path.append(path[-1] + (MOVE if rng.random() < 0.5 else -MOVE))
        d = rng.random()
        arr.append("ub" if d < 0.25 else ("us" if d < 0.5 else "inf"))
    last = None
    inv = 0
    cash = 0
    rows = []
    for t in range(1, HORIZON + 1):
        mid = START if last is None else last
        bid, ask = mid - half, mid + half
        a = arr[t - 1]
        if a == "ub":
            side = -1
        elif a == "us":
            side = 1
        elif path[t] > ask:
            side = -1
        elif path[t] < bid:
            side = 1
        else:
            side = 0
        filled = side != 0 and abs(inv + side) <= LIMIT
        price = None
        if filled:
            price = ask if side < 0 else bid
            inv += side
            cash += -side * price
            last = price
        rows.append(dict(t=t, bid=bid, ask=ask, filled=filled, price=price, side=side, inv=inv, cash=cash))
    return path[HORIZON], rows


def account(settle, rows):
    fills = [r for r in rows if r["filled"]]
    cf = sum(-r["side"] * r["price"] for r in fills)
    inv = sum(r["side"] for r in fills)
    return dict(fills=len(fills), cash_flow=cf, inv_end=inv, mark=inv * settle, pnl=cf + inv * settle,
                largest=max(abs(r["inv"]) for r in rows))


settle, rows = game(0, 10)
print("reference seed 0:", account(settle, rows))
print("fill turns:", [r["t"] for r in rows if r["filled"]])
print("fill sides/prices:", [(r["t"], "buy@bid" if r["side"] > 0 else "sell@ask", r["price"]) for r in rows if r["filled"]])
buys = [r for r in rows if r["filled"] and r["side"] > 0]
sells = [r for r in rows if r["filled"] and r["side"] < 0]
print("purchases at bid turns", [r["t"] for r in buys], "total", sum(r["price"] for r in buys))
print("sales at ask turns", [r["t"] for r in sells], "total", sum(r["price"] for r in sells))
t2 = rows[1]
t5 = rows[4]
t18 = rows[17]
print("turn 2 bid, fill:", t2["bid"], t2["price"], "| turn 5 ask, fill, inv after:", t5["ask"], t5["price"], t5["inv"],
      "| turn 18 ask, fill, inv after:", t18["ask"], t18["price"], t18["inv"])
s15, rows15 = game(0, 15)
print("counterfactual half 15:", account(s15, rows15))
print("change:", account(s15, rows15)["pnl"] - account(settle, rows)["pnl"])
print("settlement:", settle)
print("identity 30 = -9950 + 1 x 9980:", -9950 + 1 * 9980 == 30)
print("exemplar B: P&L 30 and cash flow -9950 from replay; turn 5 ask 9980 fill 9980:", t5["ask"] == 9980 and t5["price"] == 9980)
