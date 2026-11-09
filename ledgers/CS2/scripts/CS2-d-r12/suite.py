"""Run the CS2 project suite against one solution file for a list of seeds.

Usage: python suite.py <solution.py> <seeds: a-b or a,b,c> [--collect]
Copies test_project.py and instance.py from the verifier checkout's grader into a fresh temp workspace as
streamstats.py plus the grader files, runs pytest with QF_SEED set, and prints one line per seed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "CS" / "CS2" / "grader"
PY = ROOT / ".venv" / "bin" / "python"


def seeds_of(spec: str) -> list[int]:
    if "-" in spec:
        a, b = spec.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(s) for s in spec.split(",")]


def main() -> int:
    solution = Path(sys.argv[1]).resolve()
    seeds = seeds_of(sys.argv[2])
    collect = "--collect" in sys.argv
    failed = 0
    for seed in seeds:
        work = Path(tempfile.mkdtemp(prefix="cs2d_"))
        try:
            shutil.copy(GRADER / "test_project.py", work)
            shutil.copy(GRADER / "instance.py", work)
            shutil.copy(solution, work / "streamstats.py")
            env = {**os.environ, "QF_SEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1"}
            args = [str(PY), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
            if collect:
                args.append("--collect-only")
            args.append("test_project.py")
            res = subprocess.run(args, cwd=work, env=env, capture_output=True, text=True, timeout=300)
            tail = (res.stdout.strip().splitlines() or [""])[-1]
            first = next((ln for ln in res.stdout.splitlines() if ln.startswith("FAILED")), "")
            print(f"seed {seed} rc={res.returncode} {tail} {first[:160]}")
            failed += res.returncode != 0
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"seeds_failed={failed} of {len(seeds)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
