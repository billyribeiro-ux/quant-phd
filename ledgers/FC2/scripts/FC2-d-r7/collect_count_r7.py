"""Collect-only count of grader/test_project.py on the reference solution, for seeds 0..49.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/collect_count.py <repo_root>
Copies reference.py (as scanner.py), instance.py and test_project.py into an empty temp directory and runs
pytest --collect-only there with QF_SEED set to each seed. Prints one line per seed and the set of counts.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

root = sys.argv[1]
grader = os.path.join(root, "course", "modules", "FC", "FC2", "grader")
counts = {}
for seed in range(50):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(os.path.join(grader, "reference.py"), os.path.join(tmp, "scanner.py"))
        shutil.copy(os.path.join(grader, "instance.py"), tmp)
        shutil.copy(os.path.join(grader, "test_project.py"), tmp)
        env = dict(os.environ, QF_SEED=str(seed))
        out = subprocess.run(
            [os.path.join(root, ".venv", "bin", "python"), "-m", "pytest", "--collect-only", "-q",
             "-p", "no:cacheprovider", "test_project.py"],
            cwd=tmp, env=env, capture_output=True, text=True,
        )
        m = re.search(r"(\d+) tests? collected", out.stdout + out.stderr)
        n = int(m.group(1)) if m else -1
        counts.setdefault(n, []).append(seed)
        if out.returncode != 0:
            print("seed", seed, "rc", out.returncode, out.stdout[-400:], out.stderr[-400:])
for n, seeds in sorted(counts.items()):
    print("collected", n, "for", len(seeds), "seeds; first seeds", seeds[:5])
