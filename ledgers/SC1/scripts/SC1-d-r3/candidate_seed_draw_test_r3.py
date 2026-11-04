"""Candidate fix for the seed-offset survivor (m22): an exact one-step check that pins the seed and the gauss draws.

For one grid step the draw order is the same under any order, so the estimate must equal the hit fraction of
random.Random(seed).gauss(0, sqrt(H)) draws. Appends the test to a copy of test_project.py and runs the suite.
Usage: python candidate_seed_draw_test_r3.py <repo-root> <solution.py> <seed-spec>
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
SOL = Path(sys.argv[2])
SEEDS = range(50) if sys.argv[3] == "0-49" else range(10) if sys.argv[3] == "0-9" else [int(x) for x in sys.argv[3].split(",")]
GRADER = ROOT / "course/modules/SC/SC1/grader"
EXTRA = '''

import random as _random


def test_one_step_draws_are_the_seeded_gaussians() -> None:
    rng = _random.Random(INST["seed"])
    hits = sum(1 for _ in range(INST["n_paths"]) if rng.gauss(0.0, math.sqrt(INST["H"])) >= INST["a"])
    estimate, _ = sol.discrete_max_exceedance(INST, 1)
    within(estimate, hits / INST["n_paths"], 1e-12, "the one-step draws must be random.Random(seed).gauss(0, sqrt(H))")
'''


def run(seed: int) -> str:
    work = Path(tempfile.mkdtemp(prefix="sc1d-r3-seedtest-"))
    try:
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(SOL, work / "bm_checks.py")
        (work / "test_project.py").write_text((GRADER / "test_project.py").read_text() + EXTRA)
        proc = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=work, env={**os.environ, "QF_SEED": str(seed)}, capture_output=True, text=True, timeout=240,
        )
        return proc.stdout.strip().splitlines()[-1]
    finally:
        shutil.rmtree(work, ignore_errors=True)


for s in SEEDS:
    print(s, run(s))
