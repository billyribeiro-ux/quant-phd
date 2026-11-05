"""Round-10 verifier D: the Student-t variance check (test_student_t_loss_variance_matches_matched_covariance) over seeds 0-1999.

For each seed, instance = make_instance(seed) exactly as the autograder builds it. The reference's relative variance error is
|sample variance / w' Sigma w - 1| with the instance's own positions, covariance, nu and draw count (seed = the same seed).
The missing-factor probe is the reference with the matched factor replaced by 1 (returns inflated by sqrt(nu / (nu - 2))).
Prints: per nu (3..8), the number of seeds, the reference maximum error, the number of missing-factor seeds failing
the 0.30 tolerance (only nu >= 5 is checked by the test); and the reference error at seed 1093.
"""

import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
sys.path.insert(0, str(ROOT / "course/modules/M/M4/grader"))
import instance as inst  # noqa: E402
sys.path.insert(0, str(HERE))
import cross_term_d10 as ct  # noqa: E402

REF_PATH = ct.REF
MISS_PATH = HERE / "probes" / "missing_matched_factor.py"
TEXT = REF_PATH.read_text(encoding="utf-8")
OLD = "    matched = matched_scale(nu) if student and nu is not None else 1.0\n"
assert TEXT.count(OLD) == 1
MISS_PATH.write_text(TEXT.replace(OLD, "    matched = 1.0\n"), encoding="utf-8")
TOL = 0.30


def fsum_var(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def errors(seed: int):
    i = inst.make_instance(seed)
    pos, cov, nu, n = i["positions_cents"], i["cov"], i["nu"], i["n_draws"]
    target = math.fsum(pos[a] * pos[b] * cov[a][b] for a in range(len(pos)) for b in range(len(pos)))
    ref = ct.load(REF_PATH, "ref").simulate_losses(pos, cov, n, seed, "student_t", nu)
    miss = ct.load(MISS_PATH, "miss").simulate_losses(pos, cov, n, seed, "student_t", nu)
    return seed, nu, abs(fsum_var(ref) / target - 1.0), abs(fsum_var(miss) / target - 1.0)


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=12) as ex:
        rows = list(ex.map(errors, range(2000), chunksize=20))
    print("reference relative error at seed 1093:", [round(r[2], 4) for r in rows if r[0] == 1093], "nu", [r[1] for r in rows if r[0] == 1093])
    for nu in range(3, 9):
        sel = [r for r in rows if r[1] == nu]
        ref_max = max(r[2] for r in sel)
        miss_fail = sum(1 for r in sel if r[3] > TOL)
        ref_fail = sum(1 for r in sel if r[2] > TOL)
        print(f"nu {nu}: seeds {len(sel)}; reference max error {ref_max:.4f}; reference seeds over 0.30: {ref_fail}; missing-factor seeds over 0.30: {miss_fail}")
    sys.stdout.flush()
