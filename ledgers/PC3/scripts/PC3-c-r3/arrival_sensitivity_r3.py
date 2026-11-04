"""Sensitivity of seed-0 fills and P&L to the arrival probabilities (Exemplar B Assumptions claim, verifier's own code)."""
import random

H, V0 = 20, 10_000


def game(seed, p_buy, p_sell, half=10):
    rng = random.Random(seed)
    path, arr = [V0], []
    for _ in range(H):
        path.append(path[-1] + (5 if rng.random() < 0.5 else -5))
        d = rng.random()
        arr.append("ub" if d < p_buy else ("us" if d < p_buy + p_sell else "inf"))
    inv, cash, last, fills, cf = 0, 0, None, 0, 0
    for t in range(1, H + 1):
        mid = V0 if last is None else last
        bid, ask = mid - half, mid + half
        a = arr[t - 1]
        f = path[t]
        side = -1 if a == "ub" else (1 if a == "us" else (-1 if f > ask else (1 if f < bid else 0)))
        if side != 0 and abs(inv + side) <= 10:
            price = ask if side < 0 else bid
            inv += side
            cf += -side * price
            fills += 1
            last = price
    return fills, cf + inv * path[H]


base = game(0, 0.25, 0.25)
print("base (p_buy .25, p_sell .25): fills, pnl =", base)
for pb, ps in [(0.25, 0.25), (0.20, 0.25), (0.30, 0.25), (0.25, 0.20), (0.25, 0.30), (0.26, 0.25), (0.24, 0.25), (0.25, 0.26), (0.25, 0.24), (0.20, 0.20), (0.30, 0.30), (0.10, 0.10), (0.40, 0.40), (0.5, 0.0), (0.0, 0.5)]:
    r = game(0, pb, ps)
    print(f"p_buy {pb} p_sell {ps}: fills {r[0]} pnl {r[1]}  changed={r != base}")
# Count how many (p_buy, p_sell) grid points on a 0.01 grid change fills or P&L on seed 0
changed = 0
total = 0
for i in range(0, 51):
    for j in range(0, 51 - i):
        pb, ps = i / 100, j / 100
        total += 1
        if game(0, pb, ps) != base:
            changed += 1
print("grid points changed:", changed, "of", total)
