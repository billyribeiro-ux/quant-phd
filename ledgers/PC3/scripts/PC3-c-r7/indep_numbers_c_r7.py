"""Independent re-derivation of the project page's numbers from the stated rules (Conventions, Required outputs),
written without reading the page's code. Run with python -I -W error."""

import random

N = 20
V0 = 10_000
MOVE = 5
LIMIT = 10
SIZE = 1


def path_and_arrivals(seed):
    rng = random.Random(seed)
    v = [V0]
    arr = []
    for _ in range(N):
        v.append(v[-1] + (MOVE if rng.random() < 0.5 else -MOVE))
        u = rng.random()
        arr.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    return v, arr


def run(seed, half):
    v, arr = path_and_arrivals(seed)
    inv = 0
    cash = 0
    last = None
    fills = []
    maxabs = 0
    for t in range(1, N + 1):
        mid = V0 if last is None else last
        bid, ask = mid - half, mid + half
        a = arr[t - 1]
        if a == "ub":
            side = -1
        elif a == "us":
            side = 1
        elif v[t] > ask:
            side = -1
        elif v[t] < bid:
            side = 1
        else:
            side = 0
        if side and abs(inv + side) <= LIMIT:
            price = ask if side < 0 else bid
            inv += side
            cash += -side * price
            last = price
            fills.append((t, side, price))
        maxabs = max(maxabs, abs(inv))
    settle = v[N]
    mark = inv * settle
    return {"fills": len(fills), "cash": cash, "inv": inv, "settle": settle, "mark": mark,
            "pnl": cash + mark, "maxabs": maxabs, "fill_turns": [t for t, _, _ in fills], "path": v}


r10 = run(0, 10)
r15 = run(0, 15)
print("seed0 half10:", {k: r10[k] for k in ("fills", "cash", "inv", "settle", "mark", "pnl", "maxabs")})
print("seed0 fill turns:", r10["fill_turns"])
purch = [p for t, s, p in [(t, s, p) for (t, s, p) in []]]
print("seed0 half15:", {k: r15[k] for k in ("fills", "cash", "inv", "settle", "mark", "pnl", "maxabs")})
print("counterfactual change pnl:", r15["pnl"] - r10["pnl"])
ex_bid_sum = 9990 + 9980 + 9970 + 9980 + 9990
ex_ask_sum = 9980 + 9990 + 9990 + 10000
print("exemplar A sums: bids 9990+9980+9970+9980+9990 =", ex_bid_sum, " asks 9980+9990+9990+10000 =", ex_ask_sum, " cash", ex_ask_sum - ex_bid_sum)
print("exemplar A identity: 30 == -9950 + 1*9980:", 30 == -9950 + 1 * 9980)
paths = {tuple(path_and_arrivals(s)[0]) for s in range(50)}
print("distinct fixed-seed paths 0..49:", len(paths))
mx = [run(s, 10)["maxabs"] for s in range(50)]
print("largest |inventory| over seeds 0..49 with reference rule: max", max(mx))
