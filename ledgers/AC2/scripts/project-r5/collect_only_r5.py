"""Round 5 (AC2 project): count collected checks for the reference on a few seeds (scratch, not in the repo)."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/tmp/verify-ac2r5-p")
sys.path.insert(0, str(REPO / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, workspace  # noqa: E402

u = unit("AC2")
cfg = panel(u)
ref = REPO / "course/modules/AC/AC2/grader/reference.py"
work = workspace(u, ref, cfg)
try:
    for seed in (0, 1, 7, 12345):
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", cfg["suite"]],
                           cwd=work, capture_output=True, text=True, env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        m = re.search(r"(\d+) tests? collected", r.stdout + r.stderr)
        print(f"seed {seed}: rc={r.returncode} collected={m.group(1) if m else r.stdout[-200:]}")
finally:
    shutil.rmtree(work, ignore_errors=True)
