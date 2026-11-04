"""Round-6 verifier (slice d): which chi-square sharing families the chi-square independence test catches, seeds 0..49.

Three student-error families, each a complete tail_risk module (scratch, not committed), run through the grader's own
test_student_t_draws_do_not_share_chi_square with QF_SEED = seed:
  lag1_2k_2k1   : draws 2k and 2k+1 share one chi-square variable
  lag2_4j_4j2   : draws 4j and 4j+2 share one chi-square variable (draws 4j+1, 4j+3 own theirs)
  even_all      : every even-indexed draw shares the chi-square variable of draw 0
Reports the number of seeds (of 50) on which the test fails, and the reference's pass count.
Usage: .venv/bin/python ledgers/M4/scripts/M4-d-r6/sharing_families_sweep.py
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "M" / "M4" / "grader"
PY = str(ROOT / ".venv" / "bin" / "python")

FAMILY_BODY = '''
import math, random

def matched_scale(nu):
    return (nu - 2) / nu

def simulate_losses(position_cents, cov, n_draws, seed, family, nu):
    rng = random.Random(seed)
    chol = cov[0][0] ** 0.5
    out = []
    drawn = {}
    for d in range(n_draws):
        z = rng.gauss(0.0, 1.0)
        if family == "student_t":
            src = SOURCE(d)
            if src == d:
                drawn[d] = rng.gammavariate(nu / 2, 2.0)
            w = drawn[src]
            scale = math.sqrt((nu - 2) / w)
        else:
            scale = 1.0
        ret = scale * chol * z
        out.append(round(-position_cents[0] * ret))
    return out
'''

# SOURCE(d) is the draw whose chi-square variable draw d uses: d itself (own variable) or an earlier draw (shared).
POLICIES = {
    "reference_own_each_draw": "d",
    "lag1_2k_2k1": "d - d % 2",
    "lag2_4j_4j2": "(d - 2 if d % 4 == 2 else d)",
    "even_all": "(0 if d % 2 == 0 else d)",
}


def run(policy_name: str, seed: int, tmp: Path) -> bool:
    shutil.copy(GRADER / "test_project.py", tmp / "test_project.py")
    shutil.copy(GRADER / "instance.py", tmp / "instance.py")
    body = FAMILY_BODY.replace("SOURCE(d)", POLICIES[policy_name])
    (tmp / "tail_risk.py").write_text(body, encoding="utf-8")
    env = dict(os.environ, QF_SEED=str(seed))
    res = subprocess.run(
        [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
         "-k", "student_t_draws_do_not_share", "test_project.py"],
        cwd=tmp, env=env, capture_output=True, text=True,
    )
    return res.returncode == 0


if __name__ == "__main__":
    for name in POLICIES:
        passes = []
        for seed in range(50):
            tmp = Path(tempfile.mkdtemp(prefix="m4d6-"))
            try:
                passes.append(run(name, seed, tmp))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        print(f"{name}: test passes on {sum(passes)} of 50 seeds, fails on {50 - sum(passes)} of 50 seeds")
        sys.stdout.flush()
