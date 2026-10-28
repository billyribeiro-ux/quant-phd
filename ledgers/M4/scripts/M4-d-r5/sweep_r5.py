"""Round-5 verifier sweep: reference Student-t variance error per instance nu, and the missing-matched-factor mutant.

Run: python3 ledgers/M4/scripts/M4-d-r5/sweep_r5.py <lo> <hi>   (seeds lo..hi-1). Imports the grader copies in the
checkout's course/modules/M/M4/grader directory via sys.path (read-only use).
"""

import math
import random
import sys
from pathlib import Path

GRADER = Path(__file__).resolve().parents[4] / "course/modules/M/M4/grader"
sys.path.insert(0, str(GRADER))
sys.dont_write_bytecode = True
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402


def mutant_losses(pos, cov, n_draws, seed, nu):
    """Student-t losses with the matched factor deleted (scale = sqrt(nu / W))."""
    n = len(pos)
    factor = ref._cholesky(cov, n)
    rng = random.Random(seed)
    out = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        chi = rng.gammavariate(nu / 2, 2.0)
        scale = math.sqrt(nu / chi)
        total = 0.0
        for i in range(n):
            total += pos[i] * scale * sum(factor[i][k] * z[k] for k in range(i + 1))
        out.append(round(-total))
    return out


def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def target(pos, cov):
    n = len(pos)
    return math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(n) for j in range(n))


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for seed in range(lo, hi):
        inst = make_instance(seed)
        pos, cov, nu, nd = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
        t = target(pos, cov)
        ref_losses = ref.simulate_losses(pos, cov, nd, seed, "student_t", nu)
        ref_err = abs(sample_variance(ref_losses) / t - 1.0)
        mut_err = abs(sample_variance(mutant_losses(pos, cov, nd, seed, nu)) / t - 1.0)
        print(f"{seed} {nu} {nd} {len(pos)} {ref_err:.6f} {mut_err:.6f}", flush=True)


if __name__ == "__main__":
    main()
