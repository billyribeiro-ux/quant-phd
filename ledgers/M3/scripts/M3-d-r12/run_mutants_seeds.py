import pathlib, shutil, subprocess, sys, tempfile, os
R = pathlib.Path(sys.argv[1]); G = R / "course/modules/M/M3/grader"
for mpath in sys.argv[2:]:
    mp = pathlib.Path(mpath); fails = []; first = None
    for seed in range(50):
        w = pathlib.Path(tempfile.mkdtemp(prefix="mm-"))
        for n in ["test_project.py", "instance.py"]:
            shutil.copy(G / n, w / n)
        shutil.copy(mp, w / "covariance_doctor.py")
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run([sys.executable, "-m", "pytest", "--assert=plain", "-W", "error", "-q", "-p", "no:cacheprovider", "test_project.py"], cwd=w, capture_output=True, text=True, env=env)
        if r.returncode != 0:
            fails.append(seed)
            if first is None:
                first = [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:1]
        shutil.rmtree(w)
    print(mp.name, "KILLED on", len(fails), "of 50 seeds" if fails else "SURVIVED", first or "")
