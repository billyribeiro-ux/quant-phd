"""Acceptance suite for the CF1 project: capbudget.py.

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with capbudget.py importable from the same directory. Warnings are failures, as in the browser.

Each test checks a property or a number against the specification on the project page and the CF1 lessons. A failure
names the property it checks and the idea to revisit; it never prints the expected value. Tolerances are stated in the
specification and used here: relative 1e-9 for flows and NPVs, with an absolute floor of 1e-9 cents (1e-6 cents in the
named checks), 1e-7 for an IRR rate, 1e-12 for the Fisher identity, and an exact affine identity for the Monte Carlo
mean (no statistical threshold).
"""

from __future__ import annotations

import ast
import copy
import inspect
import itertools
import json
import math
import os
import random
import sys
from collections.abc import Callable
from typing import Any

import capbudget  # type: ignore[import-not-found, unused-ignore]  # the learner's engine, read as source below
import pytest
from capbudget import (  # type: ignore[import-not-found, unused-ignore]  # the learner's engine, not part of the grader
    after_tax_cash_flows,
    fisher_nominal,
    irr_roots,
    npv,
    npv_monte_carlo,
    payback_period,
)
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

pytestmark = pytest.mark.filterwarnings("error")  # the specification: no function warns

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
PROJECT: dict[str, Any] = json.loads(INST["payload"])
RATE: float = INST["nominal_rate"]
INFLATION: float = PROJECT["inflation"]
TAX: float = PROJECT["tax_rate"]
LIFE: int = PROJECT["life"]
CAPEX: int = PROJECT["capex"]


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail with the violated condition unless call() raises ValueError."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError.")


def must_accept(call: Callable[[], Any], condition: str) -> Any:
    """Return call()'s value unless it raises ValueError, which fails the test with the condition that was valid."""
    try:
        return call()
    except ValueError:
        pytest.fail(f"{condition}: the specification accepts it, so a ValueError is wrong.")


def close(a: float, b: float, rel: float = 1e-9, absolute: float = 1e-9) -> bool:
    return math.isfinite(a) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))


def with_(project: dict[str, Any], **changes: Any) -> dict[str, Any]:
    out = copy.deepcopy(project)
    out.update(changes)
    return out


def sign_changes(flows: list[float]) -> int:
    signs = [1 if cf > 0 else -1 for cf in flows if cf != 0]
    return sum(1 for a, b in itertools.pairwise(signs) if a != b)


# ---------------------------------------------------------------- net present value


def test_npv_at_zero_rate_is_the_plain_sum() -> None:
    flows = after_tax_cash_flows(PROJECT)
    assert close(npv(0.0, flows), sum(flows)), (
        "npv(0, flows) must be the undiscounted sum of the flows (t = 0 is undiscounted)."
    )


def test_npv_two_flow_closed_form() -> None:
    assert close(npv(0.1, [-110.0, 121.0]), 0.0), (
        "a 10 percent rate on -110 now and +121 next year gives NPV zero: check the exponent of the discount factor."
    )


def test_npv_of_conventional_flow_strictly_falls_with_the_rate() -> None:
    flows = after_tax_cash_flows(PROJECT)
    assert sign_changes(flows) == 1 and flows[0] < 0 and all(cf > 0 for cf in flows[1:]), "precondition: conventional"
    rates = [0.01 * k for k in range(0, 51)]
    values = [npv(r, flows) for r in rates]
    assert all(b < a for a, b in itertools.pairwise(values)), (
        "NPV of a conventional flow must fall strictly as the rate rises; check the sign of the discount exponent."
    )


@pytest.mark.parametrize("bad", [-1.0, -2.0, float("nan"), float("inf")], ids=["minus-one", "below", "nan", "inf"])
def test_npv_rejects_rates_at_or_below_minus_one(bad: float) -> None:
    must_raise(lambda: npv(bad, [-1.0, 2.0]), "a rate that is not finite or is at or below -1")


def test_npv_rejects_empty_flows() -> None:
    must_raise(lambda: npv(0.1, []), "an empty list of flows")


def test_npv_keeps_a_zero_flow_in_its_time_index() -> None:
    assert close(npv(0.1, [-100.0, 0.0, 121.0]), 0.0), (
        "the sum runs over every t: a zero flow at t = 1 still takes its place, so -100 + 0 + 121 / 1.1 ** 2 is zero; "
        "dropping the zero moves 121 to t = 1 and gives 10."
    )


def test_npv_keeps_a_leading_zero_flow_in_its_time_index() -> None:
    assert close(npv(0.1, [0.0, 121.0]), 110.0), (
        "a zero flow at t = 0 is discounted by the exponent 0 and the flow 121 at t = 1 is discounted by 1.1: "
        "the NPV is 110."
    )


def test_npv_of_a_single_flow_is_that_flow() -> None:
    assert close(npv(0.5, [7.0]), 7.0), "a one-element list is valid: its NPV is its only flow, undiscounted at t = 0."


def test_npv_reads_a_rate_above_one_as_a_decimal_per_year() -> None:
    assert close(npv(2.0, [-100.0, 0.0, 300.0]), -100.0 + 300.0 / 9.0), (
        "every rate is a decimal per year, so a rate of 2.0 is 200 percent a year and the factor at t = 2 is "
        "1 / (1 + 2.0) ** 2; a rate of 2.0 must not be read as 2 percent."
    )


def test_npv_accepts_a_rate_just_above_minus_one() -> None:
    assert close(npv(-0.999, [-1.0, 2.0]), 1999.0), (
        "a rate of -0.999 is above -1 and therefore valid: -1 + 2 / (1 - 0.999) = 1999."
    )


# ---------------------------------------------------------------- internal rate of return


def test_irr_finds_both_roots_of_a_two_sign_change_flow() -> None:
    roots = irr_roots([-100.0, 230.0, -132.0])
    assert len(roots) == 2, "a flow with two sign changes, -100, +230, -132, has the two roots 0.1 and 0.2; list both."
    assert abs(roots[0] - 0.1) <= 1e-7 and abs(roots[1] - 0.2) <= 1e-7, (
        "the roots are 0.1 and 0.2 to 1e-7: solve for x = 1/(1+r) and convert back."
    )


def test_irr_single_root() -> None:
    roots = irr_roots([-100.0, 110.0])
    assert len(roots) == 1 and abs(roots[0] - 0.1) <= 1e-7, "a single outlay and a single inflow have one root, 0.1."


def test_irr_can_return_a_negative_root() -> None:
    x = (math.sqrt(41.0) - 1.0) / 2.0  # 10 x + 10 x^2 = 100 with x = 1 / (1 + r)
    roots = irr_roots([-100.0, 10.0, 10.0])
    assert len(roots) == 1 and abs(roots[0] - (1.0 / x - 1.0)) <= 1e-7, (
        "rates above -1 include negative rates; the root of -100 + 10/(1+r) + 10/(1+r)^2 is negative."
    )


def test_irr_no_root_when_every_inflow_is_positive() -> None:
    assert irr_roots([10.0, 10.0]) == [], "with only inflows the NPV never reaches zero: return an empty list."


def test_irr_does_not_report_a_tangent_root() -> None:
    # NPV(r) = -1 + 2/(1+r) - 1/(1+r)**2 = -(1/(1+r) - 1)**2 touches zero at r = 0 and never changes sign.
    assert irr_roots([-1.0, 2.0, -1.0]) == [], (
        "a rate where the NPV touches zero without changing sign is not an IRR root: report only sign changes."
    )


def test_irr_does_not_report_a_tangent_root_at_the_window_end() -> None:
    # NPV(r) = (x - 1e-4) ** 2 with x = 1 / (1 + r): a double root at x = 1e-4, the low end of the search window.
    assert irr_roots([1e-8, -2e-4, 1.0]) == [], (
        "a zero that touches the NPV at an end of the search window is not reported: report only sign changes "
        "between two samples inside the window."
    )


def test_irr_does_not_report_a_zero_at_the_low_end_of_the_window() -> None:
    # NPV(r) = x - 1e-4 with x = 1 / (1 + r): a sign-changing zero exactly at the low end of the window (rate 9999).
    assert irr_roots([-0.0001, 1.0]) == [], (
        "a zero exactly at the low end of the search window is not reported: report only sign changes between two "
        "samples inside the window."
    )


def test_irr_does_not_report_a_zero_at_the_high_end_of_the_window() -> None:
    # NPV(r) = -10000 + 1 / (1 + r): its zero is at x = 10000 exactly, the high end of the search window (rate -0.9999).
    assert irr_roots([-10000.0, 1.0]) == [], (
        "a zero exactly at the high end of the search window is not reported: report only sign changes between two "
        "samples inside the window."
    )


def test_irr_finds_roots_across_the_whole_search_window() -> None:
    high = irr_roots([-1.0, 501.0])
    assert len(high) == 1 and abs(high[0] - 500.0) <= 1e-7, (
        "the search covers discount factors from 0.0001 to 10000: a root near rate 500 is inside it and must be found."
    )
    low = irr_roots([-5000.0, 1.0])
    assert len(low) == 1 and abs(low[0] - (-0.9998)) <= 1e-7, (
        "the search covers rates down to -0.9999: a root near rate -0.9998 is inside it and must be found."
    )


def test_irr_finds_a_root_at_the_low_end_of_the_discount_factor_window() -> None:
    # NPV(r) = -1 + (1 / 1.5e-4) * x with x = 1 / (1 + r): its zero is at x = 1.5e-4, inside [0.0001, 10000].
    roots = irr_roots([-1.0, 1.0 / 1.5e-4])
    assert len(roots) == 1 and abs(roots[0] - (1.0 / 1.5e-4 - 1.0)) <= 1e-7, (
        "the search covers discount factors from 0.0001 upward: a root at discount factor 0.00015 (rate 6665.67) is "
        "inside it and must be found."
    )


def test_irr_does_not_report_a_root_outside_the_search_window() -> None:
    # Flows -1 and +1e5: NPV = -1 + 1e5 * x with x = 1 / (1 + r), so the root has x = 1e-5 (rate 99999), below 1e-4.
    # Flows -2e4 and +1: NPV = -2e4 + x, so the root has x = 2e4 (rate -0.99995), above 1e4.
    assert irr_roots([-1.0, 1e5]) == [], (
        "a root whose discount factor is below 0.0001 (rate above 9999) lies outside the search window: report only "
        "sign changes between two samples inside the window."
    )
    assert irr_roots([-2e4, 1.0]) == [], (
        "a root whose discount factor is above 10000 (rate below -0.9999) lies outside the search window: report only "
        "sign changes between two samples inside the window."
    )


def test_irr_finds_a_root_in_the_first_grid_interval() -> None:
    # NPV(r) = -0.000100005 + x with x = 1 / (1 + r): its zero is at x = 1.00005e-4, between the low end of the window
    # (1e-4) and the next sample, so the sign change lies in the first interval of the scan.
    roots = irr_roots([-0.000100005, 1.0])
    assert len(roots) == 1 and abs(roots[0] - (1.0 / 0.000100005 - 1.0)) <= 1e-7, (
        "a sign change between the low end of the search window and the next sample is inside the window and must be "
        "found: the root at discount factor 0.000100005 (rate 9998.5) lies in the first interval of the scan."
    )


def test_irr_finds_a_root_in_the_last_grid_interval() -> None:
    # NPV(r) = -9990 + x with x = 1 / (1 + r): its zero is at x = 9990, between the previous sample (about 9954) and
    # the high end of the window (10000), so the sign change lies in the last interval of the scan (rate -0.9998999).
    roots = irr_roots([-9990.0, 1.0])
    assert len(roots) == 1 and abs(roots[0] - (1.0 / 9990.0 - 1.0)) <= 1e-7, (
        "a sign change between the last sample before the high end of the search window and the high end is inside "
        "the window and must be found: the root at discount factor 9990 (rate -0.9998999) must be reported."
    )


def test_irr_roots_are_ascending_and_distinct() -> None:
    roots = irr_roots([-100.0, 230.0, -132.0])
    assert roots == sorted(roots) and len(set(roots)) == len(roots), "return roots in ascending order, each once."


def test_irr_roots_have_zero_npv_on_the_instance() -> None:
    flows = after_tax_cash_flows(PROJECT)
    roots = irr_roots(flows)
    assert len(roots) == 1, "the instance's flow has one sign change, so it should have exactly one IRR above -1."
    scale = sum(abs(cf) for cf in flows)
    assert abs(npv(roots[0], flows)) <= 1e-9 * scale, "the NPV at each returned root must be zero to 1e-9 of the flows."
    assert npv(roots[0] - 1e-6, flows) * npv(roots[0] + 1e-6, flows) < 0, (
        "the root must sit inside a sign change of the NPV: it is a true root, not a point where NPV only touches zero."
    )


@pytest.mark.parametrize("bad", [[-100.0], []], ids=["one-element", "empty"])
def test_irr_rejects_too_short_flows(bad: list[float]) -> None:
    must_raise(lambda: irr_roots(bad), "flows with fewer than two entries")


@pytest.mark.parametrize("zeros", [[0.0, 0.0, 0.0], [0.0, 0.0]], ids=["three-zeros", "two-zeros"])
def test_irr_rejects_all_zero_flows(zeros: list[float]) -> None:
    must_raise(lambda: irr_roots(zeros), "flows that are all zero")


def test_irr_accepts_some_zero_flows_when_not_all_are_zero() -> None:
    assert irr_roots([0.0, 5.0]) == [], (
        "only all-zero flows are refused: [0, 5] is a valid request, and its NPV never changes sign, so it has no root."
    )


def test_irr_zero_flow_keeps_its_place_in_the_time_index() -> None:
    roots = irr_roots([-100.0, 0.0, 110.0])
    assert len(roots) == 1 and abs(roots[0] - (math.sqrt(1.1) - 1.0)) <= 1e-7, (
        "a zero flow at t = 1 still counts in the time index: the NPV is -100 + 110 / (1 + r) ** 2, with root "
        "sqrt(1.1) - 1; dropping the zero gives the root 0.1 of the flows -100 and 110 alone."
    )


def test_irr_root_on_a_grid_sample_is_reported_once() -> None:
    # Grid sample k = 1000 of the window (x = 0.01, rate 99). The flows -x and +1 have NPV -x + x ** 1 in the discount
    # factor, zero at exactly that sample, so the root sits on a grid point and must be reported once, not twice.
    x = math.exp(math.log(1e-4) + (math.log(1e4) - math.log(1e-4)) * 1000 / 4000)
    roots = irr_roots([-x, 1.0])
    assert len(roots) == 1 and abs(roots[0] - (1.0 / x - 1.0)) <= 1e-7, (
        "a root that falls exactly on a sample of the search grid is one root: report it once, from the sign change "
        "around it."
    )


# ---------------------------------------------------------------- payback


def test_payback_on_whole_years() -> None:
    assert close(payback_period([-100.0, 50.0, 50.0, 50.0]), 2.0), "the outlay is recovered at the end of year 2."


def test_payback_interpolates_within_the_year() -> None:
    assert close(payback_period([-100.0, 60.0, 60.0]), 1.0 + 40.0 / 60.0), (
        "recovery happens 40/60 of the way through year 2: add the fraction of the year, not only the whole years."
    )


def test_payback_with_a_later_negative_is_still_the_first_crossing() -> None:
    assert close(payback_period([-100.0, 30.0, 30.0, 60.0]), 2.0 + 40.0 / 60.0), (
        "the first year with cumulative flow of zero or more fixes the payback; take the first crossing."
    )


def test_payback_ignores_flows_after_the_cut_off() -> None:
    a = payback_period([-100.0, 50.0, 50.0, 1000.0])
    b = payback_period([-100.0, 50.0, 50.0, -1000.0])
    assert close(a, 2.0) and close(b, 2.0), (
        "simple payback stops at the cut-off: flows after the year of recovery must not change it."
    )


def test_payback_never_recovered_is_infinite() -> None:
    assert payback_period([-100.0, 10.0, 10.0]) == math.inf, "an outlay never recovered gives math.inf."


def test_payback_counts_a_year_that_exactly_recovers_the_outlay_at_the_horizon() -> None:
    assert close(payback_period([-100.0, 50.0, 50.0]), 2.0), (
        "cumulative flow of exactly zero counts as recovered ('zero or more'), also in the last year of the horizon."
    )


def test_payback_accepts_a_discount_rate_just_above_minus_one() -> None:
    value = must_accept(
        lambda: payback_period([-100.0, 60.0, 60.0], -0.999),
        "a discount rate of -0.999 is above -1 and valid in a discounted payback request",
    )
    assert isinstance(value, float), "a discounted payback request with a valid rate returns a number of years."


def test_payback_accepts_a_first_flow_just_below_zero() -> None:
    value = must_accept(lambda: payback_period([-1e-9, 1.0]), "a first flow of -1e-9 cents is negative and valid")
    assert isinstance(value, float) and abs(value - 1e-9) <= 1e-15, (
        "the payback on the flows -1e-9 and +1 is (t - 1) + (-cumulative at t - 1) / flow at t = 0 + 1e-9 / 1.0 = 1e-9 "
        "years: a first flow only just below zero is an outlay, not a refused input."
    )


def test_payback_recovered_exactly_in_year_one() -> None:
    assert close(payback_period([-100.0, 100.0]), 1.0), "an outlay recovered at the end of year 1 gives payback 1."


def test_payback_at_zero_rate_is_simple_payback() -> None:
    flows = [-100.0, 60.0, 60.0]
    assert close(payback_period(flows, 0.0), payback_period(flows)), (
        "a rate of zero discounts nothing, so discounted payback at zero is simple payback."
    )


def test_discounted_payback_uses_discounted_flows() -> None:
    d1, d2 = 60.0 / 1.1, 60.0 / 1.21
    assert close(payback_period([-100.0, 60.0, 60.0], rate=0.1), 1.0 + (100.0 - d1) / d2), (
        "discounted payback divides each flow by (1 + rate) to the power t before accumulating."
    )


def test_discounted_payback_is_never_shorter_than_simple_payback() -> None:
    flows = after_tax_cash_flows(PROJECT)
    simple, discounted = payback_period(flows), payback_period(flows, rate=RATE)
    assert discounted >= simple, "discounting shrinks later flows, so discounted payback cannot be shorter."


def test_discounted_payback_is_infinite_when_only_the_undiscounted_flows_recover() -> None:
    # Undiscounted, the flows recover the outlay in year 2 (cumulative 10). At 20 percent, the discounted flows are
    # 41.67 and 41.67, cumulative -16.67: the outlay is never recovered, so the answer is math.inf.
    assert payback_period([-100.0, 50.0, 60.0], rate=0.2) == math.inf, (
        "discounted payback uses the discounted flows only: when they never recover the outlay the answer is math.inf, "
        "even though the undiscounted flows recover it."
    )


@pytest.mark.parametrize("bad", [[], [-100.0]], ids=["empty", "outlay-only"])
def test_payback_rejects_fewer_than_two_flows(bad: list[float]) -> None:
    must_raise(lambda: payback_period(bad), "a payback request with fewer than two flows (an outlay and an inflow)")


@pytest.mark.parametrize("bad", [[0.0, 10.0], [5.0, -10.0]], ids=["zero-outlay", "positive-first"])
def test_payback_rejects_a_first_flow_that_is_not_an_outlay(bad: list[float]) -> None:
    must_raise(lambda: payback_period(bad), "a first flow that is not negative")


@pytest.mark.parametrize("bad_rate", [-1.0, -2.0], ids=["minus-one", "below-minus-one"])
def test_payback_rejects_a_discount_rate_at_or_below_minus_one(bad_rate: float) -> None:
    must_raise(
        lambda: payback_period([-100.0, 60.0, 60.0], bad_rate),
        "a discount rate at or below -1 in a discounted payback request",
    )


# ---------------------------------------------------------------- Fisher relation


def test_fisher_round_trip_is_exact() -> None:
    for real in (-0.5, -0.1, 0.0, 0.03, 0.07, 0.2):
        for pi in (-0.5, -0.02, 0.0, 0.03, 0.1):
            nominal = fisher_nominal(real, pi)
            assert close(1.0 + nominal, (1.0 + real) * (1.0 + pi), rel=1e-12, absolute=1e-12), (
                "the Fisher relation is exact: (1 + nominal) = (1 + real)(1 + inflation); no approximation."
            )


def test_fisher_with_zero_inflation_or_zero_real_rate() -> None:
    assert close(fisher_nominal(0.05, 0.0), 0.05, rel=1e-12, absolute=1e-12), (
        "with zero inflation the nominal rate is the real rate."
    )
    assert close(fisher_nominal(0.0, 0.03), 0.03, rel=1e-12, absolute=1e-12), (
        "with a zero real rate the nominal rate is inflation."
    )


@pytest.mark.parametrize(
    ("real", "pi"),
    [(-1.0, 0.02), (0.02, -1.0), (-2.0, 0.02), (0.02, -2.0)],
    ids=["real-minus-one", "inflation-minus-one", "real-below-minus-one", "inflation-below-minus-one"],
)
def test_fisher_rejects_rates_at_or_below_minus_one(real: float, pi: float) -> None:
    must_raise(lambda: fisher_nominal(real, pi), "a rate at or below -1")


def test_fisher_accepts_inflation_just_above_minus_one() -> None:
    value = must_accept(lambda: fisher_nominal(0.02, -0.999), "an inflation rate of -0.999 is above -1 and valid")
    assert close(1.0 + value, 1.02 * 0.001, rel=1e-12, absolute=1e-12), (
        "with inflation -0.999 the nominal rate is (1 + real)(1 + inflation) - 1, here 1.02 * 0.001 - 1."
    )


def test_fisher_identity_holds_for_rates_with_many_decimals() -> None:
    # Nominal rates with more than nine decimals: rounding the nominal rate to nine decimals misses the identity.
    real, pi = 0.0123456789123, 0.0314159265358
    nominal = fisher_nominal(real, pi)
    assert close(1.0 + nominal, (1.0 + real) * (1.0 + pi), rel=1e-12, absolute=1e-12), (
        "the Fisher identity holds to a relative 1e-12 for every pair of rates, not only for rates with few decimals."
    )


def test_fisher_identity_holds_on_a_seeded_sweep() -> None:
    rng = random.Random(SEED)
    for _ in range(200):
        real, pi = rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)
        nominal = fisher_nominal(real, pi)
        assert close(1.0 + nominal, (1.0 + real) * (1.0 + pi), rel=1e-12, absolute=1e-12), (
            f"the Fisher identity is exact for real {real!r} and inflation {pi!r}; a nominal rate rounded to fewer "
            "digits does not satisfy it."
        )


def test_fisher_accepts_rates_just_above_minus_one() -> None:
    assert close(fisher_nominal(-0.999, 0.0), -0.999, rel=1e-12, absolute=1e-12), (
        "a real rate of -0.999 is above -1 and valid: with zero inflation the nominal rate is the real rate."
    )


def test_instance_real_rate_round_trips_to_the_nominal_rate() -> None:
    real = (1.0 + RATE) / (1.0 + INFLATION) - 1.0
    assert close(fisher_nominal(real, INFLATION), RATE, rel=1e-12, absolute=1e-12), (
        "the real rate implied by the nominal rate and inflation must map back to the nominal rate."
    )


# ---------------------------------------------------------------- after-tax cash flows


def test_flow_vector_has_an_outlay_then_one_flow_per_year() -> None:
    flows = after_tax_cash_flows(PROJECT)
    assert len(flows) == LIFE + 1, "index 0 is the outlay, then one flow for each year of life."
    assert flows[0] == -float(CAPEX), "the outlay at t = 0 is minus the capex, exactly."


def test_depreciation_shield_is_depreciation_times_tax_rate() -> None:
    flows = after_tax_cash_flows(with_(PROJECT, nwc_share=0.0))
    depreciation = CAPEX / LIFE
    for t in range(1, LIFE + 1):
        ebitda = PROJECT["revenue"][t - 1] - PROJECT["cash_costs"][t - 1]
        expected = ebitda * (1.0 - TAX) + TAX * depreciation
        assert close(flows[t], expected, rel=1e-9, absolute=1e-6), (
            f"year {t}: the after-tax flow must be EBITDA times (1 - tax rate) plus depreciation times the tax rate; "
            "the shield enters with a plus sign because depreciation lowers taxable income."
        )


def test_working_capital_investment_and_recovery_sum_to_zero() -> None:
    with_wc = after_tax_cash_flows(PROJECT)
    without = after_tax_cash_flows(with_(PROJECT, nwc_share=0.0))
    total = sum(a - b for a, b in zip(with_wc, without, strict=True))
    assert abs(total) <= 1e-6, (
        "working capital is invested and then fully recovered at the end of the life, so its flows sum to zero; "
        "the recovery at the last year is missing or wrong."
    )
    if LIFE >= 2:
        first = with_wc[1] - without[1]
        assert close(first, -PROJECT["nwc_share"] * PROJECT["revenue"][0], rel=1e-9, absolute=1e-6), (
            "the year-1 working-capital flow is minus the share of year-1 revenue, invested at the end of year 1."
        )


def test_single_year_project_has_no_working_capital() -> None:
    one = with_(PROJECT, life=1, revenue=[PROJECT["revenue"][0]], cash_costs=[PROJECT["cash_costs"][0]])
    flows = after_tax_cash_flows(one)
    expected = (one["revenue"][0] - one["cash_costs"][0]) * (1.0 - TAX) + TAX * CAPEX
    assert len(flows) == 2 and close(flows[1], expected, absolute=1e-6), (
        "with a one-year life, working capital is never held: it is invested and recovered in the same year."
    )


def test_working_capital_flow_in_each_year_is_minus_the_change_in_the_balance() -> None:
    with_wc = after_tax_cash_flows(PROJECT)
    without = after_tax_cash_flows(with_(PROJECT, nwc_share=0.0))

    def balance(t: int) -> float:
        return 0.0 if t == 0 or t == LIFE else PROJECT["nwc_share"] * PROJECT["revenue"][t - 1]

    for t in range(1, LIFE + 1):
        expected = -(balance(t) - balance(t - 1))
        assert close(with_wc[t] - without[t], expected, rel=1e-9, absolute=1e-6), (
            f"year {t}: the working-capital flow is minus the change in the balance; the balance is zero at the start "
            "and at the end of the life, and a share of revenue in between."
        )


def test_real_flows_are_deflated_year_by_year() -> None:
    nominal = after_tax_cash_flows(PROJECT)
    real = after_tax_cash_flows(PROJECT, real=True)
    assert real[0] == nominal[0], "the outlay at t = 0 is already in today's cents: deflation leaves it unchanged."
    for t in range(1, LIFE + 1):
        assert close(real[t], nominal[t] / (1.0 + INFLATION) ** t), (
            f"year {t}: a real flow is the nominal flow divided by (1 + inflation) to the power t."
        )


def test_real_flows_at_the_real_rate_equal_nominal_flows_at_the_nominal_rate() -> None:
    real_rate = (1.0 + RATE) / (1.0 + INFLATION) - 1.0
    real_npv = npv(real_rate, after_tax_cash_flows(PROJECT, real=True))
    nominal_npv = npv(RATE, after_tax_cash_flows(PROJECT))
    assert close(real_npv, nominal_npv, rel=1e-9, absolute=1e-6), (
        "the same project gives the same NPV in real and in nominal terms when each is discounted at its own rate; "
        "a real flow must not be discounted at the nominal rate."
    )


@pytest.mark.parametrize(
    ("change", "condition"),
    [
        pytest.param({"capex": 0}, "a zero capex", id="capex-zero"),
        pytest.param({"capex": -1000}, "a negative capex", id="capex-negative"),
        pytest.param(
            {"capex": 1000.0}, "a capex given as a float rather than an integer number of cents", id="capex-float"
        ),
        pytest.param({"life": 0, "revenue": [], "cash_costs": []}, "a life of zero years", id="life-zero"),
        pytest.param(
            {"revenue": PROJECT["revenue"][:-1]}, "revenue with the wrong number of years", id="revenue-length"
        ),
        pytest.param({"cash_costs": [-1.0, *PROJECT["cash_costs"][1:]]}, "a negative cash cost", id="cost-negative"),
        pytest.param(
            {"cash_costs": [-1e-9, *PROJECT["cash_costs"][1:]]},
            "a cash cost just below zero (-1e-9 cents)",
            id="cost-just-below-zero",
        ),
        pytest.param(
            {"revenue": [float("-inf"), *PROJECT["revenue"][1:]]},
            "a revenue that is minus infinity",
            id="revenue-minus-inf",
        ),
        pytest.param(
            {"cash_costs": [float("-inf"), *PROJECT["cash_costs"][1:]]},
            "a cash cost that is minus infinity",
            id="cost-minus-inf",
        ),
        pytest.param({"tax_rate": 1.0}, "a tax rate of 100 percent", id="tax-one"),
        pytest.param({"tax_rate": -0.5}, "a negative tax rate", id="tax-negative"),
        pytest.param({"nwc_share": 1.0}, "a working-capital share of 100 percent", id="share-one"),
        pytest.param({"nwc_share": -0.1}, "a negative working-capital share", id="share-negative"),
        pytest.param({"life": 2.5}, "a life that is not a whole number of years", id="life-fractional"),
        pytest.param(
            {"cash_costs": PROJECT["cash_costs"][:-1]}, "cash costs with the wrong number of years", id="cost-length"
        ),
        pytest.param({"revenue": [-5.0, *PROJECT["revenue"][1:]]}, "a negative revenue", id="revenue-negative"),
        pytest.param(
            {"revenue": [float("nan"), *PROJECT["revenue"][1:]]}, "a revenue that is not finite", id="revenue-nan"
        ),
        pytest.param(
            {"cash_costs": [float("inf"), *PROJECT["cash_costs"][1:]]}, "a cash cost that is not finite", id="cost-inf"
        ),
        pytest.param({"inflation": -1.0}, "inflation of -100 percent", id="inflation-minus-one"),
        pytest.param({"inflation": -1.5}, "inflation below -100 percent", id="inflation-below-minus-one"),
        pytest.param({"capex": True}, "a capex given as a boolean, not a number of cents", id="capex-bool"),
        pytest.param({"capex": "900000"}, "a capex given as text, not a number of cents", id="capex-text"),
        pytest.param({"life": -1, "revenue": [], "cash_costs": []}, "a negative life", id="life-negative"),
        pytest.param(
            {"revenue": [*PROJECT["revenue"], 1.0]}, "revenue with one entry more than the life", id="revenue-too-long"
        ),
        pytest.param(
            {"cash_costs": [*PROJECT["cash_costs"], 1.0]},
            "cash costs with one entry more than the life",
            id="cost-too-long",
        ),
        pytest.param({"tax_rate": 1.5}, "a tax rate above 100 percent", id="tax-above-one"),
        pytest.param({"nwc_share": 1.5}, "a working-capital share above 100 percent", id="share-above-one"),
        pytest.param(
            {"revenue": [float("inf"), *PROJECT["revenue"][1:]]}, "a revenue that is infinite", id="revenue-inf"
        ),
        pytest.param(
            {"cash_costs": [float("nan"), *PROJECT["cash_costs"][1:]]},
            "a cash cost that is not a number",
            id="cost-nan",
        ),
    ],
)
def test_invalid_project_raises_a_named_error(change: dict[str, Any], condition: str) -> None:
    must_raise(lambda: after_tax_cash_flows(with_(PROJECT, **change)), condition)


@pytest.mark.parametrize("field", ["capex", "life", "revenue", "cash_costs", "tax_rate", "nwc_share", "inflation"])
def test_missing_field_raises_a_named_error(field: str) -> None:
    partial = {k: v for k, v in PROJECT.items() if k != field}
    must_raise(lambda: after_tax_cash_flows(partial), f"a project without the field {field}")


def test_zero_revenue_and_zero_costs_are_valid_inputs() -> None:
    flows = after_tax_cash_flows(with_(PROJECT, revenue=[0.0] * LIFE, cash_costs=[0.0] * LIFE))
    assert len(flows) == LIFE + 1, "zero is a non-negative revenue and a non-negative cost: both are valid."


def test_capex_of_one_cent_is_a_valid_project() -> None:
    flows = after_tax_cash_flows(with_(PROJECT, capex=1))
    assert flows[0] == -1.0, "a positive whole number of cents, however small, is a valid outlay."


def test_working_capital_share_of_zero_is_valid() -> None:
    flows = after_tax_cash_flows(with_(PROJECT, nwc_share=0.0))
    assert len(flows) == LIFE + 1, (
        "a working-capital share of zero is valid: the lower bound of the share is inclusive."
    )


def test_tax_rate_just_below_zero_is_refused() -> None:
    must_raise(lambda: after_tax_cash_flows(with_(PROJECT, tax_rate=-1e-9)), "a tax rate just below zero (-1e-9)")


def test_working_capital_share_just_below_zero_is_refused() -> None:
    must_raise(
        lambda: after_tax_cash_flows(with_(PROJECT, nwc_share=-1e-9)), "a working-capital share just below zero (-1e-9)"
    )


def test_revenue_just_below_zero_is_refused() -> None:
    must_raise(
        lambda: after_tax_cash_flows(with_(PROJECT, revenue=[-1e-9, *PROJECT["revenue"][1:]])),
        "a revenue just below zero (-1e-9 cents)",
    )


def test_real_flows_are_deflated_under_negative_inflation() -> None:
    project = with_(PROJECT, inflation=-0.5)
    nominal = after_tax_cash_flows(project)
    real = after_tax_cash_flows(project, real=True)
    assert real[0] == nominal[0], "the outlay at t = 0 is unchanged by deflation, whatever the sign of inflation."
    for t in range(1, LIFE + 1):
        assert close(real[t], nominal[t] / (1.0 + project["inflation"]) ** t), (
            f"year {t}: with negative inflation a real flow is still the nominal flow divided by (1 + inflation) "
            "to the power t; the sign of inflation must not switch deflation off."
        )


def test_boundary_tax_and_share_values_just_inside_the_range_are_valid() -> None:
    assert len(after_tax_cash_flows(with_(PROJECT, tax_rate=0.0))) == LIFE + 1, "a tax rate of zero is valid."
    assert len(after_tax_cash_flows(with_(PROJECT, tax_rate=0.999))) == LIFE + 1, "a tax rate below 1 is valid."
    assert len(after_tax_cash_flows(with_(PROJECT, nwc_share=0.999))) == LIFE + 1, "a share below 1 is valid."


def test_inflation_just_above_minus_one_is_valid() -> None:
    real = after_tax_cash_flows(with_(PROJECT, inflation=-0.5), real=True)
    assert len(real) == LIFE + 1, "an inflation rate above -1 (here -50 percent) is valid."


def test_tax_credit_is_paid_when_ebitda_is_zero() -> None:
    # Zero revenue and cost: EBITDA is 0, so the tax is tax_rate * (0 - capex), a credit. The flow is tax_rate * capex.
    one = with_(PROJECT, life=1, revenue=[0.0], cash_costs=[0.0], nwc_share=0.0)
    flows = after_tax_cash_flows(one)
    assert close(flows[1], TAX * CAPEX, absolute=1e-6), (
        "with no EBITDA the depreciation loss is a tax credit, so the year's flow is positive: tax_rate times capex."
    )


def test_input_project_is_not_changed() -> None:
    before = copy.deepcopy(PROJECT)
    after_tax_cash_flows(PROJECT)
    npv_monte_carlo(PROJECT, RATE, 3, 1, 0.1)
    assert before == PROJECT, "the functions must not change their arguments; work on a copy."


def test_flow_list_arguments_are_not_changed() -> None:
    flows = after_tax_cash_flows(PROJECT)
    before = list(flows)
    npv(RATE, flows)
    irr_roots(flows)
    payback_period(flows)
    payback_period(flows, RATE)
    assert flows == before, "npv, irr_roots and payback_period must not change the flows they are given."


def test_functions_never_print(capsys: pytest.CaptureFixture[str]) -> None:
    flows = after_tax_cash_flows(PROJECT)
    after_tax_cash_flows(PROJECT, real=True)
    npv(RATE, flows)
    irr_roots([-100.0, 230.0, -132.0])
    payback_period(flows, RATE)
    fisher_nominal(0.05, INFLATION)
    npv_monte_carlo(PROJECT, RATE, 3, SEED, 0.1)
    assert capsys.readouterr().out == "", "no function prints; each returns its value for the caller to show."


def test_returned_lists_are_fresh_objects() -> None:
    first = after_tax_cash_flows(PROJECT)
    second = after_tax_cash_flows(PROJECT)
    assert first is not second and first == second, "each call returns a new list with the same flows."
    first.append(0.0)
    assert len(after_tax_cash_flows(PROJECT)) == LIFE + 1, "changing one returned list must not change the next call."
    roots = irr_roots([-100.0, 230.0, -132.0])
    roots.clear()
    assert len(irr_roots([-100.0, 230.0, -132.0])) == 2, "changing one returned list must not change the next call."
    draws = npv_monte_carlo(PROJECT, RATE, 3, 1, 0.1)
    assert draws is not npv_monte_carlo(PROJECT, RATE, 3, 1, 0.1), "each call returns a new list of draws."


# ---------------------------------------------------------------- Monte Carlo NPV


def test_monte_carlo_returns_one_npv_per_draw() -> None:
    draws = npv_monte_carlo(PROJECT, RATE, 25, SEED, INST["volatility"])
    assert len(draws) == 25 and all(isinstance(d, float) for d in draws), "return one float NPV for each draw."


def test_monte_carlo_with_zero_volatility_is_the_deterministic_npv() -> None:
    deterministic = npv(RATE, after_tax_cash_flows(PROJECT))
    draws = npv_monte_carlo(PROJECT, RATE, 10, SEED, 0.0)
    assert all(close(d, deterministic) for d in draws), (
        "with zero volatility every revenue multiplier is one, so every draw equals the deterministic NPV."
    )


def test_monte_carlo_draws_follow_the_seeded_gauss_stream() -> None:
    volatility = 0.2
    rng = random.Random(42)
    draws = npv_monte_carlo(PROJECT, RATE, 3, 42, volatility)
    for k, d in enumerate(draws, start=1):
        z = rng.gauss(0.0, 1.0)
        m = math.exp(volatility * z - volatility * volatility / 2.0)
        scaled = with_(PROJECT, revenue=[m * float(x) for x in PROJECT["revenue"]])
        expected = npv(RATE, after_tax_cash_flows(scaled))
        assert close(d, expected, rel=1e-9, absolute=1e-6), (
            f"draw {k}: take one gauss(0, 1) number per draw, in draw order, and scale every revenue by "
            "exp(volatility * z - volatility squared / 2)."
        )


def test_monte_carlo_is_reproducible_for_a_seed() -> None:
    first = npv_monte_carlo(PROJECT, RATE, 50, SEED, INST["volatility"])
    second = npv_monte_carlo(PROJECT, RATE, 50, SEED, INST["volatility"])
    assert first == second, "the same seed must give the same draws, in the same order."


def test_monte_carlo_changes_with_the_seed() -> None:
    a = npv_monte_carlo(PROJECT, RATE, 50, 1, 0.2)
    b = npv_monte_carlo(PROJECT, RATE, 50, 2, 0.2)
    assert a != b, "different seeds must give different draws when volatility is positive."


def test_monte_carlo_accepts_exactly_two_draws() -> None:
    draws = npv_monte_carlo(PROJECT, RATE, 2, SEED, INST["volatility"])
    assert len(draws) == 2, "two draws is the smallest valid request: a standard error needs two draws."


def test_monte_carlo_mean_is_the_affine_identity_on_the_same_draws() -> None:
    # NPV is affine in the multiplier m: NPV(m) = a + b * m, with a the NPV at m = 0 and b the slope. The mean of the
    # draws is therefore a + b * mean(m), exactly, for the multipliers the specification gives from the same stream.
    n = INST["mc_draws"]
    volatility = INST["volatility"]
    draws = npv_monte_carlo(PROJECT, RATE, n, SEED, volatility)
    rng = random.Random(SEED)
    multipliers = [math.exp(volatility * rng.gauss(0.0, 1.0) - volatility * volatility / 2.0) for _ in range(n)]
    at_zero = npv(RATE, after_tax_cash_flows(with_(PROJECT, revenue=[0.0] * LIFE)))
    at_one = npv(RATE, after_tax_cash_flows(PROJECT))
    expected_mean = at_zero + (at_one - at_zero) * (sum(multipliers) / n)
    assert close(sum(draws) / n, expected_mean, absolute=1e-6), (
        "the draws' mean must equal a + b times the mean of the specified multipliers, where a and b come from the "
        "flows at multiplier zero and one. Check that each draw scales every revenue by the multiplier and that the "
        "multiplier is exp(volatility * z - volatility squared / 2) for the z of that draw."
    )


@pytest.mark.parametrize(
    ("args", "condition"),
    [
        pytest.param((1, 0, 0.1), "one draw", id="one-draw"),
        pytest.param((10, 0, -0.1), "negative volatility", id="negative-volatility"),
    ],
)
def test_monte_carlo_rejects_invalid_arguments(args: tuple[int, int, float], condition: str) -> None:
    n_draws, seed, volatility = args
    must_raise(lambda: npv_monte_carlo(PROJECT, RATE, n_draws, seed, volatility), condition)


def test_monte_carlo_refuses_zero_draws() -> None:
    must_raise(lambda: npv_monte_carlo(PROJECT, RATE, 0, SEED, 0.1), "zero draws: a request needs at least two")


def test_monte_carlo_refuses_negative_draws() -> None:
    must_raise(
        lambda: npv_monte_carlo(PROJECT, RATE, -5, SEED, 0.1),
        "a negative number of draws: a request needs at least two",
    )


@pytest.mark.parametrize("bad_rate", [-1.0, -2.0], ids=["minus-one", "below-minus-one"])
def test_monte_carlo_refuses_a_rate_at_or_below_minus_one(bad_rate: float) -> None:
    must_raise(
        lambda: npv_monte_carlo(PROJECT, bad_rate, 3, SEED, 0.1),
        "a rate at or below -1 in the Monte Carlo request",
    )


def test_monte_carlo_accepts_a_rate_just_above_minus_one() -> None:
    draws = must_accept(
        lambda: npv_monte_carlo(PROJECT, -0.999, 3, SEED, 0.1),
        "a rate of -0.999 is above -1 and valid in a Monte Carlo request",
    )
    assert isinstance(draws, list) and len(draws) == 3, "a valid request returns one NPV for each of its draws."


def test_monte_carlo_refuses_a_volatility_just_below_zero() -> None:
    must_raise(lambda: npv_monte_carlo(PROJECT, RATE, 3, SEED, -1e-12), "a volatility just below zero (-1e-12)")


def test_engine_imports_only_the_standard_library() -> None:
    tree = ast.parse(inspect.getsource(capbudget))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules.append(("." * node.level) + (node.module or ""))
    outside = sorted({m for m in modules if m.startswith(".") or m.split(".")[0] not in sys.stdlib_module_names})
    assert not outside, (
        "the engine uses the Python standard library only and does not import instance.py; "
        f"these imports are not standard library: {', '.join(outside)}."
    )
