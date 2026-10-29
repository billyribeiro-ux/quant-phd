"""Sample seeds 0-19 of grader/instance.py: validity under the spec, the J-bets claim in its docstring, and whether the answers differ across seeds."""

from __future__ import annotations

import importlib.util
import math
import sys
from fractions import Fraction as F
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyC3-M6-d/course/modules/M/M6/grader")
spec = importlib.util.spec_from_file_location("instance_mod", GRADER / "instance.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.path.insert(0, str(GRADER))
ref_spec = importlib.util.spec_from_file_location("ref_mod", GRADER / "reference.py")
ref = importlib.util.module_from_spec(ref_spec)
ref_spec.loader.exec_module(ref)

rows = []
for seed in range(20):
    i = mod.make_instance(seed)
    valid = (
        i["label"] == "SIMULATED"
        and 4 <= i["horizon"] <= 10
        and i["stop_level"] in (1, 2)
        and 1 <= i["stop_cap"] <= i["horizon"]
        and 1 <= i["base_stake_cents"] <= i["capital_cents"]
        and 1 <= i["barrier"] <= i["horizon"]
        and 3 <= i["dyadic_level"] <= 10
    )
    # docstring claim: exactly J bets when every bet loses, and K >= s, J in 1..8
    base, K = i["base_stake_cents"], i["capital_cents"]
    J = 0
    wealth = K
    while base * 2**J <= wealth:
        wealth -= base * 2**J
        J += 1
    out = ref.doubling_outcome(i)
    stopped = ref.stopped_value_expectation(i)
    doob = ref.doob_max_probability(i, i["barrier"])
    rows.append((seed, valid, J, out["bets_allowed"], out["expected_final_wealth_cents"], stopped, doob[0], i["capital_cents"], i["base_stake_cents"], i["horizon"], i["stop_cap"]))
    print(
        f"seed {seed:2d} valid={valid} N={i['horizon']} lvl={i['stop_level']} cap={i['stop_cap']} K={K} s={base} "
        f"dyadic={i['dyadic_level']} barrier={i['barrier']} J_loop={J} J_ref={out['bets_allowed']} "
        f"E_final={out['expected_final_wealth_cents']} E_stop={stopped} P_doob={doob[0]} "
        f"docstring_J_ok={J == out['bets_allowed']}"
    )
distinct = len({(r[4], str(r[5]), str(r[6]), r[7], r[8], r[9], r[10]) for r in rows})
print("valid for all 20:", all(r[1] for r in rows), "| J_loop == J_ref for all 20:", all(r[2] == r[3] for r in rows))
print("distinct answer tuples (E_final, E_stop, P_doob, K, s, N, cap) among 20 seeds:", distinct)
print("distinct instances:", len({tuple(sorted(mod.make_instance(s).items())) and str(mod.make_instance(s)) for s in range(20)}))
