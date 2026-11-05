"""Round 12 probe: reachability of rare branches in the window (seeds 0-49) under the reference quote, through the checkout's engine."""
import sys, collections
sys.path.insert(0, sys.argv[1])
import engine, instance
import market_maker as reference
settle = {}
inv_hits = collections.Counter()
maxabs = 0
fill_prices = set()
for s in range(50):
    log = engine.play(reference.quote, s)
    settle[s] = log["settlement_cents"]
    inv = 0
    for t in log["turns"]:
        if t["filled"]:
            inv += 1 if t["fill_price_cents"] == t["bid_cents"] else -1
            fill_prices.add(t["fill_price_cents"])
        maxabs = max(maxabs, abs(inv))
        inv_hits[inv] += 1
print("settlement min", min(settle.values()), "max", max(settle.values()), "count==10000", sum(v == 10000 for v in settle.values()))
print("inventory values reached in games (after each turn):", sorted(inv_hits))
print("max |inventory| in games", maxabs)
print("fill price range", min(fill_prices), max(fill_prices))
