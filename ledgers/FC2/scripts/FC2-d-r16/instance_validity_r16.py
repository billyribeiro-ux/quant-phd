"""Check every instance for seeds 0-49 (both chains per seed) against the spec's input rules (project.html:287-291)
and report the distinctness of the answers across seeds (findings differ, not only labels)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/FC/FC2/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref_iv", GRADER / "reference.py")
assert spec and spec.loader
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

problems = []
answers = {}
for seed in range(50):
    for label, inst in (("A", make_instance(seed)), ("B", make_instance(seed + 7_919))):
        s = inst["strikes_cents"]
        c = inst["call_cents"]
        p = inst["put_cents"]
        if not (len(s) == len(c) == len(p) and len(s) >= 3):
            problems.append((seed, label, "lengths"))
        if any(b <= a for a, b in zip(s, s[1:])) or s[0] <= 0:
            problems.append((seed, label, "strikes not strictly increasing and positive"))
        if not (1 <= inst["df_ppm"] <= 1_000_000):
            problems.append((seed, label, "df_ppm range"))
        if inst["spot_cents"] < 0 or inst["fee_cents_per_contract"] < 0 or inst["half_spread_cents"] < 0:
            problems.append((seed, label, "negative spot or cost"))
        if any(not isinstance(x, int) for x in list(s) + list(c) + list(p)):
            problems.append((seed, label, "non-integer quote"))
        chain = {
            "spot_cents": inst["spot_cents"],
            "df_ppm": inst["df_ppm"],
            "strikes_cents": list(s),
            "call_cents": list(c),
            "put_cents": list(p),
            "cost": {
                "fee_cents_per_contract": inst["fee_cents_per_contract"],
                "half_spread_cents": inst["half_spread_cents"],
            },
        }
        found = ref.scan(chain)
        answers[(seed, label)] = tuple((r["kind"], r["strike_cents"], r["net_cents"]) for r in found)

print("instances checked:", 100, "rule problems:", len(problems), problems[:5])
print("distinct answer sets over 100 instances:", len(set(answers.values())))
print("instances with at least one finding:", sum(1 for v in answers.values() if v))
print("seeds with identical A and B answers:", sum(1 for seed in range(50) if answers[(seed, 'A')] == answers[(seed, 'B')]))
