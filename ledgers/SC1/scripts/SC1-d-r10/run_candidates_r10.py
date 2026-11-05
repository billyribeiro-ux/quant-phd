"""Run candidate bm_checks.py files against the SC1 grader suite, one fresh scratch directory per run.

Usage: python -I run_candidates_r10.py <seeds like 0-49> <candidate.py> [<candidate.py> ...]
The suite is the checkout's course/modules/SC/SC1/grader/test_project.py, run as the page does:
QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py.
Prints one line per candidate: PASSED_ALL_SEEDS, or KILLED with the seeds and the first failing test.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyE10-SC1-d")
PY = str(REPO / ".venv" / "bin" / "python")
GRADER = REPO / "course" / "modules" / "SC" / "SC1" / "grader"


def run_one(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="sc1d-r10-cand-"))
    try:
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(os.environ.get("TEST_FILE", str(GRADER / "test_project.py")), work / "test_project.py")
        shutil.copy(candidate, work / "bm_checks.py")
        env = dict(os.environ, QF_SEED=str(seed))
        proc = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True, timeout=120,
        )
        out = proc.stdout + proc.stderr
        failed = re.findall(r"FAILED \S+", out)
        return proc.returncode == 0, (failed[0] if failed else out.strip().splitlines()[-1][:160])
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> None:
    lo, _, hi = sys.argv[1].partition("-")
    seeds = range(int(lo), int(hi or lo) + 1)
    for cand in map(Path, sys.argv[2:]):
        passed, killed = [], []
        for seed in seeds:
            ok, info = run_one(cand, seed)
            (passed if ok else killed).append((seed, info))
        if not killed:
            print(f"PASSED {cand.name}: all {len(passed)} seeds in {sys.argv[1]}")
        else:
            print(f"KILLED {cand.name}: {len(killed)} of {len(seeds)} seeds fail; first seed {killed[0][0]} -> {killed[0][1]}")
            print(f"   seeds that did not kill: {[s for s, _ in passed][:60]}")


if __name__ == "__main__":
    main()
