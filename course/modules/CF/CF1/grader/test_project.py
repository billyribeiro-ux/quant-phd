"""Acceptance suite for the CF1 project: capbudget.py.

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with capbudget.py importable from the same directory. Warnings are failures, as in the browser.

Each test checks a property or a number against the specification on the project page and the CF1 lessons. A failure
names the property it checks and the idea to revisit; it never prints the expected value. Tolerances are stated in the
specification and used here: relative 1e-9 for flows and NPVs, 1e-7 for an IRR rate, 1e-12 for the Fisher identity,
and three sample standard errors for the Monte Carlo mean.
"""

from __future__ import annotations

import copy
import itertools
import json
import math
import os
import random
from collections.abc import Callable
from typing import Any

import pytest
from capbudget import (  # type: ignore[import-not-found]  # the learner's engine, not part of the grader
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
    pytest.fail(f"{condition}: the specification requires a ValueError that names the rule.")


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


def test_irr_finds_roots_across_the_whole_search_window() -> None:
    high = irr_roots([-1.0, 501.0])
    assert len(high) == 1 and abs(high[0] - 500.0) <= 1e-7, (
        "the search covers discount factors from 0.0001 to 10000: a root near rate 500 is inside it and must be found."
    )
    low = irr_roots([-5000.0, 1.0])
    assert len(low) == 1 and abs(low[0] - (-0.9998)) <= 1e-7, (
        "the search covers rates down to -0.9999: a root near rate -0.9998 is inside it and must be found."
    )


def test_irr_roots_are_ascending_and_distinct() -> None:
    roots = irr_roots([-100.0, 230.0, -132.0])
    assert roots == sorted(roots) and len(set(roots)) == len(roots), "return roots in ascending order, each once."


def test_irr_roots_have_zero_npv_on_the_instance() -> None:
    flows = after_tax_cash_flows(PROJECT)
    roots = irr_roots(flows)
    assert len(roots) == 1, "the instance's flow has one sign change, so exactly one IRR above -1 (Descartes' rule)."
    scale = sum(abs(cf) for cf in flows)
    assert abs(npv(roots[0], flows)) <= 1e-9 * scale, "the NPV at each returned root must be zero to 1e-9 of the flows."
    assert npv(roots[0] - 1e-6, flows) * npv(roots[0] + 1e-6, flows) < 0, (
        "the root must sit inside a sign change of the NPV: it is a true root, not a point where NPV only touches zero."
    )


@pytest.mark.parametrize("bad", [[-100.0], []], ids=["one-element", "empty"])
def test_irr_rejects_too_short_flows(bad: list[float]) -> None:
    must_raise(lambda: irr_roots(bad), "flows with fewer than two entries")


def test_irr_rejects_all_zero_flows() -> None:
    must_raise(lambda: irr_roots([0.0, 0.0, 0.0]), "flows that are all zero")


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


def test_discounted_payback_uses_discounted_flows() -> None:
    d1, d2 = 60.0 / 1.1, 60.0 / 1.21
    assert close(payback_period([-100.0, 60.0, 60.0], rate=0.1), 1.0 + (100.0 - d1) / d2), (
        "discounted payback divides each flow by (1 + rate) to the power t before accumulating."
    )


def test_discounted_payback_is_never_shorter_than_simple_payback() -> None:
    flows = after_tax_cash_flows(PROJECT)
    simple, discounted = payback_period(flows), payback_period(flows, rate=RATE)
    assert discounted >= simple, "discounting shrinks later flows, so discounted payback cannot be shorter."


@pytest.mark.parametrize("bad", [[0.0, 10.0], [5.0, -10.0]], ids=["zero-outlay", "positive-first"])
def test_payback_rejects_a_first_flow_that_is_not_an_outlay(bad: list[float]) -> None:
    must_raise(lambda: payback_period(bad), "a first flow that is not negative")


# ---------------------------------------------------------------- Fisher relation


def test_fisher_round_trip_is_exact() -> None:
    for real in (-0.5, -0.1, 0.0, 0.03, 0.07, 0.2):
        for pi in (-0.5, -0.02, 0.0, 0.03, 0.1):
            nominal = fisher_nominal(real, pi)
            assert close(1.0 + nominal, (1.0 + real) * (1.0 + pi), rel=1e-12, absolute=1e-12), (
                "the Fisher relation is exact: (1 + nominal) = (1 + real)(1 + inflation); no approximation."
            )


def test_fisher_with_zero_inflation_or_zero_real_rate() -> None:
    assert close(fisher_nominal(0.05, 0.0), 0.05, absolute=1e-15), (
        "with zero inflation the nominal rate is the real rate."
    )
    assert close(fisher_nominal(0.0, 0.03), 0.03, absolute=1e-15), (
        "with a zero real rate the nominal rate is inflation."
    )


@pytest.mark.parametrize(("real", "pi"), [(-1.0, 0.02), (0.02, -1.0)], ids=["real", "inflation"])
def test_fisher_rejects_rates_at_or_below_minus_one(real: float, pi: float) -> None:
    must_raise(lambda: fisher_nominal(real, pi), "a rate at or below -1")


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
    ],
)
def test_invalid_project_raises_a_named_error(change: dict[str, Any], condition: str) -> None:
    must_raise(lambda: after_tax_cash_flows(with_(PROJECT, **change)), condition)


def test_missing_field_raises_a_named_error() -> None:
    partial = {k: v for k, v in PROJECT.items() if k != "tax_rate"}
    must_raise(lambda: after_tax_cash_flows(partial), "a project without a tax rate")


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


def test_monte_carlo_mean_is_within_three_standard_errors_of_the_deterministic_npv() -> None:
    n = INST["mc_draws"]
    draws = npv_monte_carlo(PROJECT, RATE, n, SEED, INST["volatility"])
    mean = sum(draws) / n
    variance = sum((d - mean) ** 2 for d in draws) / (n - 1)
    standard_error = math.sqrt(variance / n)
    deterministic = npv(RATE, after_tax_cash_flows(PROJECT))
    assert abs(mean - deterministic) <= 3.0 * standard_error, (
        "the revenue multiplier has mean one, so the draws' mean estimates the deterministic NPV. A mean that is off "
        "by more than three standard errors usually means the lognormal correction -volatility**2/2 is missing."
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
