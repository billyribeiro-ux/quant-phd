"""Verifier round 3 (E2-d): each alt_r3_*.py through the E2 project suite on seeds 0-49 (as auction_sim.py).

Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r3/run_r3.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/E/E2/grader"
HERE = Path(__file__).resolve().parent


def passes(solution: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="e2-r3-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(solution, work / "auction_sim.py")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=work, capture_output=True, text=True, env=env, check=False,
        )
        tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-200:]
        return r.returncode == 0, tail
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    bad = 0
    files = [Path(a) for a in sys.argv[1:]] or sorted(HERE.glob("alt_r3_*.py"))
    for alt in files:
        fails = []
        for seed in range(50):
            ok, tail = passes(alt, seed)
            if not ok:
                fails.append((seed, tail))
        status = "PASS" if not fails else "FAIL"
        bad += bool(fails)
        print(f"{alt.name}: {status} (50 seeds); failures: {fails[:3]}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
