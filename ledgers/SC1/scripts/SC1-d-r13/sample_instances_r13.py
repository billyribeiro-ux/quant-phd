"""Samples 20 seeds (7, 13, 21, ..., spread over 0..999) through the instance generator: every instance valid, and the
answers change across seeds (the continuous tail and the grid-4 estimate of the reference engine)."""

import math
import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE13-SC1-d/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

seeds = [7 + 50 * k for k in range(20)]
rows = []
for s in seeds:
    i = make_instance(s)
    valid = (
        i["label"] == "SIMULATED"
        and i["H"] > 0
        and i["a"] > 0
        and 4 <= i["n_steps"] <= 256
        and 400 <= i["n_paths"] <= 800
        and i["n_steps"] * i["n_paths"] <= 200_000
    )
    tail = math.erfc(i["a"] / math.sqrt(2.0 * i["H"]))
    est4, _ = ref.discrete_max_exceedance(i, 4)
    rows.append((s, valid, i["H"], i["a"], i["n_steps"], i["n_paths"], round(tail, 6), est4))
    print(f"seed {s:4d} valid={valid} H={i['H']} a={i['a']} n={i['n_steps']} N={i['n_paths']} tail={tail:.6f} est4={est4:.6f}")
print("all 20 valid:", all(r[1] for r in rows))
print("distinct tails:", len({r[6] for r in rows}), "distinct levels:", len({r[3] for r in rows}), "distinct horizons:", len({r[2] for r in rows}))
print("distinct grid-4 estimates:", len({r[7] for r in rows}))
