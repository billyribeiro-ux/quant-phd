"""Round 6 (M7-d): does the suite refuse non-numeric multiplier values? Learner = reference with the multipliers returned
as text (or booleans). project.html:300 says: budget is a number; lower, upper, turnover_plus and turnover_minus are lists
of n numbers; sector is a list of Z numbers; turnover_total is a number. Runs the full suite under the page's flags."""

import os
import shutil
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD6-M7-d"
G = os.path.join(ROOT, "course/modules/M/M7/grader")
PY = os.path.join(ROOT, ".venv/bin/python")
VARIANTS = {
    "text": "lambda v: str(v)",
    "bool": "lambda v: bool(v)",
}
for name, conv in VARIANTS.items():
    D = f"/tmp/m7d-r6-types-{name}"
    shutil.rmtree(D, ignore_errors=True)
    os.makedirs(D)
    for f in ("test_project.py", "instance.py"):
        shutil.copy(os.path.join(G, f), D)
    src = open(os.path.join(G, "reference.py"), encoding="utf-8").read()
    src += f'''

_CONV = {conv}


def allocate(instance):  # learner variant: every multiplier returned through _CONV
    out = _allocate_numeric(instance)
    m = out["multipliers"]
    for key, value in m.items():
        m[key] = [_CONV(v) for v in value] if isinstance(value, list) else _CONV(value)
    return out
'''
    src = src.replace("def allocate(instance: dict[str, Any]) -> dict[str, Any]:", "def _allocate_numeric(instance: dict[str, Any]) -> dict[str, Any]:", 1)
    open(os.path.join(D, "constrained_allocator.py"), "w", encoding="utf-8").write(src)
    for seed in (0, 7):
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=D, capture_output=True, text=True,
                           env={**os.environ, "QF_SEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1"})
        print(f"multipliers as {name}, seed {seed}: {r.stdout.strip().splitlines()[-1]}")
        for line in r.stdout.splitlines():
            if line.startswith("FAILED"):
                print("   ", line[:160])
