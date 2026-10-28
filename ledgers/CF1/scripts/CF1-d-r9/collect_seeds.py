"""Collect-only count of the CF1 grader on the reference solution for each seed (uses tools/run_graders workspace)."""
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
print("panel", {k: v for k, v in cfg.items() if k in ("grader", "suite", "solution", "support")})
ref = u.directory / cfg["grader"] / "reference.py"
counts = {}
for seed in range(int(sys.argv[2])):
    work = workspace(u, ref, cfg)
    try:
        r = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-m", "pytest", "--collect-only", "-q",
                            "-p", "no:cacheprovider", "--assert=plain", "-W", "error", cfg["suite"]],
                           cwd=work, capture_output=True, text=True,
                           env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        m = re.search(r"(\d+) tests? collected", r.stdout + r.stderr)
        counts.setdefault(m.group(1) if m else "NONE:" + r.stdout[-200:], []).append(seed)
    finally:
        shutil.rmtree(work, ignore_errors=True)
print({k: (len(v), v[:3]) for k, v in counts.items()})
