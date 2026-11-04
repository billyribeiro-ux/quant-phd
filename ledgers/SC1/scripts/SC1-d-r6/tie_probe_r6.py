"""Verifier round 6 probe (not a grader edit): does a path whose grid maximum equals the level count as reaching it?

The first Gaussian draw of random.Random(seed).gauss(0, sqrt(H)) is v. With the level set to exactly v, the single path
of a one-step grid has maximum exactly v (0.0 + v == v in floats), so it must be counted as reaching the level.
Usage: tie_probe_r6.py <candidate bm_checks.py>   (run under python -I; copies the grader files to a scratch dir)
"""

import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-d/course/modules/SC/SC1/grader")
cand = Path(sys.argv[1]).resolve()
work = Path(tempfile.mkdtemp(prefix="sc1d-r6-tie-"))
try:
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    shutil.copy(cand, work / "bm_checks.py")
    probe = '''
import math, random, sys
sys.path.insert(0, '.')
import bm_checks as sol
from instance import make_instance
bad = []
for seed in range(20):
    inst = make_instance(seed)
    rng = random.Random(inst["seed"])
    v = rng.gauss(0.0, math.sqrt(inst["H"]))
    n = inst["n_paths"]
    rng = random.Random(inst["seed"])
    draws = [rng.gauss(0.0, math.sqrt(inst["H"])) for _ in range(n)]
    expected_hits = sum(1 for x in draws if x >= draws[0])
    est, _ = sol.discrete_max_exceedance({**inst, "a": draws[0]}, 1)
    fine, _ = sol.nested_grid_counts({**inst, "a": draws[0]}, 1, 1)
    if abs(est - expected_hits / n) > 1e-12 or fine != expected_hits:
        bad.append(seed)
print("tie probe failing seeds:", bad)
sys.exit(1 if bad else 0)
'''
    (work / "probe.py").write_text(probe, encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", "probe.py"], cwd=work, capture_output=True, text=True, timeout=300)
    print(cand.name, "exit", p.returncode, p.stdout.strip(), p.stderr.strip()[-300:])
finally:
    shutil.rmtree(work, ignore_errors=True)
