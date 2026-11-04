"""Round-8: run each mutant as elicit.py against the E3 grader suite, seeds 0-49, in a scratch copy.

Usage: .venv/bin/python -I ledgers/E3/scripts/E3-e-r8/kill_r8.py <mutant.py> [<mutant.py> ...]
Prints, per mutant, the seeds on which the suite fails and the first failing test name for the first such seed.
The repository copy of the grader is only read; the scratch copy is under /tmp/e3e_r8/kill/.
"""

import os
import pathlib
import shutil
import subprocess
import sys

CHECKOUT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-e")
GRADER = CHECKOUT / "course/modules/E/E3/grader"
PY = CHECKOUT / ".venv/bin/python"
SCRATCH = pathlib.Path("/tmp/e3e_r8/kill")

for mutant_arg in sys.argv[1:]:
    mutant = pathlib.Path(mutant_arg).resolve()
    work = SCRATCH / mutant.stem
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    shutil.copy(mutant, work / "elicit.py")
    failing: list[tuple[int, str]] = []
    passing = 0
    for seed in range(int(os.environ.get('SEED_COUNT', '50'))):
        env = dict(os.environ, QF_SEED=str(seed))
        result = subprocess.run(
            [str(PY), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True, timeout=600,
        )
        if result.returncode == 0:
            passing += 1
            continue
        first = next((line for line in result.stdout.splitlines() if line.startswith("FAILED")), "(no FAILED line)")
        failing.append((seed, first[:200]))
    print(f"mutant {mutant.name}: killed on {len(failing)} of {int(os.environ.get('SEED_COUNT', '50'))} seeds, survived on {passing} seeds")
    for seed, first in failing[:3]:
        print(f"  seed {seed}: {first}")
