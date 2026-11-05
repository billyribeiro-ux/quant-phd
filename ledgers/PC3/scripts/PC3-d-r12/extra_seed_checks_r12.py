"""Seed-1 game summary (L04 E1) and seed-5/seed-6 deque operation counts (L05 Part 1, E2), re-derived. Standard library only."""
import random


def game(seed):
    rng_ = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        mv = 5 if rng_.random() < 0.5 else -5
        v.append(v[-1] + mv)
        u = rng_.random()
        arr.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    return v, arr


v1, a1 = game(1)
inv = 0
cf = 0
last = None
fills = []
for t in range(1, 21):
    mid = 10000 if last is None else last
    b_, a_ = mid - 10, mid + 10
    arr_ = a1[t - 1]
    fv = v1[t]
    side = -1 if arr_ == "ub" else (1 if arr_ == "us" else (-1 if fv > a_ else (1 if fv < b_ else 0)))
    if side != 0 and abs(inv + side) <= 10:
        price = a_ if side < 0 else b_
        cf += -side * price
        inv += side
        last = price
        fills.append(price)
print("seed 1: fills", len(fills), "cash flow", cf, "inventory", inv, "settlement", v1[20], "P&L", cf + inv * v1[20])
assert (len(fills), cf, inv, v1[20], cf + inv * v1[20]) == (16, 20100, -2, 10020, 60)


def deque_ops(xs, k):
    dq = []
    comps = pushes = removals = 0
    for i, x in enumerate(xs, 1):
        while dq:
            comps += 1
            if xs[dq[-1] - 1] <= x:
                dq.pop()
                removals += 1
            else:
                break
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:
            dq.pop(0)
            removals += 1
    return comps, pushes, removals


rng5 = random.Random(5)
xs5 = [rng5.randint(0, 999) for _ in range(200)]
rng6 = random.Random(6)
xs6 = [rng6.randint(0, 999) for _ in range(200)]
print("seed 5, window 8: comparisons, pushes, removals =", deque_ops(xs5, 8))
print("seed 6, window 8: comparisons, pushes, removals =", deque_ops(xs6, 8))
assert deque_ops(xs5, 8) == (354, 200, 199)
assert deque_ops(xs6, 8) == (350, 200, 197)
print("ALL OK")
