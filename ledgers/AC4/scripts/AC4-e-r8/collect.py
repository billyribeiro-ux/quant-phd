"""Collect-only count and seed run of the AC4 autograder against a solution file."""
import sys
from pathlib import Path
sys.path.insert(0, "/tmp/verify8-AC4-e/tools")
from coursekit import unit
from run_graders import panel, workspace, run_suite, PYTEST_FLAGS
import subprocess
u = unit("AC4")
cfg = panel(u)
sol = Path(sys.argv[1])
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
work = workspace(u, sol, cfg)
print("PYTEST_FLAGS", PYTEST_FLAGS)
r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", *PYTEST_FLAGS, cfg["suite"]], cwd=work, capture_output=True, text=True)
print(r.stdout[-300:], r.stderr[-300:])
ok, out, el = run_suite(work, cfg["suite"], seed)
print("seed", seed, "ok", ok, "elapsed", round(el, 2))
print(out[-400:])
