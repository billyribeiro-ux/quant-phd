import os, shutil, subprocess, sys, tempfile, pathlib
R = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M3-d")
G = R / "course/modules/M/M3/grader"
ALT = R / "ledgers/M3/alternatives"
py = str(R / ".venv/bin/python")
flags = ["--assert=plain", "-W", "error", "-q", "-p", "no:cacheprovider"]
for alt in sorted(ALT.glob("*.py")):
    fails = []
    for seed in range(50):
        w = pathlib.Path(tempfile.mkdtemp(prefix="alt-"))
        for n in ["test_project.py", "instance.py"]:
            shutil.copy(G / n, w / n)
        shutil.copy(alt, w / "covariance_doctor.py")
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run([py, "-m", "pytest", *flags, "test_project.py"], cwd=w, capture_output=True, text=True, env=env, timeout=300)
        if r.returncode != 0:
            fails.append(seed)
        shutil.rmtree(w)
    print(alt.name, "seeds failing:", fails if fails else "none", "of 50")
