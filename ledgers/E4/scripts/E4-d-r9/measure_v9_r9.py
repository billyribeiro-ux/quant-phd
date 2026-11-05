"""Measure the size of the output differences of the round-9 surviving mutants against the reference.

Run: python3 -I measure_v9_r9.py <repo-root>
- gap at the reported fraction (reference) over seeds 0-49: largest |gap|, the value the mutant v9_04 reports as 0.0
- G(1e-12) - G(0) over seeds 0-49: the difference that mutant v9_06 introduces at fraction 0
- largest |informed_fraction(reference) - informed_fraction(lower-end stop)| over seeds 0-49 (mutant v9_02)
"""
import importlib.util
import math
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/E/E4/grader"))
from instance import make_instance  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(root / "course/modules/E/E4/grader/reference.py", "ref")
v02 = load(root / "ledgers/E4/mutants/mutant_v9_02_stop_rule_relative_to_lower_end.py", "v02")
max_gap_root = 0.0
max_diff_gap0 = 0.0
max_diff_v02 = 0.0
max_diff_v02_gap = 0.0
for seed in range(50):
    inst = make_instance(seed)
    sd, cost = inst["noise_sd"], inst["info_cost"]
    out = ref.solve_model(sd, cost)
    max_gap_root = max(max_gap_root, abs(out["indifference_gap"]))
    max_diff_gap0 = max(max_diff_gap0, abs(ref.indifference_gap(1e-12, sd, cost) - ref.gap_at_zero(sd, cost)))
    o2 = v02.solve_model(sd, cost)
    max_diff_v02 = max(max_diff_v02, abs(o2["informed_fraction"] - out["informed_fraction"]))
    max_diff_v02_gap = max(max_diff_v02_gap, abs(o2["indifference_gap"] - out["indifference_gap"]))
print(f"seeds 0-49: max |reference gap at reported fraction| = {max_gap_root:.3e}")
print(f"seeds 0-49: max |G(1e-12) - G(0)| = {max_diff_gap0:.3e}")
print(f"seeds 0-49: max |lambda(lower-end stop) - lambda(reference)| = {max_diff_v02:.3e}")
print(f"seeds 0-49: max |gap(lower-end stop) - gap(reference)| = {max_diff_v02_gap:.3e}")
