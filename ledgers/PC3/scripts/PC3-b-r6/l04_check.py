"""Independent check of L04 numbers (PC3-b round 6). Re-implements the game from the page text, not from the lab.

Draw order per page/lab docstring: per turn, one uniform for the move (<0.5 means +5), one for the arrival
(<0.25 uninformed buy, <0.5 uninformed sell, else informed). Uses only the standard library.
"""

import random
from fractions import Fraction as F

def play(seed):
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        v.append(v[-1] + (5 if rng.random() < 0.5 else -5))
        u = rng.random()
        arr.append("B" if u < 0.25 else ("S" if u < 0.5 else "I"))
    inv, cash, last = 0, 0, None
    fills = []
    for t in range(1, 21):
        m = 10000 if last is None else last
        bid, ask = m - 10, m + 10
        a = arr[t - 1]
        if a == "B":
            side = -1
        elif a == "S":
            side = +1
        else:
            side = -1 if v[t] > ask else (+1 if v[t] < bid else 0)
        if side != 0 and abs(inv + side) <= 10:
            price = ask if side < 0 else bid
            cash += -side * price
            inv += side
            last = price
            fills.append((t, price, -side * price))
    settle = v[20]
    cf = sum(x[2] for x in fills)
    pnl = cash + inv * settle
    return dict(fills=len(fills), cash_flow=cf, inv=inv, settle=settle, mark=inv * settle, pnl=pnl,
                arrivals_informed=arr.count("I"), arr=arr, v=v)

r0 = play(0)
r1 = play(1)
print("seed0", {k: r0[k] for k in ("fills", "cash_flow", "inv", "settle", "mark", "pnl", "arrivals_informed")})
print("seed1", {k: r1[k] for k in ("fills", "cash_flow", "inv", "settle", "mark", "pnl")})
# E2: informed share 13/20 of seed 0 arrivals, two-sided z under p=1/2
se = (0.25 / 20) ** 0.5
print("E2 se", round(se, 4), "z", round((13 / 20 - 0.5) / se, 4))
# Prop 3.1 closed form vs brute enumeration, p=1/2, quote 9990/10010, inventory 0, all v in 9950..10050
def E(v, a, b, p=F(1, 2)):
    tot = F(0)
    for prob, side in ((F(1, 4), -1), (F(1, 4), +1)):
        price = a if side < 0 else b
        tot += prob * (-side * price + side * v)
    if v > a:
        tot += p * (a - v)
    elif v < b:
        tot += p * (v - b)
    return tot
def closed(v, a, b, p=F(1, 2)):
    h = F(a - b, 2)
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))
bad = [v for v in range(9900, 10101) if E(v, 10010, 9990) != closed(v, 10010, 9990)]
print("Prop3.1 general p=1/2 mismatches over 9900..10100:", bad)
for p in (F(1, 3), F(3, 5), F(1, 1), F(0, 1)):
    bad = [v for v in range(9900, 10101) if E(v, 10010, 9990, p) != closed(v, 10010, 9990, p)]
    print("p", p, "mismatches", len(bad))
print("Example 3.2 values", [str(E(v, 10010, 9990)) for v in (10000, 10020, 9985)])
print("R1 d at p=3/5 h=10:", F(2, 5) * 10 / F(3, 5), float(F(2, 5) * 10 / F(3, 5)))
print("E3 pnl settle/mid:", -9950 + 1 * 9980, -9950 + 1 * 9990)
print("Remark 4.2 sd I=3:", 5 * 3, "I=10:", 5 * 10)
print("Remark 4.2 I=10 trade term, buy only:", F(1, 4) * 10)
print("seed0 last mid", (r0["v"][20]), "last quote mid check")
