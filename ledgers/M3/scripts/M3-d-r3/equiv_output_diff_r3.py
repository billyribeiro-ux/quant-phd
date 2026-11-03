"""Compare projection_repair outputs of the reference and the three 'equivalent' files on seeds 0-49 (verifier round 3).

Reports the largest entry difference from the reference output per file; a difference above 0 means the files are not
exactly equivalent (they differ below the stopping tolerance). Run from the checkout root with -I.
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, "course/modules/M/M3/grader")
from instance import make_instance  # noqa: E402


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load("course/modules/M/M3/grader/reference.py", "ref")
cands = {p: load(p, Path(p).stem) for p in sys.argv[1:]}
worst = {p: 0.0 for p in cands}
exact = {p: 0 for p in cands}
for seed in range(50):
    inst = make_instance(seed)
    r = ref.projection_repair(inst["corr"])
    for p, m in cands.items():
        y = m.projection_repair(inst["corr"])
        d = max(abs(y[i][j] - r[i][j]) for i in range(len(r)) for j in range(len(r)))
        worst[p] = max(worst[p], d)
        exact[p] += d == 0.0
for p in cands:
    print(f"{p}: exact-equal seeds {exact[p]}/50, largest entry difference from reference {worst[p]:.3e}")
