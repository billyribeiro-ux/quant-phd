"""Round 12 verifier: every alternative correct implementation of slice c, run through the checkout's grader on the
seeds given on the command line, with the page's pytest flags. Copies into scratch directories; never edits the repo."""

import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE12-PC3-c"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
PY = f"{ROOT}/.venv/bin/python"
files = sorted(set(glob.glob(f"{ROOT}/ledgers/PC3/alternatives/alt*.py")
               + glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alts/*.py")
               + glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alt*.py")))
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
seeds = [int(s) for s in sys.argv[1].split(",")]
for path in files:
    work = tempfile.mkdtemp(prefix="pc3alt-r12-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    failed = []
    for seed in seeds:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0",
               "PYTHONDONTWRITEBYTECODE": "1"}
        r = subprocess.run([PY, "-B", "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env,
                           capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(seed)
    print(f"{os.path.relpath(path, ROOT)}: fails on {len(failed)} of {len(seeds)} seeds {failed[:8]}", flush=True)
    shutil.rmtree(work, ignore_errors=True)
print("ALTS DONE", flush=True)
