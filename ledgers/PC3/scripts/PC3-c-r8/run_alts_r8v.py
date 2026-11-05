"""Round 8 verifier: run the alternative correct implementations through this checkout's grader on seeds 0-49, 50 and
seeds 848197495 and 1712259056, with the page's pytest flags. Copies files into scratch dirs; never edits the repo."""

import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-c"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
PY = f"{ROOT}/.venv/bin/python"
files = sorted(glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r8/alts/alt_r8_*.py"))
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
seeds = list(range(0, 50)) + [50, 848197495, 1712259056]
for path in files:
    work = tempfile.mkdtemp(prefix="pc3alt-r8v-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    passed, failed, detail = [], [], ""
    for seed in seeds:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([PY, "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env,
                           capture_output=True, text=True)
        if r.returncode == 0:
            passed.append(seed)
        else:
            failed.append(seed)
            if not detail:
                detail = (r.stdout.strip().splitlines() or [r.stderr[-300:]])[-1]
    print(f"{os.path.basename(path)}: passes {len(passed)}/{len(seeds)} seeds; failing seeds {failed[:10]} {detail}")
    shutil.rmtree(work, ignore_errors=True)
sys.stdout.flush()
