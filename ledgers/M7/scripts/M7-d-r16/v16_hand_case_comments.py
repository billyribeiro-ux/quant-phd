"""Check the numbers in the new hand-case comments of test_project.py (round-16 verifier).

Prints the reference's weights, sector multipliers and certificate for the six new hand cases, and for the start-in-place
answer of the turnover case (the comment says about 5e-7), computed in exact arithmetic. Run from the repository root with -I.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v16_probe as P  # noqa: E402

GRADER = P.GRADER
spec = importlib.util.spec_from_file_location("test_project_v16", GRADER / "test_project.py")
assert spec is not None and spec.loader is not None
# test_project imports constrained_allocator and instance; load it with the grader folder on the path
sys.path.insert(0, str(GRADER))
sys.modules["constrained_allocator"] = P.REF
TP = importlib.util.module_from_spec(spec)
spec.loader.exec_module(TP)

for name, (case, expected) in TP.HAND_CASES.items():
    if "one billionth" not in name and "billionth" not in name:
        continue
    out = P.REF.allocate(json.loads(json.dumps(case)))
    rec = P.recomputed(case, out)
    print(f"[{name}] weights={out['weights']} expected={expected}")
    print(f"    sector multipliers={out['multipliers']['sector']} lower={out['multipliers']['lower']} upper={out['multipliers']['upper']} kappa={out['multipliers']['turnover_total']}")
    print(f"    recomputed primal={float(rec['primal'])} stat={float(rec['stationarity'])} dual={float(rec['dual'])} comp={float(rec['complementary'])}")

# start-in-place answer of 'turnover limit of one billionth': multipliers forced by stationarity with w = w0
case, _ = TP.HAND_CASES["turnover limit of one billionth"]
w0 = [0.5, 0.5]
g = [Fraction(1000) * 0 + Fraction(0.5) - Fraction(1000), Fraction(0.5)]
nu = Fraction(499.5)  # the budget multiplier that minimises kappa with two sign rows; kappa = 500
kappa = Fraction(500)
comp = kappa * Fraction(1, 10**9)
print("start-in-place (turnover case): kappa=500 (eta(+,-)=500, nu=499.5) -> complementary product", float(comp))
