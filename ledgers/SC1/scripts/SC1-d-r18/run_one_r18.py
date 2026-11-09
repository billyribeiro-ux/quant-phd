"""Run one candidate bm_checks.py against the SC1 grader for seeds 0-49 in its own scratch copy.
Usage (run without -I from the checkout root): run_one_r18.py <checkout root> <candidate .py> <scratch dir>. Prints one line."""
import os
import shutil
import subprocess
import sys

root, cand, scratch = sys.argv[1], sys.argv[2], sys.argv[3]
grader = os.path.join(root, "course/modules/SC/SC1/grader")
py = os.path.join(root, ".venv/bin/python")
name = cand.replace("/", "__")[:-3]
work = os.path.join(scratch, name)
shutil.rmtree(work, ignore_errors=True)
os.makedirs(work)
shutil.copy(cand, os.path.join(work, "bm_checks.py"))
shutil.copy(os.path.join(grader, "test_project.py"), work)
shutil.copy(os.path.join(grader, "instance.py"), work)
failed = []
for seed in range(50):
    env = dict(os.environ, QF_SEED=str(seed))
    r = subprocess.run(
        [py, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=work, env=env, capture_output=True, text=True,
    )
    if r.returncode != 0:
        last = (r.stdout.strip().splitlines() or [""])[-1]
        failed.append((seed, last[:160]))
print(f"{cand}: {50 - len(failed)}/50 seeds pass; first failures: {failed[:3]}")
