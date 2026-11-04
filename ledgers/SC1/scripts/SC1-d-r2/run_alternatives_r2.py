"""Run the SC1 grader's suite on the reference and on each round-2 alternative, for the given seeds.

Usage: python ledgers/SC1/scripts/SC1-d-r2/run_alternatives_r2.py <repo-root> <seed-spec> [name-filter]
Each run copies test_project.py and instance.py from grader/ into a scratch directory with the candidate as bm_checks.py,
and runs pytest with the browser's flags (--assert=plain -W error) and QF_SEED set to the seed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
SEEDS = range(50) if sys.argv[2] == "0-49" else [int(x) for x in sys.argv[2].split(",")]
FILTER = sys.argv[3] if len(sys.argv) > 3 else ""
GRADER = ROOT / "course/modules/SC/SC1/grader"
ALTS = sorted((ROOT / "ledgers/SC1/scripts/SC1-d-r2/alternatives").glob("*.py"))
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(solution: Path, seed: int, timeout: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="sc1d-r2-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(solution, work / "bm_checks.py")
    env = {**os.environ, "QF_SEED": str(seed)}
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True, timeout=timeout,
        )
        last = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-300:]
        return proc.returncode == 0, last
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {timeout}s"
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> None:
    targets = [GRADER / "reference.py", *ALTS]
    failed_any = False
    for target in targets:
        if FILTER and FILTER not in target.name:
            continue
        bad: list[tuple[int, str]] = []
        for seed in SEEDS:
            ok, last = run(target, seed, timeout=240)
            if not ok:
                bad.append((seed, last))
                if "TIMEOUT" in last:
                    break
        status = "PASS" if not bad else "FAIL"
        failed_any |= bool(bad)
        print(f"{target.name}: {status} ({len(SEEDS) - len(bad)}/{len(SEEDS)} seeds pass)")
        for seed, last in bad[:6]:
            print(f"   seed {seed}: {last}")
    sys.exit(1 if failed_any else 0)


if __name__ == "__main__":
    main()
