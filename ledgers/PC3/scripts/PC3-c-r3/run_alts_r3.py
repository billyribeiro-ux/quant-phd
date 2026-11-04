"""Run every alternative (builder alt1-5, round-1 alt6, round-2 alt7-8, round-3 alt9-10) through the grader suite on seeds 0-49."""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE3-PC3-c"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
files = sorted(glob.glob(f"{ROOT}/ledgers/PC3/alternatives/*.py")) + sorted(
    glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r1/alt6*.py")
) + sorted(glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r2/alt[78]*.py")) + sorted(
    glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r3/alt*.py")
)
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
for path in files:
    work = tempfile.mkdtemp(prefix="pc3alt-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    passed, failed = [], []
    for seed in range(0, 50):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([f"{ROOT}/.venv/bin/python", "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env, capture_output=True, text=True)
        (passed if r.returncode == 0 else failed).append(seed)
    print(f"{os.path.basename(path)}: passes {len(passed)}/50 seeds; failing seeds {failed[:10]}")
    shutil.rmtree(work, ignore_errors=True)
