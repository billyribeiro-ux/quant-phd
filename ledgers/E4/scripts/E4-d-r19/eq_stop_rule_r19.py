"""Round 19 (E4-d): ruling 17 check. For the three stop-rule variants, the largest |variant - reference| / root over
3000 random inputs with an interior root and tau-bar >= 1e-2, sd >= 1e-50 (the page's accuracy domain). Also the
largest relative difference against the closed form of Proposition 4. Run with SOLVER_DIR set (solver.py = reference).
"""
import importlib.util
import math
import os
import random
import sys

CHECKOUT = "/Users/billyribeiro/.fanout/wt/verifyE19-E4-d"
sys.path.insert(0, os.environ["SOLVER_DIR"])
import solver as ref  # noqa: E402
import test_project as tp  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


variants = {
    "r6_08": f"{CHECKOUT}/ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py",
    "r7_01": f"{CHECKOUT}/ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py",
    "v9_02": f"{CHECKOUT}/ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py",
}
rng = random.Random(1917)
pts = []
while len(pts) < 3000:
    sd = 10 ** rng.uniform(-50, 2)
    cost = rng.uniform(0.0, 0.2)
    t = 2 * math.exp(-4 * cost) - 1
    if t >= 1e-2 and 0 < t < 1 / (1 + 4 * sd * sd):
        pts.append((sd, cost))
for name, path in variants.items():
    mod = load(path, "v_" + name)
    worst = 0.0
    worst_cf = 0.0
    ndiff = 0
    for sd, cost in pts:
        a = ref.solve_model(sd, cost)["informed_fraction"]
        b = mod.solve_model(sd, cost)["informed_fraction"]
        cf = tp.closed_form_root(sd, cost)
        if a != b:
            ndiff += 1
        worst = max(worst, abs(a - b) / cf)
        worst_cf = max(worst_cf, abs(b - cf) / cf)
    print(f"{name}: differing fractions {ndiff}/3000; max |variant - reference|/root = {worst:.3e}; "
          f"max |variant - closed form|/root = {worst_cf:.3e} (page tolerance 1e-10)")
