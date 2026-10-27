"""Collect the AC2 grader with QF_SEED set to several seeds; the count must be 240 on each."""
import os, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa
from run_graders import panel, workspace  # noqa
u = unit("AC2"); cfg = panel(u)
for seed in [0, 1, 7, 25, 49]:
    work = workspace(u, ROOT / "course/modules/AC/AC2/grader/reference.py", cfg)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", cfg["suite"]], cwd=work, capture_output=True, text=True,
                           env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        print("seed", seed, r.stdout.strip().splitlines()[-1])
    finally:
        shutil.rmtree(work, ignore_errors=True)
