"""Run the CF1 suite on each engine file for seeds 0-49. Usage (-I): run_variants_r5.py <checkout> <engine.py>..."""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1])
GRADER = ROOT / "course/modules/CF/CF1/grader"
PY = str(ROOT / ".venv/bin/python")
for engine in sys.argv[2:]:
    work = pathlib.Path(tempfile.mkdtemp(prefix="cf1r5-"))
    for f in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / f, work / f)
    shutil.copy(engine, work / "capbudget.py")
    fails = []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                            "test_project.py"], cwd=work, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            last = [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:1]
            fails.append((seed, last[0][:160] if last else r.stdout[-300:]))
    print(f"{pathlib.Path(engine).name}: seeds failing {len(fails)} of 50", fails[:2])
    shutil.rmtree(work, ignore_errors=True)
