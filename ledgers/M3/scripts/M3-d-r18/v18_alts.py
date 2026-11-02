import os, shutil, subprocess, sys, tempfile, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB18-M3-d")
PY = str(ROOT / ".venv/bin/python")
G = ROOT / "course/modules/M/M3/grader"
alts = sorted((ROOT / "ledgers/M3/alternatives").glob("*.py"))
for alt in alts:
    passes = fails = 0
    for seed in range(50):
        d = tempfile.mkdtemp(prefix="v18alt_")
        shutil.copy(G / "test_project.py", d)
        shutil.copy(G / "instance.py", d)
        shutil.copy(alt, os.path.join(d, "covariance_doctor.py"))
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=d, env=env, capture_output=True, text=True, timeout=300)
        if r.returncode == 0: passes += 1
        else:
            fails += 1
            if fails <= 2: print(alt.name, "seed", seed, r.stdout[-400:])
        shutil.rmtree(d)
    print(f"{alt.name}: pass={passes} fail={fails}", flush=True)
