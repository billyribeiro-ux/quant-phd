"""Check the grader comment in test_draws_depend_on_the_instance_seed: at the instance's own level, seed 32 at grids
16, 32 and 64 gives estimates of 0. Also reports seed 32 + 7919 for the same grids, and whether any seed in 0-49
gives a zero estimate at its own level on grids 16, 32 and 64.
Usage: comment_claim_seed32_r14.py <checkout root>
"""
import sys

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

inst = make_instance(32)
other = make_instance(32 + 7919)
print("seed 32: a =", inst["a"], " H =", inst["H"], " N =", inst["n_paths"], " tail =", ref.reflection_tail(inst["a"], inst["H"]))
for g in (16, 32, 64):
    print("  grid", g, "estimate at own level:", ref.discrete_max_exceedance(inst, g)[0])
print("seed 32+7919 at its own level:", [ref.discrete_max_exceedance(other, g)[0] for g in (16, 32, 64)])
zero_seeds = []
for seed in range(50):
    i = make_instance(seed)
    if all(ref.discrete_max_exceedance(i, g)[0] == 0.0 for g in (16, 32, 64)):
        zero_seeds.append(seed)
print("seeds 0-49 with zero estimates on grids 16, 32, 64 at own level:", zero_seeds)
