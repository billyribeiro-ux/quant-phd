"""Check the grader comment at test_project.py:471-474: at the instance's own level, seed 32's grids 16, 32 and 64
give estimate 0.0. Usage: seed32_comment_r16.py <checkout root>."""
import sys

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

inst = make_instance(32)
print("seed 32: H =", inst["H"], "a =", inst["a"], "n_steps =", inst["n_steps"], "n_paths =", inst["n_paths"])
for g in (4, 8, 16, 32, 64, 128):
    est, se = ref.discrete_max_exceedance(inst, g)
    print(f"  grid {g}: estimate {est} se {se}")
print("tail", ref.reflection_tail(inst["a"], inst["H"]))
