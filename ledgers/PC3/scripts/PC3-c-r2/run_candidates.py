"""Run candidate market_maker.py modules through the PC3 grader suite, seed by seed (round 1, slice c).

Each candidate is copied as market_maker.py into a fresh temporary workspace together with the public grader files
(test_project.py, engine.py, instance.py), and the suite runs under the browser's flags with QF_SEED set to each seed.
A candidate that is a correct implementation must pass every seed; a mutant must fail at least one.

Usage (from the checkout root):
    .venv/bin/python ledgers/PC3/scripts/PC3-c-r1/run_candidates.py --seeds 0-49 <candidate.py> [<candidate.py> ...]
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

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/PC/PC3/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def parse_seeds(text: str) -> list[int]:
    seeds: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        seeds.extend(range(int(lo), int(hi or lo) + 1))
    return seeds


def run_one(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="pc3c-cand-"))
    try:
        for name in ("test_project.py", "engine.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(candidate, work / "market_maker.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        found = re.search(r"FAILED \S+::(\S+)", result.stdout)
        return result.returncode == 0, found.group(1) if found else ""
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="0-49")
    parser.add_argument("candidates", nargs="+", type=Path)
    args = parser.parse_args()
    seeds = parse_seeds(args.seeds)
    for candidate in args.candidates:
        failures: dict[int, str] = {}
        for seed in seeds:
            ok, name = run_one(candidate, seed)
            if not ok:
                failures[seed] = name
        verdict = "PASS" if not failures else "FAIL"
        first = next(iter(failures.items()), None)
        detail = f"first failing seed {first[0]} test {first[1]}" if first else f"all {len(seeds)} seeds pass"
        print(f"{verdict} {candidate.name}: {len(seeds) - len(failures)}/{len(seeds)} seeds pass; {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
