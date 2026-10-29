"""Round-3: show which test fails for alternative 4 (bisection inversion of the prospect value) on seeds 26, 29, 44, 45.
Usage (from the checkout): .venv/bin/python -I ledgers/E3/scripts/E3-d-r3/alt4_failures.py
The alternative is built by ledgers/E3/scripts/run_alternatives.py (its build function), staged in a scratch directory.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "ledgers/E3/scripts"))
import run_alternatives as ra  # noqa: E402

GRADER = ROOT / "course/modules/E/E3/grader"
for seed in (26, 29, 44, 45):
    work = Path(tempfile.mkdtemp(prefix="e3-alt4-"))
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / f, work / f)
        (work / "elicit.py").write_text(ra.build("alt4"), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, capture_output=True, text=True, check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        )
        lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.startswith(("FAILED", "E  ", "E ")) or "passed" in ln or "failed" in ln]
        print("seed", seed, "rc", r.returncode)
        for ln in lines[:6]:
            print("   ", ln[:300])
    finally:
        shutil.rmtree(work, ignore_errors=True)
