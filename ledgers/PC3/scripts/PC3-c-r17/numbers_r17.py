"""Round 17, independent recomputation of the project's numbers (no page or twin code is imported).

Rules are re-derived from project.html's conventions: fair value starts at 10000, moves +5/-5 with probability 1/2
(draw < 0.5 is +5), arrival: draw < 0.25 uninformed buy, < 0.5 uninformed sell, else informed (same draw order:
move, then arrival, per turn). Fill rule: side from arrival or price; |inventory| after fill <= 10; size >= 1.
Fractions are not needed: all money is integer cents.
"""
import random

def game(seed):
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        v.append(v[-1] + (5 if rng.random() < 0.5 else -5))
        d = rng.random()
        arr.append("buy" if d < 0.25 else ("sell" if d < 0.5 else "inf"))
    return v, arr

def run(seed, half):
    v, arr = game(seed)
    inv, cash, last, fills = 0, 0, None, []
    for t in range(1, 21):
        mid = 10000 if last is None else last
        bid, ask = mid - half, mid + half
        a = arr[t - 1]
        if a == "buy":
            side = -1
        elif a == "sell":
            side = 1
        elif v[t] > ask:
            side = -1
        elif v[t] < bid:
            side = 1
        else:
            side = 0
        if side and abs(inv + side) <= 10:
            price = ask if side < 0 else bid
            inv += side
            cash += -side * price
            last = price
            fills.append((t, side, price))
    settle = v[20]
    mark = inv * settle
    return dict(fills=len(fills), cash=cash, inv=inv, mark=mark, pnl=cash + mark, settle=settle, fill_turns=[f[0] for f in fills])

ref = run(0, 10)
cf = run(0, 15)
print("seed0 half10:", ref)
print("seed0 half15:", cf)
print("change in pnl:", cf["pnl"] - ref["pnl"])
buys = [p for (_, s, p) in [(f[0], f[1], f[2]) for f in []]]
v, arr = game(0)
print("settlement", v[20], "path head", v[:4])
print("arrivals", arr)
