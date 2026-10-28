"""Largest Student-t relative variance error by nu over seeds 0-49, for the reference and the verifier's alternatives A to C.

Checks the grader comment (test_project.py lines 31-35), which quotes 0.52 at nu = 3 and 0.31 at nu = 4 for five streams.
Usage: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/measure_streams.py
"""

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "course/modules/M/M4/grader"))
from instance import make_instance  # noqa: E402

HERE = ROOT / "ledgers/M4/scripts/M4-d-r1"
mods = {"reference": str(ROOT / "course/modules/M/M4/grader/reference.py")}
for k in ("a", "b", "c"):
    mods[f"alt_r1_{k}"] = str(HERE / f"alt_r1_{k}.py")
for k in range(1, 6):
    mods[f"builder_alt_{k}"] = str(ROOT / f"ledgers/M4/scripts/alt_{k}.py")
for name, path in mods.items():
    spec = importlib.util.spec_from_file_location(name, path)
    sol = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sol)
    worst: dict[int, float] = {}
    for seed in range(0, 50):
        inst = make_instance(seed)
        if inst["nu"] not in (3, 4):
            continue
        pos, cov, nu, nd = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
        n = len(pos)
        target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(n) for j in range(n))
        x = sol.simulate_losses(pos, cov, nd, seed, "student_t", nu)
        m = math.fsum(x) / len(x)
        v = math.fsum((a - m) ** 2 for a in x) / (len(x) - 1)
        worst[nu] = max(worst.get(nu, 0.0), abs(v / target - 1))
    print(name, {k: round(v, 4) for k, v in sorted(worst.items())})
