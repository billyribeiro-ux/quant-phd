"""Round-6 verifier sweep (slice d): seed-by-seed variance check for the Student-t family, matched and unmatched.

For seeds 0..1999, uses the grader's own make_instance and the reference solution's simulate_losses (matched), and an
unmatched variant (scale sqrt(nu / W), i.e. no matched factor) that differs from the reference only in that factor.
Writes one JSON line per seed: seed, nu, n_draws, rel_matched, rel_unmatched, where rel = |sample_var / w'Sigma w - 1|.
Run from the checkout root: .venv/bin/python ledgers/M4/scripts/M4-d-r6/sweep_variance_tolerance.py 0 1999 out.jsonl
"""

import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "M" / "M4" / "grader"
sys.path.insert(0, str(GRADER))
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402


def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def unmatched_student_t(position_cents, cov, n_draws, seed, nu):
    n = len(position_cents)
    factor = ref._cholesky(cov, n)
    rng = random.Random(seed)
    losses = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        chi = rng.gammavariate(nu / 2, 2.0)
        scale = math.sqrt(nu / chi)  # no matched factor
        total = 0.0
        for i in range(n):
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
            total += position_cents[i] * ret
        losses.append(round(-total))
    return losses


def main():
    lo, hi, out = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
    with out.open("w") as fh:
        for seed in range(lo, hi + 1):
            inst = make_instance(seed)
            pos, cov, nu, n = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
            pos_list = [int(p) for p in pos]
            target = math.fsum(pos_list[i] * pos_list[j] * cov[i][j] for i in range(len(pos_list)) for j in range(len(pos_list)))
            matched = ref.simulate_losses(pos_list, cov, n, seed, "student_t", nu)
            unmatched = unmatched_student_t(pos_list, cov, n, seed, nu)
            rel_m = abs(sample_variance(matched) / target - 1.0)
            rel_u = abs(sample_variance(unmatched) / target - 1.0)
            fh.write(json.dumps({"seed": seed, "nu": nu, "n_draws": n, "rel_matched": rel_m, "rel_unmatched": rel_u}) + "\n")
            fh.flush()


if __name__ == "__main__":
    main()
