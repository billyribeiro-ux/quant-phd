import engine, market_maker as sol
log = engine.play(sol.quote, 0)
fills = [(t["turn"], t["fill_price_cents"], "ask" if t["fill_price_cents"] == t["ask_cents"] else "bid", t["inventory_after"], t["cash_after_cents"], t["arrival"]) for t in log["turns"] if t["filled"]]
print("settlement", log["settlement_cents"], "nfills", len(fills))
for f in fills: print(f)
print("replay", sol.replay(log))
buys = sum(f[1] for f in fills if f[2] == "bid"); sells = sum(f[1] for f in fills if f[2] == "ask")
print("bid-fills sum", buys, "ask-fills sum", sells, "max|inv|", max(abs(t["inventory_after"]) for t in log["turns"]))
print("turn19 inv", log["turns"][18]["inventory_after"], "turn20 inv", log["turns"][19]["inventory_after"])
# counterfactual: half-spread 15 with same arrivals (engine uses same instance)
def wide(state):
    mid = 10000
    for r in state["history"]:
        if r["filled"] is True: mid = r["fill_price_cents"]
    return mid - 15, mid + 15, 1
log2 = engine.play(wide, 0)
print("wide nfills", sum(t["filled"] for t in log2["turns"]), "pnl", sol.replay(log2)["pnl_cents"], "pnl base", sol.replay(log)["pnl_cents"])
