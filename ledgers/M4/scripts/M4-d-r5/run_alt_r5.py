"""Run the M4 suite (grader/test_project.py, the page's own flags) against each round-5 alternative, seed by seed.

Usage: python3 ledgers/M4/scripts/M4-d-r5/run_alt_r5.py <lo> <hi>
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
HERE = Path(__file__).resolve().parent
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(solution: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="m4-r5-alt-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(solution, work / "tail_risk.py")
        env = dict(os.environ, QF_SEED=str(seed))
        res = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        failed = [line.split("::")[-1] for line in res.stdout.splitlines() if line.startswith("FAILED")]
        return res.returncode == 0, ", ".join(failed)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    lo, hi = (int(x) for x in sys.argv[1:3])
    impls = [*sorted(HERE.glob("alt_r5_*.py")), ROOT / "ledgers/M4/scripts/alt_1.py"]
    status = 0
    for impl in impls:
        bad = []
        for seed in range(lo, hi):
            ok, detail = run(impl, seed)
            if not ok:
                bad.append((seed, detail))
        print(f"{impl.relative_to(ROOT)}: {'PASS' if not bad else 'FAIL'} seeds {lo}-{hi - 1} ({len(bad)} failing)")
        for seed, detail in bad[:5]:
            print(f"   seed {seed}: {detail}")
        status |= bool(bad)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
