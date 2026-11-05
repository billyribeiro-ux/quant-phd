"""Round-13 BK4-c: check a candidate fixture that kills mutant r13d (fund layer capped at the survivors' pool).

Loads the reference and the mutant as modules from the repository and evaluates the candidate fixture on both.
Run: python3 -I ledgers/BK4/scripts/BK4-c-r13/fixture_probe_r13d.py   (from the checkout root)
"""

import importlib.util
import os
import sys

ROOT = os.getcwd()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ref = load(os.path.join(ROOT, "course/modules/BK/BK4/grader/reference.py"), "ref")
mut = load(os.path.join(ROOT, "ledgers/BK4/mutants/r13d_fund_layer_capped_at_survivor_pool.py"), "mut")
margins = {1: 0, 2: 0, 3: 100}
funds = {1: 10, 2: 20, 3: 50}
for name, mod in (("reference", ref), ("mutant r13d", mut)):
    w = mod.waterfall(200, 3, margins, funds, 30)
    print(name, "margin", w.margin_cents, "fund", w.default_fund_cents, "capital", w.ccp_capital_cents,
          "survivors", w.survivor_cents, "uncovered", w.uncovered_cents)
exp = (100, 50, 30, {1: 7, 2: 13}, 0)
got = ref.waterfall(200, 3, margins, funds, 30)
assert (got.margin_cents, got.default_fund_cents, got.ccp_capital_cents, got.survivor_cents, got.uncovered_cents) == (
    100, 50, 30, {1: 7, 2: 13}, 0), "candidate fixture is not what the reference gives"
mw = mut.waterfall(200, 3, margins, funds, 30)
assert (mw.default_fund_cents, mw.survivor_cents) != (50, {1: 7, 2: 13}), "fixture does not separate the mutant"
print("candidate fixture: reference gives (100, 50, 30, {1: 7, 2: 13}, 0); mutant differs")
