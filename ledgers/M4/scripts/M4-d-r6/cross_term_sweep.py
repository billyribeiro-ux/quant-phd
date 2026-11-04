"""Round-6 verifier (slice d): the Student-t cross-term check in test_project.py, its reference error over seeds 0..49,
and the three per-asset variants the page describes (one matched asset, one chi-square per asset) at seeds 0..9.

Cross term: positions (1e6, 1e6) and (1e6, -1e6), cov [[4e-4, 4.8e-4], [4.8e-4, 9e-4]], nu = 5, 100,000 draws.
target = 4 w1 w2 Cov(R1, R2) = 1.92e9; measured = sample_var(plus) - sample_var(minus); rel = |measured / target - 1|.
Usage: .venv/bin/python ledgers/M4/scripts/M4-d-r6/cross_term_sweep.py
"""

import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "M" / "M4" / "grader"
sys.path.insert(0, str(GRADER))
import reference as ref  # noqa: E402

COV = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
NU = 5
N = 100_000
W1 = 1_000_000
TARGET = 4.0 * W1 * W1 * COV[0][1]
LOW = ref._cholesky(COV, 2)


def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def sim(positions, seed, mode):
    rng = random.Random(seed)
    out = []
    for _ in range(N):
        z = [rng.gauss(0.0, 1.0) for _ in range(2)]
        if mode == "reference":
            w = rng.gammavariate(NU / 2, 2.0)
            s = [math.sqrt((NU - 2) / w)] * 2
        elif mode == "matched_asset1_unmatched_asset2":
            w = rng.gammavariate(NU / 2, 2.0)
            s = [math.sqrt((NU - 2) / w), math.sqrt(NU / w)]
        elif mode == "matched_asset1_gaussian_asset2":
            w = rng.gammavariate(NU / 2, 2.0)
            s = [math.sqrt((NU - 2) / w), 1.0]
        elif mode == "chi_square_per_asset":
            ws = [rng.gammavariate(NU / 2, 2.0) for _ in range(2)]
            s = [math.sqrt((NU - 2) / wi) for wi in ws]
        else:
            raise ValueError(mode)
        r = [s[i] * sum(LOW[i][k] * z[k] for k in range(i + 1)) for i in range(2)]
        out.append(round(-(positions[0] * r[0] + positions[1] * r[1])))
    return out


def cross_rel(seed, mode):
    plus = sim([W1, W1], seed, mode)
    minus = sim([W1, -W1], seed, mode)
    measured = sample_variance(plus) - sample_variance(minus)
    return abs(measured / TARGET - 1.0)


if __name__ == "__main__":
    ref_errs = {s: cross_rel(s, "reference") for s in range(50)}
    worst = max(ref_errs, key=ref_errs.get)
    print(f"reference: max rel error over seeds 0..49 = {ref_errs[worst]:.4f} at seed {worst}")
    for mode in ("matched_asset1_unmatched_asset2", "matched_asset1_gaussian_asset2", "chi_square_per_asset"):
        errs = [cross_rel(s, mode) for s in range(10)]
        print(f"{mode}: seeds 0..9 rel errors min {min(errs):.4f} median {sorted(errs)[5]:.4f} max {max(errs):.4f}")
