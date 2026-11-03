"""Run each alternative as covariance_doctor.py against test_project.py for seeds 0-49 (verifier scratch)."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-M3-d")
PY = str(ROOT / ".venv/bin/python")
GRADER = ROOT / "course/modules/M/M3/grader"
ALTS = sorted((ROOT / "ledgers/M3/alternatives").glob("*.py"))
seeds = range(int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else range(50)
for alt in ALTS:
    fails = []
    for seed in seeds:
        work = Path(tempfile.mkdtemp(prefix="m3alt_"))
        try:
            shutil.copy(GRADER / "test_project.py", work / "test_project.py")
            shutil.copy(GRADER / "instance.py", work / "instance.py")
            shutil.copy(alt, work / "covariance_doctor.py")
            env = {**os.environ, "QF_SEED": str(seed)}
            r = subprocess.run(
                [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 str(work / "test_project.py")],
                capture_output=True, text=True, env=env, cwd=str(work), timeout=600,
            )
            last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-200:]
            if r.returncode != 0:
                fails.append((seed, last))
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"{alt.name}: seeds {seeds.start}-{seeds.stop - 1}: {len(seeds) - len(fails)}/{len(seeds)} pass")
    for seed, last in fails[:5]:
        print(f"   FAIL seed {seed}: {last}")
