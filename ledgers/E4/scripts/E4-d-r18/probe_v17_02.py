"""Round 18 probe: does mutant_v17_02 (b_s without the (1-lam) tau_y term) meet the page's 1e-14 gap precision
at the reported fraction, as the test at test_project.py:312 requires? Oracle = test module's oracle_gap.
Run with -I from the scratch probe dir, which holds solver.py (reference), instance.py and test_project.py."""
import importlib.util
import math
import random
import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E4-d-r18/probe")
import solver as ref  # reference.py copied as solver.py
import test_project as tp  # oracle_gap, oracle_root, closed_form_root

spec = importlib.util.spec_from_file_location(
    "mut", "/Users/billyribeiro/.fanout/wt/verifyE18-E4-d/ledgers/E4/equivalent/mutant_v17_02_price_slope_drops_uninformed_term.py"
)
mut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mut)

random.seed(18)
pts = []
for _ in range(400):
    pts.append((math.exp(random.uniform(math.log(0.05), math.log(3.0))), random.uniform(0.0, 0.5)))
for _ in range(200):
    pts.append((random.uniform(0.5, 0.75), random.uniform(0.12, 0.15)))
worst = (0.0, None)
worst_ref_formula = (0.0, None)
n_interior = 0
n_fail = 0
lam_worst = (0.0, None)
for sd, c in pts:
    m = mut.solve_model(sd, c)
    r = ref.solve_model(sd, c)
    lam = m["informed_fraction"]
    if not (0.0 < lam < 1.0):
        continue
    n_interior += 1
    limit = tp.oracle_gap(lam, sd, c)
    rel = abs(m["indifference_gap"] - limit) / max(1.0, abs(limit))
    if rel > worst[0]:
        worst = (rel, (sd, c, lam, m["indifference_gap"], limit))
    if rel > 1e-14:
        n_fail += 1
    # the same comparison against the reference's own formula at the mutant's fraction (no oracle)
    rf = ref.indifference_gap(lam, sd, c)
    rel2 = abs(m["indifference_gap"] - rf) / max(1.0, abs(rf))
    if rel2 > worst_ref_formula[0]:
        worst_ref_formula = (rel2, (sd, c, lam))
    dl = abs(m["informed_fraction"] - r["informed_fraction"]) / r["informed_fraction"]
    if dl > lam_worst[0]:
        lam_worst = (dl, (sd, c))
print("points", len(pts), "interior_mutant", n_interior, "exceed_1e-14_vs_oracle", n_fail)
print("worst_rel_gap_vs_oracle", worst)
print("worst_rel_gap_vs_reference_formula", worst_ref_formula)
print("worst_rel_lambda_diff_vs_reference", lam_worst)
