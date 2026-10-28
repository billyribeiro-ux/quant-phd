import sys, subprocess, shutil, os
sys.path.insert(0, "/tmp/verify13-CF1-d/tools")
from coursekit import unit
from run_graders import panel, workspace
u = unit("CF1"); cfg = panel(u)
seeds = [0, 1, 7, 49, 134675774]
counts = {}
for s in seeds:
    work = workspace(u, u.directory / cfg["grader"] / "reference.py", cfg)
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", cfg["suite"]], cwd=work,
                       capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
    counts[s] = r.stdout.strip().splitlines()[-1]
    shutil.rmtree(work, ignore_errors=True)
print(counts)
