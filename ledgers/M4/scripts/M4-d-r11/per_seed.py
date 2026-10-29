"""Run the M4 suite once per seed (QF_SEED) against one solution file in a fresh temp dir; print the seeds it fails."""
import os, shutil, subprocess, sys, tempfile, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M4-d")
G = ROOT / "course/modules/M/M4/grader"
PY = ROOT / ".venv/bin/python"
sol = pathlib.Path(sys.argv[1])
seeds = range(int(sys.argv[2]), int(sys.argv[3]) + 1)
failed, passed = [], []
for s in seeds:
    w = pathlib.Path(tempfile.mkdtemp(prefix="M4-d-r11-ps.", dir="/tmp"))
    shutil.copy(G / "test_project.py", w); shutil.copy(G / "instance.py", w); shutil.copy(sol, w / "tail_risk.py")
    env = dict(os.environ, QF_SEED=str(s))
    r = subprocess.run([str(PY), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                       cwd=w, env=env, capture_output=True, text=True)
    (failed if r.returncode else passed).append(s)
    shutil.rmtree(w, ignore_errors=True)
print(f"{sol.name}: fails on {len(failed)} of {len(list(seeds))} seeds; failing seeds: {failed[:20]}")
