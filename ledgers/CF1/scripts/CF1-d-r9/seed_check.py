"""Run the CF1 suite on the reference solution for one seed (uses tools/run_graders workspace), print failures."""
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, workspace  # noqa: E402

u = unit("CF1")
cfg = panel(u)
seed = int(sys.argv[2])
ref = u.directory / cfg["grader"] / "reference.py"
work = workspace(u, ref, cfg)
try:
    r = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "--assert=plain", "-W", "error", cfg["suite"]],
                       cwd=work, capture_output=True, text=True,
                       env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
    print("exit", r.returncode)
    print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if l.startswith("FAILED") or "passed" in l or "failed" in l or l.startswith("E ")))
    print("tail:", r.stdout[-1500:])
finally:
    shutil.rmtree(work, ignore_errors=True)
