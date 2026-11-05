"""Round 7 (SC1-d): validity and materiality of 20 sampled instances, and of all 50 seeds 0-49.

Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-d-r7/instances_r7.py
Checks each instance against the page's ranges and the 200,000-draw cap, and recomputes the reference answers
(reflection tail, one-step estimate, nested counts) to show the answers change with the seed.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
import importlib.util
GRADER = ROOT / "course/modules/SC/SC1/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402
_spec = importlib.util.spec_from_file_location("ref_bm_checks", GRADER / "reference.py")
ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ref)  # the reference engine is grader/reference.py

SAMPLE = [0, 1, 2, 3, 5, 8, 13, 21, 34, 42, 49, 77, 101, 250, 333, 499, 1000, 2024, 4096, 9999]
bad = []
levels = set()
for s in range(50):
    i = make_instance(s)
    levels.add(i["a"])
    ok = (i["H"] > 0 and i["a"] > 0 and 4 <= i["n_steps"] <= 256 and 400 <= i["n_paths"] <= 800
          and i["n_steps"] * i["n_paths"] <= 200_000 and i["label"] == "SIMULATED" and i["seed"] == s)
    if not ok:
        bad.append(s)
print(f"seeds 0-49 valid: {50 - len(bad)}/50; distinct levels: {len(levels)}; invalid seeds: {bad}")
print("sample of 20 seeds: seed H a n_steps n_paths tail one_step_est nested(fine,coarse 4)")
rows = set()
for s in SAMPLE:
    i = make_instance(s)
    tail = ref.reflection_tail(i["a"], i["H"])
    est, se = ref.discrete_max_exceedance(i, 1)
    fine, coarse = ref.nested_grid_counts(i, 8, 4)
    rows.add((round(tail, 9), est, fine, coarse))
    print(f"{s} {i['H']} {i['a']} {i['n_steps']} {i['n_paths']} {tail:.6f} {est:.6f} ({fine},{coarse})")
print(f"distinct (tail, one-step estimate, nested) rows among the 20 sampled seeds: {len(rows)}")
