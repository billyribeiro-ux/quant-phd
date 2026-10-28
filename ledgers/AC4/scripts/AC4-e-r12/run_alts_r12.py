import os, shutil, subprocess, sys, pathlib
ROOT = pathlib.Path(sys.argv[1]); ALTS = pathlib.Path(sys.argv[2]); SCR = pathlib.Path(sys.argv[3])
G = ROOT / "course/modules/AC/AC4/grader"; PY = str(ROOT / ".venv/bin/python")
seeds = range(50)
for alt in sorted(ALTS.glob("*.py")):
    res = {}
    for seed in seeds:
        d = SCR / alt.stem / str(seed)
        if d.exists(): shutil.rmtree(d)
        d.mkdir(parents=True)
        for f in ("instance.py", "test_project.py", "starter.py"): shutil.copy(G / f, d / f)
        shutil.copy(alt, d / "budget_engine.py")
        p = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=d, env=dict(os.environ, QF_SEED=str(seed), PYTHONHASHSEED="0"), capture_output=True, text=True, timeout=300)
        if p.returncode != 0:
            res[seed] = [l for l in p.stdout.splitlines() if l.startswith("FAILED")][:2]
    print(alt.name, "PASS 50/50" if not res else f"FAILED on {len(res)} seeds", flush=True)
    for s, f in list(res.items())[:3]:
        print("   seed", s, f, flush=True)
