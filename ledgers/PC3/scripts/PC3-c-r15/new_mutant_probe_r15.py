import sys, importlib.util, warnings
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
M = "/Users/billyribeiro/.fanout/wt/verifyE15-PC3-c/ledgers/PC3/mutants/"
r1 = load(M + "r15_01_replay_prints_at_ending_inventory_plus_ten.py", "r1")
r2 = load(M + "r15_02_quote_warns_on_turn_twenty_at_inventory_minus_nine.py", "r2")
r3 = load(M + "r15_03_quote_locks_the_market_on_turn_five_at_inventory_minus_one.py", "r3")
# r15_01: a log whose ending inventory is +10 (ten sales at the ask on turns 1-10)
turns = []
for t in range(1, 21):
    filled = t <= 10
    turns.append({"turn": t, "bid_cents": 9990, "ask_cents": 10010, "size": 1, "arrival": "uninformed-buy",
                  "filled": filled, "fill_price_cents": 9990 if filled else None,
                  "inventory_after": min(t, 10), "cash_after_cents": 10010 * min(t, 10)})
print("r15_01 replay:", r1.replay({"seed": 0, "settlement_cents": 10000, "turns": turns}))
# r15_02: turn 20, inventory -9, previous record filled
hist = [{"turn": t, "filled": t == 19, "fill_price_cents": 10010 if t == 19 else None} for t in range(1, 20)]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    q = r2.quote({"turn": 20, "inventory": -9, "cash_cents": 0, "max_size": 5, "limit": 10, "history": hist})
print("r15_02 quote:", q, "warnings:", [str(x.message) for x in w])
print("r15_03 quote:", r3.quote({"turn": 5, "inventory": -1, "cash_cents": 0, "max_size": 5, "limit": 10,
      "history": [{"turn": t, "filled": t == 2, "fill_price_cents": 10020 if t == 2 else None} for t in range(1, 5)]}))
