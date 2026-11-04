"""Round-4 verifier runner: every candidate module under the M3 project suite, for a seed window.

Each candidate is copied with test_project.py and instance.py into a fresh scratch directory as covariance_doctor.py
and run with the browser's pytest flags. Usage (from the checkout root):
    .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/run_alts_r4.py <lo> <hi> <candidate.py> [<candidate.py> ...]
A candidate passes when every seed in [lo, hi] passes.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
GRADER = ROOT / "course/modules/M/M3/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="m3alt-"))
    shutil.copy(candidate, work / "covariance_doctor.py")
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    env = {"PATH": os.environ["PATH"], "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    res = subprocess.run(
        [sys.executable, "-I", "-m", "pytest", *FLAGS, "test_project.py"],
        cwd=work, capture_output=True, text=True, env=env, timeout=300,
    )
    shutil.rmtree(work, ignore_errors=True)
    tail = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else res.stderr.strip()[-200:]
    return res.returncode == 0, tail


def main() -> int:
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    bad = 0
    for arg in sys.argv[3:]:
        cand = Path(arg).resolve()
        failed = []
        last = ""
        for seed in range(lo, hi + 1):
            ok, tail = run(cand, seed)
            last = tail
            if not ok:
                failed.append(seed)
        verdict = "PASS" if not failed else "FAIL"
        bad += bool(failed)
        print(f"{verdict} {cand.relative_to(ROOT)}: seeds {lo}-{hi} failing {failed[:10]} (count {len(failed)}); last: {last}", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
