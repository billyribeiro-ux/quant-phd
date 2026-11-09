"""Run each correct alternative (bm_checks.py candidate) against the SC1 grader for seeds 0-49, in scratch copies.
Usage: run_alternatives_r15.py <checkout root> <alternatives dir> <scratch dir>. Same flags as the browser."""
import glob
import os
import shutil
import subprocess
import sys

root, alt_dir, scratch = sys.argv[1], sys.argv[2], sys.argv[3]
grader = os.path.join(root, "course/modules/SC/SC1/grader")
py = os.path.join(root, ".venv/bin/python")
for cand in sorted(glob.glob(os.path.join(alt_dir, "*.py"))):
    name = os.path.basename(cand)[:-3]
    work = os.path.join(scratch, name)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    shutil.copy(cand, os.path.join(work, "bm_checks.py"))
    shutil.copy(os.path.join(grader, "test_project.py"), work)
    shutil.copy(os.path.join(grader, "instance.py"), work)
    passed, failed = [], []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [py, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True,
        )
        last = (r.stdout.strip().splitlines() or [""])[-1]
        (passed if r.returncode == 0 else failed).append((seed, last))
    print(f"{name}: {len(passed)}/50 seeds pass")
    for seed, last in failed[:5]:
        print(f"   seed {seed}: {last}")
