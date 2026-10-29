"""Verifier M5-d round 1: run the project suite (course/modules/M/M5/grader) against each given solution module.

Usage: .venv/bin/python ledgers/M5/scripts/M5-d-r1/run_d_variants.py --seeds 0-49 FILE [FILE ...]
Prints, per file, PASS (all seeds green) or the first failing seed with its failing test names.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M5/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def seeds_of(text: str) -> list[int]:
    out: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


def run(solution: Path, seed: int) -> tuple[int, str]:
    work = Path(tempfile.mkdtemp(prefix="m5d-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work)
        shutil.copy(solution, work / "contraction_solver.py")
        res = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=600,
        )
        failed = [ln.split("::", 1)[1].split(" ")[0] for ln in res.stdout.splitlines() if ln.startswith("FAILED")]
        tail = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else res.stderr.strip()[-200:]
        return res.returncode, ", ".join(failed[:4]) + " | " + tail
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="0-49")
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()
    for f in args.files:
        path = Path(f)
        result = "PASS"
        for seed in seeds_of(args.seeds):
            code, info = run(path, seed)
            if code != 0:
                result = f"FAIL seed {seed}: {info}"
                break
        print(f"{path.name}: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
