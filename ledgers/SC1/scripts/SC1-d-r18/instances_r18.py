"""Sample 20 seeds (0-19) and 50 seeds: validity of each instance and whether the answers change (tail, one-step
estimate). Imports the grader's instance.py and reference.py from the checkout. Usage: python3 -I instances_r18.py <root>"""
import sys
sys.path.insert(0, sys.argv[1] + "/course/modules/SC/SC1/grader")
import math  # noqa: E402
from instance import make_instance  # noqa: E402
import reference as ref  # noqa: E402

rows = []
for seed in range(20):
    inst = make_instance(seed)
    ok = inst["H"] > 0 and inst["a"] > 0 and 4 <= inst["n_steps"] <= 256 and 400 <= inst["n_paths"] <= 800 \
        and inst["n_steps"] * inst["n_paths"] <= 200_000 and inst["label"] == "SIMULATED"
    tail = ref.reflection_tail(inst["a"], inst["H"])
    est, se = ref.discrete_max_exceedance(inst, 1)
    rows.append((seed, inst["H"], inst["a"], inst["n_steps"], inst["n_paths"], round(tail, 6), round(est, 6), ok))
    print(f"seed {seed:2d} H {inst['H']:.3f} a {inst['a']:.3f} n_steps {inst['n_steps']:3d} N {inst['n_paths']:3d} "
          f"tail {tail:.6f} one-step {est:.6f} valid {ok}")
levels_50 = {make_instance(s)["a"] for s in range(50)}
tails_50 = {round(ref.reflection_tail(make_instance(s)["a"], make_instance(s)["H"]), 9) for s in range(50)}
print("distinct levels over seeds 0-49:", len(levels_50), "; distinct tails:", len(tails_50))
print("all 20 sampled valid:", all(r[-1] for r in rows))
