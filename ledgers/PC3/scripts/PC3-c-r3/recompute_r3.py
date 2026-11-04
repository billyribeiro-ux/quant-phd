"""Independent recomputation of every project.html number (verifier's own game code, from the spec text)."""
import random

H = 20
V0 = 10_000


def draws(seed, p_buy=0.25, p_sell=0.25):
    rng = random.Random(seed)
    path, arr = [V0], []
    for _ in range(H):
        path.append(path[-1] + (5 if rng.random() < 0.5 else -5))
        d = rng.random()
        if d < p_buy:
            arr.append("ub")
        elif d < p_buy + p_sell:
            arr.append("us")
        else:
            arr.append("inf")
    return path, arr


def run(seed, half=10, quote_fn=None, p_buy=0.25, p_sell=0.25, limit=10):
    path, arr = draws(seed, p_buy, p_sell)
    inv, cash, last = 0, 0, None
    log = []
    for t in range(1, H + 1):
        mid = V0 if last is None else last
        bid, ask, size = mid - half, mid + half, 1
        if quote_fn is not None:
            bid, ask, size = quote_fn(log, t, inv, cash)
        a = arr[t - 1]
        f = path[t]
        if a == "ub":
            side = -1
        elif a == "us":
            side = 1
        elif f > ask:
            side = -1
        elif f < bid:
            side = 1
        else:
            side = 0
        filled = side != 0 and size >= 1 and abs(inv + side) <= limit
        price = None
        if filled:
            price = ask if side < 0 else bid
            inv += side
            cash += -side * price
            last = price
        log.append(dict(turn=t, bid=bid, ask=ask, size=size, arr=a, filled=filled, price=price, inv=inv, cash=cash))
    return path, log, inv, cash


def account(path, log):
    cf = sum(-(1 if r["price"] == r["bid"] else -1) * r["price"] for r in log if r["filled"])
    inv = sum((1 if r["price"] == r["bid"] else -1) for r in log if r["filled"])
    mark = inv * path[H]
    return cf, inv, mark, cf + mark


path, log, inv, cash = run(0)
fills = [r for r in log if r["filled"]]
print("seed0 settlement", path[H], "fills", len(fills), [r["turn"] for r in fills])
print("seed0 fill lines:")
for r in fills:
    side = -1 if r["price"] == r["ask"] else 1
    print(f"  turn {r['turn']:2d} {'sell@ask' if side < 0 else 'buy@bid'} price {r['price']} cash_step {-side*r['price']:+d} inv {r['inv']:+d}")
cf, iv, mk, pnl = account(path, log)
print("cash_flow", cf, "inv", iv, "mark", mk, "pnl", pnl, "identity", pnl == cf + iv * path[H], "largest |inv|", max(abs(r["inv"]) for r in log))
print("cash after last == cf:", cash == cf, "last cash", log[-1]["cash"])
print("turn 5 ask", log[4]["ask"], "turn 5 price", log[4]["price"], "turn5 inv", log[4]["inv"])
print("turn 18 ask", log[17]["ask"], "turn 18 price", log[17]["price"], "turn18 inv", log[17]["inv"])
print("turn 2 bid", log[1]["bid"], "price", log[1]["price"], "turn2 inv", log[1]["inv"])
print("turn 13 ask", log[12]["ask"], "turn 7 ask", log[6]["ask"])
buys = [r["price"] for r in fills if r["price"] == r["bid"]]
sells = [r["price"] for r in fills if r["price"] == r["ask"]]
print("purchases at bid turns", [r["turn"] for r in fills if r["price"] == r["bid"]], "sum", sum(buys))
print("sales at ask turns", [r["turn"] for r in fills if r["price"] == r["ask"]], "sum", sum(sells))
print("sum check cash flow", sum(sells) - sum(buys))
# Lab 2 interpretation: mark 9990 -> pnl
print("mark 9990 pnl", cf + 1 * 9990, " mark 9980 pnl", cf + 1 * 9980)
# Lab 3 counterfactual: half-spread 15, same seed
p2, log2, inv2, cash2 = run(0, half=15)
cf2, iv2, mk2, pnl2 = account(p2, log2)
print("counterfactual half 15: fills", sum(r["filled"] for r in log2), "pnl", pnl2, "delta", pnl2 - pnl, "cf", cf2, "inv", iv2, "mark", mk2)
print("counterfactual same settlement", p2[H] == path[H], "same arrivals", draws(0)[1] == draws(0)[1])
# Round-2 check of spread 9 and 11 for sensitivity to the claim 'a wider spread would have helped'
for h in (5, 8, 9, 10, 11, 12, 15, 20):
    p3, l3, _, _ = run(0, half=h)
    c3 = account(p3, l3)
    print("half", h, "fills", sum(r["filled"] for r in l3), "pnl", c3[3])
