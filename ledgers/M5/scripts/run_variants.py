"""Run the M5 suite against each correct alternative (must pass) and each mutant (must fail on some seed).

Usage, from the repository root:

    .venv/bin/python ledgers/M5/scripts/run_variants.py --seeds 0-49 --mutant-seeds 0-9
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GRADER = ROOT / "course/modules/M/M5/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def parse(text: str) -> list[int]:
    seeds: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        seeds.extend(range(int(lo), int(hi or lo) + 1))
    return seeds


def run(solution: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="m5-variant-"))
    try:
        shutil.copy(GRADER / "test_project.py", work)
        shutil.copy(GRADER / "instance.py", work)
        shutil.copy(solution, work / "contraction_solver.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        failed = [line.split("::", 1)[1].split(" ")[0] for line in result.stdout.splitlines() if line.startswith("FAILED")]
        return result.returncode == 0, ", ".join(failed[:3])
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="0-49")
    parser.add_argument("--mutant-seeds", default="0-9")
    args = parser.parse_args()
    bad = 0
    for alt in sorted((ROOT / "ledgers/M5/alternatives").glob("*.py")):
        failures = []
        for seed in parse(args.seeds):
            ok, names = run(alt, seed)
            if not ok:
                failures.append((seed, names))
        print(f"ALTERNATIVE {alt.name}: {'PASS' if not failures else f'FAIL {failures[:3]}'}")
        bad += bool(failures)
    for mutant in sorted((ROOT / "ledgers/M5/mutants").glob("*.py")):
        killed = None
        for seed in parse(args.mutant_seeds):
            ok, names = run(mutant, seed)
            if not ok:
                killed = (seed, names)
                break
        print(f"MUTANT {mutant.name}: {'KILLED' if killed else 'SURVIVED'} (seed, first failing tests) {killed}")
        bad += killed is None
    print(f"run_variants: {'PASS' if not bad else 'FAIL'} ({bad} problems)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
