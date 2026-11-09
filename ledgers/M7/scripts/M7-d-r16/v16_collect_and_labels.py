"""Round-16 verifier: collected test count per seed (0-49), HAND_CASES size, and the SIMULATED label on every hand case.

Run from the repository root with -I: .venv/bin/python -I ledgers/M7/scripts/M7-d-r16/v16_collect_and_labels.py
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
GRADER = ROOT / "course/modules/M/M7/grader"
SCRATCH = Path("/private/tmp/v16-m7d/ref")
PY = str(ROOT / ".venv/bin/python")
counts: dict[str, int] = {}
for seed in range(50):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed)}
    res = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                          "--collect-only", "test_project.py"], cwd=SCRATCH, capture_output=True, text=True, env=env, check=False)
    last = res.stdout.strip().splitlines()[-1]
    counts[last.split()[0]] = counts.get(last.split()[0], 0) + 1
print("collected counts over seeds 0-49:", counts)

sys.path.insert(0, str(SCRATCH))
sys.path.insert(0, str(GRADER))
os.environ["QF_SEED"] = "0"
spec = importlib.util.spec_from_file_location("tp_labels", GRADER / "test_project.py")
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print("HAND_CASES entries:", len(module.HAND_CASES))
missing = [name for name, (case, _) in module.HAND_CASES.items() if "SIMULATED" not in str(case.get("label", ""))]
print("hand cases without a SIMULATED label:", missing)
