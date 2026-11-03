"""Run each alternative as instruments.py with the FC1 project suite on seeds 0..N-1 (scratch copies under /tmp)."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c")
SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 50
PY = str(ROOT / ".venv" / "bin" / "python")
GRADER = ROOT / "course" / "modules" / "FC" / "FC1" / "grader"
HERE = ROOT / "ledgers/FC1/scripts/FC1-c-r4"
ALTS = sorted(ROOT.glob("ledgers/FC1/alternatives/a*.py")) + sorted((HERE / "alt").glob("*.py"))
ALTS += sorted((ROOT / "ledgers/FC1/scripts/FC1-c-r3/alt").glob("alt*.py"))
ALTS += sorted((ROOT / "ledgers/FC1/scripts/FC1-c-r3/alt_v4").glob("*.py"))
work = Path("/tmp/fc1c_r4_alts")
shutil.rmtree(work, ignore_errors=True)
for alt in ALTS:
    d = work / f"{alt.parent.name}_{alt.stem}"
    d.mkdir(parents=True)
    shutil.copy(alt, d / "instruments.py")
    shutil.copy(GRADER / "test_project.py", d / "test_project.py")
    shutil.copy(GRADER / "instance.py", d / "instance.py")
    failing = []
    for seed in range(SEEDS):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=d, env=env, capture_output=True, text=True,
        )
        if r.returncode != 0:
            failing.append(seed)
    print(f"{alt.parent.name}/{alt.name}: failing seeds {failing if failing else 'none'} of 0-{SEEDS - 1}")
