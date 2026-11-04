"""Run the grader on every alternative and on the reference, seeds 0-49, under the browser's pytest flags (run_graders convention)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
GRADER = ROOT / "course/modules/SC/SC1/grader"
ALTS = sorted((ROOT / "ledgers/SC1/scripts/SC1-d-r1/alternatives").glob("*.py"))
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(solution: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="sc1d-alt-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(solution, work / "bm_checks.py")
    env = {**os.environ, "QF_SEED": str(seed)}
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
        cwd=work, env=env, capture_output=True, text=True, timeout=300,
    )
    last = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-300:]
    shutil.rmtree(work, ignore_errors=True)
    return proc.returncode == 0, last


def main() -> None:
    targets = [(ROOT / "course/modules/SC/SC1/grader/reference.py")] + ALTS
    failed_any = False
    for target in targets:
        bad: list[tuple[int, str]] = []
        for seed in range(50):
            ok, last = run(target, seed)
            if not ok:
                bad.append((seed, last))
        status = "PASS" if not bad else "FAIL"
        failed_any |= bool(bad)
        print(f"{target.name}: {status} ({50 - len(bad)}/50 seeds pass)")
        for seed, last in bad[:6]:
            print(f"   seed {seed}: {last}")
    sys.exit(1 if failed_any else 0)


if __name__ == "__main__":
    main()
