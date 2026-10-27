"""Round 5 (AC2 project): run the AC2 suite on one candidate module over a seed window (scratch harness, not in the repo)."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/tmp/verify-ac2r6-p")
sys.path.insert(0, str(REPO / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, parse_seeds, workspace  # noqa: E402


def main() -> int:
    cand = Path(sys.argv[1]).resolve()
    seeds = parse_seeds(sys.argv[2] if len(sys.argv) > 2 else "0-9")
    u = unit("AC2")
    cfg = panel(u)
    work = workspace(u, cand, cfg)
    passed_seeds = 0
    try:
        for seed in seeds:
            r = subprocess.run(
                [sys.executable, "-m", "pytest", *PYTEST_FLAGS, cfg["suite"]],
                cwd=work, capture_output=True, text=True, check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            summary = (r.stdout.strip().splitlines() or [""])[-1]
            if r.returncode == 0:
                passed_seeds += 1
            else:
                fails = re.findall(r"FAILED \S+::(\S+)", r.stdout)
                print(f"seed {seed}: rc={r.returncode} :: {summary} :: {fails[:3]}")
        print(f"{cand.name}: passed {passed_seeds}/{len(seeds)} seeds")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
