"""Candidate extra test for the seed-dependence gap (mutant m20): run it against reference.py and against mutant m20, seeds 0-49.

Usage: python ledgers/SC1/scripts/SC1-d-r2/candidate_seed_test.py <repo-root>
The candidate test asserts that changing only the instance seed changes the sampled grid estimates. It is appended to a
scratch copy of test_project.py; the repository grader is not modified.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
GRADER = ROOT / "course/modules/SC/SC1/grader"
CANDIDATE = '''

def test_candidate_draws_depend_on_the_instance_seed() -> None:
    other = with_(INST, seed=INST["seed"] + 1)
    pairs = {(sol.discrete_max_exceedance(INST, g), sol.discrete_max_exceedance(other, g)) for g in (4, INST["n_steps"])}
    expect(any(first != second for first, second in pairs), "candidate: changing only the seed must change the sample")
'''
TARGETS = {
    "reference": GRADER / "reference.py",
    "m20": ROOT / "ledgers/SC1/mutants/m20_draws_seeded_with_zero_for_every_instance.py",
}
for label, solution in TARGETS.items():
    failing = []
    for seed in range(50):
        work = Path(tempfile.mkdtemp(prefix="sc1d-cand-"))
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        (work / "test_project.py").write_text((GRADER / "test_project.py").read_text(encoding="utf-8") + CANDIDATE, encoding="utf-8")
        shutil.copy(solution, work / "bm_checks.py")
        env = {**os.environ, "QF_SEED": str(seed)}
        proc = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py", "-k", "candidate"],
            cwd=work, env=env, capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            failing.append(seed)
        shutil.rmtree(work, ignore_errors=True)
    print(f"{label}: candidate test fails on {len(failing)} of 50 seeds")
