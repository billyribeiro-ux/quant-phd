"""Round-5: show that the two surviving mutants (v21, v22) are wrong on legal engine logs the suite never replays.

Usage: python3 -I survivor_demo_r5.py <grader_dir> <mutants_dir>. Uses the engine of the checkout unchanged.
v21 is loaded as module market_maker from the mutants directory; the oracle is the page's own fills rule (one unit per fill).
"""
import importlib.util
import sys

grader, mutdir = sys.argv[1], sys.argv[2]
sys.path.insert(0, grader)
import engine  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(name, f"{mutdir}/{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def oracle(log):
    cash = inv = 0
    for t in log["turns"]:
        if t["filled"]:
            side = 1 if t["fill_price_cents"] == t["bid_cents"] else -1
            cash += -side * t["fill_price_cents"]
            inv += side
    return cash, inv


# v21: quote size 5 on every turn (legal: 0..5); a fill is one unit, so the oracle counts one unit per fill.
v21 = load("v21_replay_scales_each_fill_by_quoted_size")
log = engine.play(lambda s: (9_990, 10_010, 5), 0)
fills = sum(1 for t in log["turns"] if t["filled"])
print("v21 on a size-5 log: fills", fills, "replay", v21.replay(log)["cash_flow_cents"], "oracle cash", oracle(log)[0])

# v22: a bid of 0 is legal (only bid >= ask is refused); a fill at price 0 is a legal fill, refused only if the price is None.
v22 = load("v22_replay_refuses_a_zero_fill_price")
log0 = engine.play(lambda s: (0, 9_990, 1), 0)
zero = [t["turn"] for t in log0["turns"] if t["filled"] and t["fill_price_cents"] == 0]
print("zero-price fill turns on the bid-0 log:", zero)
try:
    v22.replay(log0)
    print("v22 replay: accepted")
except ValueError as error:
    print("v22 replay refused the log with:", error)
print("reference oracle on the same log: cash", oracle(log0)[0], "inventory", oracle(log0)[1])
