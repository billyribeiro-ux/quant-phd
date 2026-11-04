"""Collect-only count of the suite on reference.py for seeds 0-49, and instance distinctness for seeds 0-19 (CS2 slice d, r7)."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
grader = ROOT / "course/modules/CS/CS2/grader"
counts = {}
for seed in range(50):
    work = Path(tempfile.mkdtemp(prefix="cs2r7-collect-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(grader / name, work / name)
    shutil.copy(grader / "reference.py", work / "streamstats.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--collect-only", "test_project.py"],
                       cwd=work, capture_output=True, text=True, env=env)
    last = [ln for ln in r.stdout.splitlines() if "test" in ln and ("collected" in ln or "selected" in ln or ln.strip().endswith("tests"))]
    line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]
    counts.setdefault(line, []).append(seed)
    shutil.rmtree(work, ignore_errors=True)
for k, v in counts.items():
    print(f"{k!r}: seeds {v[0]}..{v[-1]} ({len(v)} seeds)")
sys.path.insert(0, str(grader))
import importlib.util
spec = importlib.util.spec_from_file_location("inst", grader / "instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)
import json
from fractions import Fraction
sigs = set()
answers = set()
for seed in range(20):
    p = json.loads(inst.make_instance(seed)["payload"])
    vals = [float(x) for x in p["values"]]
    n = len(vals)
    mean = sum(Fraction(x) for x in vals) / n
    var = sum((Fraction(x) - mean) ** 2 for x in vals) / (n - 1)
    sigs.add((n, p["window"], p["epsilon"], float(var)))
    answers.add(float(mean))
print("distinct (n, window, epsilon, exact sample variance) over seeds 0-19:", len(sigs))
print("distinct exact means over seeds 0-19:", len(answers))
