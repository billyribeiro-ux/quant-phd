"""Run each alternative correct implementation on seeds 0-19 under the browser's pytest flags (read-only on the checkout).

Usage: run_alts_r2.py <checkout> <scratch dir> <alt file> [...]  -> prints one line per file: failing seeds (none = all pass).
"""
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
py = root / ".venv/bin/python"
for alt in sys.argv[3:]:
    alt_path = Path(alt)
    for name in ("test_project.py", "instance.py"):
        shutil.copy(root / "course/modules/FC/FC1/grader" / name, scratch / name)
    shutil.copy(alt_path, scratch / "instruments.py")
    failing, detail = [], []
    for seed in range(20):
        proc = subprocess.run(
            [str(py), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=scratch, env={"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}, capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            failing.append(seed)
            detail.append(proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-200:])
    print(f"{alt_path.name}: failing seeds {failing if failing else 'none'} of 0-19" + (f" | first: {detail[0]}" if detail else " | 68 passed on every seed"))
