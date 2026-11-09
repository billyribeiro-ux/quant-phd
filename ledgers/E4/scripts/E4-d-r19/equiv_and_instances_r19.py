"""Round 19 (E4-d): (1) literal_price_sign and the stop-rule variants vs the reference, bitwise, on random inputs;
(2) mutant_v17_02 at the new domain point; (3) instance validity and variety for seeds 0-19 and 0-49.
Run with SOLVER_DIR set to a workspace holding solver.py (= reference), test_project.py and instance.py.
"""

import importlib.util
import os
import random
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE19-E4-d"
SOLVER_DIR = os.environ["SOLVER_DIR"]
sys.path.insert(0, SOLVER_DIR)
import solver as ref  # noqa: E402
import test_project as tp  # noqa: E402
import instance as inst  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


variants = {
    "literal_price_sign": f"{ROOT}/ledgers/E4/equivalent/literal_price_sign.py",
    "r6_08_reports_lower_end": f"{ROOT}/ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py",
    "r7_01_reports_bracket_lower_end": f"{ROOT}/ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py",
    "v9_02_stop_rule_relative_to_lower_end": f"{ROOT}/ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py",
}
rng = random.Random(1919)
pts = [(rng.uniform(0.05, 3.0), rng.uniform(0.0, 0.4)) for _ in range(3000)]
for name, path in variants.items():
    mod = load(path, "v_" + name.replace("-", "_"))
    diffs = 0
    maxdiff = 0.0
    for sd, c in pts:
        a = ref.solve_model(sd, c)
        b = mod.solve_model(sd, c)
        for k in a:
            if a[k] != b[k]:
                diffs += 1
                maxdiff = max(maxdiff, abs(a[k] - b[k]))
    print(f"{name}: 3000 inputs, differing outputs (any key) = {diffs}, max abs difference = {maxdiff:.3e}")

# literal_price_sign: the only source difference from the reference
import difflib  # noqa: E402
ref_lines = open(f"{ROOT}/course/modules/E/E4/grader/reference.py", encoding="utf-8").read().splitlines()
lit_lines = open(variants["literal_price_sign"], encoding="utf-8").read().splitlines()
for line in difflib.unified_diff(ref_lines, lit_lines, lineterm="", n=0):
    if not line.startswith(("---", "+++")):
        print("literal diff:", line)

# (2) mutant_v17_02 at the domain point and a few neighbours
mut = load(f"{ROOT}/ledgers/E4/mutants/mutant_v17_02_price_slope_drops_uninformed_term.py", "m17")
sd, c = 3.3245979322709314e-22, 0.059130434782608696
out_ref = ref.solve_model(sd, c)
lam = out_ref["informed_fraction"]
exact = float(tp.prop3_gap_exact(lam, sd, c))
out_m = mut.solve_model(sd, c)
print(f"v17_02 at domain point: ref root {lam:.6e}; mutant root {out_m['informed_fraction']:.6e}; "
      f"mutant gap {out_m['indifference_gap']:+.6e}; exact Prop3 gap at mutant's own fraction "
      f"{float(tp.prop3_gap_exact(out_m['informed_fraction'], sd, c)):+.6e}; "
      f"mutant-vs-exact at its fraction {abs(out_m['indifference_gap'] - float(tp.prop3_gap_exact(out_m['informed_fraction'], sd, c))):.3e} "
      f"(tol 1e-14*max(1,|gap|)={1e-14*max(1.0, abs(exact)):.1e})")

# (3) instances
fails = 0
seen = set()
for seed in range(50):
    d = inst.make_instance(seed)
    ok = 0.5 <= d["noise_sd"] <= 0.75 and 0.12 <= d["info_cost"] <= 0.15 and round(d["noise_sd"], 3) == d["noise_sd"]
    fails += not ok
    if seed < 20:
        o = ref.solve_model(d["noise_sd"], d["info_cost"])
        seen.add(round(o["informed_fraction"], 9))
        assert 0.0 < o["informed_fraction"] < 1.0, seed
print(f"instances 0-49: invalid = {fails}; distinct informed fractions over seeds 0-19 = {len(seen)}")
print("seed 0 instance:", inst.make_instance(0), "seed 1:", inst.make_instance(1))
