"""Check the grader's make_instance against the independent generator of indep_numbers_c_r7.py for seeds 0-49, and
the engine's play against the independent run for the reference rule (10 cents) on seeds 0-49."""
import sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE7-PC3-c/course/modules/PC/PC3/grader")
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE7-PC3-c/ledgers/PC3/scripts/PC3-c-r7")
import importlib.util
spec = importlib.util.spec_from_file_location("ind", "/Users/billyribeiro/.fanout/wt/verifyE7-PC3-c/ledgers/PC3/scripts/PC3-c-r7/indep_numbers_c_r7.py")
ind = importlib.util.module_from_spec(spec)
src = open(spec.origin).read().split("r10 = run(0, 10)")[0]
exec(compile(src, "ind", "exec"), ind.__dict__)
import instance, engine
bad_inst = 0
bad_play = 0
def ref_quote(state):
    mid = 10000
    for r in state["history"]:
        if r["filled"] is True:
            mid = r["fill_price_cents"]
    return mid - 10, mid + 10, 1
for s in range(50):
    v, arr = ind.path_and_arrivals(s)
    inst = instance.make_instance(s)
    m = {"ub": "uninformed-buy", "us": "uninformed-sell", "inf": "informed"}
    if inst["fair_path_cents"] != v or inst["arrivals"] != [m[a] for a in arr]:
        bad_inst += 1
    log = engine.play(ref_quote, s)
    r = ind.run(s, 10)
    got = (sum(1 for t in log["turns"] if t["filled"]), sum(-(1 if t["fill_price_cents"] == t["bid_cents"] else -1) * t["fill_price_cents"] for t in log["turns"] if t["filled"]))
    if got[0] != r["fills"] or got[1] != r["cash"]:
        bad_play += 1
print("instance mismatches over seeds 0..49:", bad_inst)
print("engine-vs-independent play mismatches (fills, cash) over seeds 0..49:", bad_play)
