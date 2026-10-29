"""Run the CS2 project suite against candidate streamstats.py files, seed by seed (verifier script, CS2-d round 1).

Usage: python -I run_candidates.py <checkout> <seeds a-b> <candidate.py> [<candidate.py> ...]
Copies the grader's suite and instance into a fresh temporary workspace per candidate, runs the suite under the
same flags as tools/run_graders.py (-W error, --assert=plain, QF_SEED), and prints pass counts and the failing tests.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    checkout = Path(sys.argv[1])
    lo, _, hi = sys.argv[2].partition("-")
    seeds = range(int(lo), int(hi or lo) + 1)
    grader = checkout / "course/modules/CS/CS2/grader"
    py = checkout / ".venv/bin/python"
    for cand in map(Path, sys.argv[3:]):
        work = Path(tempfile.mkdtemp(prefix="cs2-cand-"))
        shutil.copy(grader / "test_project.py", work)
        shutil.copy(grader / "instance.py", work)
        shutil.copy(cand, work / "streamstats.py")
        passed = 0
        failing: dict[str, list[int]] = {}
        for seed in seeds:
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
            res = subprocess.run(
                [str(py), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                cwd=work, capture_output=True, text=True, env=env, check=False, timeout=600,
            )
            if res.returncode == 0:
                passed += 1
            for name in re.findall(r"FAILED test_project\.py::(\S+)", res.stdout):
                failing.setdefault(name.split("[")[0], []).append(seed)
        print(f"{cand.name}: {passed}/{len(seeds)} seeds pass")
        for name, got in sorted(failing.items()):
            print(f"  fails {name} on seeds {got[:12]}{' ...' if len(got) > 12 else ''} ({len(got)} seeds)")
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
