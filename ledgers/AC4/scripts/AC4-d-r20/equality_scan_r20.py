"""Round 20: count exact-equality pairs (t_min == t_max) in the L07 generator over seeds 1-40, plus the shipped seed."""

import sys
import types
from pathlib import Path

ROOT = Path(sys.argv[1])
src = (ROOT / "tests/labs/AC4/lab-AC4-L07-1.py").read_text(encoding="utf-8").rstrip()
mod = types.ModuleType("twin_L07")
sys.modules[mod.__name__] = mod
exec(compile(src[: -len("main()")], "lab-L07", "exec"), mod.__dict__)
ns = mod.__dict__
res = {}
for seed in list(range(1, 41)) + [ns["SEED"]]:
    cases = ns["generate"](seed, ns["N_CASES"])
    eq = [c.case_id for c in cases if c.q <= c.capacity and ns["t_min"](c) == ns["t_max"](c)]
    res[seed] = eq
print("seeds with at least one generated exact-equality pair:", {s: v for s, v in res.items() if v})
print("shipped seed", ns["SEED"], "equality pairs among generated:", res[ns["SEED"]])
