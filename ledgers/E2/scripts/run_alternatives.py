"""Run each alternative correct implementation through the E2 suite on seeds 0-49, in a scratch workspace.

Usage (from the repository root): .venv/bin/python -I ledgers/E2/scripts/run_alternatives.py
Every alternative must pass every seed. The symmetric bid of each alternative is also compared with the reference over
n = 2..5 and value = 0..10000 (exhaustive, exact integers).
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GRADER = ROOT / "course" / "modules" / "E" / "E2" / "grader"
SCRIPTS = Path(__file__).resolve().parent


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def suite_passes(solution: Path, seed: int) -> bool:
    work = Path(tempfile.mkdtemp(prefix="e2-alt-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(solution, work / "auction_sim.py")
        result = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=work, capture_output=True, text=True, check=False,
            env={"PATH": "/usr/bin:/bin", "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        )
        return result.returncode == 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    reference = load(GRADER / "reference.py", "reference")
    status = 0
    for alt in sorted(SCRIPTS.glob("alt*.py")):
        module = load(alt, alt.stem)
        mismatches = sum(
            1
            for n in range(2, 6)
            for value in range(0, 10_001)
            if module.symmetric_bid_single_unit("discriminatory", n, value)
            != reference.symmetric_bid_single_unit("discriminatory", n, value)
        )
        passed = sum(suite_passes(alt, seed) for seed in range(50))
        verdict = "PASS" if passed == 50 and mismatches == 0 else "FAIL"
        status |= verdict == "FAIL"
        print(f"{alt.name}: {verdict} suite {passed}/50 seeds; symmetric-bid mismatches vs reference {mismatches}")
    return status


if __name__ == "__main__":
    sys.exit(main())
