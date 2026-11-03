"""Run each alternative as instruments.py with the grader suite on seeds 0..N-1 (default 20); scratch copies under /tmp."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
PY = str(ROOT / ".venv" / "bin" / "python")
GRADER = ROOT / "course" / "modules" / "FC" / "FC1" / "grader"
ALTS = sorted(ROOT.glob("ledgers/FC1/alternatives/a*.py")) + sorted(
    (ROOT / "ledgers/FC1/scripts/FC1-c-r3/alt_v4").glob("*.py")
)
work = Path("/tmp/fc1c_v4_alts")
shutil.rmtree(work, ignore_errors=True)
for alt in ALTS:
    d = work / alt.stem
    d.mkdir(parents=True)
    shutil.copy(alt, d / "instruments.py")
    shutil.copy(GRADER / "test_project.py", d / "test_project.py")
    shutil.copy(GRADER / "instance.py", d / "instance.py")
    failing = []
    last = []
    for seed in range(SEEDS):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=d, env=env, capture_output=True, text=True,
        )
        last.append(r.stdout.strip().splitlines()[-1])
        if r.returncode != 0:
            failing.append(seed)
    print(f"{alt.name}: failing seeds {failing if failing else 'none'} of 0-{SEEDS - 1} | seed0: {last[0]} | seed{SEEDS - 1}: {last[-1]}")
