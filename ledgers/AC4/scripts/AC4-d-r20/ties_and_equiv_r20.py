"""Round 20: prove the two lab-twin survivors are equivalent on the shipped seed (tie count and self-pair rule)."""

import sys
import types
from pathlib import Path

ROOT = Path(sys.argv[1])
src = (ROOT / "tests/labs/AC4/lab-AC4-L08-1.py").read_text(encoding="utf-8").rstrip()
body = src[: -len("main()")]
mod = types.ModuleType("twin_L08")
sys.modules[mod.__name__] = mod
exec(compile(body, "lab-L08", "exec"), mod.__dict__)
ns = mod.__dict__
divs = ns["generate"](ns["SEED"], ns["N_DIVISIONS"])
ties = 0
pairs = 0
for i, a in enumerate(divs):
    for b in divs[i + 1 :]:
        pairs += 1
        by_ri = ns["residual_income"](a) - ns["residual_income"](b)
        by_ratio = ns["return_ratio"](a) - ns["return_ratio"](b)
        if by_ri == 0 or by_ratio == 0:
            ties += 1
print("pairs", pairs, "pairs with a tie in either measure", ties)
# self pair: a.name <= b.name includes a with itself, whose differences are both zero
a = divs[0]
self_diff = (ns["residual_income"](a) - ns["residual_income"](a), ns["return_ratio"](a) - ns["return_ratio"](a))
print("self-pair differences", self_diff, "counted by the mutant rule", (self_diff[0] > 0) != (self_diff[1] > 0) and self_diff[0] != 0 and self_diff[1] != 0)
