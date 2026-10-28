"""For each nu, the share of seeds where an UNMATCHED Student-t (no (nu-2)/nu factor) fails the suite's 0.60 variance check.

Usage: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/detect_unmatched.py 0 999
Expected inflation nu/(nu-2): nu=3 -> 3.0, nu=4 -> 2.0, nu=5 -> 1.667, nu=6 -> 1.5, nu=7 -> 1.4, nu=8 -> 1.333.
"""

import math
import random
import sys

sys.path.insert(0, "course/modules/M/M4/grader")
from instance import make_instance  # noqa: E402


def unmatched(pos, cov, nd, seed, nu):
    rng = random.Random(seed)
    lf = [[math.sqrt(cov[0][0]), 0.0], [cov[1][0] / math.sqrt(cov[0][0]), 0.0]]
    lf[1][1] = math.sqrt(cov[1][1] - lf[1][0] ** 2)
    out = []
    for _ in range(nd):
        z = [rng.gauss(0, 1), rng.gauss(0, 1)] if len(pos) == 2 else None
        w = rng.gammavariate(nu / 2, 2.0)
        s = math.sqrt(nu / w)  # the mutant: no matched factor
        r = [s * (lf[0][0] * z[0]), s * (lf[1][0] * z[0] + lf[1][1] * z[1])]
        out.append(round(-(pos[0] * r[0] + pos[1] * r[1])))
    return out


lo, hi = int(sys.argv[1]), int(sys.argv[2])
counts = {nu: [0, 0] for nu in range(3, 9)}
for seed in range(lo, hi + 1):
    inst = make_instance(seed)
    if len(inst["positions_cents"]) != 2:
        continue
    pos, cov, nu, nd = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    target = sum(pos[i] * pos[j] * cov[i][j] for i in range(2) for j in range(2))
    x = unmatched(pos, cov, nd, seed, nu)
    m = sum(x) / len(x)
    v = sum((a - m) ** 2 for a in x) / (len(x) - 1)
    counts[nu][0] += 1
    counts[nu][1] += abs(v / target - 1) > 0.60
for nu, (n, k) in counts.items():
    print(f"nu={nu}: two-asset seeds {n}, unmatched fails {k}")
