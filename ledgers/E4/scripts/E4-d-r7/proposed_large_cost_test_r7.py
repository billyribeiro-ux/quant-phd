"""Validate (in scratch only) a proposed test for mutant_r7_03: a valid large information cost must be accepted."""
import math, sys
G = "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d/course/modules/E/E4/grader"
sys.path.insert(0, G)
import importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
ref = load(f"{G}/reference.py", "ref")
mut = load("/Users/billyribeiro/.fanout/wt/verifyE7-E4-d/ledgers/E4/mutants/mutant_r7_03_rejects_cost_above_one.py", "mut")
for name, mod in (("reference", ref), ("mutant_r7_03", mut)):
    try:
        out = mod.solve_model(0.6, 2.0)
        ok = set(out) == {"informed_fraction", "price_informativeness", "indifference_gap"} and all(isinstance(v, float) and math.isfinite(v) for v in out.values())
        print(name, "accepts cost 2.0:", ok, "informed_fraction =", out["informed_fraction"], "gap =", out["indifference_gap"])
    except ValueError as err:
        print(name, "raised ValueError:", err)
