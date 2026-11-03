"""For each mutant given, list every failing test of the CS2 suite on seed 0 (all failures, not only the first).
Usage: python -I kill_detail.py <repo_root> <mutant.py> [...]"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, workspace  # noqa: E402

u = unit("CS2")
cfg = panel(u)
for name in sys.argv[2:]:
    path = Path(name).resolve()
    work = workspace(u, path, cfg)
    try:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": os.environ.get("SEED", "0"), "PYTHONHASHSEED": "0"}
        res = subprocess.run([sys.executable, "-m", "pytest", *PYTEST_FLAGS, "-rf", cfg["suite"]], cwd=work,
                             capture_output=True, text=True, env=env, check=False)
        failed = re.findall(r"^FAILED \S+::(\S+)", res.stdout, re.M)
        print(f"{path.name}: {len(failed)} failing tests on seed 0; exit {res.returncode}")
        for f in failed:
            print("   ", f)
    finally:
        shutil.rmtree(work, ignore_errors=True)
