"""Round 2, slice c: independent recomputation of every number on project.html (no imports from the course).

Usage (checkout root): .venv/bin/python -I ledgers/PC3/scripts/PC3-c-r2/recompute_r2.py
"""

from __future__ import annotations

import random
from fractions import Fraction

START = 10_000
MOVE = 5
HALF = 10
LIMIT = 10
HORIZON = 20


def game(seed: int) -> tuple[list[int], list[str]]:
    # Independent draw order: per turn, one move draw then one arrival draw (the Lesson 4 order).
    rng = random.Random(seed)
    path = [START]
    arrivals = []
    for _ in range(HORIZON):
        path.append(path[-1] + (MOVE if rng.random() < 0.5 else -MOVE))
        u = rng.random()
        arrivals.append("UB" if u < 0.25 else ("US" if u < 0.5 else "IN"))
    return path, arrivals


def run(seed: int, half: int, quote_fn=None):
    path, arrivals = game(seed)
    inv = 0
    cash = 0
    last = None
    fills = []
    rows = []
    max_abs = 0
    for t in range(1, HORIZON + 1):
        mid = START if last is None else last
        bid, ask, size = mid - half, mid + half, 1
        a = arrivals[t - 1]
        if a == "UB":
            side = -1
        elif a == "US":
            side = 1
        elif path[t] > ask:
            side = -1
        elif path[t] < bid:
            side = 1
        else:
            side = 0
        filled = side != 0 and size >= 1 and abs(inv + side) <= LIMIT
        price = None
        if filled:
            price = ask if side < 0 else bid
            inv += side
            cash += -side * price
            last = price
            fills.append((t, side, price))
            max_abs = max(max_abs, abs(inv))
        rows.append((t, bid, ask, a, filled, price, inv, cash))
    settle = path[HORIZON]
    cash_flow = sum(-s * p for _, s, p in fills)
    inv_end = sum(s for _, s, _ in fills)
    mark = inv_end * settle
    return {
        "path": path,
        "arrivals": arrivals,
        "fills": fills,
        "rows": rows,
        "settle": settle,
        "cash_flow": cash_flow,
        "inv_end": inv_end,
        "mark": mark,
        "pnl": cash_flow + mark,
        "max_abs": max_abs,
        "n_fills": len(fills),
    }


def main() -> None:
    ref = run(0, HALF)
    print("check1 seed0 reference:", "settle", ref["settle"], "fills", ref["n_fills"], "cash", ref["cash_flow"],
          "inv", ref["inv_end"], "mark", ref["mark"], "pnl", ref["pnl"], "max|inv|", ref["max_abs"])
    print("fill turns:", [t for t, _, _ in ref["fills"]])
    print("fill prices:", [(t, "sale" if s < 0 else "purchase", p) for t, s, p in ref["fills"]])
    sales_at_ask = [t for t, s, p in ref["fills"] if s < 0]
    purch = [p for t, s, p in ref["fills"] if s > 0]
    sales = [p for t, s, p in ref["fills"] if s < 0]
    print("sales at ask: count", len(sales_at_ask), "turns", sales_at_ask, "sum", sum(sales))
    print("purchases at bid: sum", sum(purch), "count", len(purch))
    wide = run(0, 15)
    print("check3 counterfactual half 15: fills", wide["n_fills"], "pnl", wide["pnl"], "delta", wide["pnl"] - ref["pnl"])
    # Lab 2 interpretation: quote at the last turn and the mid
    last_mid_t20 = ref["rows"][-1][1:3]
    print("turn-20 quote (bid, ask):", last_mid_t20, "mid", sum(last_mid_t20) / 2)
    # alternative marks for ending inventory 1
    for m in (9980, 9990, 9990 + 0):
        print("mark at", m, "pnl", ref["cash_flow"] + ref["inv_end"] * m)
    # Lab 3 with the stated half-spreads on other seeds, for context only (not claimed in the page)
    # Instance match: lab draw order vs grader instance order, same algorithm; compare with counts of distinct paths
    paths = {tuple(game(s)[0]) for s in range(0, 20)}
    print("distinct paths seeds 0..19:", len(paths))
    print("arrival counts seed0:", {k: ref["arrivals"].count(k) for k in ("UB", "US", "IN")})
    print("settlement mid rule check: Fraction(sum of bid, ask)/2 for turn 20:", Fraction(sum(last_mid_t20), 2))


if __name__ == "__main__":
    main()
