"""Share of nu = 3 seeds whose Student-t variance check (tolerance 0.60) fails, for one implementation over a seed range.

Usage: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/nu3_false_fail_rate.py <module path> 0 999
"""

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "course/modules/M/M4/grader"))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("impl", sys.argv[1])
sol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sol)
lo, hi = int(sys.argv[2]), int(sys.argv[3])
total, fails, worst = 0, [], 0.0
for seed in range(lo, hi + 1):
    inst = make_instance(seed)
    if inst["nu"] != 3:
        continue
    pos, cov, nd = inst["positions_cents"], inst["cov"], inst["n_draws"]
    n = len(pos)
    target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(n) for j in range(n))
    x = sol.simulate_losses(pos, cov, nd, seed, "student_t", 3)
    m = math.fsum(x) / len(x)
    v = math.fsum((a - m) ** 2 for a in x) / (len(x) - 1)
    e = abs(v / target - 1)
    total += 1
    worst = max(worst, e)
    if e > 0.60:
        fails.append(seed)
print(f"{sys.argv[1]}: nu=3 seeds {total}, failing {len(fails)} {fails[:10]}, worst {worst:.4f}")
