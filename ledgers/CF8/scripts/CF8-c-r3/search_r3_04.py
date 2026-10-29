"""Search random cases for an input where the r3-04 mutant's required commitment differs from the reference's."""

import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyC3-CF8-c")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/CF/CF8/grader/reference.py", "ref")
mut = load(ROOT / "ledgers/CF8/mutants/r3-04-required-is-capped-peak-plus-shortfall.py", "mut")
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
found = 0
trials = 0
example = None
for _ in range(20000):
    trials += 1
    case = {
        "horizon_weeks": 13,
        "opening_cash_cents": rng.randrange(0, 2_000_001, 1000),
        "minimum_cash_cents": rng.randrange(100_000, 1_000_001, 1000),
        "revolver_commitment_cents": rng.randrange(0, 2_000_001, 1000),
        "opening_drawn_cents": 0,
        "covenant_threshold_cents": 0,
        "collection_lag_days": rng.randint(0, 80),
        "payment_lag_days": rng.randint(0, 50),
        "weekly_sales_cents": [rng.randrange(0, 1_500_001, 1000) for _ in range(13)],
        "weekly_purchases_cents": [rng.randrange(0, 1_500_001, 1000) for _ in range(13)],
        "weekly_opex_cents": [rng.randrange(0, 300_001, 1000) for _ in range(13)],
    }
    case["opening_drawn_cents"] = rng.randrange(0, case["revolver_commitment_cents"] + 1, 1000)
    a = ref.revolver_plan(case)["required_commitment_cents"]
    b = mut.revolver_plan(case)["required_commitment_cents"]
    if a != b:
        found += 1
        if example is None:
            example = (a, b, case)
print("trials", trials, "differ", found)
if example:
    a, b, c = example
    print("reference required", a, "mutant required", b)
    print({k: c[k] for k in c if k not in ("horizon_weeks",)})
