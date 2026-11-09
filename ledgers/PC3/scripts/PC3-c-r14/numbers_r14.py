"""Independent recomputation of the project's reference numbers (seed 0), from the Conventions alone.

It does not import the course engine. It uses only the fair path and arrivals, which the page says come from
grader/instance.py, and re-implements the trade rules and the replay from the page text.
"""
import random
import sys

sys.path.insert(0, sys.argv[1] + "/course/modules/PC/PC3/grader")
import instance  # only the fair path / arrival generator (SIMULATED), see instance.py docstring

HALF = {"ref": 10, "cf": 15}


def game(seed, half):
    inst = instance.make_instance(seed)
    path, arr = inst["fair_path_cents"], inst["arrivals"]
    mid, inv, cash, fills, rows = 10_000, 0, 0, [], []
    for t in range(1, 21):
        bid, ask, size = mid - half, mid + half, 1
        a = arr[t - 1]
        v = path[t]
        if a == "uninformed-buy":
            side = -1
        elif a == "uninformed-sell":
            side = 1
        elif v > ask:
            side = -1
        elif v < bid:
            side = 1
        else:
            side = 0
        filled = side != 0 and size >= 1 and abs(inv + side) <= 10
        if filled:
            price = ask if side == -1 else bid
            inv += side
            cash += -side * price
            fills.append((t, side, price, inv, cash))
            mid = price
        rows.append((t, bid, ask, a, filled))
    settlement = path[20]
    mark = inv * settlement
    return dict(fills=fills, cash_flow=cash, inv=inv, mark=mark, pnl=cash + mark, settlement=settlement,
                max_abs_inv=max(abs(f[3]) for f in fills) if fills else 0, rows=rows)


ref = game(0, HALF["ref"])
cf = game(0, HALF["cf"])
print("ref fills", len(ref["fills"]), "cash_flow", ref["cash_flow"], "inv", ref["inv"], "mark", ref["mark"],
      "pnl", ref["pnl"], "settlement", ref["settlement"], "max|inv|", ref["max_abs_inv"])
for f in ref["fills"]:
    print("  turn %2d side %+d price %d inv_after %d cash_after %d" % (f[0], f[1], f[2], f[3], f[4]))
print("cf fills", len(cf["fills"]), "pnl", cf["pnl"], "change", cf["pnl"] - ref["pnl"])
print("ref turn-2 row", ref["rows"][1], "turn-5 fill", [f for f in ref["fills"] if f[0] == 5])
print("ref identity", ref["pnl"] == ref["cash_flow"] + ref["inv"] * ref["settlement"])
