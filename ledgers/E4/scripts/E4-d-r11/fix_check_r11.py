"""Proposed tightened interior-gap check: |gap(lam*) - oracle_gap(lam*)| <= 1e-14 * max(1, |oracle|), seeds 0-49.
Reports, for the reference and for the surviving mutant, the number of seeds that would fail the proposed check.
Usage: python3 -I fix_check_r11.py <scratch dir with instance.py, test_project.py, solver.py> <mutant.py> <root>"""
import importlib.util
import os
import sys

scratch, mutant_path, root = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, scratch)
import importlib  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(f"{scratch}/solver.py", "ref_solver")
mut = load(mutant_path, "mut_solver")
results = {"reference": 0, "mutant": 0}
for seed in range(50):
    os.environ["QF_SEED"] = str(seed)
    for m in ("test_project", "instance"):
        sys.modules.pop(m, None)
    t = importlib.import_module("test_project")
    inst = t.make_instance(seed)
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    lam = ref.solve_model(sd, cost)["informed_fraction"]
    if not (0.0 < lam < 1.0):
        continue
    oracle = t.oracle_gap(lam, sd, cost)
    for name, mod in (("reference", ref), ("mutant", mut)):
        g = mod.indifference_gap(lam, sd, cost)
        if abs(g - oracle) > 1e-14 * max(1.0, abs(oracle)):
            results[name] += 1
print("seeds failing the proposed 1e-14 check (of interior seeds, 0-49):", results)
