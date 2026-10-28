"""Run alternative correct implementations through the AC4 suite on seeds 0-9 and 25 (fresh dir per file)."""
import os, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
SCR = pathlib.Path(sys.argv[2]).resolve()
G = ROOT / "course/modules/AC/AC4/grader"
PY = str(ROOT / ".venv/bin/python")
for src in sys.argv[3:]:
    src = pathlib.Path(src).resolve()
    d = SCR / src.stem
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for f in ("instance.py", "test_project.py", "starter.py"):
        shutil.copy(G / f, d / f)
    shutil.copy(src, d / "budget_engine.py")
    res = []
    for seed in list(range(10)) + [25]:
        p = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                            "test_project.py"], cwd=d, env=dict(os.environ, QF_SEED=str(seed)),
                           capture_output=True, text=True)
        res.append((seed, p.returncode, (p.stdout.strip().splitlines() or [''])[-1]))
    bad = [r for r in res if r[1] != 0]
    print(src.name, "PASS 11/11 seeds" if not bad else f"FAIL {bad[:2]}", res[0][2])
