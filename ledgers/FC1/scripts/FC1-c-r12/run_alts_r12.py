"""Run the grader suite on alternative solution files over seeds (FC1 slice c, round 12).

Usage: run_alts_r12.py SEEDS FILE [FILE ...]   (SEEDS like 0-19). Uses the same pytest flags and environment
as tools/run_graders.py (run_suite). Prints one line per (file, seed) failure and a summary per file.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-FC1-c")
GRADER = ROOT / "course/modules/FC/FC1/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(solution: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="fc1c-r12-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(solution, work / "instruments.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        out = result.stdout[-2000:] + result.stderr[-2000:]
        found = re.search(r"FAILED \S+::(\S+)", out)
        tail = out.strip().splitlines()[-1] if out.strip() else ""
        return result.returncode == 0, (found.group(1) if found else tail)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    lo, hi = (int(x) for x in sys.argv[1].split("-"))
    failures = 0
    for arg in sys.argv[2:]:
        path = Path(arg).resolve()
        bad = []
        for seed in range(lo, hi + 1):
            ok, why = run(path, seed)
            if not ok:
                bad.append((seed, why))
        failures += len(bad)
        verdict = "PASS" if not bad else "FAIL"
        print(f"{verdict} {path.name}: {hi - lo + 1 - len(bad)}/{hi - lo + 1} seeds pass")
        for seed, why in bad[:5]:
            print(f"    seed {seed}: {why}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
