"""Build a scratch workspace from the FC1 grader and count pytest collect-only tests."""
import shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD16-FC1-c")
grader = ROOT / "course/modules/FC/FC1/grader"
work = Path(tempfile.mkdtemp(prefix="fc1c16-collect-"))
for name in ["test_project.py", "instance.py"]:
    shutil.copy(grader / name, work / name)
shutil.copy(grader / "reference.py", work / "instruments.py")
r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
                   cwd=work, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "QF_SEED": "0", "PYTHONHASHSEED": "0"})
print(r.stdout[-400:], r.stderr[-400:])
shutil.rmtree(work, ignore_errors=True)
