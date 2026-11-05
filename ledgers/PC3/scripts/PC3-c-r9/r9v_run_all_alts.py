"""Round 9 verifier: every alternative correct implementation written in slice c (ledgers/PC3/alternatives and the
PC3-c-r* scripts), run through this checkout's grader on seeds 0-49, 50 and 848197495 with the page's pytest flags.
Copies into scratch directories only; never edits the repo."""

import glob
import os
import shutil
import subprocess
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE9-PC3-c"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
PY = f"{ROOT}/.venv/bin/python"
files = sorted(glob.glob(f"{ROOT}/ledgers/PC3/alternatives/alt*.py")
               + glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alts/*.py")
               + glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alt*.py"))
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
seeds = list(range(0, 50)) + [50, 848197495]
for path in files:
    work = tempfile.mkdtemp(prefix="pc3alt-all-r9v-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    failed = []
    for seed in seeds:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([PY, "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env,
                           capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(seed)
    print(f"{os.path.relpath(path, ROOT)}: fails on {len(failed)} of {len(seeds)} seeds {failed[:8]}", flush=True)
    shutil.rmtree(work, ignore_errors=True)
print("ALTS DONE", flush=True)
