"""Verifier round 1: run every alternative correct implementation through the E1 project suite for seeds 0-9.

Each alternative is copied, with the repository's test_project.py and instance.py, into a scratch directory as
market_structure.py, and pytest runs with the browser's flags (--assert=plain -W error) and QF_SEED set per seed.
Usage: .venv/bin/python -I ledgers/E1/scripts/E1-d-r1/run_alt_seeds_0_9.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/E/E1/grader"
ALTS = sorted((ROOT / "ledgers/E1/scripts/E1-d-r1/alternatives").glob("*.py"))
for alt in ALTS:
    scratch = Path(tempfile.mkdtemp(prefix="e1d-alt-"))
    shutil.copy(GRADER / "test_project.py", scratch / "test_project.py")
    shutil.copy(GRADER / "instance.py", scratch / "instance.py")
    shutil.copy(alt, scratch / "market_structure.py")
    results: list[str] = []
    for seed in range(10):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        run = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=scratch, capture_output=True, text=True, check=False, env=env,
        )
        last = (run.stdout.strip().splitlines() or ["<no output>"])[-1]
        results.append(f"seed{seed}:{'ok' if run.returncode == 0 else 'FAIL'}")
        if run.returncode != 0:
            results.append(f"   last line: {last}")
    print(f"{alt.name}: " + " ".join(r for r in results if not r.startswith("   ")))
    for r in results:
        if r.startswith("   "):
            print(r)
    shutil.rmtree(scratch, ignore_errors=True)
