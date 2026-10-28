import sys, pathlib, subprocess, shutil, os
ROOT = pathlib.Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, workspace
u = unit("AC4"); cfg = panel(u)
work = workspace(u, u.directory / cfg["grader"] / "reference.py", cfg)
try:
    for s in [int(x) for x in sys.argv[2:]]:
        env = dict(os.environ, QF_SEED=str(s))
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", cfg["suite"]], cwd=work, capture_output=True, text=True, env=env)
        print("seed", s, r.stdout.strip().splitlines()[-1])
finally:
    shutil.rmtree(work, ignore_errors=True)
