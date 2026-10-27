"""Round 3 (AC2 project): concrete witnesses that the eleven surviving mutants violate the contract the suite does not test.

Loads each mutant and the course reference by path (read-only) and prints the contract's required behaviour next to the
mutant's observed behaviour on a minimal input. Usage (repository root):
.venv/bin/python ledgers/AC2/scripts/project-r3/witness_r3.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MUT = ROOT / "ledgers/AC2/mutants"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(label: str, fn):  # type: ignore[no-untyped-def]
    try:
        out = fn()
    except Exception as exc:  # noqa: BLE001 - the observed exception is the point
        out = f"raises {type(exc).__name__}: {str(exc)[:90]}"
    print(f"{label}: {out}")


def obs(end, filed, val, form="10-K", accn=None, unit_start="2021-01-01", flow=True):  # type: ignore[no-untyped-def]
    o = {"end": end, "val": val, "filed": filed, "form": form, "fp": "FY"}
    if accn is not None:
        o["accn"] = accn
    if flow:
        o["start"] = unit_start
    return o


def facts(tag, units):  # type: ignore[no-untyped-def]
    return {"facts": {"us-gaap": {tag: {"units": units}}}}


ref = load("ref", ROOT / "course/modules/AC/AC2/grader/reference.py")
M = {k: load(k, MUT / f"{k}.py") for k in [
    "p14_standardize_reads_every_unit_of_a_tag",
    "p15_accn_read_by_direct_indexing",
    "p16_tie_break_orders_form_before_accn",
    "p17_modified_jones_needs_five_firm_years",
    "p18_modified_jones_finiteness_skips_regressors",
    "p20_piotroski_roa_plain_division",
    "p21_piotroski_shares_by_direct_indexing",
    "p29_beneish_current_liabilities_by_direct_indexing",
    "p35_accruals_cash_flow_zero_average_raises_zero_division",
    "p36_accruals_balance_sheet_plain_division",
    "p37_conflict_check_skipped_when_accn_missing",
]}
ASSET_END = "2021-12-31"

print("== p14: a shares-unit observation on a money tag (contract: unit USD only, so Assets is absent)")
f14 = facts("Assets", {"shares": [obs(ASSET_END, "2022-02-01", 5.0, flow=False)]})
run("reference standardize", lambda: ref.standardize(f14))
run("p14 standardize", lambda: M["p14_standardize_reads_every_unit_of_a_tag"].standardize(f14))

print("== p15: annual observation without accn (contract: accn optional, tie-break uses '')")
f15 = facts("Assets", {"USD": [obs(ASSET_END, "2022-02-01", 100.0, flow=False)]})
run("reference standardize", lambda: ref.standardize(f15))
run("p15 standardize", lambda: M["p15_accn_read_by_direct_indexing"].standardize(f15))

print("== p16: same filing date, 10-K accn ...002 = 100, 10-K/A accn ...001 = 90 (contract: greatest accn wins)")
f16 = facts("Assets", {"USD": [
    obs(ASSET_END, "2022-03-01", 100.0, accn="0000000002-22-000002", flow=False),
    obs(ASSET_END, "2022-03-01", 90.0, form="10-K/A", accn="0000000001-22-000001", flow=False),
]})
run("reference standardize", lambda: ref.standardize(f16))
run("p16 standardize", lambda: M["p16_tie_break_orders_form_before_accn"].standardize(f16))

print("== p37: same filing date, no accn, values 100 and 90 (contract: tie on (filed, '') with different values raises)")
f37 = facts("Assets", {"USD": [
    obs(ASSET_END, "2022-03-01", 100.0, flow=False),
    obs(ASSET_END, "2022-03-01", 90.0, flow=False),
]})
run("reference standardize", lambda: ref.standardize(f37))
run("p37 standardize", lambda: M["p37_conflict_check_skipped_when_accn_missing"].standardize(f37))

print("== p15 also: the observation set of p37 has no accn; the mutant raises KeyError on the same input")
run("p15 standardize (no accn)", lambda: M["p15_accn_read_by_direct_indexing"].standardize(f37))

SAMPLE = [
    {"total_accruals": -4.0e6, "lag_assets": 1.0e8, "d_revenue": 6.0e6, "d_receivables": 1.0e6, "ppe": 3.0e7},
    {"total_accruals": -2.5e6, "lag_assets": 8.0e7, "d_revenue": 3.0e6, "d_receivables": 0.5e6, "ppe": 2.4e7},
    {"total_accruals": -5.2e6, "lag_assets": 1.3e8, "d_revenue": 9.0e6, "d_receivables": 2.0e6, "ppe": 4.5e7},
    {"total_accruals": -1.1e6, "lag_assets": 5.0e7, "d_revenue": 1.5e6, "d_receivables": 0.2e6, "ppe": 1.1e7},
]
print("== p17: exactly four firm-years (contract: fewer than four raises; four is legal)")
run("reference modified_jones", lambda: round(ref.modified_jones(SAMPLE)["coefficients"][0], 3))
run("p17 modified_jones", lambda: round(M["p17_modified_jones_needs_five_firm_years"].modified_jones(SAMPLE)["coefficients"][0], 3))

print("== p18: NaN in d_revenue of one firm-year (contract: a non-finite value raises ValueError)")
bad = [dict(r) for r in SAMPLE]
bad[1]["d_revenue"] = float("nan")
run("reference modified_jones", lambda: ref.modified_jones(bad))
run("p18 modified_jones", lambda: M["p18_modified_jones_finiteness_skips_regressors"].modified_jones(bad))

ST = {
    "2021-12-31": {"revenue": 1000.0, "cogs": 600.0, "sga": 100.0, "depreciation": 50.0, "net_income": 80.0,
                   "cfo": 95.0, "total_assets": 900.0, "current_assets": 400.0, "cash": 60.0, "receivables": 120.0,
                   "ppe": 300.0, "current_liabilities": 200.0, "long_term_debt": 150.0, "equity": 400.0,
                   "shares_outstanding": 1000.0},
    "2022-12-31": {"revenue": 1200.0, "cogs": 700.0, "sga": 120.0, "depreciation": 55.0, "net_income": 110.0,
                   "cfo": 130.0, "total_assets": 1100.0, "current_assets": 500.0, "cash": 90.0, "receivables": 150.0,
                   "ppe": 330.0, "current_liabilities": 220.0, "long_term_debt": 180.0, "equity": 460.0,
                   "shares_outstanding": 1000.0},
    "2020-12-31": {"revenue": 900.0, "cogs": 560.0, "sga": 90.0, "depreciation": 45.0, "net_income": 60.0,
                   "cfo": 70.0, "total_assets": 850.0, "current_assets": 380.0, "cash": 50.0, "receivables": 110.0,
                   "ppe": 280.0, "current_liabilities": 190.0, "long_term_debt": 140.0, "equity": 380.0,
                   "shares_outstanding": 990.0},
}
END, PREV = "2022-12-31", "2021-12-31"

print("== p20: previous-year total assets zero (contract: a zero denominator raises ValueError)")
st20 = {k: dict(v) for k, v in ST.items()}
st20[PREV]["total_assets"] = 0.0
run("reference piotroski", lambda: ref.piotroski_f_score(st20, END))
run("p20 piotroski", lambda: M["p20_piotroski_roa_plain_division"].piotroski_f_score(st20, END))

print("== p21: latest shares_outstanding missing (contract: a missing item raises ValueError)")
st21 = {k: dict(v) for k, v in ST.items()}
del st21[END]["shares_outstanding"]
run("reference piotroski", lambda: ref.piotroski_f_score(st21, END))
run("p21 piotroski", lambda: M["p21_piotroski_shares_by_direct_indexing"].piotroski_f_score(st21, END))

print("== p29: latest current_liabilities missing (contract: a missing item raises ValueError)")
st29 = {k: dict(v) for k, v in ST.items()}
del st29[END]["current_liabilities"]
run("reference beneish", lambda: ref.beneish_m_score(st29, END))
run("p29 beneish", lambda: M["p29_beneish_current_liabilities_by_direct_indexing"].beneish_m_score(st29, END))

print("== p35/p36: average total assets zero (contract: a zero denominator raises ValueError)")
st35 = {k: dict(v) for k, v in ST.items()}
st35[END]["total_assets"] = -st35[PREV]["total_assets"]
run("reference accruals_cash_flow", lambda: ref.accruals_cash_flow(st35, END))
run("p35 accruals_cash_flow", lambda: M["p35_accruals_cash_flow_zero_average_raises_zero_division"].accruals_cash_flow(st35, END))
run("reference accruals_balance_sheet", lambda: ref.accruals_balance_sheet(st35, END))
run("p36 accruals_balance_sheet", lambda: M["p36_accruals_balance_sheet_plain_division"].accruals_balance_sheet(st35, END))
