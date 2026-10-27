# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Witness inputs for the three surviving mutants (p01, p02, p03): the contract's answer versus the mutant's answer.

Usage (from the repository root): .venv/bin/python ledgers/AC2/scripts/project-r1/witness_survivors.py

For each survivor, builds a small input that the A15 contract decides (ValueError or a value), then runs the reference
(course grader/reference.py, read-only) and the mutant (ledgers/AC2/mutants/*.py) on it and prints both outcomes.
Uses the seed-0 filer from the course's instance.py so the input is a real generated filer, not a hand-made one.
"""

from __future__ import annotations

import copy
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "AC" / "AC2" / "grader"
MUT = ROOT / "ledgers" / "AC2" / "mutants"


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(fn) -> str:  # type: ignore[no-untyped-def]
    try:
        value = fn()
    except ValueError as exc:
        return f"ValueError ({exc})"
    except Exception as exc:
        return f"{type(exc).__name__} ({exc})"
    return f"returns {value!r}"


def main() -> int:
    ref = load("ref_mod", GRADER / "reference.py")
    inst = load("inst_mod", GRADER / "instance.py")
    mutants = {
        "p01": load("p01", MUT / "p01_previous_year_without_the_350_380_window.py"),
        "p02": load("p02", MUT / "p02_annual_duration_narrowed_to_360_370_days.py"),
        "p03": load("p03", MUT / "p03_ratio_result_not_checked_for_finiteness.py"),
        "p06": load("p06", MUT / "p06_missing_val_taken_as_zero.py"),
        "p07": load("p07", MUT / "p07_prior_year_balance_filled_from_current_year.py"),
    }
    payload = json.loads(inst.make_instance(0)["payload"])
    facts = payload["facts"]
    ends = payload["period_ends"]
    latest, prior, prior2 = ends[-1], ends[-2], ends[-3]
    final = payload["truth"]["final"]

    # p01: no period end 350 to 380 days before the latest one, but an earlier one exists (two years back)
    st = {prior2: copy.deepcopy(final[prior2]), latest: copy.deepcopy(final[latest])}
    print("p01 dupont with only two-years-back history (contract: no previous year, ValueError)")
    print("  reference:", outcome(lambda: ref.dupont(st, latest)))
    print("  mutant   :", outcome(lambda: mutants["p01"].dupont(st, latest)))

    # p02: a 10-K/A-free annual fact whose duration is 375 days (contract: annual, within 350 to 380 days)
    f = copy.deepcopy(facts)
    end = dt.date.fromisoformat(latest)
    obs = {
        "end": latest,
        "start": (end - dt.timedelta(days=375)).isoformat(),
        "val": 123456789.0,
        "filed": "2999-01-01",
        "form": "10-K",
        "fp": "FY",
        "accn": "zz-9999",
    }
    f["facts"]["us-gaap"].setdefault("NetIncomeLoss", {"units": {}})["units"].setdefault("USD", []).append(obs)
    print("p02 standardize with a 375-day 10-K fact for net income (contract: annual, so it supplies the value)")
    print("  reference: net_income", ref.standardize(f)[latest]["net_income"])
    print("  mutant   : net_income", mutants["p02"].standardize(f)[latest]["net_income"])

    # p03: a ratio whose denominator is positive and tiny, so the quotient overflows to infinity
    big = {latest: {"current_assets": 1e300, "current_liabilities": 1e-300}}
    print(
        "p03 current_ratio with current_assets 1e300 and current_liabilities 1e-300 (contract: non-finite -> ValueError)"
    )
    print("  reference:", outcome(lambda: ref.current_ratio(big, latest)))
    print("  mutant   :", outcome(lambda: mutants["p03"].current_ratio(big, latest)))
    # p06: an observation without val (contract: ValueError; a missing val is not a number)
    f6 = copy.deepcopy(facts)
    f6["facts"]["us-gaap"]["Assets"]["units"]["USD"].append(
        {"end": latest, "filed": "2999-01-01", "form": "10-K", "fp": "FY", "accn": "zz-8888"}
    )
    print("p06 standardize with an annual Assets observation that has no val (contract: ValueError)")
    print("  reference:", outcome(lambda: ref.standardize(f6)))
    print("  mutant   :", outcome(lambda: mutants["p06"].standardize(f6)))

    # p07: last year's total assets missing (contract: nothing is imputed, ValueError)
    st7 = copy.deepcopy(final)
    del st7[prior]["total_assets"]
    print("p07 dupont with prior-year total assets missing (contract: nothing is imputed, ValueError)")
    print("  reference:", outcome(lambda: ref.dupont(st7, latest)))
    print("  mutant   :", outcome(lambda: mutants["p07"].dupont(st7, latest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
