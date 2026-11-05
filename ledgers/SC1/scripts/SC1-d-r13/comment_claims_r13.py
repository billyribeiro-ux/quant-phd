"""Checks the grader comment in test_draws_depend_on_the_instance_seed: 'At the instance's own level the tail is so small
for some seeds that no path reaches it, and both estimates are 0.' Uses the reference engine on seeds 0..49."""

from __future__ import annotations

import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE13-SC1-d/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

zero_seeds = []
pairs_both_zero = []
for seed in range(50):
    inst = make_instance(seed)
    est, _ = ref.discrete_max_exceedance(inst, 4)
    if est == 0.0:
        zero_seeds.append(seed)
    other = make_instance(seed + 7_919)
    est2, _ = ref.discrete_max_exceedance(other, 4)
    if est == 0.0 and est2 == 0.0:
        pairs_both_zero.append(seed)
print("seeds 0..49 whose own-level grid-4 estimate is 0:", zero_seeds)
print("seeds whose own-level estimate AND seed+7919 own-level estimate are both 0 (n=4):", pairs_both_zero)
