"""Verifier round 2 runner: each alt_r2_*.py through the E2 suite on seeds 0-49, plus an exhaustive symmetric-bid check.

Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r2/run_r2.py
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/E/E2/grader"
HERE = Path(__file__).resolve().parent


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def passes(solution: Path, seed: int) -> bool:
    work = Path(tempfile.mkdtemp(prefix="e2-r2-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(solution, work / "auction_sim.py")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run(
            [
                sys.executable,
                "-I",
                "-m",
                "pytest",
                "-q",
                "-p",
                "no:cacheprovider",
                "--assert=plain",
                "-W",
                "error",
                "test_project.py",
            ],
            cwd=work,
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        return r.returncode == 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    ref = load(GRADER / "reference.py", "reference")
    status = 0
    for path in sorted(HERE.glob("alt_r2_*.py")):
        alt = load(path, path.stem)
        mism = sum(
            1
            for n in range(2, 6)
            for v in range(10001)
            if alt.symmetric_bid_single_unit("discriminatory", n, v)
            != ref.symmetric_bid_single_unit("discriminatory", n, v)
        )
        passed = sum(passes(path, s) for s in range(50))
        ok = passed == 50 and mism == 0
        status |= not ok
        print(
            f"{path.name}: {'PASS' if ok else 'FAIL'} suite {passed}/50 seeds; symmetric-bid mismatches vs reference {mism}"
        )
    return status


if __name__ == "__main__":
    raise SystemExit(main())
