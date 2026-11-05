"""Measure how closely the suite's oracle gap agrees with the reference gap at the reported fraction, seeds 0-49.
Usage: python3 -I oracle_gap_precision_r11.py <scratch dir containing instance.py, test_project.py, solver.py>"""
import math
import os
import sys

scratch = sys.argv[1]
sys.path.insert(0, scratch)
os.environ.setdefault("QF_SEED", "0")
import importlib

worst_interior = 0.0
rows = []
for seed in range(50):
    os.environ["QF_SEED"] = str(seed)
    for mod in ("test_project", "instance", "solver"):
        sys.modules.pop(mod, None)
    t = importlib.import_module("test_project")
    inst = t.make_instance(seed)
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    out = t.run(sd, cost)
    lam = out["informed_fraction"]
    if 0.0 < lam < 1.0:
        d = abs(out["indifference_gap"] - t.oracle_gap(lam, sd, cost))
        worst_interior = max(worst_interior, d)
        rows.append((seed, d))
print(f"interior seeds: {len(rows)}; max |reference gap - oracle gap| at lam* = {worst_interior:.3e}")
print("all seeds with an interior root differ by <= 1e-12:", all(d <= 1e-12 for _, d in rows))
