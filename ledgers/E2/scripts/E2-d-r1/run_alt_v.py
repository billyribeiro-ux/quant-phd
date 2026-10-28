"""Verifier runner: the alternative above through the E2 suite on seeds 0-49, and an exhaustive symmetric-bid check.

Usage: .venv/bin/python -I ledgers/E2/scripts/E2-d-r1/run_alt_v.py   (from the repository root)
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
ALT = Path(__file__).resolve().parent / "alt_v_divmod.py"


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def passes(seed: int) -> bool:
    work = Path(tempfile.mkdtemp(prefix="e2-altv-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(ALT, work / "auction_sim.py")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain",
                            "-W", "error", "test_project.py"], cwd=work, capture_output=True, text=True, env=env,
                           check=False)
        return r.returncode == 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    ref = load(GRADER / "reference.py", "reference")
    alt = load(ALT, "alt_v")
    mism = sum(1 for n in range(2, 6) for v in range(10001)
               if alt.symmetric_bid_single_unit("discriminatory", n, v) != ref.symmetric_bid_single_unit("discriminatory", n, v))
    passed = sum(passes(s) for s in range(50))
    print(f"alt_v_divmod: suite {passed}/50 seeds, symmetric-bid mismatches vs reference {mism}")
    return 0 if passed == 50 and mism == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
