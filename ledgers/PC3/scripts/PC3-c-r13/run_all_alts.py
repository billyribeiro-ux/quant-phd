"""Round 13: every alternative correct implementation of slice c (prior rounds' files and this round's five), each run as
market_maker.py through the checkout's grader on seeds 0-49 with the page's pytest flags. Scratch copies only."""
import glob
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-PC3-c")
GRADER = ROOT / "course/modules/PC/PC3/grader"
PY = str(ROOT / ".venv/bin/python")
files = sorted({*glob.glob(f"{ROOT}/ledgers/PC3/alternatives/alt*.py"),
                *glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alts/*.py"),
                *glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alt*.py")})
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
summary = []
for path in files:
    rel = os.path.relpath(path, ROOT)
    work = Path("/tmp/pc3c-r13-all") / Path(path).stem
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(path, work / "market_maker.py")
    failed = []
    for seed in range(50):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1"}
        r = subprocess.run([PY, "-B", "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env,
                           capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(seed)
    line = f"{rel}: fails on {len(failed)} of 50 seeds" + (f" {failed[:10]}" if failed else "")
    print(line, flush=True)
    summary.append(line)
print("TOTAL files", len(files), "files with any failing seed", sum(1 for s in summary if "fails on 0 of" not in s), flush=True)
