"""Worst absolute error of alt_r10_b (composite Simpson, 2000 panels) against math.erfc over the instance probes of
seeds 0-49, against the page's 1e-12 rule. Usage: alt_r10_b_error_r15.py <checkout root> (run without -I)."""
import importlib.util
import math
import sys

root = sys.argv[1]
spec = importlib.util.spec_from_file_location("alt10b", f"{root}/ledgers/SC1/scripts/SC1-d-r10/alternatives/alt_r10_b_quadrature_tail.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
from instance import make_instance  # noqa: E402

worst, where = 0.0, None
for seed in range(50):
    inst = make_instance(seed)
    for a, t in ((inst["a"], inst["H"]), (inst["a"] * 0.5, inst["H"]), (1e-9, inst["H"]), (inst["a"], 1e-9)):
        err = abs(mod.reflection_tail(a, t) - math.erfc(a / math.sqrt(2 * t)))
        if err > worst:
            worst, where = err, (seed, a, t)
print("alt_r10_b worst |tail - erfc| over seeds 0-49 probes:", worst, "at (seed, a, t) =", where, "; page rule 1e-12")
