"""Acceptance suite for the AC2 project: the Atlas A15 fundamentals engine (atlas/fundamentals.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your atlas/fundamentals.py and instance.py next to this file. Warnings are failures, as in the browser.

Each test checks a number, an invariant, an error class or a purity property against the A15 contract. A failure
names the property it checks and the idea to revisit. It never prints the expected value. The grader checks the
exception type (ValueError), not the wording of the message.
"""

from __future__ import annotations

import ast
import contextlib
import copy
import datetime as dt
import io
import json
import math
import os
import sys
import warnings
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from atlas import fundamentals as sol  # type: ignore[attr-defined]
from instance import (
    BENEISH_COEFFICIENTS,
    BENEISH_INTERCEPT,
    ITEMS,
    TAG_PRIORITY,
    make_instance,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
PAYLOAD: dict[str, Any] = json.loads(INST["payload"])
FACTS: dict[str, Any] = PAYLOAD["facts"]
FINAL: dict[str, dict[str, float]] = PAYLOAD["truth"]["final"]
AS_OF: dict[str, dict[str, dict[str, float]]] = PAYLOAD["truth"]["as_of"]
CUTS: dict[str, str | None] = PAYLOAD["cutoffs"]
LATEST: str = INST["latest"]
PRIOR: str = INST["prior"]
PRIOR2: str = INST["prior2"]
PERIODS: list[str] = PAYLOAD["period_ends"]
OLDEST: str = PERIODS[0]
SAMPLE: list[dict[str, float]] = PAYLOAD["sample"]
PLANTED: list[bool] = PAYLOAD["planted"]
RISKY_TAGS = ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet")

# ---------------------------------------------------------------- helpers


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError: the grader checks the exception type."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError.")


# Float comparisons. The A15 contract states no numerical tolerance except the DuPont identity (relative 1e-12,
# asserted as such). A correct implementation of the same formula differs from another only by rounding, so the
# comparisons use this one documented bound, FLOAT_RTOL, with an absolute floor FLOAT_ATOL.
FLOAT_RTOL = 1e-6
FLOAT_ATOL = 1e-9


def close(a: float, b: float, rel: float = FLOAT_RTOL) -> bool:
    return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=FLOAT_ATOL)


def assert_statements_equal(actual: Mapping[str, Mapping[str, float]], expected: Mapping[str, Any], what: str) -> None:
    assert list(actual) == list(expected), f"{what}: the period ends must be the reference's, in ascending order."
    for end in expected:
        assert set(actual[end]) == set(expected[end]), f"{what}: the items present for one period end differ."
        for item, value in expected[end].items():
            assert close(actual[end][item], value), f"{what}: a standardized value differs from the reference."


def scaled_statements(st: Mapping[str, Mapping[str, float]], c: float) -> dict[str, dict[str, float]]:
    """Every money item multiplied by c; share counts are not money and stay as they are."""
    return {end: {k: (v if k == "shares_outstanding" else v * c) for k, v in row.items()} for end, row in st.items()}


def scaled_facts(facts: Mapping[str, Any], c: float) -> dict[str, Any]:
    out = copy.deepcopy(dict(facts))
    for entry in out["facts"]["us-gaap"].values():
        for obs in entry["units"].get("USD", []):
            obs["val"] = obs["val"] * c
    return out


def annual_obs(end: str, filed: str, val: float, accn: str) -> dict[str, Any]:
    start = dt.date.fromisoformat(end) - dt.timedelta(days=364)
    return {
        "end": end,
        "start": start.isoformat(),
        "val": val,
        "filed": filed,
        "form": "10-K",
        "fp": "FY",
        "accn": accn,
    }


def with_obs(facts: Mapping[str, Any], tag: str, obs: dict[str, Any], unit: str = "USD") -> dict[str, Any]:
    out = copy.deepcopy(dict(facts))
    gaap = out["facts"]["us-gaap"]
    gaap.setdefault(tag, {"label": tag, "units": {}})["units"].setdefault(unit, []).append(obs)
    return out


def without_tags(facts: Mapping[str, Any], tags: tuple[str, ...]) -> dict[str, Any]:
    out = copy.deepcopy(dict(facts))
    for tag in tags:
        out["facts"]["us-gaap"].pop(tag, None)
    return out


def ratio_call(name: str, st: Mapping[str, Mapping[str, float]]) -> Callable[[], object]:
    return lambda: RATIO_CALLS[name](st, LATEST)


def ex(end: str, item: str, st: Mapping[str, Mapping[str, float]] = FINAL) -> float:
    return float(st[end][item])


def mj_design(rows: list[dict[str, float]]) -> tuple[np.ndarray, np.ndarray]:
    lag = np.array([r["lag_assets"] for r in rows], dtype=np.float64)
    y = np.array([r["total_accruals"] for r in rows], dtype=np.float64) / lag
    design = np.column_stack(
        [
            1.0 / lag,
            (np.array([r["d_revenue"] for r in rows]) - np.array([r["d_receivables"] for r in rows])) / lag,
            np.array([r["ppe"] for r in rows]) / lag,
        ]
    )
    return design, y


# ---------------------------------------------------------------- the contract's tables and surface


def test_items_table_is_the_contract() -> None:
    assert len(sol.ITEMS) == 17, "the A15 contract names seventeen standardized items."
    assert tuple(sol.ITEMS) == tuple(ITEMS), "ITEMS must list the contract's items in the contract's table order."


def test_tag_priority_is_the_contract() -> None:
    assert {k: tuple(v) for k, v in sol.TAG_PRIORITY.items()} == {k: tuple(v) for k, v in TAG_PRIORITY.items()}, (
        "TAG_PRIORITY must map each item to the contract's us-gaap tags, in priority order."
    )


def test_beneish_constants_are_exported() -> None:
    assert sol.BENEISH_INTERCEPT == BENEISH_INTERCEPT, (
        "BENEISH_INTERCEPT must be the shared intercept, which is UNCONFIRMED (see instance.BENEISH_STATUS)."
    )
    assert set(sol.BENEISH_COEFFICIENTS) == {"DSRI", "GMI", "AQI", "SGI", "DEPI", "SGAI", "LVGI", "TATA"}, (
        "BENEISH_COEFFICIENTS must hold the eight variable names, DSRI through TATA."
    )
    for name, value in BENEISH_COEFFICIENTS.items():
        assert sol.BENEISH_COEFFICIENTS[name] == value, (
            "a Beneish coefficient differs from the shared (unconfirmed) table in instance.py."
        )


@pytest.mark.parametrize(
    "name",
    [
        "standardize",
        "dupont",
        "roic",
        "current_ratio",
        "gross_margin",
        "debt_to_assets",
        "days_sales_outstanding",
        "accruals_cash_flow",
        "accruals_balance_sheet",
        "modified_jones",
        "piotroski_f_score",
        "beneish_m_score",
    ],
)
def test_public_function_exists(name: str) -> None:
    assert callable(getattr(sol, name, None)), f"{name} must be a public function of the A15 module."


# ---------------------------------------------------------------- standardization and the as-of rule


def test_standardize_matches_the_final_numbers() -> None:
    assert_statements_equal(sol.standardize(FACTS), FINAL, "standardize with no cut-off")


def test_standardize_matches_each_as_of_cut() -> None:
    for name, iso in CUTS.items():
        if iso is None:
            continue
        assert_statements_equal(sol.standardize(FACTS, iso), AS_OF[iso], f"standardize as of the {name} cut-off")


def test_as_of_none_is_the_latest_filing() -> None:
    assert_statements_equal(sol.standardize(FACTS, None), FINAL, "standardize with as_of=None")
    assert_statements_equal(sol.standardize(FACTS, CUTS["latest_filing"]), FINAL, "standardize as of the last filing")


def test_as_of_cut_is_inclusive_and_excludes_the_latest_year() -> None:
    assert LATEST in sol.standardize(FACTS, CUTS["latest_filing"]), (
        "an observation filed on the as-of date is known on that date (filed <= as_of)."
    )
    assert LATEST not in sol.standardize(FACTS, CUTS["before_latest_filing"]), (
        "the latest year's 10-K is not known the day before it was filed."
    )


def test_as_of_is_monotone() -> None:
    cuts = sorted(iso for iso in CUTS.values() if iso is not None)
    pairs_before: set[tuple[str, str]] = set()
    periods_before: set[str] = set()
    for iso in cuts:
        st = sol.standardize(FACTS, iso)
        pairs = {(end, item) for end, row in st.items() for item in row}
        assert pairs_before <= pairs, "a later as-of date cannot lose a value that an earlier one already knew."
        assert periods_before <= set(st), "a later as-of date cannot lose a period end."
        pairs_before, periods_before = pairs, set(st)


def test_restatement_changes_the_value_only_after_the_amendment() -> None:
    year, item = PAYLOAD["restatement"]["year"], PAYLOAD["restatement"]["item"]
    if CUTS["original_restatement"] is not None:
        before = sol.standardize(FACTS, CUTS["original_restatement"])[year][item]
        assert close(before, AS_OF[CUTS["original_restatement"]][year][item]), (
            "before the amendment is filed, the original 10-K's value is the one known (filed, accn) rule."
        )
    after = sol.standardize(FACTS, CUTS["after_restatement"])[year][item]
    assert close(after, FINAL[year][item]), "after the 10-K/A is filed, its restated value is the one known."


def test_tied_observations_with_different_values_raise() -> None:
    must_raise(
        lambda: sol.standardize(PAYLOAD["conflict"]),
        "two annual observations of one tag and period end that tie on (filed, accn) with different values",
    )


def test_tied_observations_with_equal_values_are_not_a_conflict() -> None:
    twin_facts = copy.deepcopy(FACTS)
    latest_assets = [
        obs
        for obs in twin_facts["facts"]["us-gaap"]["Assets"]["units"]["USD"]
        if obs["end"] == LATEST and obs["form"] == "10-K"
    ]
    twin_facts["facts"]["us-gaap"]["Assets"]["units"]["USD"].append(dict(latest_assets[0]))
    assert_statements_equal(sol.standardize(twin_facts), FINAL, "a repeated observation with the same value")


def test_standardize_ignores_observation_order() -> None:
    reversed_facts = copy.deepcopy(dict(FACTS))
    for entry in reversed_facts["facts"]["us-gaap"].values():
        for obs_list in entry["units"].values():
            obs_list.reverse()
    assert_statements_equal(sol.standardize(reversed_facts), FINAL, "standardize with observations reversed")


def test_tag_priority_first_present_tag_wins() -> None:
    f1 = with_obs(FACTS, "Revenues", annual_obs(LATEST, str(CUTS["latest_filing"]), 1234567.0, "zz-0001"))
    assert close(sol.standardize(f1)[LATEST]["revenue"], 1234567.0), (
        "when Revenues has an annual observation for the period end, it supplies revenue (first in the priority list)."
    )
    f2 = with_obs(
        without_tags(FACTS, RISKY_TAGS),
        "SalesRevenueNet",
        annual_obs(LATEST, str(CUTS["latest_filing"]), 7654321.0, "zz-0002"),
    )
    assert close(sol.standardize(f2)[LATEST]["revenue"], 7654321.0), (
        "with no higher-priority tag for the period end, the next tag in the list supplies the value."
    )


def test_missing_item_is_absent_not_imputed() -> None:
    row = sol.standardize(FACTS)[OLDEST]
    assert "cfo" not in row, "a period end with no tag in the list has no value: the key is absent, nothing is imputed."
    assert "cfo" in sol.standardize(FACTS)[LATEST], "the latest year reports cfo under its tag."


def test_period_ends_are_ascending_and_nonempty() -> None:
    out = sol.standardize(FACTS)
    assert list(out) == sorted(out), "period ends must be ascending."
    assert all(out[end] for end in out), "a period end appears only when it has at least one item."


def test_standardized_values_are_floats() -> None:
    out = sol.standardize(FACTS)
    assert all(isinstance(v, float) for row in out.values() for v in row.values()), (
        "every standardized value is a float (the engine never converts the filing's units)."
    )


@pytest.mark.parametrize(
    ("bad", "condition"),
    [
        pytest.param(lambda: sol.standardize({"cik": 1}), "a mapping without a 'facts' key", id="no-facts"),
        pytest.param(
            lambda: sol.standardize(
                with_obs(FACTS, "Assets", {"val": 1.0, "filed": LATEST, "form": "10-K", "fp": "FY"})
            ),
            "an observation without an end date",
            id="no-end",
        ),
        pytest.param(
            lambda: sol.standardize(with_obs(FACTS, "Assets", {"end": LATEST, "val": 1.0, "form": "10-K", "fp": "FY"})),
            "an observation without a filing date",
            id="no-filed",
        ),
        pytest.param(
            lambda: sol.standardize(
                with_obs(FACTS, "Assets", {"end": LATEST, "val": 1.0, "filed": LATEST, "fp": "FY"})
            ),
            "an observation without a form",
            id="no-form",
        ),
        pytest.param(
            lambda: sol.standardize(
                with_obs(
                    FACTS, "Assets", {"end": LATEST, "val": float("nan"), "filed": LATEST, "form": "10-K", "fp": "FY"}
                )
            ),
            "an observation whose value is NaN",
            id="nan",
        ),
        pytest.param(
            lambda: sol.standardize(
                with_obs(
                    FACTS, "Assets", {"end": LATEST, "val": float("inf"), "filed": LATEST, "form": "10-K", "fp": "FY"}
                )
            ),
            "an observation whose value is infinite",
            id="inf",
        ),
        pytest.param(
            lambda: sol.standardize(
                with_obs(FACTS, "Assets", {"end": LATEST, "val": "123", "filed": LATEST, "form": "10-K", "fp": "FY"})
            ),
            "an observation whose value is a string",
            id="string-value",
        ),
        pytest.param(
            lambda: sol.standardize(
                with_obs(
                    FACTS, "Assets", {"end": "2020-13-01", "val": 1.0, "filed": LATEST, "form": "10-K", "fp": "FY"}
                )
            ),
            "an end date that is not a valid ISO date",
            id="bad-end",
        ),
        pytest.param(
            lambda: sol.standardize(
                with_obs(
                    FACTS, "Assets", {"end": LATEST, "val": 1.0, "filed": "2020/12/31", "form": "10-K", "fp": "FY"}
                )
            ),
            "a filing date in another format",
            id="bad-filed",
        ),
        pytest.param(
            lambda: sol.standardize(
                with_obs(
                    FACTS,
                    "NetIncomeLoss",
                    {"end": LATEST, "start": "not-a-date", "val": 1.0, "filed": LATEST, "form": "10-K", "fp": "FY"},
                )
            ),
            "a start date that is not a valid ISO date",
            id="bad-start",
        ),
        pytest.param(lambda: sol.standardize(FACTS, "2020/01/01"), "an as-of date in another format", id="bad-as-of"),
        pytest.param(
            lambda: sol.standardize(FACTS, "2020-02-30"), "an as-of date that does not exist", id="impossible-as-of"
        ),
        pytest.param(lambda: sol.standardize(FACTS, 20200101), "an as-of date that is not a string", id="int-as-of"),
    ],
)
def test_invalid_facts_raise(bad: Callable[[], object], condition: str) -> None:
    must_raise(bad, condition)


# ---------------------------------------------------------------- ratios on the reference numbers


def test_dupont_numbers() -> None:
    out = sol.dupont(FINAL, LATEST)
    avg_ta = (ex(LATEST, "total_assets") + ex(PRIOR, "total_assets")) / 2
    avg_eq = (ex(LATEST, "equity") + ex(PRIOR, "equity")) / 2
    rev, ni = ex(LATEST, "revenue"), ex(LATEST, "net_income")
    expected = {
        "net_margin": ni / rev,
        "asset_turnover": rev / avg_ta,
        "leverage": avg_ta / avg_eq,
        "roe": ni / avg_eq,
        "roa": ni / avg_ta,
    }
    assert set(out) == set(expected), (
        "dupont must return exactly the keys net_margin, asset_turnover, leverage, roe, roa."
    )
    for key, value in expected.items():
        assert close(out[key], value), f"dupont['{key}'] must follow the definition with average balances."


def test_dupont_identity_holds() -> None:
    out = sol.dupont(FINAL, LATEST)
    assert math.isclose(out["roe"], out["net_margin"] * out["asset_turnover"] * out["leverage"], rel_tol=1e-12), (
        "DuPont identity: roe = net margin x asset turnover x leverage, to relative 1e-12."
    )


def test_roic_number() -> None:
    tax = 0.25
    avg_ic = (
        (ex(LATEST, "equity") + ex(LATEST, "long_term_debt") - ex(LATEST, "cash"))
        + (ex(PRIOR, "equity") + ex(PRIOR, "long_term_debt") - ex(PRIOR, "cash"))
    ) / 2
    expected = ex(LATEST, "operating_income") * (1 - tax) / avg_ic
    assert close(sol.roic(FINAL, LATEST, tax), expected), (
        "ROIC = operating_income (1 - tax) / average invested capital, with invested capital equity + LTD - cash."
    )


@pytest.mark.parametrize("tax", [0.0, 0.999])
def test_roic_accepts_the_whole_tax_range(tax: float) -> None:
    assert math.isfinite(sol.roic(FINAL, LATEST, tax)), "0 <= tax_rate < 1 is a legal tax rate."


@pytest.mark.parametrize(
    ("tax", "condition"),
    [
        pytest.param(1.0, "a tax rate of one", id="one"),
        pytest.param(-0.01, "a negative tax rate", id="negative"),
        pytest.param(float("nan"), "a NaN tax rate", id="nan"),
        pytest.param(float("inf"), "an infinite tax rate", id="inf"),
    ],
)
def test_roic_rejects_invalid_tax_rates(tax: Any, condition: str) -> None:
    must_raise(lambda: sol.roic(FINAL, LATEST, tax), f"roic with {condition}")


def test_roic_rejects_nonpositive_invested_capital() -> None:
    st = copy.deepcopy(FINAL)
    for end in (LATEST, PRIOR):
        st[end]["cash"] = st[end]["equity"] + st[end]["long_term_debt"] + 1.0  # invested capital = -1
    must_raise(lambda: sol.roic(st, LATEST, 0.25), "roic when average invested capital is not positive")


def test_single_ratio_numbers() -> None:
    assert close(sol.current_ratio(FINAL, LATEST), ex(LATEST, "current_assets") / ex(LATEST, "current_liabilities"))
    rev, cogs = ex(LATEST, "revenue"), ex(LATEST, "cogs")
    assert close(sol.gross_margin(FINAL, LATEST), (rev - cogs) / rev), "gross margin is (revenue - cogs) / revenue."
    assert close(sol.debt_to_assets(FINAL, LATEST), ex(LATEST, "long_term_debt") / ex(LATEST, "total_assets"))
    assert close(sol.days_sales_outstanding(FINAL, LATEST), ex(LATEST, "receivables") / rev * 365.0), (
        "days sales outstanding is receivables / revenue * 365."
    )


def test_accruals_cash_flow_number() -> None:
    avg_ta = (ex(LATEST, "total_assets") + ex(PRIOR, "total_assets")) / 2
    expected = (ex(LATEST, "net_income") - ex(LATEST, "cfo")) / avg_ta
    assert close(sol.accruals_cash_flow(FINAL, LATEST), expected), (
        "cash-flow accruals = (net income - cfo) / average total assets."
    )


def test_accruals_balance_sheet_number() -> None:
    avg_ta = (ex(LATEST, "total_assets") + ex(PRIOR, "total_assets")) / 2
    d_ca = ex(LATEST, "current_assets") - ex(PRIOR, "current_assets")
    d_cash = ex(LATEST, "cash") - ex(PRIOR, "cash")
    d_cl = ex(LATEST, "current_liabilities") - ex(PRIOR, "current_liabilities")
    expected = ((d_ca - d_cash) - d_cl - ex(LATEST, "depreciation")) / avg_ta
    assert close(sol.accruals_balance_sheet(FINAL, LATEST), expected), (
        "Sloan accruals: [(d current assets - d cash) - d current liabilities - depreciation] / average assets."
    )


def test_cash_is_subtracted_in_the_balance_sheet_accruals() -> None:
    avg_ta = (ex(LATEST, "total_assets") + ex(PRIOR, "total_assets")) / 2
    st = copy.deepcopy(FINAL)
    base = sol.accruals_balance_sheet(st, LATEST)
    st[LATEST]["cash"] += 1000.0  # more cash is not an accrual, so the measure must fall by 1000 / average assets
    assert close(sol.accruals_balance_sheet(st, LATEST), base - 1000.0 / avg_ta, rel=FLOAT_RTOL), (
        "an increase in cash lowers the balance-sheet accruals: cash is excluded from accruals (Sloan 1996)."
    )


def test_cfo_lowers_the_cash_flow_accruals() -> None:
    avg_ta = (ex(LATEST, "total_assets") + ex(PRIOR, "total_assets")) / 2
    st = copy.deepcopy(FINAL)
    base = sol.accruals_cash_flow(st, LATEST)
    st[LATEST]["cfo"] += 1000.0
    assert close(sol.accruals_cash_flow(st, LATEST), base - 1000.0 / avg_ta, rel=FLOAT_RTOL), (
        "more operating cash flow lowers cash-flow accruals, (net income - cfo) / average assets."
    )


RATIO_CALLS: dict[str, Callable[..., Any]] = {
    "dupont": lambda st, e: sol.dupont(st, e),
    "roic": lambda st, e: sol.roic(st, e, 0.25),
    "current_ratio": lambda st, e: sol.current_ratio(st, e),
    "gross_margin": lambda st, e: sol.gross_margin(st, e),
    "debt_to_assets": lambda st, e: sol.debt_to_assets(st, e),
    "days_sales_outstanding": lambda st, e: sol.days_sales_outstanding(st, e),
    "accruals_cash_flow": lambda st, e: sol.accruals_cash_flow(st, e),
    "accruals_balance_sheet": lambda st, e: sol.accruals_balance_sheet(st, e),
    "piotroski_f_score": lambda st, e: sol.piotroski_f_score(st, e),
    "beneish_m_score": lambda st, e: sol.beneish_m_score(st, e),
}

NEEDS_ITEMS: dict[str, tuple[str, ...]] = {
    "dupont": ("revenue", "net_income", "total_assets", "equity"),
    "roic": ("operating_income", "equity", "long_term_debt", "cash"),
    "current_ratio": ("current_assets", "current_liabilities"),
    "gross_margin": ("revenue", "cogs"),
    "debt_to_assets": ("long_term_debt", "total_assets"),
    "days_sales_outstanding": ("receivables", "revenue"),
    "accruals_cash_flow": ("net_income", "cfo", "total_assets"),
    "accruals_balance_sheet": ("current_assets", "cash", "current_liabilities", "depreciation", "total_assets"),
}


@pytest.mark.parametrize("name", list(NEEDS_ITEMS))
def test_each_ratio_raises_on_a_missing_item(name: str) -> None:
    for item in NEEDS_ITEMS[name]:
        st = copy.deepcopy(FINAL)
        del st[LATEST][item]
        must_raise(ratio_call(name, st), f"{name} with {item} missing")


@pytest.mark.parametrize(
    "name", ["dupont", "roic", "accruals_cash_flow", "accruals_balance_sheet", "piotroski_f_score", "beneish_m_score"]
)
def test_ratios_that_need_the_prior_year_raise_without_it(name: str) -> None:
    only_latest = {LATEST: FINAL[LATEST]}
    must_raise(lambda: RATIO_CALLS[name](only_latest, LATEST), f"{name} with no previous year in the statements")


@pytest.mark.parametrize("name", ["current_ratio", "gross_margin", "debt_to_assets", "days_sales_outstanding"])
def test_single_year_ratios_need_only_the_period(name: str) -> None:
    only_latest = {LATEST: FINAL[LATEST]}
    assert math.isfinite(float(RATIO_CALLS[name](only_latest, LATEST))), (
        f"{name} needs only its own period end: a statement set with one year is enough."
    )


@pytest.mark.parametrize(
    ("name", "item"),
    [
        ("dupont", "revenue"),
        ("current_ratio", "current_liabilities"),
        ("gross_margin", "revenue"),
        ("debt_to_assets", "total_assets"),
        ("days_sales_outstanding", "revenue"),
    ],
)
def test_zero_denominator_raises(name: str, item: str) -> None:
    st = copy.deepcopy(FINAL)
    st[LATEST][item] = 0.0
    must_raise(lambda: RATIO_CALLS[name](st, LATEST), f"{name} with a zero {item} in a denominator")


def test_zero_average_assets_raise() -> None:
    st = copy.deepcopy(FINAL)
    st[LATEST]["total_assets"] = -st[PRIOR]["total_assets"]  # the two-year average is zero
    must_raise(lambda: sol.dupont(st, LATEST), "dupont with average total assets of zero")


def test_zero_average_equity_raises() -> None:
    st = copy.deepcopy(FINAL)
    st[LATEST]["equity"] = -st[PRIOR]["equity"]  # the two-year average equity is zero
    must_raise(lambda: sol.dupont(st, LATEST), "dupont with average equity of zero")


@pytest.mark.parametrize("name", list(RATIO_CALLS))
def test_unknown_or_malformed_period_end_raises(name: str) -> None:
    must_raise(lambda: RATIO_CALLS[name](FINAL, "1999-01-01"), f"{name} for a period end not in the statements")
    must_raise(lambda: RATIO_CALLS[name](FINAL, "2020/12/31"), f"{name} for a period end that is not an ISO date")


@pytest.mark.parametrize("name", list(RATIO_CALLS))
def test_ratios_are_invariant_to_money_units(name: str) -> None:
    for c in (1e3, 3.7e-4):
        a = RATIO_CALLS[name](FINAL, LATEST)
        b = RATIO_CALLS[name](scaled_statements(FINAL, c), LATEST)
        if isinstance(a, dict) and "signals" in a:
            assert tuple(a["signals"]) == tuple(b["signals"]), f"{name} signals must not change when money is rescaled."
            assert int(a["score"]) == int(b["score"]), f"{name} score must not change when money is rescaled."
        elif isinstance(a, dict):
            assert a.keys() == b.keys(), f"{name} must keep its keys when money is rescaled."
            for key in a:
                assert close(float(a[key]), float(b[key])), f"{name}['{key}'] must be invariant to units."
        else:
            assert close(float(a), float(b)), (
                f"{name} is a ratio of money items, so multiplying every money item by a constant must not change it."
            )


def test_engine_scales_money_consistently() -> None:
    c = 1e3
    assert_statements_equal(
        sol.standardize(scaled_facts(FACTS, c)), scaled_statements(FINAL, c), "standardize of scaled money"
    )


# ---------------------------------------------------------------- modified Jones


def test_modified_jones_coefficients_are_the_least_squares_fit() -> None:
    design, y = mj_design(SAMPLE)
    expected = np.linalg.lstsq(design, y, rcond=None)[0]
    out = sol.modified_jones(SAMPLE)
    assert len(out["coefficients"]) == 3, "modified_jones must return three coefficients (a1, a2, a3)."
    assert np.allclose(np.asarray(out["coefficients"]), expected, rtol=FLOAT_RTOL, atol=FLOAT_ATOL), (
        "the coefficients are the OLS fit of accruals / lag on [1/lag, (dRev - dRec)/lag, ppe/lag], no intercept."
    )


def test_modified_jones_fitted_and_discretionary_identities() -> None:
    design, y = mj_design(SAMPLE)
    coef = np.linalg.lstsq(design, y, rcond=None)[0]
    out = sol.modified_jones(SAMPLE)
    fitted = np.asarray(out["nondiscretionary"])
    disc = np.asarray(out["discretionary"])
    assert fitted.shape == (len(SAMPLE),) and disc.shape == (len(SAMPLE),), "one value per firm-year, in sample order."
    assert np.allclose(fitted, design @ coef, rtol=FLOAT_RTOL, atol=FLOAT_ATOL), (
        "nondiscretionary_i is the fitted value, in sample order."
    )
    assert np.allclose(fitted + disc, y, rtol=FLOAT_RTOL, atol=FLOAT_ATOL), (
        "discretionary_i = accruals_i / lag_i - fitted_i, so the two parts add back to the scaled accruals."
    )


def test_modified_jones_is_invariant_to_money_units() -> None:
    c = 1e3
    scaled = [{k: v * c for k, v in row.items()} for row in SAMPLE]  # every field is in currency units
    a = sol.modified_jones(SAMPLE)
    b = sol.modified_jones(scaled)
    assert np.allclose(b["discretionary"], a["discretionary"], rtol=FLOAT_RTOL, atol=FLOAT_ATOL), (
        "accruals and all balances scale together, so the scaled discretionary accruals are unchanged."
    )
    assert math.isclose(b["coefficients"][0], c * a["coefficients"][0], rel_tol=FLOAT_RTOL), (
        "the intercept-like coefficient a1 multiplies 1/lag, so it scales by the money unit."
    )
    assert np.allclose(b["coefficients"][1:], a["coefficients"][1:], rtol=FLOAT_RTOL), (
        "the scaled-ratio coefficients a2 and a3 do not depend on the money unit."
    )


def test_modified_jones_accepts_tuples_and_numpy_values() -> None:
    a = sol.modified_jones(SAMPLE)
    as_tuple = tuple(SAMPLE)
    as_numpy = [{k: np.float64(v) for k, v in row.items()} for row in SAMPLE]
    b = sol.modified_jones(as_tuple)
    c = sol.modified_jones(as_numpy)
    assert np.allclose(b["discretionary"], a["discretionary"], rtol=FLOAT_RTOL), (
        "a tuple of firm-years is a valid sequence."
    )
    assert np.allclose(c["discretionary"], a["discretionary"], rtol=FLOAT_RTOL), "NumPy scalar values are numbers."


def test_modified_jones_accepts_integer_values() -> None:
    ints = [{k: round(v) for k, v in row.items()} for row in SAMPLE]
    floats = [{k: float(round(v)) for k, v in row.items()} for row in SAMPLE]
    a = sol.modified_jones(floats)
    b = sol.modified_jones(ints)
    assert np.allclose(b["discretionary"], a["discretionary"], rtol=FLOAT_RTOL, atol=FLOAT_ATOL), (
        "integer-valued firm-years must give the same answer as the same values stored as floats."
    )
    assert np.allclose(b["coefficients"], a["coefficients"], rtol=FLOAT_RTOL), "integer inputs must not change the fit."


@pytest.mark.parametrize(
    ("bad", "condition"),
    [
        pytest.param(lambda: sol.modified_jones(SAMPLE[:3]), "three firm-years, fewer than four", id="three"),
        pytest.param(lambda: sol.modified_jones([]), "an empty sample", id="empty"),
        pytest.param(
            lambda: sol.modified_jones([*SAMPLE[:-1], {**SAMPLE[-1], "lag_assets": 0.0}]),
            "a firm-year with zero lagged assets",
            id="zero-lag",
        ),
        pytest.param(
            lambda: sol.modified_jones([*SAMPLE[:-1], {**SAMPLE[-1], "lag_assets": -5.0e8}]),
            "a firm-year with negative lagged assets",
            id="negative-lag",
        ),
        pytest.param(
            lambda: sol.modified_jones([*SAMPLE[:-1], {**SAMPLE[-1], "total_accruals": float("nan")}]),
            "a firm-year with NaN total accruals",
            id="nan",
        ),
        pytest.param(
            lambda: sol.modified_jones([*SAMPLE[:-1], {**SAMPLE[-1], "ppe": float("inf")}]),
            "a firm-year with infinite ppe",
            id="inf",
        ),
        pytest.param(
            lambda: sol.modified_jones([{**row, "ppe": 0.0} for row in SAMPLE]),
            "every firm-year with zero ppe, so a regressor is identically zero",
            id="rank-zero-column",
        ),
        pytest.param(
            lambda: sol.modified_jones([{**row, "d_receivables": row["d_revenue"]} for row in SAMPLE]),
            "a regressor that is identically zero: revenue change equals receivables change",
            id="rank-zero-diff",
        ),
    ],
)
def test_modified_jones_invalid_input_raises(bad: Callable[[], object], condition: str) -> None:
    must_raise(bad, condition)


# ---------------------------------------------------------------- Piotroski and Beneish


def test_piotroski_signals_match_the_definitions() -> None:
    st = FINAL
    t, t1, t2 = LATEST, PRIOR, PRIOR2
    roa = ex(t, "net_income") / ex(t1, "total_assets")
    roa_prev = ex(t1, "net_income") / ex(t2, "total_assets")
    cfo = ex(t, "cfo") / ex(t1, "total_assets")
    lev = ex(t, "long_term_debt") / ((ex(t, "total_assets") + ex(t1, "total_assets")) / 2)
    lev_prev = ex(t1, "long_term_debt") / ((ex(t1, "total_assets") + ex(t2, "total_assets")) / 2)
    cr, cr_prev = (
        ex(t, "current_assets") / ex(t, "current_liabilities"),
        ex(t1, "current_assets") / ex(t1, "current_liabilities"),
    )
    gm = (ex(t, "revenue") - ex(t, "cogs")) / ex(t, "revenue")
    gm_prev = (ex(t1, "revenue") - ex(t1, "cogs")) / ex(t1, "revenue")
    ato = ex(t, "revenue") / ex(t1, "total_assets")
    ato_prev = ex(t1, "revenue") / ex(t2, "total_assets")
    expected = (
        int(roa > 0),
        int(cfo > 0),
        int(roa > roa_prev),
        int(cfo > roa),
        int(lev < lev_prev),
        int(cr > cr_prev),
        int(ex(t, "shares_outstanding") <= ex(t1, "shares_outstanding")),
        int(gm > gm_prev),
        int(ato > ato_prev),
    )
    out = sol.piotroski_f_score(st, t)
    assert tuple(int(s) for s in out["signals"]) == expected, (
        "each of the nine signals must follow its definition exactly."
    )
    assert int(out["score"]) == sum(expected), "the score is the sum of the nine signals."


def test_piotroski_returns_nine_binary_signals() -> None:
    out = sol.piotroski_f_score(FINAL, LATEST)
    assert len(out["signals"]) == 9, "nine signals."
    assert all(int(s) in (0, 1) for s in out["signals"]), "each signal is 0 or 1."
    assert int(out["score"]) == sum(int(s) for s in out["signals"])


def test_piotroski_needs_two_preceding_years() -> None:
    two = {LATEST: FINAL[LATEST], PRIOR: FINAL[PRIOR]}
    must_raise(lambda: sol.piotroski_f_score(two, LATEST), "the F-score with only one preceding year in the statements")


def test_piotroski_zero_assets_two_years_back_raise() -> None:
    st = copy.deepcopy(FINAL)
    st[PRIOR2]["total_assets"] = 0.0
    must_raise(lambda: sol.piotroski_f_score(st, LATEST), "the F-score with zero total assets two years back")


def test_piotroski_ties_follow_the_strict_and_weak_inequalities() -> None:
    # Powers of two make every ratio exact: ROA(t-1) = ROA(t) = 0.0625 and leverage(t-1) = leverage(t) = 0.25.
    st = copy.deepcopy(FINAL)
    st[PRIOR2]["total_assets"] = 2048.0
    st[PRIOR]["total_assets"] = 1024.0
    st[PRIOR]["net_income"] = 128.0
    st[PRIOR]["long_term_debt"] = 384.0
    st[LATEST]["total_assets"] = 2048.0
    st[LATEST]["net_income"] = 64.0
    st[LATEST]["long_term_debt"] = 384.0
    st[LATEST]["shares_outstanding"] = st[PRIOR]["shares_outstanding"]
    signals = sol.piotroski_f_score(st, LATEST)["signals"]
    assert int(signals[2]) == 0, "signal 3 is strict: ROA equal to the previous year's scores 0."
    assert int(signals[4]) == 0, "signal 5 is strict: leverage equal to the previous year's scores 0."
    assert int(signals[6]) == 1, "signal 7 is weak: equal share counts (no issuance) score 1."


def test_beneish_variables_and_score_match_the_definitions() -> None:
    t, t1 = LATEST, PRIOR

    def g(end: str, k: str) -> float:
        return ex(end, k)

    gm, gm1 = (g(t, "revenue") - g(t, "cogs")) / g(t, "revenue"), (g(t1, "revenue") - g(t1, "cogs")) / g(t1, "revenue")
    expected = {
        "DSRI": (g(t, "receivables") / g(t, "revenue")) / (g(t1, "receivables") / g(t1, "revenue")),
        "GMI": gm1 / gm,
        "AQI": (1 - (g(t, "current_assets") + g(t, "ppe")) / g(t, "total_assets"))
        / (1 - (g(t1, "current_assets") + g(t1, "ppe")) / g(t1, "total_assets")),
        "SGI": g(t, "revenue") / g(t1, "revenue"),
        "DEPI": (g(t1, "depreciation") / (g(t1, "depreciation") + g(t1, "ppe")))
        / (g(t, "depreciation") / (g(t, "depreciation") + g(t, "ppe"))),
        "SGAI": (g(t, "sga") / g(t, "revenue")) / (g(t1, "sga") / g(t1, "revenue")),
        "LVGI": ((g(t, "current_liabilities") + g(t, "long_term_debt")) / g(t, "total_assets"))
        / ((g(t1, "current_liabilities") + g(t1, "long_term_debt")) / g(t1, "total_assets")),
        "TATA": (g(t, "net_income") - g(t, "cfo")) / g(t, "total_assets"),
    }
    out = sol.beneish_m_score(FINAL, t)
    for name, value in expected.items():
        assert close(out[name], value), f"Beneish variable {name} must follow its definition."
    m = BENEISH_INTERCEPT + sum(BENEISH_COEFFICIENTS[k] * v for k, v in expected.items())
    assert close(out["m_score"], m), (
        "M = intercept + sum of coefficient x variable, with the shared constants "
        "(UNCONFIRMED, see instance.BENEISH_STATUS)."
    )


@pytest.mark.parametrize(
    ("item", "period"),
    [
        ("depreciation", PRIOR),
        ("ppe", PRIOR),
        ("sga", LATEST),
        ("receivables", PRIOR),
        ("cfo", LATEST),
        ("current_liabilities", LATEST),
    ],
)
def test_beneish_raises_on_a_missing_item(item: str, period: str) -> None:
    st = copy.deepcopy(FINAL)
    del st[period][item]
    must_raise(lambda: sol.beneish_m_score(st, LATEST), f"beneish_m_score with {item} missing for {period}")


def test_beneish_zero_prior_receivables_raise() -> None:
    st = copy.deepcopy(FINAL)
    st[PRIOR]["receivables"] = 0.0
    must_raise(
        lambda: sol.beneish_m_score(st, LATEST), "beneish_m_score with zero receivables in the previous year (DSRI)"
    )


# ---------------------------------------------------------------- purity, silence, types and views


def call_every_public(
    facts: Mapping[str, Any], st: Mapping[str, Mapping[str, float]], sample: list[dict[str, float]]
) -> None:
    sol.standardize(facts, CUTS["latest_filing"])
    sol.dupont(st, LATEST)
    sol.roic(st, LATEST, 0.25)
    sol.current_ratio(st, LATEST)
    sol.gross_margin(st, LATEST)
    sol.debt_to_assets(st, LATEST)
    sol.days_sales_outstanding(st, LATEST)
    sol.accruals_cash_flow(st, LATEST)
    sol.accruals_balance_sheet(st, LATEST)
    sol.modified_jones(sample)
    sol.piotroski_f_score(st, LATEST)
    sol.beneish_m_score(st, LATEST)


def test_every_public_function_is_silent_and_pure() -> None:
    facts_before = copy.deepcopy(FACTS)
    st_before = copy.deepcopy(FINAL)
    sample_before = copy.deepcopy(SAMPLE)
    out, err = io.StringIO(), io.StringIO()
    with (
        warnings.catch_warnings(record=True) as caught,
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(err),
    ):
        warnings.simplefilter("always")
        call_every_public(FACTS, FINAL, SAMPLE)
    assert out.getvalue() == "", "functions must not print to standard output."
    assert err.getvalue() == "", "functions must not write to standard error."
    assert not caught, "functions must not warn on valid inputs."
    assert facts_before == FACTS, "standardize must not change the company-facts mapping it reads."
    assert st_before == FINAL, "the ratio functions must not change their statements."
    assert sample_before == SAMPLE, "modified_jones must not change its sample."


def test_invalid_inputs_do_not_print_or_mutate() -> None:
    st = copy.deepcopy(FINAL)
    before = copy.deepcopy(st)
    del st[LATEST]["cash"]
    snapshot = copy.deepcopy(st)
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(ValueError):
        sol.accruals_balance_sheet(st, LATEST)
    assert out.getvalue() == "", "a function that raises must not print either."
    assert st == snapshot, "a function that raises must not change its input."
    assert before != snapshot, "internal: the test must have removed the item."


def test_integer_observation_values_give_the_float_results() -> None:
    int_facts = copy.deepcopy(dict(FACTS))
    float_facts = copy.deepcopy(dict(FACTS))
    for _tag, entry in int_facts["facts"]["us-gaap"].items():
        for unit, obs_list in entry["units"].items():
            if unit != "USD":
                continue
            for obs in obs_list:
                obs["val"] = round(obs["val"])
    for _tag, entry in float_facts["facts"]["us-gaap"].items():
        for unit, obs_list in entry["units"].items():
            if unit != "USD":
                continue
            for obs in obs_list:
                obs["val"] = float(round(obs["val"]))
    assert_statements_equal(sol.standardize(int_facts), sol.standardize(float_facts), "integer observation values")


def test_integer_statements_give_the_float_ratios() -> None:
    ints = {end: {k: round(v) for k, v in row.items()} for end, row in FINAL.items()}
    floats = {end: {k: float(round(v)) for k, v in row.items()} for end, row in FINAL.items()}
    for name, call in RATIO_CALLS.items():
        a, b = call(floats, LATEST), call(ints, LATEST)
        if isinstance(a, dict):
            for key in a:
                assert np.allclose(np.asarray(b[key], dtype=float), np.asarray(a[key], dtype=float), rtol=FLOAT_RTOL), (
                    f"{name}: integer statements must give the float answer."
                )
        else:
            assert close(float(b), float(a)), f"{name}: integer statements must give the float answer."


def test_numpy_scalar_observations_give_the_same_standardization() -> None:
    np_facts = copy.deepcopy(dict(FACTS))
    for entry in np_facts["facts"]["us-gaap"].values():
        for obs_list in entry["units"].values():
            for obs in obs_list:
                if isinstance(obs.get("val"), float):
                    obs["val"] = np.float64(obs["val"])
    assert_statements_equal(sol.standardize(np_facts), FINAL, "NumPy float64 observation values")


def test_outputs_have_the_contract_types() -> None:
    d = sol.dupont(FINAL, LATEST)
    assert all(isinstance(v, float) for v in d.values()), "dupont values are floats."
    p = sol.piotroski_f_score(FINAL, LATEST)
    assert all(int(s) in (0, 1) for s in p["signals"]), "each Piotroski signal is 0 or 1."
    b = sol.beneish_m_score(FINAL, LATEST)
    assert all(isinstance(v, float) for v in b.values()), "Beneish values and m_score are floats."


def test_imports_only_numpy_and_standard_library() -> None:
    source = Path(sol.__file__).read_text(encoding="utf-8")
    allowed = set(sys.stdlib_module_names) | {"numpy", "__future__"}
    for node in ast.walk(ast.parse(source)):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names = [node.module]
        for name in names:
            assert name.split(".")[0] in allowed, (
                f"atlas/fundamentals may import only NumPy and the standard library, not {name}."
            )


# ---------------------------------------------------------------- edges the contract states

NEW_END = "2100-06-30"  # a period end that no generated filer reports


def shift_days(iso: str, days: int) -> str:
    return (dt.date.fromisoformat(iso) + dt.timedelta(days=days)).isoformat()


def same_result(a: Any, b: Any) -> bool:
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same_result(a[k], b[k]) for k in a)
    if isinstance(a, (tuple, list)):
        return len(a) == len(b) and all(same_result(x, y) for x, y in zip(a, b, strict=True))
    if isinstance(a, str):
        return bool(a == b)
    return close(float(a), float(b))


@pytest.mark.parametrize(("days", "kept"), [(349, False), (350, True), (380, True), (381, False)])
@pytest.mark.parametrize("name", ["dupont", "roic", "accruals_cash_flow", "accruals_balance_sheet"])
def test_previous_year_window_edges(name: str, days: int, kept: bool) -> None:
    # Contract: the previous year is the latest period end 350 to 380 days earlier. Its prior-year values are
    # copied from FINAL, so only the date of that period end differs between the cases.
    st = {LATEST: FINAL[LATEST], shift_days(LATEST, -days): FINAL[PRIOR]}
    if kept:
        assert same_result(RATIO_CALLS[name](st, LATEST), RATIO_CALLS[name](FINAL, LATEST)), (
            f"{name}: a period end {days} days earlier is the previous year (350 to 380 days, both included)."
        )
    else:
        must_raise(lambda: RATIO_CALLS[name](st, LATEST), f"{name} with the only earlier period end {days} days back")


@pytest.mark.parametrize("name", ["dupont", "roic", "accruals_cash_flow", "accruals_balance_sheet"])
def test_period_two_years_back_is_not_the_previous_year(name: str) -> None:
    st = {LATEST: FINAL[LATEST], PRIOR2: FINAL[PRIOR2]}
    must_raise(lambda: RATIO_CALLS[name](st, LATEST), f"{name} with only a period end two years back")


@pytest.mark.parametrize("name", ["dupont", "roic", "accruals_cash_flow", "accruals_balance_sheet"])
def test_previous_year_is_the_latest_period_end_in_the_window(name: str) -> None:
    # Contract: the previous year is the LATEST period end 350 to 380 days earlier. Here an earlier period end, 372 days
    # back, is also inside the window. Its balances are inflated, so picking it instead of the real prior year changes
    # the answer.
    earlier = shift_days(LATEST, -372)
    decoy = {k: (v * 1.5 if k in ("total_assets", "equity") else v) for k, v in FINAL[PRIOR].items()}
    st = {LATEST: FINAL[LATEST], PRIOR: FINAL[PRIOR], earlier: decoy}
    assert same_result(RATIO_CALLS[name](st, LATEST), RATIO_CALLS[name](FINAL, LATEST)), (
        f"{name}: of two period ends inside the 350 to 380 day window, the latest is the previous year."
    )


@pytest.mark.parametrize(
    ("days", "kept"), [(349, False), (350, True), (351, True), (379, True), (380, True), (381, False)]
)
def test_annual_flow_duration_window_edges(days: int, kept: bool) -> None:
    # Contract: an annual flow observation has form 10-K*, fp FY and 350 <= (end - start).days <= 380.
    obs = {
        "end": NEW_END,
        "start": shift_days(NEW_END, -days),
        "val": 123456.0,
        "filed": "2100-09-01",
        "form": "10-K",
        "fp": "FY",
        "accn": "edge-0001",
    }
    out = sol.standardize(with_obs(FACTS, "NetIncomeLoss", obs))
    if kept:
        assert NEW_END in out and close(out[NEW_END]["net_income"], 123456.0), (
            f"a 10-K flow of {days} days (fiscal year, 350 to 380 days) is annual and supplies net income."
        )
    else:
        assert NEW_END not in out or "net_income" not in out[NEW_END], (
            f"a 10-K flow of {days} days is outside the 350 to 380 day window: it is not annual."
        )


@pytest.mark.parametrize(
    ("name", "edit"),
    [
        ("current_ratio", {"current_assets": 1e300, "current_liabilities": 1e-300}),
        ("gross_margin", {"revenue": 1e-300, "cogs": -1e300}),
        ("debt_to_assets", {"long_term_debt": 1e300, "total_assets": 1e-300}),
        ("days_sales_outstanding", {"receivables": 1e300, "revenue": 1e-300}),
        ("dupont", {"revenue": 1e-300, "net_income": 1e300}),
        ("accruals_cash_flow", {"net_income": 1e300, "cfo": 0.0}),
    ],
)
def test_overflowing_quotient_raises(name: str, edit: dict[str, float]) -> None:
    # Contract: a non-finite result raises ValueError. The denominators here are finite and not zero.
    st = copy.deepcopy(FINAL)
    for item, value in edit.items():
        st[LATEST][item] = value
    if name == "accruals_cash_flow":
        st[LATEST]["total_assets"] = 1e-300
        st[PRIOR]["total_assets"] = 1e-300
    must_raise(lambda: RATIO_CALLS[name](st, LATEST), f"{name} whose quotient overflows to a non-finite value")


def test_overflowing_roic_raises() -> None:
    st = copy.deepcopy(FINAL)
    for end in (LATEST, PRIOR):
        st[end]["equity"], st[end]["long_term_debt"], st[end]["cash"] = 1e-300, 0.0, 0.0
    st[LATEST]["operating_income"] = 1e300
    must_raise(lambda: sol.roic(st, LATEST, 0.25), "roic whose quotient overflows to a non-finite value")


@pytest.mark.parametrize("field", ["end", "val", "filed", "form"])
def test_observation_without_a_named_field_raises(field: str) -> None:
    obs = {
        "end": LATEST,
        "val": 1.0,
        "filed": str(CUTS["latest_filing"]),
        "form": "10-K",
        "fp": "FY",
        "accn": "edge-0002",
    }
    obs.pop(field)
    must_raise(lambda: sol.standardize(with_obs(FACTS, "Assets", obs)), f"an observation without {field}")


PRIOR_ITEM_USE: dict[str, tuple[str, ...]] = {
    "dupont": ("total_assets", "equity"),
    "roic": ("equity", "long_term_debt", "cash"),
    "accruals_cash_flow": ("total_assets",),
    "accruals_balance_sheet": ("current_assets", "cash", "current_liabilities", "total_assets"),
    "piotroski_f_score": (
        "net_income",
        "total_assets",
        "long_term_debt",
        "current_assets",
        "current_liabilities",
        "revenue",
        "cogs",
        "shares_outstanding",
    ),
    "beneish_m_score": (
        "revenue",
        "receivables",
        "cogs",
        "current_assets",
        "ppe",
        "total_assets",
        "depreciation",
        "sga",
        "current_liabilities",
        "long_term_debt",
    ),
}


@pytest.mark.parametrize(("name", "item"), [(name, item) for name, items in PRIOR_ITEM_USE.items() for item in items])
def test_missing_previous_year_item_raises(name: str, item: str) -> None:
    # Contract: nothing is imputed; a function that needs a missing item raises ValueError.
    st = copy.deepcopy(FINAL)
    del st[PRIOR][item]
    must_raise(lambda: RATIO_CALLS[name](st, LATEST), f"{name} with {item} missing for the previous year")


def test_piotroski_missing_assets_two_years_back_raises() -> None:
    st = copy.deepcopy(FINAL)
    del st[PRIOR2]["total_assets"]
    must_raise(lambda: sol.piotroski_f_score(st, LATEST), "piotroski_f_score with total assets missing two years back")


def test_piotroski_strict_inequality_on_a_cfo_tie() -> None:
    # Powers of two: ROA(t) = 64 / 1024 = 0.0625; cfo(t) = 64 gives CFO/assets = 0.0625, a tie. Signal 4 is strict.
    st = copy.deepcopy(FINAL)
    st[PRIOR2]["total_assets"] = 2048.0
    st[PRIOR]["total_assets"] = 1024.0
    st[PRIOR]["net_income"] = 128.0
    st[PRIOR]["long_term_debt"] = 384.0
    st[LATEST]["total_assets"] = 2048.0
    st[LATEST]["net_income"] = 64.0
    st[LATEST]["long_term_debt"] = 384.0
    st[LATEST]["cfo"] = 64.0
    signals = sol.piotroski_f_score(st, LATEST)["signals"]
    assert int(signals[3]) == 0, "signal 4 is strict: CFO scaled equal to ROA scores 0."


def test_instant_observation_with_a_start_date_is_ignored() -> None:
    # Contract: an instant item is annual only when the observation has no start date; other observations are ignored.
    obs = {
        "end": NEW_END,
        "start": shift_days(NEW_END, -364),
        "val": 987654.0,
        "filed": "2100-09-01",
        "form": "10-K",
        "fp": "FY",
        "accn": "edge-0003",
    }
    out = sol.standardize(with_obs(FACTS, "Assets", obs))
    assert NEW_END not in out or "total_assets" not in out[NEW_END], (
        "an instant item with a start date is not annual: it must be ignored."
    )


def test_modified_jones_rejects_a_collinear_design_without_a_zero_column() -> None:
    # Contract: a rank-deficient design raises ValueError. Here ppe equals d_revenue - d_receivables, so the second and
    # third regressors are identical and no regressor is identically zero.
    collinear = [{**row, "ppe": row["d_revenue"] - row["d_receivables"]} for row in SAMPLE]
    must_raise(lambda: sol.modified_jones(collinear), "a rank-deficient design of two identical non-zero regressors")


PIOTROSKI_TIE_EDITS: list[tuple[str, int, dict[tuple[str, str], float]]] = [
    # (name, signal index, edits to the tie base). Each signal is strict (contract) and must score 0 at an exact tie.
    ("signal 1: ROA > 0 at zero profit", 0, {(LATEST, "net_income"): 0.0}),
    ("signal 2: CFO > 0 at zero cash flow", 1, {(LATEST, "cfo"): 0.0}),
    (
        "signal 6: current ratio strictly higher, equal at 2.0",
        5,
        {
            (PRIOR, "current_assets"): 2.0,
            (PRIOR, "current_liabilities"): 1.0,
            (LATEST, "current_assets"): 4.0,
            (LATEST, "current_liabilities"): 2.0,
        },
    ),
    (
        "signal 8: gross margin strictly higher, equal at 0.5",
        7,
        {(PRIOR, "revenue"): 8.0, (PRIOR, "cogs"): 4.0, (LATEST, "revenue"): 8.0, (LATEST, "cogs"): 4.0},
    ),
    (
        "signal 9: asset turnover strictly higher, equal at 1.0",
        8,
        {(PRIOR, "revenue"): 2048.0, (LATEST, "revenue"): 1024.0},
    ),
]


@pytest.mark.parametrize(
    ("name", "index", "edits"), PIOTROSKI_TIE_EDITS, ids=[e[0].split(":")[0] for e in PIOTROSKI_TIE_EDITS]
)
def test_piotroski_strict_signals_score_zero_at_an_exact_tie(
    name: str, index: int, edits: dict[tuple[str, str], float]
) -> None:
    # Powers of two keep every ratio exact: ROA(t) = 0.0625, ROA(t-1) = 0.0625, leverage 0.25 in both years.
    st = copy.deepcopy(FINAL)
    st[PRIOR2]["total_assets"] = 2048.0
    st[PRIOR]["total_assets"] = 1024.0
    st[PRIOR]["net_income"] = 128.0
    st[PRIOR]["long_term_debt"] = 384.0
    st[LATEST]["total_assets"] = 2048.0
    st[LATEST]["net_income"] = 64.0
    st[LATEST]["long_term_debt"] = 384.0
    st[LATEST]["cfo"] = 64.0
    for (end, item), value in edits.items():
        st[end][item] = value
    signals = sol.piotroski_f_score(st, LATEST)["signals"]
    assert int(signals[index]) == 0, f"{name}: the contract's inequality is strict, so an exact tie scores 0."


def test_as_of_before_any_filing_gives_an_empty_mapping() -> None:
    # Contract: a period end with no observation at or before as_of does not exist; nothing is raised.
    assert sol.standardize(FACTS, "1990-01-01") == {}, (
        "when no annual observation is filed by the cut-off, no period end exists and the mapping is empty."
    )


def test_flow_observation_without_a_start_date_is_ignored() -> None:
    # Contract: an annual flow observation has a start date with 350 <= (end - start).days <= 380.
    obs = {"end": NEW_END, "val": 555.0, "filed": "2100-09-01", "form": "10-K", "fp": "FY", "accn": "edge-0004"}
    out = sol.standardize(with_obs(FACTS, "NetIncomeLoss", obs))
    assert NEW_END not in out or "net_income" not in out[NEW_END], (
        "a flow observation without a start date is not annual, so it must be ignored."
    )


# ---------------------------------------------------------------- more of what the contract states


@pytest.mark.parametrize("unit", ["shares", "EUR"])
def test_money_tag_in_another_unit_is_not_read(unit: str) -> None:
    # Contract: money is in unit USD (share counts in shares). An observation of a money tag in another unit is ignored.
    obs = {"end": NEW_END, "val": 123.0, "filed": "2100-09-01", "form": "10-K", "fp": "FY", "accn": "edge-0005"}
    out = sol.standardize(with_obs(FACTS, "Assets", obs, unit=unit))
    assert NEW_END not in out or "total_assets" not in out[NEW_END], (
        f"an annual observation of Assets in unit {unit} is not a money observation: it must be ignored."
    )


def test_observation_without_an_accession_number_is_valid() -> None:
    # Contract: accn is optional and is used only as a tie-break (an absent accn counts as "").
    obs = {"end": NEW_END, "val": 123.0, "filed": "2100-09-01", "form": "10-K", "fp": "FY"}
    out = sol.standardize(with_obs(FACTS, "Assets", obs))
    assert NEW_END in out and close(out[NEW_END]["total_assets"], 123.0), (
        "an annual observation without accn is valid: accn is optional."
    )


@pytest.mark.parametrize(
    ("accn_10k", "val_10k", "accn_10ka", "val_10ka", "expected"),
    [
        pytest.param("edge-0010", 100.0, "edge-0009", 90.0, 100.0, id="10-K-has-larger-accn"),
        pytest.param("edge-0009", 100.0, "edge-0010", 90.0, 90.0, id="10-K-A-has-larger-accn"),
    ],
)
def test_same_day_amendment_is_decided_by_accn_not_form(
    accn_10k: str, val_10k: float, accn_10ka: str, val_10ka: float, expected: float
) -> None:
    # Contract: on one filing date the greatest (filed, accn or "") wins. The form string plays no part in the choice.
    # This is a fixed same-day case, so it is checked on every seed, not only on the seeds whose filer draws one.
    original = {"end": NEW_END, "val": val_10k, "filed": "2100-09-01", "form": "10-K", "fp": "FY", "accn": accn_10k}
    amended = {"end": NEW_END, "val": val_10ka, "filed": "2100-09-01", "form": "10-K/A", "fp": "FY", "accn": accn_10ka}
    f = with_obs(with_obs(FACTS, "Assets", original), "Assets", amended)
    assert close(sol.standardize(f)[NEW_END]["total_assets"], expected), (
        "two annual observations filed on one date: the greater accn is known; the form does not decide."
    )


def test_same_filing_date_without_accn_and_different_values_raise() -> None:
    # Contract: a tie on (filed, accn or "") with different values is inconsistent facts, and standardize raises.
    first = {"end": NEW_END, "val": 100.0, "filed": "2100-09-01", "form": "10-K", "fp": "FY"}
    second = {**first, "val": 90.0}
    f = with_obs(with_obs(FACTS, "Assets", first), "Assets", second)
    must_raise(lambda: sol.standardize(f), "two annual observations that tie on (filed, '') with different values")


def test_modified_jones_accepts_exactly_four_firm_years() -> None:
    # Contract: fewer than four firm-years raises; four is legal.
    rows = SAMPLE[:4]
    design, y = mj_design(rows)
    expected = np.linalg.lstsq(design, y, rcond=None)[0]
    out = sol.modified_jones(rows)
    assert np.allclose(np.asarray(out["coefficients"]), expected, rtol=FLOAT_RTOL, atol=FLOAT_ATOL), (
        "four firm-years is the least sample the contract allows: the coefficients are the OLS fit of those four rows."
    )


@pytest.mark.parametrize("value", [float("nan"), float("inf")], ids=["nan", "inf"])
@pytest.mark.parametrize("field", ["d_revenue", "d_receivables"])
def test_modified_jones_rejects_a_non_finite_regressor(field: str, value: float) -> None:
    # Contract: a non-finite value raises ValueError. The change in revenue and in receivables are regressor inputs too.
    bad = [dict(row) for row in SAMPLE]
    bad[1][field] = value
    must_raise(lambda: sol.modified_jones(bad), f"a non-finite {field} in one firm-year")


def test_piotroski_zero_assets_one_year_back_raise() -> None:
    # Contract: a zero denominator raises ValueError. ROA and the asset turnover divide by last year's total assets.
    st = copy.deepcopy(FINAL)
    st[PRIOR]["total_assets"] = 0.0
    must_raise(lambda: sol.piotroski_f_score(st, LATEST), "the F-score with zero total assets one year back")


PIOTROSKI_LATEST_ITEMS: tuple[str, ...] = (
    "net_income",
    "cfo",
    "long_term_debt",
    "total_assets",
    "current_assets",
    "current_liabilities",
    "revenue",
    "cogs",
    "shares_outstanding",
)


@pytest.mark.parametrize("item", PIOTROSKI_LATEST_ITEMS)
def test_piotroski_missing_latest_item_raises(item: str) -> None:
    # Contract: nothing is imputed; a function that needs a missing item raises ValueError.
    st = copy.deepcopy(FINAL)
    del st[LATEST][item]
    must_raise(lambda: sol.piotroski_f_score(st, LATEST), f"piotroski_f_score with {item} missing for the period end")


@pytest.mark.parametrize("name", ["dupont", "accruals_cash_flow", "accruals_balance_sheet"])
def test_zero_average_assets_raise_in_each_asset_ratio(name: str) -> None:
    # Contract: a zero denominator raises ValueError, whatever the numerator is.
    st = copy.deepcopy(FINAL)
    st[LATEST]["total_assets"] = -st[PRIOR]["total_assets"]  # the two-year average total assets is zero
    must_raise(lambda: RATIO_CALLS[name](st, LATEST), f"{name} with average total assets of zero")


def test_return_containers_are_the_contract_types() -> None:
    # Contract: coefficients and signals are tuples; the residual lists are lists, in sample order.
    fit = sol.modified_jones(SAMPLE)
    assert isinstance(fit["coefficients"], tuple), "modified_jones returns coefficients as the tuple (a1, a2, a3)."
    assert isinstance(fit["nondiscretionary"], list) and isinstance(fit["discretionary"], list), (
        "modified_jones returns nondiscretionary and discretionary as lists."
    )
    assert isinstance(sol.piotroski_f_score(FINAL, LATEST)["signals"], tuple), (
        "piotroski_f_score returns signals as the tuple (s1, ..., s9)."
    )
