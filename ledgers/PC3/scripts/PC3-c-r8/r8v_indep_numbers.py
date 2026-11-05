"""Independent re-derivation of the seed-0 numbers on project.html (written from the page's spec text, not from the labs)."""
import random

H = 20

def path_and_arrivals(seed):
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(H):
        step = 5 if rng.random() < 0.5 else -5
        v.append(v[-1] + step)
        u = rng.random()
        arr.append("B" if u < 0.25 else ("S" if u < 0.5 else "I"))
    return v, arr

def run(seed, half):
    v, arr = path_and_arrivals(seed)
    inv, cash, last = 0, 0, None
    rows = []
    for t in range(1, H + 1):
        mid = 10000 if last is None else last
        bid, ask = mid - half, mid + half
        a = arr[t - 1]
        if a == "B":
            side = -1
        elif a == "S":
            side = 1
        elif v[t] > ask:
            side = -1
        elif v[t] < bid:
            side = 1
        else:
            side = 0
        filled = side != 0 and abs(inv + side) <= 10
        price = None
        if filled:
            price = ask if side < 0 else bid
            inv += side
            cash += -side * price
            last = price
        rows.append((t, bid, ask, filled, price, inv, cash, side))
    settle = v[H]
    cf = sum(-r[7] * r[4] for r in rows if r[3])
    mark = inv * settle
    return rows, settle, cf, inv, mark, cf + mark

rows, settle, cf, inv, mark, pnl = run(0, 10)
print("settlement", settle, "fills", sum(r[3] for r in rows))
for r in rows:
    if r[3]:
        print(" turn", r[0], "side", "sell@ask" if r[7] < 0 else "buy@bid", "price", r[4], "cf", -r[7] * r[4], "inv", r[5])
print("cash_flow", cf, "inv_end", inv, "mark", mark, "pnl", pnl, "identity", pnl == cf + inv * settle)
print("cash after last", rows[-1][6], "largest |inv|", max(abs(r[5]) for r in rows))
print("purchases at bid total", sum(r[4] for r in rows if r[3] and r[7] == 1), "sales at ask total", sum(r[4] for r in rows if r[3] and r[7] == -1))
_, _, cf2, inv2, mark2, pnl2 = run(0, 15)
print("counterfactual fills", sum(r[3] for r in run(0, 15)[0]), "pnl", pnl2, "change", pnl2 - pnl)
# arrival counts and threshold check for seed 0
v, arr = path_and_arrivals(0)
print("arrival counts", {k: arr.count(k) for k in "BSI"})
