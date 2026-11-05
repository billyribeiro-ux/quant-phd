"""Run each alternative in ledgers/FC2/scripts/FC2-d-r10/alts (and ledgers/FC2/mutants excluded) as scanner.py on seeds 0..49
against the pin's grader (test_project.py, instance.py), in an empty temp directory per run. Usage: run_alts_r10.py <repo_root>"""

import glob
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

root = os.path.abspath(sys.argv[1])
grader = os.path.join(root, "course", "modules", "FC", "FC2", "grader")
alts = sorted(glob.glob(os.path.join(root, "ledgers", "FC2", "scripts", "FC2-d-r10", "alts", "*.py")))
py = os.path.join(root, ".venv", "bin", "python")


def one(job: tuple[str, int]) -> tuple[str, int, int]:
    alt, seed = job
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(alt, os.path.join(tmp, "scanner.py"))
        shutil.copy(os.path.join(grader, "test_project.py"), tmp)
        shutil.copy(os.path.join(grader, "instance.py"), tmp)
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [py, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=tmp, env=env, capture_output=True, text=True,
        )
        return os.path.basename(alt), seed, r.returncode


jobs = [(a, s) for a in alts for s in range(50)]
with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(one, jobs))
for alt in alts:
    name = os.path.basename(alt)
    rcs = [rc for n, _, rc in results if n == name]
    print(f"{name}: {sum(1 for rc in rcs if rc == 0)}/{len(rcs)} seeds pass the suite")
