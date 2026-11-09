"""Run the E4 project suite against one candidate solver, mirroring tools/run_graders.py workspace().

Usage: python -I run_candidate.py <solver.py> <seed-spec e.g. 0-49> [--collect]
Prints one line per seed: PASS/FAIL and the first failing test line; with --collect prints the collect-only count.
The suite is copied from course/modules/E/E4/grader/ (the panel's data-suite and data-support), the candidate becomes solver.py,
and pytest runs with the same flags and environment as run_graders.py (QF_SEED per seed, PYTHONHASHSEED=0).
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.environ.get("E4_ROOT", "/Users/billyribeiro/.fanout/wt/verifyE15-E4-d"))
GRADER = ROOT / "course/modules/E/E4/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def workspace(candidate: Path) -> Path:
    work = Path(tempfile.mkdtemp(prefix="e4cand-"))
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    shutil.copy(candidate, work / "solver.py")
    return work


def run(work: Path, seed: int | None, extra: list[str]) -> subprocess.CompletedProcess[str]:
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PYTHONHASHSEED": "0"}
    if seed is not None:
        env["QF_SEED"] = str(seed)
    return subprocess.run(
        [sys.executable, "-I", "-m", "pytest", *FLAGS, *extra, "test_project.py"],
        cwd=work, capture_output=True, text=True, check=False, env=env, timeout=300,
    )


def main() -> None:
    cand = Path(sys.argv[1]).resolve()
    if "--collect" in sys.argv:
        work = workspace(cand)
        r = run(work, 0, ["--collect-only"])
        print("\n".join(l for l in r.stdout.splitlines() if "collected" in l or "tests collected" in l or re.search(r"\d+ tests? collected", l)))
        print("collect exit", r.returncode)
        return
    lo, _, hi = sys.argv[2].partition("-")
    seeds = range(int(lo), int(hi or lo) + 1)
    fails = []
    for seed in seeds:
        work = workspace(cand)
        r = run(work, seed, [])
        if r.returncode != 0:
            failed = [l for l in r.stdout.splitlines() if l.startswith("FAILED")]
            fails.append((seed, failed[:2] or [r.stdout[-300:]]))
        shutil.rmtree(work, ignore_errors=True)
    print(f"{cand.name}: {len(seeds) - len(fails)}/{len(seeds)} seeds pass")
    for seed, f in fails[:5]:
        print(f"  seed {seed}: {f}")


if __name__ == "__main__":
    main()
