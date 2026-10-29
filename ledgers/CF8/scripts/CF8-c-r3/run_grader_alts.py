"""Run the CF8 grader (test_project.py, instance.py) against each module in argv on seeds 0-49 under the browser flags."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRADER = Path(sys.argv[1])
PY = sys.argv[2]
for mod in sys.argv[3:]:
    src = Path(mod)
    fails = []
    for seed in range(50):
        work = Path(tempfile.mkdtemp(prefix="cf8c-alt-"))
        for n in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / n, work / n)
        shutil.copy(src, work / "treasury_forecast.py")
        env = {"QF_SEED": str(seed), "PATH": os.environ["PATH"]}
        r = subprocess.run(
            [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, capture_output=True, text=True, env=env,
        )
        if r.returncode != 0:
            fails.append((seed, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]))
        shutil.rmtree(work)
    print(f"{src.name}: {'PASS' if not fails else 'FAIL'} over 50 seeds" + ("" if not fails else f"; first {fails[0]}"))
