"""Independent recomputation of the seed-0 numbers on project.html (own accounting, grader engine and reference).

Usage: python -I numbers_r16.py <grader dir>. Prints the fills, the four numbers, the counterfactual, and the
exemplar-A arithmetic (purchases, sales, cash flow, mark) so each prose number can be compared with its source.
"""
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
import engine  # noqa: E402
import reference  # noqa: E402
from instance import make_instance  # noqa: E402


def quote_with(half: int):
    def q(state):
        mid = 10_000
        for r in state["history"]:
            if r["filled"] is True:
                mid = r["fill_price_cents"]
        return mid - half, mid + half, 1

    return q


def account(log):
    cash, inv, fills = 0, 0, []
    for t in log["turns"]:
        if t["filled"]:
            p = t["fill_price_cents"]
            side = -1 if p == t["ask_cents"] else 1
            cash += -side * p
            inv += side
            fills.append((t["turn"], side, p, t["inventory_after"]))
    return cash, inv, inv * log["settlement_cents"], fills


log = engine.play(reference.quote, 0)
cash, inv, mark, fills = account(log)
print("settlement", log["settlement_cents"], "fills", len(fills), "turns", [f[0] for f in fills])
print("cash_flow", cash, "inventory_end", inv, "mark", mark, "pnl", cash + mark)
print("purchases (turn, price):", [(f[0], f[2]) for f in fills if f[1] > 0], "sum", sum(f[2] for f in fills if f[1] > 0))
print("sales (turn, price):", [(f[0], f[2]) for f in fills if f[1] < 0], "sum", sum(f[2] for f in fills if f[1] < 0))
print("largest |inventory|", max(abs(t["inventory_after"]) for t in log["turns"]))
print("ex-A turn 5 inventory_after", [f[3] for f in fills if f[0] == 5], "turn 18 inventory_after", [f[3] for f in fills if f[0] == 18])
wide = engine.play(quote_with(15), 0)
wcash, winv, wmark, wfills = account(wide)
print("counterfactual half 15: fills", len(wfills), "pnl", wcash + wmark, "change", wcash + wmark - (cash + mark))
print("fair path seed 0 move count of +5:", sum(1 for a, b in zip(make_instance(0)["fair_path_cents"], make_instance(0)["fair_path_cents"][1:]) if b > a))
print("arrival counts seed 0:", {k: make_instance(0)["arrivals"].count(k) for k in ("uninformed-buy", "uninformed-sell", "informed")})
