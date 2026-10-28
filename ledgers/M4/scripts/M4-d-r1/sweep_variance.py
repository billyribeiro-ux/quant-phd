"""Sweep the grader's variance checks over a seed range using the reference solution (verifier round 1).

Usage: .venv/bin/python ledgers/M4/scripts/M4-d-r1/sweep_variance.py 0 999
Prints counts of seeds where the Gaussian (tol 0.10) or Student-t (tol 0.60) variance check fails, and the worst error.
"""

import math
import sys

sys.path.insert(0, "course/modules/M/M4/grader")
import reference as sol  # noqa: E402
from instance import make_instance  # noqa: E402


def sv(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)


lo, hi = int(sys.argv[1]), int(sys.argv[2])
g_fail, t_fail, worst_g, worst_t, worst_t_seed = [], [], 0.0, 0.0, None
for seed in range(lo, hi + 1):
    inst = make_instance(seed)
    pos, cov, nu, nd = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    n = len(pos)
    target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(n) for j in range(n))
    g = sol.simulate_losses(pos, cov, nd, seed, "gaussian", None)
    t = sol.simulate_losses(pos, cov, nd, seed, "student_t", nu)
    eg = abs(sv(g) / target - 1)
    et = abs(sv(t) / target - 1)
    worst_g = max(worst_g, eg)
    if et > worst_t:
        worst_t, worst_t_seed = et, (seed, nu, nd)
    if eg > 0.10:
        g_fail.append(seed)
    if et > 0.60:
        t_fail.append((seed, nu))
print(f"seeds {lo}-{hi}: gaussian fails {len(g_fail)} worst {worst_g:.4f}; student_t fails {len(t_fail)} worst {worst_t:.4f} at (seed, nu, n_draws)={worst_t_seed}")
print("student_t failing (seed, nu):", t_fail[:50])
