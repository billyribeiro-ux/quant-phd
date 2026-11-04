"""Validity and variation of the grader instances for seeds 0-49 (VERIFIER_RULES 2.6 item 2). Uses grader/instance.py itself."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("instance", ROOT / "course/modules/SC/SC1/grader/instance.py")
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

insts = [mod.make_instance(s) for s in range(50)]
bad = [i["seed"] for i in insts if not (i["H"] > 0 and i["a"] > 0 and 4 <= i["n_steps"] <= 256 and 400 <= i["n_paths"] <= 800 and i["n_steps"] * i["n_paths"] <= 200_000 and i["label"] == "SIMULATED")]
print("invalid seeds:", bad)
print("distinct levels a over 50 seeds:", len({i["a"] for i in insts}))
print("distinct horizons H over 50 seeds:", len({i["H"] for i in insts}))
print("distinct grid sizes n_steps over 50 seeds:", len({i["n_steps"] for i in insts}))
tails = {round(math.erfc(i["a"] / math.sqrt(2 * i["H"])), 6) for i in insts}
print("distinct continuous tails (6 dp) over 50 seeds:", len(tails))
print("seeds 0-19 (H, a, n_steps, n_paths, tail):")
for i in insts[:20]:
    print(" ", i["seed"], i["H"], i["a"], i["n_steps"], i["n_paths"], round(math.erfc(i["a"] / math.sqrt(2 * i["H"])), 6))
