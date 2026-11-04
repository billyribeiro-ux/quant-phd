"""Survey the 50 seeded instances from grader/instance.py: validity, distinct levels and horizons, distinct continuous tails."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1] + "/course/modules/SC/SC1/grader")
from instance import make_instance  # noqa: E402

insts = [make_instance(s) for s in range(50)]
invalid = [i["seed"] for i in insts if not (i["H"] > 0 and i["a"] > 0 and 4 <= i["n_steps"] <= 256 and 400 <= i["n_paths"] <= 800 and i["n_steps"] * i["n_paths"] <= 200_000)]
print("invalid seeds:", invalid)
print("distinct levels:", len({i["a"] for i in insts}), "distinct horizons:", len({i["H"] for i in insts}))
tails = {round(math.erfc(i["a"] / math.sqrt(2 * i["H"])), 6) for i in insts}
print("distinct continuous tails (6dp):", len(tails))
print("seed 0:", {k: insts[0][k] for k in ("H", "a", "n_steps", "n_paths")}, "seed 7919 (second instance):", {k: make_instance(7919)[k] for k in ("H", "a", "n_steps", "n_paths")})
print("labels:", {i["label"] for i in insts})
