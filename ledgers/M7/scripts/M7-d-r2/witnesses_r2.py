"""Round-2 over-constraint and tolerance witnesses for the M7 project suite.

Usage: .venv/bin/python ledgers/M7/scripts/M7-d-r2/witnesses_r2.py <scratch-dir>
Builds two workspaces under <scratch-dir> (each with the grader's test_project.py and instance.py):
  hand-2e-9/  the reference, with every two-asset answer moved 2e-9 along the budget-preserving direction;
  start-5e-9/ the reference with the starting-portfolio tolerance set to 5e-9 (the page states 1e-9).
Then runs the suite on seed 0 in each and prints the failing tests (or the pass count).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M7/grader"
REFERENCE = (GRADER / "reference.py").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")

HAND_WRAPPER = '''

def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    """Witness: the reference, with each two-asset answer moved 2e-9 along the budget-preserving direction."""
    out = _allocate_ref(instance)
    if len(out["weights"]) == 2:
        w = list(out["weights"])
        out["weights"] = [w[0] + 2e-9, w[1] - 2e-9]
    return out
'''


def workspace(name: str, source: str) -> Path:
    target = Path(sys.argv[1]) / name
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    shutil.copy(GRADER / "test_project.py", target)
    shutil.copy(GRADER / "instance.py", target)
    (target / "constrained_allocator.py").write_text(source, encoding="utf-8")
    return target


def run(target: Path) -> str:
    env = dict(os.environ, QF_SEED="0")
    proc = subprocess.run(
        [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=target, env=env, capture_output=True, text=True, check=False,
    )
    lines = [ln for ln in proc.stdout.splitlines() if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    return "\n".join(lines)


def main() -> int:
    hand = REFERENCE.replace("def allocate(instance: dict[str, Any]) -> dict[str, Any]:", "def _allocate_ref(instance: dict[str, Any]) -> dict[str, Any]:", 1)
    hand += HAND_WRAPPER
    print("hand-2e-9:\n" + run(workspace("hand-2e-9", hand)))
    tol = REFERENCE.replace("TOL = Fraction(1, 10**9)", "TOL = Fraction(5, 10**9)", 1)
    print("start-5e-9:\n" + run(workspace("start-5e-9", tol)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
