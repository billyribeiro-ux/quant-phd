"""Cross-checks: lab draw_game equals instance.make_instance on seeds 0-49; the lab's play equals the engine with the reference rule;
exemplar arithmetic; the counterfactual with the engine; inventory bounds on engine logs; reference quote matches the lab rule."""
import ast
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-PC3-c")
GRADER = ROOT / "course/modules/PC/PC3/grader"
sys.path.insert(0, str(GRADER))
import engine  # noqa: E402
import instance  # noqa: E402
import reference  # noqa: E402


def lab_functions(path):
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    keep = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign))]
    mod = ast.Module(body=keep, type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), str(path), "exec"), ns)
    return ns


lab3 = lab_functions(ROOT / "tests/labs/PC3/lab-PC3-project-3.py")
lab1 = lab_functions(ROOT / "tests/labs/PC3/lab-PC3-project-1.py")

same_draw = all(lab1["draw_game"](s) == (instance.make_instance(s)["fair_path_cents"], instance.make_instance(s)["arrivals"]) for s in range(50))
print("lab1 draw_game == instance.make_instance on seeds 0-49:", same_draw)

ref_log = engine.play(reference.quote, 0)
ref_out = reference.replay(ref_log)
print("engine+reference seed 0 replay:", ref_out, "fills:", sum(t["filled"] for t in ref_log["turns"]))
lab_ref = lab3["play"](0, 10)
print("lab3 play(0,10) equals engine+reference log:", lab_ref == ref_log)
print("lab3 replay of lab log:", lab3["replay"](lab_ref))

def wide_quote(state):
    mid = 10_000
    for r in state["history"]:
        if r["filled"] is True:
            mid = r["fill_price_cents"]
    return mid - 15, mid + 15, 1

wide_log = engine.play(wide_quote, 0)
wide_out = reference.replay(wide_log)
print("engine counterfactual half-spread 15 seed 0:", wide_out, "fills", sum(t["filled"] for t in wide_log["turns"]))
print("lab3 play(0,15) equals engine wide log:", lab3["play"](0, 15) == wide_log)

# Inventory bounds and fills on engine logs for the reference rule over seeds 0-49
bad = 0
for s in range(50):
    log = engine.play(reference.quote, s)
    if any(abs(t["inventory_after"]) > 10 for t in log["turns"]):
        bad += 1
    out = reference.replay(log)
    if out["pnl_cents"] != out["cash_flow_cents"] + out["inventory_end"] * log["settlement_cents"]:
        bad += 1
print("reference rule seeds 0-49: inventory or identity violations:", bad)

# Exemplar arithmetic and log facts used in prose (seed 0, reference rule)
fills = [(t["turn"], t["fill_price_cents"], t["bid_cents"], t["ask_cents"], t["inventory_after"]) for t in ref_log["turns"] if t["filled"]]
print("fills (turn, price, bid, ask, inventory_after):", fills)
buys = sum(p for (_, p, b, a, _) in fills if p == b)
sells = sum(p for (_, p, b, a, _) in fills if p == a)
print("buys at bid total", buys, "sells at ask total", sells, "cash flow", sells - buys)
print("turn 2 bid/fill:", [f for f in fills if f[0] == 2], "turn 5:", [f for f in fills if f[0] == 5], "turn 18:", [f for f in fills if f[0] == 18])
print("settlement", ref_log["settlement_cents"], "largest |inv|", max(abs(t["inventory_after"]) for t in ref_log["turns"]))
print("arrival thresholds 1/4, 1/4, 1/2 ->", 0.25, 0.25, 0.5)
