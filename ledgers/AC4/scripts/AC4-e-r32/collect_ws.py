import sys, pathlib, subprocess
ROOT = pathlib.Path("/tmp/verify32-AC4-e"); sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, workspace
u = unit("AC4"); cfg = panel(u)
src = pathlib.Path(sys.argv[1])
work = workspace(u, src, cfg)
r = subprocess.run([sys.executable, "-I", "-m", "pytest", "--collect-only", "-q", "-W", "error", cfg["suite"]], cwd=work, capture_output=True, text=True)
print(r.stdout[-400:], r.stderr[-400:], "rc", r.returncode)
