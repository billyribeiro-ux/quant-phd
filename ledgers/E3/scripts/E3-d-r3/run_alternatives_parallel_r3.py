"""Round-3 verifier (E3-d): the five alternatives of ledgers/E3/scripts/run_alternatives.py, one (alternative, seed)
pair per process, run in parallel. Same build() and the same pytest flags as the tool; only the scheduling differs.

Usage: .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/run_alternatives_parallel_r3.py --seeds 0-9 --workers 12
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "ledgers/E3/scripts"
GRADER = ROOT / "course/modules/E/E3/grader"
sys.path.insert(0, str(SCRIPTS))
import run_alternatives as ra  # noqa: E402


def run_one(name: str, seed: int) -> tuple[str, int, bool, str]:
    work = Path(tempfile.mkdtemp(prefix=f"e3-r3-{name}-{seed}-"))
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / f, work / f)
        (work / "elicit.py").write_text(ra.build(name), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "pytest",
                "-q",
                "-p",
                "no:cacheprovider",
                "--assert=plain",
                "-W",
                "error",
                "test_project.py",
            ],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0",
                 "PYTHONDONTWRITEBYTECODE": "1"},
        )
        tail = (result.stdout.strip().splitlines() or [""])[-1]
        return name, seed, result.returncode == 0, tail
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="0-9")
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    seeds = ra.seeds_of(args.seeds)
    jobs = [(name, seed) for name in ra.ALTERNATIVES for seed in seeds]
    results: dict[str, list[tuple[int, bool, str]]] = {name: [] for name in ra.ALTERNATIVES}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for name, seed, ok, tail in pool.map(lambda j: run_one(*j), jobs):
            results[name].append((seed, ok, tail))
            print(f"{name} seed {seed}: {'pass' if ok else 'FAIL'} [{tail}]", flush=True)
    status = 0
    for name, rows in results.items():
        failed = sorted(seed for seed, ok, _ in rows if not ok)
        verdict = "PASS" if not failed else "FAIL"
        status |= bool(failed)
        print(f"{name}: {verdict} ({len(rows) - len(failed)}/{len(rows)} seeds"
              f"{'' if not failed else f'; failing seeds {failed}'})", flush=True)
    return status


if __name__ == "__main__":
    sys.exit(main())
