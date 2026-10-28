import sys, pathlib, subprocess, os, shutil
ROOT = pathlib.Path("/tmp/verify42-AC4-e"); sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, workspace
u = unit("AC4"); cfg = panel(u)
src = ROOT / "course/modules/AC/AC4/grader/reference.py"
counts = {}
work = workspace(u, src, cfg)
try:
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run([sys.executable, "-I", "-m", "pytest", "--collect-only", "-q", "-W", "error", cfg["suite"]], cwd=work, capture_output=True, text=True, env=env)
        line = [l for l in r.stdout.splitlines() if "collected" in l or "selected" in l]
        counts.setdefault(line[-1] if line else "none:" + str(r.returncode), []).append(seed)
finally:
    shutil.rmtree(work, ignore_errors=True)
for k, v in counts.items(): print(k, "seeds", len(v), v[:5], "...")
