"""Run the CS2 grader suite (test_project.py) against one streamstats.py candidate, seed by seed.

Usage: python -I harness.py <candidate.py> <seed_lo> <seed_hi>
Copies the grader's suite and instance into a fresh temp directory outside the checkout, as streamstats.py
the candidate, and runs pytest with the same flags and environment as tools/run_graders.py.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyD15-CS2-d/course/modules/CS/CS2/grader")
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="cs2d-r15-"))
    try:
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(candidate, work / "streamstats.py")
        res = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        out = res.stdout[-3000:] + res.stderr[-1000:]
        return res.returncode == 0, out
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    cand = Path(sys.argv[1]).resolve()
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    failed: list[int] = []
    first_out = ""
    for seed in range(lo, hi + 1):
        ok, out = run(cand, seed)
        if not ok:
            failed.append(seed)
            if not first_out:
                first_out = out
    total = hi - lo + 1
    print(f"{cand.name}: {total - len(failed)}/{total} seeds pass; failing seeds: {failed[:12]}")
    if failed:
        lines = [ln for ln in first_out.splitlines() if "FAILED" in ln or "passed" in ln or "failed" in ln]
        print("\n".join(lines[:8]))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
