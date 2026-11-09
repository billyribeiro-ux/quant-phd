"""Sample 20 seeds (every 2.5th seed of 0-49, plus the two seeds used by the suite) and check the instances are valid,
differ in level and horizon, and give different answers. Prints one line per seed.
Usage: sample_instances_r14.py <checkout root>
"""
import sys

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

seeds = list(range(0, 50, 3))[:17] + [1234, 987654]
rows = []
for s in seeds:
    i = make_instance(s)
    valid = i["H"] > 0 and i["a"] > 0 and 4 <= i["n_steps"] <= 256 and 400 <= i["n_paths"] <= 800 and i["n_steps"] * i["n_paths"] <= 200000
    e1, _ = ref.discrete_max_exceedance(i, 1)
    e4, _ = ref.discrete_max_exceedance(i, 4)
    tail = ref.reflection_tail(i["a"], i["H"])
    rows.append((s, valid, i["H"], i["a"], i["n_steps"], i["n_paths"], round(tail, 6), e1, e4))
    print(f"seed {s:>6}: valid={valid} H={i['H']} a={i['a']} n_steps={i['n_steps']} N={i['n_paths']} tail={tail:.6f} est1={e1:.6f} est4={e4:.6f}")
print("all valid:", all(r[1] for r in rows))
print("distinct levels:", len({r[3] for r in rows}), "of", len(rows), "; distinct tails:", len({r[6] for r in rows}))
print("distinct one-step estimates:", len({r[7] for r in rows}))
