"""Round-5 verifier (CS2-d): list every failing test of one module on one seed (not just the first)."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "tools"))
import os  # noqa: E402

from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, workspace  # noqa: E402

u = unit("CS2")
cfg = panel(u)
seed = int(sys.argv[2])
for name in sys.argv[3:]:
    work = workspace(u, Path(name).resolve(), cfg)
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pytest", *PYTEST_FLAGS, cfg["suite"]],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        )
        failed = re.findall(r"FAILED \S+::(\S+)", r.stdout + r.stderr)
        print(Path(name).name, "seed", seed, "failed:", failed)
    finally:
        shutil.rmtree(work, ignore_errors=True)
