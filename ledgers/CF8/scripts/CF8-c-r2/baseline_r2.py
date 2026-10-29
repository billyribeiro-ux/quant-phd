import sys
sys.path.insert(0, "/tmp/cf8-v/c")
import witness_r2 as w
REF = w.REF
for sel in ["fresh_objects or fresh", "prints_or_warns or writes_to_stdout", "does_not_import_instance or imports_only"]:
    print("baseline", sel, w.run("base", REF, sel))
import subprocess, shutil, tempfile, os
from pathlib import Path
work = Path(tempfile.mkdtemp())
for n in ("test_project.py", "instance.py"):
    shutil.copy(w.GRADER / n, work / n)
(work / "treasury_forecast.py").write_text(REF, encoding="utf-8")
for sel in ["fresh", "prints_or_warns", "does_not_import_instance", "imports_only", "writes_to_stdout"]:
    r = subprocess.run([w.PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--collect-only", "-k", sel, "test_project.py"], cwd=work, capture_output=True, text=True, env={"QF_SEED": "0", "PATH": os.environ["PATH"]})
    print(sel, r.stdout.strip().splitlines()[-1])
