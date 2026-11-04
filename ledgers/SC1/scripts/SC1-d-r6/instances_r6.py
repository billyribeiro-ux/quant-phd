"""Verifier round 6 (SC1 slice d): sample 20 seeds, check each instance is valid and the answers change.

Runs the grader's own instance.py (copied to a scratch dir) and recomputes the continuous tail for each sampled seed.
"""

import math
import random
import shutil
import sys
import tempfile
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-d/course/modules/SC/SC1/grader")
work = Path(tempfile.mkdtemp(prefix="sc1d-r6-inst-"))
try:
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    sys.path.insert(0, str(work))
    from instance import make_instance  # type: ignore[import-not-found]

    rng = random.Random(20260)
    seeds = sorted(rng.sample(range(50), 20)) + [0]
    rows = []
    for s in seeds:
        inst = make_instance(s)
        ok = (
            inst["label"] == "SIMULATED"
            and inst["H"] > 0
            and inst["a"] > 0
            and 4 <= inst["n_steps"] <= 256
            and 400 <= inst["n_paths"] <= 800
            and inst["n_steps"] * inst["n_paths"] <= 200_000
        )
        tail = math.erfc(inst["a"] / math.sqrt(2 * inst["H"]))
        rows.append((s, inst["H"], inst["a"], inst["n_steps"], inst["n_paths"], round(tail, 6), ok))
        print(f"seed {s:2d} H={inst['H']:.3f} a={inst['a']:.3f} n_steps={inst['n_steps']:3d} "
              f"n_paths={inst['n_paths']:3d} tail={tail:.6f} valid={ok}")
    print("all valid:", all(r[-1] for r in rows))
    print("distinct tails among sampled seeds:", len({r[5] for r in rows}), "of", len(rows))
    print("distinct levels among seeds 0-49:", len({make_instance(s)["a"] for s in range(50)}), "(test requires >= 45)")
finally:
    shutil.rmtree(work, ignore_errors=True)
