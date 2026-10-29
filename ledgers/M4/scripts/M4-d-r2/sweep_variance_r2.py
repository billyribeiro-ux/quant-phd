"""Sweep the current grader's variance checks over a seed range with the reference solution (verifier round 2).

Usage: .venv/bin/python ledgers/M4/scripts/M4-d-r2/sweep_variance_r2.py 0 1999
Reports, for the Student-t check (nu of 5 or more, tolerance read from test_project.py), the worst relative error per
nu, and the seeds that fail; and the worst Gaussian relative error (tolerance read from test_project.py).
"""

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
sys.path.insert(0, str(GRADER))
import reference as sol  # noqa: E402
from instance import make_instance  # noqa: E402

src = (GRADER / "test_project.py").read_text(encoding="utf-8")
TOL_G = float(re.search(r"TOL_GAUSSIAN_VARIANCE = ([0-9.]+)", src).group(1))
TOL_T = float(re.search(r"TOL_T_VARIANCE = ([0-9.]+)", src).group(1))
MIN_NU = int(re.search(r"MIN_NU_FOR_T_VARIANCE_CHECK = ([0-9]+)", src).group(1))


def sv(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)


lo, hi = int(sys.argv[1]), int(sys.argv[2])
worst_g = 0.0
worst_t_by_nu: dict[int, tuple[float, int]] = {}
t_fail: list[tuple[int, int]] = []
g_fail: list[int] = []
for seed in range(lo, hi + 1):
    inst = make_instance(seed)
    pos, cov, nu, nd = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    n = len(pos)
    target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(n) for j in range(n))
    g = sol.simulate_losses(pos, cov, nd, seed, "gaussian", None)
    eg = abs(sv(g) / target - 1.0)
    worst_g = max(worst_g, eg)
    if eg > TOL_G:
        g_fail.append(seed)
    if nu >= MIN_NU:
        t = sol.simulate_losses(pos, cov, nd, seed, "student_t", nu)
        et = abs(sv(t) / target - 1.0)
        if et > worst_t_by_nu.get(nu, (0.0, -1))[0]:
            worst_t_by_nu[nu] = (et, seed)
        if et > TOL_T:
            t_fail.append((seed, nu))
print(f"tolerances read from test_project.py: gaussian {TOL_G}, student_t {TOL_T}, min nu {MIN_NU}")
print(f"seeds {lo}-{hi}: gaussian worst {worst_g:.4f}, gaussian fails {len(g_fail)}")
for nu in sorted(worst_t_by_nu):
    et, seed = worst_t_by_nu[nu]
    print(f"student_t nu={nu}: worst relative error {et:.4f} at seed {seed}")
print(f"student_t fails at tolerance {TOL_T}: {len(t_fail)} {t_fail[:20]}")
