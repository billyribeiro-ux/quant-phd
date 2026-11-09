"""Instance validity and materiality over seeds 0-49 (all seeds) and a 20-seed sample, using the reference engine.
Usage: instances_r16.py <checkout root>. Run without -I so the grader directory is importable."""
import sys

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

insts = [make_instance(s) for s in range(50)]
bad = []
for s, i in enumerate(insts):
    ok = (i["label"] == "SIMULATED" and i["H"] > 0 and i["a"] > 0 and 4 <= i["n_steps"] <= 256
          and 400 <= i["n_paths"] <= 800 and i["n_steps"] * i["n_paths"] <= 200000 and i["seed"] == s)
    if not ok:
        bad.append(s)
print("invalid instances among seeds 0-49:", bad)
print("distinct levels:", len({i["a"] for i in insts}), "of 50; distinct horizons:", len({i["H"] for i in insts}))
print("distinct grid sizes:", len({i["n_steps"] for i in insts}), "; distinct path counts:", len({i["n_paths"] for i in insts}))
est = []
for s, i in enumerate(insts):
    p, _ = ref.discrete_max_exceedance(i, 1)
    est.append(round(p, 6))
print("distinct one-step estimates over 50 seeds:", len(set(est)))
sample = [0, 3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 44, 46, 47, 48, 49, 5, 9]
print("20-seed sample (seed, H, a, n_steps, n_paths, one-step estimate, tail):")
for s in sample:
    i = insts[s]
    p, se = ref.discrete_max_exceedance(i, 1)
    print(" ", s, i["H"], i["a"], i["n_steps"], i["n_paths"], round(p, 6), round(ref.reflection_tail(i["a"], i["H"]), 6))
