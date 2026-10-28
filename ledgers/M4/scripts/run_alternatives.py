#!/usr/bin/env python3
"""Run the M4 suite against each alternative implementation (alt_1..alt_5) and the reference, seed by seed.

Each implementation must pass the whole suite (grader/test_project.py, under the browser's pytest flags) on every
seed in the window. A failing seed is printed with the failing test names only.

Usage::

    python3 ledgers/M4/scripts/run_alternatives.py --seeds 0-49
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GRADER = ROOT / "course/modules/M/M4/grader"
SCRIPTS = Path(__file__).resolve().parent
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run_one(solution: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="m4-alt-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(solution, work / "tail_risk.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        failed = re.findall(r"FAILED \S+::(\S+)", result.stdout)
        return result.returncode == 0, ", ".join(failed) or result.stdout[-400:]
    finally:
        shutil.rmtree(work, ignore_errors=True)


def parse_seeds(text: str) -> list[int]:
    lo, _, hi = text.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seeds", default="0-49")
    args = parser.parse_args()
    seeds = parse_seeds(args.seeds)
    solutions = [GRADER / "reference.py", *sorted(SCRIPTS.glob("alt_*.py"))]
    failures = 0
    for solution in solutions:
        bad = []
        for seed in seeds:
            ok, detail = run_one(solution, seed)
            if not ok:
                bad.append(f"seed {seed}: {detail}")
        failures += bool(bad)
        verdict = "PASS" if not bad else "FAIL"
        print(f"{solution.relative_to(ROOT)}: {verdict} ({len(seeds) - len(bad)}/{len(seeds)} seeds)")
        for line in bad[:5]:
            print(f"    {line}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
