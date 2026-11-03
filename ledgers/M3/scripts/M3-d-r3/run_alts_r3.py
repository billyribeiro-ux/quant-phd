"""Run every alternative correct implementation and every equivalent file under the M3 grader, seeds 0-49 (verifier round 3).

Each candidate is copied with the suite and instance.py into a fresh scratch directory as covariance_doctor.py and run
with the browser's pytest flags. Usage (from the checkout root):
    .venv/bin/python -I ledgers/M3/scripts/M3-d-r3/run_alts_r3.py <candidate.py> [<candidate.py> ...]
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
    bad = 0
    for arg in sys.argv[1:]:
        cand = Path(arg).resolve()
        failed = []
        last = ""
        for seed in range(50):
            ok, tail = run(cand, seed)
            last = tail
            if not ok:
                failed.append(seed)
        verdict = "PASS" if not failed else "FAIL"
        bad += bool(failed)
        print(f"{verdict} {cand.relative_to(ROOT)}: failing seeds {failed[:10]}{' ...' if len(failed) > 10 else ''} (count {len(failed)}); last: {last}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
