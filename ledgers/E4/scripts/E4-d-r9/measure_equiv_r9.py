"""Measure output differences of the equivalent-folder variants against the reference over seeds 0-49 and the grid.

Run: python3 -I measure_equiv_r9.py <repo-root>
"""
import importlib.util
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
for fname in ["mutant_r6_08_reports_lower_end.py", "mutant_r6_09_always_200_halvings.py"]:
    var = load(root / "ledgers/E4/equivalent" / fname, fname.replace(".", "_"))
    worst_lam = 0.0
    worst_gap = 0.0
    n_diff = 0
    pts = [(make_instance(s)["noise_sd"], make_instance(s)["info_cost"]) for s in range(50)]
    pts += [(sd, c) for sd in (0.5, 0.625, 0.75) for c in (0.12, 0.135, 0.15)]
    pts += [(1e-6, 0.13), (1e-9, 0.13), (1e-40, 0.15), (0.6, 0.30), (2.0, 0.0)]
    for sd, c in pts:
        a = ref.solve_model(sd, c)
        b = var.solve_model(sd, c)
        if a["informed_fraction"] != b["informed_fraction"]:
            n_diff += 1
        worst_lam = max(worst_lam, abs(a["informed_fraction"] - b["informed_fraction"]))
        worst_gap = max(worst_gap, abs(a["indifference_gap"] - b["indifference_gap"]))
    print(f"{fname}: points {len(pts)}, bitwise-different fractions {n_diff}, max |dlambda| {worst_lam:.3e}, max |dgap| {worst_gap:.3e}")
