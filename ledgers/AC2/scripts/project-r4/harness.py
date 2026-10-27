"""Scratch harness: run the AC2 project suite on a candidate fundamentals.py for given seeds (not in the repo)."""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path("/tmp/verify-ac2r4-p")
sys.path.insert(0, str(REPO / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, parse_seeds, workspace  # noqa: E402


def main() -> int:
    cand = Path(sys.argv[1]).resolve()
    seeds = parse_seeds(sys.argv[2] if len(sys.argv) > 2 else "0-9")
    u = unit("AC2")
    cfg = panel(u)
    import shutil, os
    work = workspace(u, cand, cfg)
    total_fail = 0
    try:
        for seed in seeds:
            r = subprocess.run(
                [sys.executable, "-m", "pytest", *PYTEST_FLAGS, cfg["suite"]],
                cwd=work, capture_output=True, text=True, check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            fails = re.findall(r"FAILED \S+::(\S+?)(?: - (.*))?$", r.stdout, re.M)
            m = re.search(r"(\d+) (passed|failed)", r.stdout + r.stderr)
            summary = (r.stdout.strip().splitlines() or [""])[-1]
            print(f"seed {seed}: rc={r.returncode} :: {summary}")
            for name, msg in fails:
                print(f"   FAILED {name} :: {msg[:300]}")
            total_fail += len(fails)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
