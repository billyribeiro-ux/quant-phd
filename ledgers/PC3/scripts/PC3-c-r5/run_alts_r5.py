"""Run every alternative solution (ledgers/PC3/alternatives and the round-1..4 alternatives plus this round's) through
the checkout's grader files, on seeds 0-49, with the page's pytest flags. Prints passes per file. Copies, never edits."""

import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE5-PC3-c"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
PY = f"{ROOT}/.venv/bin/python"
S = f"{ROOT}/ledgers/PC3/scripts"
files = (
    sorted(glob.glob(f"{ROOT}/ledgers/PC3/alternatives/*.py"))
    + sorted(glob.glob(f"{S}/PC3-c-r2/alt[78]*.py"))
    + sorted(glob.glob(f"{S}/PC3-c-r3/alt*.py"))
    + sorted(glob.glob(f"{S}/PC3-c-r4/alts/alt*.py"))
    + sorted(glob.glob(f"{S}/PC3-c-r5/alts/alt*.py"))
)
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
for path in files:
    work = tempfile.mkdtemp(prefix="pc3alt5-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    passed, failed, detail = [], [], ""
    for seed in range(0, 50):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([PY, "-I", "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env, capture_output=True, text=True)
        if r.returncode == 0:
            passed.append(seed)
        else:
            failed.append(seed)
            if not detail:
                detail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]
    print(f"{os.path.relpath(path, ROOT)}: passes {len(passed)}/50 seeds; failing seeds {failed[:10]} {detail}")
    shutil.rmtree(work, ignore_errors=True)
