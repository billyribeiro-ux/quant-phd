"""Round-15: for seeds 0-49: instance label/determinism/feasibility (exact Fractions), and collected test count per seed."""
import json, subprocess, sys, tempfile, shutil, os
from fractions import Fraction as F
ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/course/modules/M/M7/grader")
import instance as inst
bad = []
for seed in range(50):
    a = inst.make_instance(seed); b = inst.make_instance(seed)
    assert a == b, seed
    assert "SIMULATED" in a["label"], seed
    c = json.loads(a["payload"]); n = len(c["mu"]); z = len(c["sector_caps"])
    w0 = [F(repr(x)) for x in c["w0"]]; lo = [F(repr(x)) for x in c["lower"]]; up = [F(repr(x)) for x in c["upper"]]
    caps = [F(repr(x)) for x in c["sector_caps"]]
    if not (sum(w0) == 1 and all(lo[i] <= w0[i] <= up[i] for i in range(n)) and z == 2 and n in (3, 4, 5)
            and all(sum(w0[i] for i in range(n) if c["sector"][i] == k) <= caps[k] for k in range(z)) and c["turnover_limit"] >= 0):
        bad.append(seed)
print("seeds 0-49: label SIMULATED and deterministic on 50 of 50; infeasible starts:", bad)
G = ROOT + "/course/modules/M/M7/grader"
counts = {}
for seed in range(50):
    work = tempfile.mkdtemp(prefix="m7r15col-")
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(os.path.join(G, name), work)
        shutil.copy(os.path.join(G, "reference.py"), os.path.join(work, "constrained_allocator.py"))
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
                           cwd=work, capture_output=True, text=True, env={"PATH": os.environ.get("PATH", ""), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        line = r.stdout.strip().splitlines()[-1]
        counts[seed] = line
    finally:
        shutil.rmtree(work, ignore_errors=True)
from collections import Counter
print("collected-count lines (seeds 0-49):", Counter(counts.values()))
