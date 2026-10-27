import shutil, subprocess, sys
from pathlib import Path
ROOT = Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa
from run_graders import panel, workspace  # noqa
u = unit("AC2"); cfg = panel(u)
work = workspace(u, ROOT / "course/modules/AC/AC2/grader/reference.py", cfg)
try:
    r = subprocess.run([str(ROOT / ".venv/bin/python"), "-m", "pytest", "--collect-only", "-q", cfg["suite"]], cwd=work, capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1])
finally:
    shutil.rmtree(work, ignore_errors=True)
