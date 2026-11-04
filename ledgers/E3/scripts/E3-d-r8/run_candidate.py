# Runs the E3 grader suite (test_project.py, instance.py) against one candidate elicit.py for each seed.
import os, shutil, subprocess, sys, tempfile, pathlib, re
G = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/grader")
PY = "/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/.venv/bin/python"
cand = pathlib.Path(sys.argv[1]).resolve()
seeds = sys.argv[2]
lo, _, hi = seeds.partition("-")
results = []
for seed in range(int(lo), int(hi or lo) + 1):
    work = pathlib.Path(tempfile.mkdtemp(prefix="cand-e3-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(G / name, work / name)
    shutil.copy(cand, work / "elicit.py")
    env = dict(os.environ, QF_SEED=str(seed))
    r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                       cwd=work, env=env, capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-200:]
    failed = re.findall(r"FAILED test_project.py::(\S+)", r.stdout)
    results.append(f"seed {seed}: rc={r.returncode} {last} {failed[:3]}")
    shutil.rmtree(work, ignore_errors=True)
print("\n".join(results))
