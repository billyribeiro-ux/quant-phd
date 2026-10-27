# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Witnesses for the two round-2 survivors (AC2 project): the mutant is accepted where the contract requires an error
or a strict result. Usage (from the repository root): .venv/bin/python ledgers/AC2/scripts/project-r2/witness_r2.py
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/AC/AC2/grader"
MUT = ROOT / "ledgers/AC2/mutants"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ref = load("w_ref", GRADER / "reference.py")
p08 = load("w_p08", MUT / "p08_rank_checks_only_zero_columns.py")
p09 = load("w_p09", MUT / "p09_piotroski_roa_signal_weak_inequality.py")

# p08: ppe equal to (dRev - dRec) makes regressors 2 and 3 proportional (ppe/lag = (dRev-dRec)/lag).
rows = [
    {"total_accruals": 1.0 + i, "lag_assets": 100.0 + 7 * i, "d_revenue": 10.0 + i, "d_receivables": 2.0,
     "ppe": 8.0 + i}
    for i in range(6)
]
for r in rows:
    r["ppe"] = r["d_revenue"] - r["d_receivables"]
try:
    ref.modified_jones(rows)
    print("reference: accepted (unexpected)")
except ValueError as e:
    print("reference: ValueError:", e)
out = p08.modified_jones(rows)
print("p08 mutant: accepted, coefficients", [round(c, 6) for c in out["coefficients"]])

# p09: ROA_t exactly 0 (net income zero in the latest year).
st = {
    "2020-12-31": {"revenue": 100.0, "cogs": 60.0, "sga": 10.0, "net_income": 5.0, "cfo": 8.0, "total_assets": 200.0,
                   "current_assets": 90.0, "current_liabilities": 50.0, "long_term_debt": 40.0, "shares_outstanding": 10.0,
                   "receivables": 20.0, "ppe": 60.0, "depreciation": 6.0, "cash": 10.0, "equity": 100.0,
                   "operating_income": 15.0, "total_liabilities": 100.0},
    "2021-12-31": {"revenue": 110.0, "cogs": 60.0, "sga": 11.0, "net_income": 0.0, "cfo": 8.0, "total_assets": 210.0,
                   "current_assets": 95.0, "current_liabilities": 50.0, "long_term_debt": 38.0, "shares_outstanding": 10.0,
                   "receivables": 22.0, "ppe": 62.0, "depreciation": 6.0, "cash": 10.0, "equity": 110.0,
                   "operating_income": 15.0, "total_liabilities": 100.0},
}
st["2019-12-31"] = copy.deepcopy(st["2020-12-31"])
st["2019-12-31"]["total_assets"] = 190.0
st["2019-12-31"]["net_income"] = 4.0
print("reference signal 1 (ROA_t > 0, ROA_t = 0):", ref.piotroski_f_score(st, "2021-12-31")["signals"][0])
print("p09 mutant signal 1 (ROA_t >= 0):", p09.piotroski_f_score(st, "2021-12-31")["signals"][0])
