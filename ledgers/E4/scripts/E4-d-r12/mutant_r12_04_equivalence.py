"""Compare mutant_r12_04 (gap-based stop) with reference.py: largest output differences over the instance box and the corner."""
import importlib.util
import math
import random
import sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ref = load("course/modules/E/E4/grader/reference.py", "ref")
mut = load("ledgers/E4/mutants/mutant_r12_04_stops_when_midpoint_gap_is_tiny.py", "mut")
rng = random.Random(12)
cases = [(round(rng.uniform(0.5, 0.75), 3), round(rng.uniform(0.12, 0.15), 3)) for _ in range(3000)]
cases += [(1e-50 * (1 + 0.0001 * i), 0.1707691121) for i in range(40)]
cases += [(10 ** rng.uniform(-50, 3), rng.uniform(0.0, 0.1707)) for _ in range(3000)]
worst_fraction_abs = worst_fraction_rel = worst_gap = 0.0
worst_case = None
for sd, c in cases:
    r = ref.solve_model(sd, c)
    m = mut.solve_model(sd, c)
    d_abs = abs(r["informed_fraction"] - m["informed_fraction"])
    if r["informed_fraction"] > 0:
        d_rel = d_abs / r["informed_fraction"]
        if d_rel > worst_fraction_rel:
            worst_fraction_rel, worst_case = d_rel, (sd, c, r["informed_fraction"], m["informed_fraction"])
    worst_fraction_abs = max(worst_fraction_abs, d_abs)
    worst_gap = max(worst_gap, abs(r["indifference_gap"] - m["indifference_gap"]))
print("cases", len(cases))
print("max |fraction difference| =", f"{worst_fraction_abs:.3e}")
print("max relative fraction difference (interior cases) =", f"{worst_fraction_rel:.3e}", "at", worst_case)
print("max |gap difference| =", f"{worst_gap:.3e}")
