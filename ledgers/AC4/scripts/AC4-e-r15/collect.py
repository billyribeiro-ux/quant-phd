import sys, pathlib, subprocess, shutil
ROOT = pathlib.Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, workspace, PYTEST_FLAGS
u = unit("AC4"); cfg = panel(u)
work = workspace(u, u.directory / cfg["grader"] / "reference.py", cfg)
try:
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", cfg["suite"]], cwd=work, capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1])
finally:
    shutil.rmtree(work, ignore_errors=True)
