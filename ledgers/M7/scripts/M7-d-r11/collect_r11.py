"""Collect the M7 suite on seeds 0-49 in a fresh workspace per seed; print the collected count per seed."""
import os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
GRADER = ROOT / "course/modules/M/M7/grader"
PY = str(ROOT / ".venv/bin/python")
counts = {}
for seed in range(50):
    work = Path(tempfile.mkdtemp(prefix="m7c-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(GRADER / "reference.py", work / "constrained_allocator.py")
    r = subprocess.run([PY, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                       cwd=work, capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
    m = re.search(r"(\d+) tests? collected", r.stdout + r.stderr)
    counts[seed] = (int(m.group(1)) if m else None, r.returncode)
    shutil.rmtree(work, ignore_errors=True)
print("distinct counts:", sorted({v for v, _ in counts.values()}, key=str))
print("rc values:", sorted({rc for _, rc in counts.values()}))
print("per-seed:", counts)
