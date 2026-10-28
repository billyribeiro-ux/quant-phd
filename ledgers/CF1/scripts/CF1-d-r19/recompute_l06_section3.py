"""Recompute the unrounded L06 Lab 1 quantiles and the E1/E2 arithmetic (round 19, slice d).

Runs the twin's own functions without the final main() call, so nothing is printed by the lab; the draws are
the same seeded sequence main() uses (random.Random(SEED), npv_of over N_MAX draws of YEARS receipts).
"""

import math
import random
import sys

src = open(sys.argv[1], encoding="utf-8").read().rstrip()
assert src.endswith("main()")
ns: dict = {"__name__": "lab"}
exec(compile(src[: -len("main()")], "lab", "exec"), ns)
rng = random.Random(ns["SEED"])
npvs = [ns["npv_of"]([rng.randint(ns["LOW"], ns["HIGH"]) for _ in range(ns["YEARS"])]) for _ in range(ns["N_MAX"])]
o = sorted(npvs)
q10, q90 = ns["quantile"](o, 0.10), ns["quantile"](o, 0.90)
print(f"q10 {q10:.6f} q90 {q90:.6f} unrounded width {q90 - q10:.4f} printed-width-difference {143406.13 - 14896.62:.2f}")
e = 84543.40 - 79078.68
z = e / 4400.22
print(f"E1 error {e:.2f} z {z:.4f} two-sided tail {2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))):.4f}")
print(f"E2 band {0.0552 - 1.96 * 0.0010:.5f} to {0.0552 + 1.96 * 0.0010:.5f}")
