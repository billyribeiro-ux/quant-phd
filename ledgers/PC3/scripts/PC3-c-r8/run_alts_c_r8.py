"""Run the six alternative correct implementations in ledgers/PC3/alternatives through the current grader on seeds 0-49,
with the page's pytest flags. Copies files into scratch dirs and never edits the repo."""

import glob
import os
import shutil
import subprocess
import tempfile

ROOT = "/Users/billyribeiro/dev/quant-phd"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
PY = f"{ROOT}/.venv/bin/python"
files = sorted(glob.glob(f"{ROOT}/ledgers/PC3/alternatives/alt*.py"))
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
for path in files:
    work = tempfile.mkdtemp(prefix="pc3alt8-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    passed, failed, detail = [], [], ""
    for seed in range(0, 50):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([PY, "-I", "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env,
                           capture_output=True, text=True)
        if r.returncode == 0:
            passed.append(seed)
        else:
            failed.append(seed)
            if not detail:
                detail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]
    print(f"{os.path.relpath(path, ROOT)}: passes {len(passed)}/50 seeds; failing seeds {failed[:10]} {detail}")
    shutil.rmtree(work, ignore_errors=True)
