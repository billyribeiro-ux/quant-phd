"""Verifier r5: which seeds have both estimates zero at the instance's own level (the old draws test's failure mode)."""
import importlib.util
import sys
from pathlib import Path

G = Path("/Users/billyribeiro/.fanout/wt/verifyE5-SC1-d/course/modules/SC/SC1/grader")
def load(name):
    spec = importlib.util.spec_from_file_location(name, G / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

inst_mod = load("instance")
ref = load("reference")
GRIDS = (4, 8, 16, 32, 64)
both_zero = []
for seed in range(0, 3000):
    inst = inst_mod.make_instance(seed)
    other = dict(inst, seed=seed + 7919)
    z1 = all(ref.discrete_max_exceedance(inst, g)[0] == 0.0 for g in GRIDS)
    z2 = all(ref.discrete_max_exceedance(other, g)[0] == 0.0 for g in GRIDS)
    if z1 and z2:
        both_zero.append((seed, inst["H"], inst["a"], inst["n_paths"], round(ref.reflection_tail(inst["a"], inst["H"]), 12)))
print("seeds 0-2999 with both draw sets all zero at own level:", len(both_zero))
for row in both_zero[:8]:
    print("  seed %d H=%s a=%s N=%d tail=%s" % row)
