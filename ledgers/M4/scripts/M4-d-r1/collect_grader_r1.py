"""Verifier round 1 (M4-d): collect-only count of the M4 project grader, with the reference as tail_risk (copied to a
fresh empty directory, so no repo file shadows the imports)."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M4-d")
GRADER = ROOT / "course/modules/M/M4/grader"
work = Path(tempfile.mkdtemp(prefix="m4-collect-"))
for name in ("test_project.py", "instance.py", "reference.py"):
    shutil.copy(GRADER / name, work / name)
shutil.copy(GRADER / "reference.py", work / "tail_risk.py")
r = subprocess.run([sys.executable, "-I", "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
                   cwd=work, capture_output=True, text=True, check=False)
print(r.stdout[-600:])
print("stderr:", r.stderr[-300:])
print("exit", r.returncode)
shutil.rmtree(work, ignore_errors=True)
