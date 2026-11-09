"""Independent recomputation of the project's printed numbers (Labs 1 and 3) from the engine and the instance.

Run as: python -I ledgers/PC3/scripts/PC3-c-r14/numbers_check.py <checkout-root>
Nothing here reads the page's expected blocks; it prints the values, and the verifier compares them to the page text.
"""
import sys
from fractions import Fraction

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/PC/PC3/grader")
import engine  # noqa: E402
from instance import make_instance  # noqa: E402

# Independent oracle (not the reference module): accounts from the fills alone.
def accounts(log):
    cash = 0
    inv = 0
    for t in log["turns"]:
        if t["filled"]:
            p = t["fill_price_cents"]
            side = 1 if p == t["bid_cents"] else -1
            cash += -side * p
            inv += side
    return cash, inv, inv * log["settlement_cents"], cash + inv * log["settlement_cents"]

def rule(half):
    def q(state):
        mid = 10_000
        for r in state["history"]:
            if r["filled"]:
                mid = r["fill_price_cents"]
        return mid - half, mid + half, 1
    return q

inst = make_instance(0)
ref = engine.play(rule(10), 0)
wid = engine.play(rule(15), 0)
print("instance seed0 path head", inst["fair_path_cents"][:6], "settlement", inst["settlement_cents"])
print("lab1 settlement", ref["settlement_cents"], "fills", sum(t["filled"] for t in ref["turns"]))
c, i, m, p = accounts(ref)
print("reference cash_flow", c, "inventory_end", i, "mark", m, "pnl", p)
print("reference max |inventory|", max(abs(t["inventory_after"]) for t in ref["turns"]))
print("reference fill turns", [t["turn"] for t in ref["turns"] if t["filled"]])
buys = [t["fill_price_cents"] for t in ref["turns"] if t["filled"] and t["fill_price_cents"] == t["bid_cents"]]
sells = [t["fill_price_cents"] for t in ref["turns"] if t["filled"] and t["fill_price_cents"] == t["ask_cents"]]
print("maker purchases at bid", buys, sum(buys), "maker sales at ask", sells, sum(sells))
cw, iw, mw, pw = accounts(wid)
print("wider(15) fills", sum(t["filled"] for t in wid["turns"]), "cash", cw, "inv", iw, "pnl", pw, "delta", pw - p)
print("identity ref", p == c + i * ref["settlement_cents"], "identity wid", pw == cw + iw * wid["settlement_cents"])
for t in ref["turns"]:
    if t["turn"] in (2, 5, 18):
        print("turn", t["turn"], "bid", t["bid_cents"], "ask", t["ask_cents"], "fill", t["fill_price_cents"], "inv_after", t["inventory_after"])
print("exact P&L fraction", Fraction(p))
print("exemplar A identity", 30 == -9950 + 1 * 9980, "sums", 49910 - 39960 == 9950, 39960 - 49910)
