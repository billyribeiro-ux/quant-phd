import os, re, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, "/tmp/verify-ac2r4-p/tools")
from coursekit import unit  # noqa
from run_graders import panel, parse_seeds, workspace  # noqa
u = unit("AC2"); cfg = panel(u)
work = workspace(u, Path("/tmp/verify-ac2r4-p/course/modules/AC/AC2/grader/reference.py"), cfg)
counts = {}
try:
    for seed in parse_seeds(sys.argv[1]):
        r = subprocess.run([sys.executable, "-I", "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", cfg["suite"]],
                           cwd=work, capture_output=True, text=True,
                           env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        m = re.search(r"(\d+) tests? collected", r.stdout + r.stderr)
        counts[seed] = int(m.group(1)) if m else ("no count", r.stdout[-200:])
finally:
    shutil.rmtree(work, ignore_errors=True)
print("collect-only counts:", counts)
print("distinct:", sorted({str(v) for v in counts.values()}))
