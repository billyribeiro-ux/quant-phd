"""Run the CS2 suite on one candidate file for each seed and report the seeds it passes and the failing tests.
Usage: QF_SEEDS=0-49 python -I run_seeds_pass.py <repo_root> <candidate.py>"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, parse_seeds, workspace  # noqa: E402

u = unit("CS2")
cfg = panel(u)
cand = Path(sys.argv[2]).resolve()
passed: list[int] = []
fails: dict[int, list[str]] = {}
for seed in parse_seeds(os.environ.get("QF_SEEDS", "0-49")):
    work = workspace(u, cand, cfg)
    try:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        res = subprocess.run([sys.executable, "-m", "pytest", *PYTEST_FLAGS, "-rf", cfg["suite"]], cwd=work,
                             capture_output=True, text=True, env=env, check=False)
        if res.returncode == 0:
            passed.append(seed)
        else:
            fails[seed] = re.findall(r"^FAILED \S+::(\S+)", res.stdout, re.M)
    finally:
        shutil.rmtree(work, ignore_errors=True)
print(f"{cand.name}: passes the suite on {len(passed)} of {len(passed) + len(fails)} seeds")
print("seeds passed:", passed)
for s in sorted(fails)[:12]:
    print(f"seed {s} fails:", fails[s][:4])
