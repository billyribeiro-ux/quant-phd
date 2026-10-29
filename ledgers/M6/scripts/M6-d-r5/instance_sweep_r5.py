"""Round-4 sweep of the M6 generator docstring claims and the reference engine over seeds 0-20000.

Usage: instance_sweep.py GRADER_DIR. Imports instance.py and reference.py from GRADER_DIR (read only).
Checks: horizon/stop/cap/barrier ranges; bets_allowed == J from the generator; K >= s; fair stopped value 0;
control stopped value nonzero; fair doubling expectation == capital; distinct answer tuples over seeds.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

grader = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(grader))
sys.dont_write_bytecode = True
import instance  # noqa: E402
import reference as ref  # noqa: E402

seen: set[tuple[object, ...]] = set()
violations: list[str] = []
control_zero = 0
fair_nonzero = 0
bad_bets = 0
for seed in range(0, 20001):
    inst = instance.make_instance(seed)
    if not (4 <= inst["horizon"] <= 10 and inst["stop_level"] in (1, 2)):
        violations.append(f"seed {seed}: horizon/level range")
    if not (1 <= inst["stop_cap"] <= inst["horizon"]):
        violations.append(f"seed {seed}: cap range")
    if not (1 <= inst["barrier"] <= inst["horizon"]):
        violations.append(f"seed {seed}: barrier range")
    s, K = inst["base_stake_cents"], inst["capital_cents"]
    if not (1 <= s <= 25 and K >= s):
        violations.append(f"seed {seed}: stake/capital")
    fair = ref.stopped_value_expectation(inst)
    if fair != 0:
        fair_nonzero += 1
    ctl = dict(inst, win_probability=Fraction(1, 3))
    if ref.stopped_value_expectation(ctl) == 0:
        control_zero += 1
    out = ref.doubling_outcome(inst)
    if out["expected_final_wealth_cents"] != K:
        violations.append(f"seed {seed}: fair doubling expectation != capital")
    # J from the generator: capital K = s*(2**J-1)+e with 0 <= e < s*2**J
    J = None
    for j in range(1, 9):
        if s * (2**j - 1) <= K < s * (2**j - 1) + s * 2**j:
            J = j
    if J is None or out["bets_allowed"] != J:
        bad_bets += 1
    seen.add(
        (
            inst["horizon"],
            inst["stop_level"],
            inst["stop_cap"],
            K,
            s,
            inst["dyadic_level"],
            inst["barrier"],
            out["expected_final_wealth_cents"],
        )
    )
print("seeds 0-20000")
print("violations", len(violations), violations[:5])
print("fair stopped value nonzero", fair_nonzero)
print("control stopped value zero", control_zero)
print("bets_allowed != generator J", bad_bets)
print("distinct instance+answer tuples", len(seen))
print("seed 0 instance", instance.make_instance(0))
