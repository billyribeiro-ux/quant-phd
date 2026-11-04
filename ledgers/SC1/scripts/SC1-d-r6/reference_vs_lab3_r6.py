"""Verifier round 6 (SC1 slice d): the reference engine reproduces the Lab 3 printed numbers for seed 0.

Imports the grader's reference.py and instance.py from a scratch copy (run with python -I; no edits to the repo).
Compares each printed value of project.html Lab 3 (expected block at project.html:418-428) and the walk counts.
"""

import math
import shutil
import sys
import tempfile
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-d/course/modules/SC/SC1/grader")
work = Path(tempfile.mkdtemp(prefix="sc1d-r6-ref-"))
try:
    shutil.copy(GRADER / "reference.py", work / "reference.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    sys.path.insert(0, str(work))
    import instance  # type: ignore[import-not-found]
    import reference as ref  # type: ignore[import-not-found]

    inst = instance.make_instance(0)
    d = {"seed": inst["seed"], "H": inst["H"], "a": inst["a"], "n_steps": inst["n_steps"], "n_paths": inst["n_paths"]}
    print("instance", inst["H"], inst["a"], inst["n_paths"])
    print(f"tail {ref.reflection_tail(inst['a'], inst['H']):.6f} (page 0.086497)")
    page = {1: (0.059548, 0.010735, 0.026948), 4: (0.049281, 0.009819, 0.037215),
            16: (0.065708, 0.011239, 0.020788), 64: (0.088296, 0.012870, -0.001799),
            256: (0.082136, 0.012455, 0.004361)}
    tail = ref.reflection_tail(inst["a"], inst["H"])
    ok = True
    for n, (pe, ps, pd) in page.items():
        est, se = ref.discrete_max_exceedance(d, n)
        good = round(est, 6) == pe and round(se, 6) == ps and round(tail - est, 6) == pd
        ok &= good
        print(f"n={n:3d} est={est:.6f} se={se:.6f} tail-est={tail - est:.6f} matches page: {good}")
    fine, c64 = ref.nested_grid_counts(d, 256, 64)
    _, c16 = ref.nested_grid_counts(d, 256, 16)
    _, c4 = ref.nested_grid_counts(d, 256, 4)
    _, c1 = ref.nested_grid_counts(d, 256, 1)
    print("nested fine", fine, "coarse 64/16/4/1:", c64, c16, c4, c1, "page 40; 35 29 27 22")
    print("walk n=12 a=3:", ref.srw_max_count(12, 3), ref.srw_terminal_count(12, 3), "page 1588 794")
    print("all grid rows match page:", ok, "nested match:", (fine, c64, c16, c4, c1) == (40, 35, 29, 27, 22))
finally:
    shutil.rmtree(work, ignore_errors=True)
