"""Seeds 0-49: collected test count, SIMULATED label, instance validity, and the reference answer's active set.

Run: python -I ledgers/M7/scripts/M7-d-r14/seed_sweep_r14.py <repo_root>
Collect counts come from pytest --collect-only in a scratch copy with the reference as the solution.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1]).resolve()
grader = root / "course/modules/M/M7/grader"
sys.path.insert(0, str(grader))
from instance import make_instance  # noqa: E402
import reference as ref  # noqa: E402

counts = {}
work = Path(tempfile.mkdtemp(prefix="m7sweep-"))
shutil.copy(grader / "test_project.py", work / "test_project.py")
shutil.copy(grader / "instance.py", work / "instance.py")
shutil.copy(grader / "reference.py", work / "constrained_allocator.py")
for seed in range(50):
    r = subprocess.run(
        [sys.executable, "-I", "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=work, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}, check=False,
    )
    last = r.stdout.strip().splitlines()[-1]
    counts[seed] = int(last.split()[0])
shutil.rmtree(work, ignore_errors=True)
print("collected counts over seeds 0-49:", sorted(set(counts.values())), "distinct values")

labels_ok = 0
valid = 0
sizes = {}
answers = set()
bad = []
for seed in range(50):
    inst = make_instance(seed)
    if "SIMULATED" in inst["label"]:
        labels_ok += 1
    case = json.loads(inst["payload"])
    n = len(case["mu"])
    sizes[n] = sizes.get(n, 0) + 1
    sig = [[F(repr(v)) for v in row] for row in case["sigma"]]
    sym = all(sig[i][j] == sig[j][i] for i in range(n) for j in range(n))
    w0 = [F(repr(v)) for v in case["w0"]]
    lo = [F(repr(v)) for v in case["lower"]]
    up = [F(repr(v)) for v in case["upper"]]
    caps = [F(repr(v)) for v in case["sector_caps"]]
    ok = sym and ref._positive_definite(sig) and sum(w0) == 1 and all(lo[i] <= w0[i] <= up[i] for i in range(n))
    ok = ok and all(sum(w0[i] for i in range(n) if case["sector"][i] == k) <= caps[k] for k in range(len(caps)))
    ok = ok and case["turnover_limit"] >= 0 and len(caps) == 2 and set(case["sector"]) == {0, 1}
    if ok:
        valid += 1
    else:
        bad.append(seed)
    out = ref.allocate(case)
    answers.add(tuple(round(x, 12) for x in out["weights"]))
    active = []
    for i in range(n):
        if abs(out["weights"][i] - case["lower"][i]) < 1e-12:
            active.append(f"lower{i}")
        if abs(out["weights"][i] - case["upper"][i]) < 1e-12:
            active.append(f"upper{i}")
    if out["multipliers"]["turnover_total"] > 1e-12:
        active.append("turnover")
    if any(m > 1e-12 for m in out["multipliers"]["sector"]):
        active.append("sector")
    print(seed, "n=", n, "gamma=", case["gamma"], "active:", ",".join(active) or "none", "answer:", [round(x, 4) for x in out["weights"]])
print("SIMULATED label present on", labels_ok, "of 50 seeds")
print("instances valid (symmetric, PD, feasible start, caps, labels) on", valid, "of 50 seeds; invalid:", bad)
print("asset counts over seeds:", sizes)
print("distinct reference answers over seeds 0-49:", len(answers))
print("seeds whose collected count is 364:", sum(1 for v in counts.values() if v == 364), "of 50")
