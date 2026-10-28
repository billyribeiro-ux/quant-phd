import os, shutil, subprocess, sys, pathlib
ROOT = pathlib.Path("/tmp/verifyB2-E1-d")
GR = ROOT / "course/modules/E/E1/grader"
ALT = ROOT / "ledgers/E1/scripts/E1-d-r2/alternatives"
PY = str(ROOT / ".venv/bin/python")
cands = sorted(ALT.glob("*.py")) + [ROOT / "ledgers/E1/scripts" / f"alt{i}_{n}.py" for i, n in []]
cands += sorted((ROOT / "ledgers/E1/scripts").glob("alt*.py"))
cands += sorted((ROOT / "ledgers/E1/scripts/E1-d-r1/alternatives").glob("*.py"))
for src in cands:
    work = pathlib.Path("/tmp/E1d-r2/work") / src.parent.name / src.stem
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    for f in ("test_project.py", "instance.py"):
        shutil.copy(GR / f, work / f)
    shutil.copy(src, work / "market_structure.py")
    fails = []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=work, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            fails.append((seed, [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:2]))
    print(src.parent.name + "/" + src.name, "seeds failing:", len(fails), fails[:2])
