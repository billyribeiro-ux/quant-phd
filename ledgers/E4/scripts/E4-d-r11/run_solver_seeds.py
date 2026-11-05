"""Run the E4 project suite (test_project.py) on one solver file over seeds 0 to 49.

Usage: python3 -I run_solver_seeds.py <repo-root> <solver.py path> [first last]
Copies instance.py, test_project.py and the solver (as solver.py) into a fresh scratch dir, runs pytest per seed
with the repo venv's interpreter, and prints PASS/FAIL per seed and a total.
"""

import os
import shutil
import subprocess
import sys
import tempfile

root, solver = sys.argv[1], sys.argv[2]
first = int(sys.argv[3]) if len(sys.argv) > 3 else 0
last = int(sys.argv[4]) if len(sys.argv) > 4 else 49
py = os.path.join(root, ".venv", "bin", "python")
grader = os.path.join(root, "course", "modules", "E", "E4", "grader")
scratch = tempfile.mkdtemp(prefix="e4r9-solver-")
shutil.copy(os.path.join(grader, "instance.py"), scratch)
shutil.copy(os.path.join(grader, "test_project.py"), scratch)
shutil.copy(solver, os.path.join(scratch, "solver.py"))
ok = 0
fails = []
for seed in range(first, last + 1):
    env = dict(os.environ, QF_SEED=str(seed), PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run(
        [py, "-I", "-W", "error", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
         "test_project.py"],
        cwd=scratch, env=env, capture_output=True, text=True,
    )
    if r.returncode == 0:
        ok += 1
    else:
        last_line = (r.stdout.strip().splitlines() or ["?"])[-1]
        fails.append((seed, last_line))
print(f"{os.path.basename(solver)}: {ok}/{last - first + 1} seeds pass")
for seed, line in fails[:12]:
    print(f"  seed {seed}: {line}")
shutil.rmtree(scratch, ignore_errors=True)
