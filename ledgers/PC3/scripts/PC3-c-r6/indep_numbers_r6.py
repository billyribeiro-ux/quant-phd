"""Round-6 independent re-derivation of every number on the project page (slice c). Written from the page's conventions
and Lesson 4 wording, not from the page code. Run: python3 -I <this file>. Writes nothing into the repo."""
import random
from fractions import Fraction

H = 20
V0 = 10_000
STEP = 5
LIMIT = 10


def game(seed, half_spread):
    rng = random.Random(seed)
    # Turn t: first the fair-value move, then the arrival. Move: +5 if u<1/2 else -5. Arrival: buy u<1/4, sell u<1/2, else informed.
    fair = [V0]
    arr = []
    for t in range(H):
        u = rng.random()
        fair.append(fair[-1] + (STEP if u < Fraction(1, 2) else -STEP))
        w = rng.random()
        arr.append("buy" if w < Fraction(1, 4) else ("sell" if w < Fraction(1, 2) else "inf"))
    inv = 0
    last = None
    fills = []  # (turn, side, price)
    inv_path = []
    for t in range(1, H + 1):
        mid = V0 if last is None else last
        bid, ask = mid - half_spread, mid + half_spread
        a = arr[t - 1]
        f = fair[t]
        if a == "buy":
            side = -1
        elif a == "sell":
            side = 1
        elif f > ask:
            side = -1
        elif f < bid:
            side = 1
        else:
            side = 0
        if side != 0 and abs(inv + side) <= LIMIT:
            price = ask if side == -1 else bid
            inv += side
            last = price
            fills.append((t, side, price))
        inv_path.append(inv)
    cash = sum(-s * p for _, s, p in fills)
    settle = fair[H]
    mark = inv * settle
    return dict(fair=fair, arr=arr, fills=fills, inv_end=inv, inv_path=inv_path, cash=cash, settle=settle,
                mark=mark, pnl=cash + mark, n_fills=len(fills), max_abs_inv=max(abs(x) for x in inv_path))


ref = game(0, 10)
print("seed0 settlement", ref["settle"], "fills", ref["n_fills"], "fill turns", [t for t, _, _ in ref["fills"]])
print("cash", ref["cash"], "inv_end", ref["inv_end"], "mark", ref["mark"], "pnl", ref["pnl"], "identity", ref["pnl"] == ref["cash"] + ref["inv_end"] * ref["settle"])
print("max |inventory|", ref["max_abs_inv"], "limit ok", ref["max_abs_inv"] <= LIMIT)
print("fills (turn, side, price):", ref["fills"])
buys = [p for _, s, p in ref["fills"] if s == 1]
sells = [p for _, s, p in ref["fills"] if s == -1]
print("purchases at bid turns", [t for t, s, _ in ref["fills"] if s == 1], "sum", sum(buys))
print("sales at ask turns", [t for t, s, _ in ref["fills"] if s == -1], "sum", sum(sells), "cash = sales - purchases", sum(sells) - sum(buys))
cf = game(0, 15)
print("counterfactual half-spread 15: fills", cf["n_fills"], "pnl", cf["pnl"], "change", cf["pnl"] - ref["pnl"], "settle", cf["settle"])
print("lab1 hypothesis: fills 9? ", ref["n_fills"] == 9, " cash -9950? ", ref["cash"] == -9950, " inv 1?", ref["inv_end"] == 1,
      " settle 9980?", ref["settle"] == 9980, " pnl 30?", ref["pnl"] == 30)
print("inv path seed0:", ref["inv_path"])
# instance agreement with the page: Lesson 4 order (move then arrival), seed 0 must give the same path as the engine's instance.
import sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE6-PC3-c/course/modules/PC/PC3/grader")
import instance  # noqa: E402
inst = instance.make_instance(0)
print("instance(0) fair path equals indep path:", inst["fair_path_cents"] == ref["fair"], " arrivals equal:",
      inst["arrivals"] == [{"buy": "uninformed-buy", "sell": "uninformed-sell", "inf": "informed"}[a] for a in ref["arr"]])
paths = {tuple(instance.make_instance(s)["fair_path_cents"]) for s in range(50)}
print("distinct fixed-seed paths 0..49:", len(paths))
