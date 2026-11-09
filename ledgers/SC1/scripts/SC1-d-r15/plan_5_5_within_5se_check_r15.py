"""Plan 5.5 states: discrete_max_exceedance's estimate lies within 5 se of reflection_tail(a, H). Check the reference
against that statement for grids 1, 4 and the instance's own n_steps over seeds 0-49, and against the one-step target
tail/2 that the page's test uses. Usage: plan_5_5_within_5se_check_r15.py <checkout root> (run without -I)."""
import sys
root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

fails_plan = {}
for seed in range(50):
    inst = make_instance(seed)
    tail = ref.reflection_tail(inst["a"], inst["H"])
    for g in (1, 4, inst["n_steps"]):
        est, se = ref.discrete_max_exceedance(inst, g)
        if abs(est - tail) > 5 * se:
            fails_plan.setdefault(seed, []).append((g, round(est, 6), round(tail, 6), round(se, 6)))
print("seeds where the plan's within-5se-of-tail statement fails the reference (seed: [(grid, est, tail, se)]):")
for s, v in fails_plan.items():
    print(" ", s, v)
print("count of seeds failing:", len(fails_plan), "of 50")
