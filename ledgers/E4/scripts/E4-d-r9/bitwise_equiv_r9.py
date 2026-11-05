"""Bitwise comparison of an equivalent-folder variant with the reference over seeds 0-49 and a 9-point grid.

Run: python3 -I bitwise_equiv_r9.py <repo-root> <variant.py>
"""
import importlib.util
import sys
from pathlib import Path

root, variant = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "course/modules/E/E4/grader"))
from instance import make_instance  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(root / "course/modules/E/E4/grader/reference.py", "ref")
var = load(variant, "var")
pts = [(make_instance(s)["noise_sd"], make_instance(s)["info_cost"]) for s in range(50)]
pts += [(sd, c) for sd in (0.5, 0.625, 0.75) for c in (0.12, 0.135, 0.15)]
same = sum(1 for sd, c in pts if repr(ref.solve_model(sd, c)) == repr(var.solve_model(sd, c)))
print(f"{variant.name}: bitwise identical outputs on {same}/{len(pts)} points")
