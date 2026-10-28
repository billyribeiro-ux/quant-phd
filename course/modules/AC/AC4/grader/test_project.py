"""Acceptance suite for the AC4 project: the budget and variance engine (budget_engine.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your budget_engine.py next to this file. Warnings are failures, as in the browser.

Every expected value is computed here, from the case's own numbers, by the rules of the project specification. The
oracle below is written independently of any solution: it uses exact fractions and states each rule once. A failure
names the property it checks and the idea to revisit; it never prints the expected value.
"""

from __future__ import annotations

import ast
import contextlib
import copy
import io
import json
import math
import os
import sys
import types
from collections.abc import Callable, Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

import budget_engine as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
CASE: dict[str, Any] = json.loads(make_instance(SEED)["payload"])
PRODUCTS: list[dict[str, Any]] = CASE["products"]
FIXED: int = CASE["fixed_overhead_cents"]
INPUT_PRICE: int = CASE["input_price_cents"]
ACTUAL_INPUTS: int = CASE["actual_inputs_used"]
FUNCTIONS: tuple[str, ...] = ("master_budget", "flexible_budget", "variance_decomposition")
VARIANCES: tuple[str, ...] = ("sales_price", "sales_volume", "sales_mix", "efficiency")
# The case as generated, before any test runs. The purity test builds its own case from PRISTINE through fresh(), and
# test_shared_case_is_unchanged_by_the_suite compares CASE with PRISTINE at the end of the run.
PRISTINE: dict[str, Any] = copy.deepcopy(CASE)


def fresh(**changes: Any) -> dict[str, Any]:
    """A deep copy of the case as generated, with top-level fields replaced."""
    case = copy.deepcopy(PRISTINE)
    case.update(changes)
    return case


def with_products(products: list[dict[str, Any]], **changes: Any) -> dict[str, Any]:
    case = fresh(**changes)
    case["products"] = products
    return case


def half_up(x: Fraction) -> int:
    """The nearest whole cent, halves up, for a non-negative fraction."""
    return math.floor(x + Fraction(1, 2))


def oracle(case: Mapping[str, Any]) -> dict[str, Any]:
    """Every expected value of the specification, from the case's numbers, in exact arithmetic."""
    s = case["input_price_cents"]
    fixed = case["fixed_overhead_cents"]
    aq = case["actual_inputs_used"]
    rows = case["products"]
    budget_units = sum(r["budget_units"] for r in rows)
    budget_revenue = sum(r["budget_units"] * r["budget_price_cents"] for r in rows)
    budget_variable = sum(r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows)
    master_profit = budget_revenue - budget_variable - fixed
    actual_total = sum(r["actual_units"] for r in rows)
    flex_rev_exact = Fraction(actual_total * budget_revenue, budget_units)
    flex_var_exact = Fraction(actual_total * budget_variable, budget_units)
    flex_profit = half_up(flex_rev_exact) - half_up(flex_var_exact) - fixed
    flex_profit_exact = flex_rev_exact - flex_var_exact - fixed
    actual_mix_margin = sum(
        r["actual_units"] * (r["budget_price_cents"] - r["standard_inputs_per_unit"] * s) for r in rows
    )
    standard_for_actual = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in rows)
    actual_profit = sum(r["actual_units"] * r["actual_price_cents"] for r in rows) - s * aq - fixed
    price = sum((r["actual_price_cents"] - r["budget_price_cents"]) * r["actual_units"] for r in rows)
    variances = {
        "sales_price": price,
        "sales_volume": flex_profit - master_profit,
        "sales_mix": actual_mix_margin - fixed - flex_profit,
        "efficiency": s * (standard_for_actual - aq),
    }
    return {
        "master_profit": master_profit,
        "budget_units": budget_units,
        "budget_revenue": budget_revenue,
        "budget_variable": budget_variable,
        "flex_profit": flex_profit,
        "flex_profit_exact": flex_profit_exact,
        "flex_revenue": half_up(flex_rev_exact),
        "flex_variable": half_up(flex_var_exact),
        "exact_mix": (actual_mix_margin - fixed) - flex_profit_exact,
        "variances": variances,
        "total": actual_profit - master_profit,
    }


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError: the grader checks the exception type."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError.")


def decomposition_matches(case: Mapping[str, Any]) -> None:
    expected = oracle(case)
    got = sol.variance_decomposition(case)
    assert set(got) == {*VARIANCES, "total"}, (
        "variance_decomposition must return the keys sales_price, sales_volume, sales_mix, efficiency and total."
    )
    for key in VARIANCES:
        assert got[key] == expected["variances"][key], (
            f"{key}: check the rule that defines this variance in the specification."
        )
    assert got["total"] == expected["total"], "total: the total is the actual profit less the master budget profit."


# ---------------------------------------------------------------- interface and instance


def test_module_defines_the_three_functions() -> None:
    for name in FUNCTIONS:
        assert callable(getattr(sol, name, None)), f"budget_engine.py must define {name}."


def test_signatures_match_the_contract() -> None:
    import inspect

    assert list(inspect.signature(sol.master_budget).parameters) == ["case"], (
        "master_budget must take the single argument case."
    )
    assert list(inspect.signature(sol.flexible_budget).parameters) == ["case", "actual_units"], (
        "flexible_budget must take the two arguments case and actual_units."
    )
    assert list(inspect.signature(sol.variance_decomposition).parameters) == ["case"], (
        "variance_decomposition must take the single argument case."
    )


def test_instance_case_is_a_valid_case() -> None:
    assert len(PRODUCTS) == 3, "make_instance must generate three products."
    assert sum(r["budget_units"] for r in PRODUCTS) > 0, (
        "make_instance must generate a positive total of budgeted units."
    )
    for row in PRODUCTS:
        for field in (
            "budget_units",
            "budget_price_cents",
            "standard_inputs_per_unit",
            "actual_units",
            "actual_price_cents",
        ):
            assert type(row[field]) is int, f"{field} must be a whole number."
        assert row["actual_units"] >= 1 and row["budget_price_cents"] > row["standard_inputs_per_unit"] * INPUT_PRICE, (
            "make_instance must give each product one or more actual units and a budget price above its input cost."
        )


def test_instance_is_deterministic_and_labelled() -> None:
    again = json.loads(make_instance(SEED)["payload"])
    assert again == CASE, "make_instance must return the same case for the same seed."
    assert "SIMULATED" in make_instance(SEED)["label"], "every instance is labelled SIMULATED."


def test_only_standard_library_imports() -> None:
    source = Path(sol.__file__).read_text(encoding="utf-8")
    names = {a.name.split(".")[0] for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Import) for a in n.names}
    names |= {
        (n.module or "").split(".")[0]
        for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.ImportFrom) and n.level == 0
    }
    outside = sorted(name for name in names if name and name not in sys.stdlib_module_names)
    assert not outside, "budget_engine.py must use the standard library only."
    assert "instance" not in names and "test_project" not in names, "budget_engine.py must not import a grader file."


# ---------------------------------------------------------------- master budget


@pytest.mark.parametrize("row", PRODUCTS, ids=lambda r: r["name"])
def test_master_units_by_product(row: dict[str, Any]) -> None:
    assert sol.master_budget(CASE)["units"][row["name"]] == row["budget_units"], (
        "master_budget: units by product must equal each product's budgeted units."
    )


@pytest.mark.parametrize("row", PRODUCTS, ids=lambda r: r["name"])
def test_master_revenue_by_product(row: dict[str, Any]) -> None:
    expected = row["budget_units"] * row["budget_price_cents"]
    assert sol.master_budget(CASE)["revenue_cents"][row["name"]] == expected, (
        "master_budget: revenue by product must be budgeted units times budgeted price."
    )


@pytest.mark.parametrize("row", PRODUCTS, ids=lambda r: r["name"])
def test_master_variable_cost_by_product(row: dict[str, Any]) -> None:
    expected = row["budget_units"] * row["standard_inputs_per_unit"] * INPUT_PRICE
    assert sol.master_budget(CASE)["variable_cost_cents"][row["name"]] == expected, (
        "master_budget: variable cost by product must be budgeted units times standard inputs times input price."
    )


def test_master_totals_and_profit() -> None:
    got = sol.master_budget(CASE)
    expected = oracle(CASE)
    assert got["total_units"] == expected["budget_units"], (
        "master_budget: total units must be the sum of the budgeted units."
    )
    assert got["total_revenue_cents"] == expected["budget_revenue"], (
        "master_budget: total revenue must be the sum of the product revenues."
    )
    assert got["total_variable_cost_cents"] == expected["budget_variable"], (
        "master_budget: total variable cost must be the sum of the product variable costs."
    )
    assert got["fixed_cost_cents"] == FIXED, "master_budget: fixed cost must equal the fixed overhead in the case."
    assert got["profit_cents"] == expected["master_profit"], (
        "budgeted profit is revenue less variable cost less fixed overhead."
    )


def test_master_ignores_the_actual_period() -> None:
    changed = copy.deepcopy(CASE)
    for row in changed["products"]:
        row["actual_units"] += 37
        row["actual_price_cents"] += 11
    changed["actual_inputs_used"] += 500
    assert sol.master_budget(changed) == sol.master_budget(CASE), "the master budget is built from budget fields only."


def test_master_returns_fresh_objects() -> None:
    first = sol.master_budget(CASE)
    second = sol.master_budget(CASE)
    assert first == second and first is not second, (
        "master_budget: repeated calls must return equal results as separate objects."
    )
    first["units"].clear()
    assert sol.master_budget(CASE)["units"], "a returned object must not share state with the next call."


# ---------------------------------------------------------------- flexible budget


def test_flexed_at_actual_total_matches_oracle() -> None:
    total = sum(r["actual_units"] for r in PRODUCTS)
    expected = oracle(CASE)
    got = sol.flexible_budget(CASE, total)
    assert got["units"] == total, "flexible_budget: units must equal the actual total passed in."
    assert got["revenue_cents"] == expected["flex_revenue"], "revenue flexes at the budgeted mix, to the nearest cent."
    assert got["variable_cost_cents"] == expected["flex_variable"], "variable cost flexes at the budgeted mix."
    assert got["fixed_cost_cents"] == FIXED, "flexible_budget: fixed cost must equal the fixed overhead in the case."
    assert got["profit_cents"] == expected["flex_profit"], (
        "flexible_budget: profit at the actual total must be revenue less variable cost less fixed overhead."
    )


def test_flexed_at_budgeted_total_reproduces_the_master_budget() -> None:
    budget_total = sum(r["budget_units"] for r in PRODUCTS)
    flexed = sol.flexible_budget(CASE, budget_total)
    master = sol.master_budget(CASE)
    assert flexed["revenue_cents"] == master["total_revenue_cents"], (
        "flexible_budget at the budgeted total: revenue must equal the master budget's total revenue."
    )
    assert flexed["variable_cost_cents"] == master["total_variable_cost_cents"], (
        "flexible_budget at the budgeted total: variable cost must equal the master budget's total variable cost."
    )
    assert flexed["profit_cents"] == master["profit_cents"], (
        "at the budgeted volume the flexed budget is the master budget."
    )


def test_flexed_profit_is_revenue_less_variable_less_fixed() -> None:
    flexed = sol.flexible_budget(CASE, 777)
    assert (
        flexed["profit_cents"] == flexed["revenue_cents"] - flexed["variable_cost_cents"] - flexed["fixed_cost_cents"]
    ), "flexible_budget: profit must be revenue less variable cost less fixed overhead."


def test_flexed_zero_units_leaves_only_fixed_overhead() -> None:
    flexed = sol.flexible_budget(CASE, 0)
    assert flexed["revenue_cents"] == 0 and flexed["variable_cost_cents"] == 0, (
        "flexible_budget with zero units: revenue and variable cost must both be zero."
    )
    assert flexed["profit_cents"] == -FIXED, "with no units the flexed profit is the fixed overhead, negative."


def test_flexed_budget_returns_integer_cents() -> None:
    flexed = sol.flexible_budget(CASE, 1234)
    for key in ("revenue_cents", "variable_cost_cents", "fixed_cost_cents", "profit_cents"):
        assert type(flexed[key]) is int, f"{key} must be whole cents (int), not a fraction or a float."


@pytest.mark.parametrize("seed", range(50))
def test_flexed_amounts_round_half_up_on_other_seeds(seed: int) -> None:
    case = json.loads(make_instance(seed)["payload"])
    total = sum(r["actual_units"] for r in case["products"])
    expected = oracle(case)
    got = sol.flexible_budget(case, total)
    assert got["revenue_cents"] == expected["flex_revenue"], (
        "flexible_budget: revenue at the actual total must round half up to the nearest cent."
    )
    assert got["variable_cost_cents"] == expected["flex_variable"], (
        "flexible_budget: variable cost at the actual total must round half up to the nearest cent."
    )
    assert got["profit_cents"] == expected["flex_profit"], (
        "the flexed profit is the rounded revenue less the rounded variable cost, less fixed overhead."
    )


def test_exact_half_cent_rounds_up() -> None:
    # Budgeted units: one at 1001 cents, one at 0 cents. At one unit in total, revenue is 1001 / 2 = 500.5 cents.
    rows = [
        {
            "name": "Half",
            "budget_units": 1,
            "budget_price_cents": 1001,
            "standard_inputs_per_unit": 0,
            "actual_units": 1,
            "actual_price_cents": 1001,
        },
        {
            "name": "Zero",
            "budget_units": 1,
            "budget_price_cents": 0,
            "standard_inputs_per_unit": 0,
            "actual_units": 0,
            "actual_price_cents": 0,
        },
    ]
    case = with_products(rows, actual_inputs_used=0)
    assert sol.flexible_budget(case, 1)["revenue_cents"] == 501, "a half cent must round up, not down."
    assert oracle(case)["flex_revenue"] == 501, "the test oracle must round a half cent up."
    decomposition_matches(case)


def test_exact_half_cent_in_variable_cost_rounds_up() -> None:
    # Budgeted variable cost 2 cents over 4 budgeted units: at one unit in total it flexes to 1/2 cent, which rounds up.
    rows = [
        {
            "name": "Cord",
            "budget_units": 2,
            "budget_price_cents": 10,
            "standard_inputs_per_unit": 1,
            "actual_units": 1,
            "actual_price_cents": 10,
        },
        {
            "name": "Free",
            "budget_units": 2,
            "budget_price_cents": 0,
            "standard_inputs_per_unit": 0,
            "actual_units": 0,
            "actual_price_cents": 0,
        },
    ]
    case = with_products(rows, input_price_cents=1, actual_inputs_used=1)
    assert sol.flexible_budget(case, 1)["variable_cost_cents"] == 1, (
        "a half cent of variable cost must round up, not down."
    )
    assert oracle(case)["flex_variable"] == 1, "the test oracle must round a half cent of variable cost up."
    decomposition_matches(case)


def test_flexed_variable_cost_below_half_a_cent_rounds_down() -> None:
    # Budgeted variable cost 1 cent over 3 budgeted units: one unit flexes to 1/3 of a cent, which rounds down to 0.
    rows = [
        {
            "name": "Pen",
            "budget_units": 1,
            "budget_price_cents": 0,
            "standard_inputs_per_unit": 1,
            "actual_units": 1,
            "actual_price_cents": 0,
        },
        {
            "name": "Ink",
            "budget_units": 2,
            "budget_price_cents": 0,
            "standard_inputs_per_unit": 0,
            "actual_units": 0,
            "actual_price_cents": 0,
        },
    ]
    case = with_products(rows, input_price_cents=1, actual_inputs_used=1)
    assert sol.flexible_budget(case, 1)["variable_cost_cents"] == 0, (
        "a third of a cent of variable cost must round down, not up."
    )
    assert oracle(case)["flex_variable"] == 0, "the test oracle must round a third of a cent of variable cost down."
    decomposition_matches(case)


# ---------------------------------------------------------------- the four variances and the total


def test_four_variances_and_total_match_oracle() -> None:
    decomposition_matches(CASE)


def test_reconciliation_is_exact() -> None:
    got = sol.variance_decomposition(CASE)
    parts = got["sales_price"] + got["sales_volume"] + got["sales_mix"] + got["efficiency"]
    assert parts == got["total"], "the four variances must sum to the total profit variance with no residual."


def test_variances_are_whole_cents() -> None:
    got = sol.variance_decomposition(CASE)
    for key in (*VARIANCES, "total"):
        assert type(got[key]) is int, f"{key} must be an int in cents."


def test_master_budget_values_are_integers() -> None:
    # Equality alone would accept 1000.0 for 1000, so the type of every amount and unit count is checked.
    got = sol.master_budget(CASE)
    values = [
        *got["units"].values(),
        *got["revenue_cents"].values(),
        *got["variable_cost_cents"].values(),
        got["total_units"],
        got["total_revenue_cents"],
        got["total_variable_cost_cents"],
        got["fixed_cost_cents"],
        got["profit_cents"],
    ]
    for value in values:
        assert type(value) is int, (
            "master_budget: every amount must be whole cents and every unit count a whole number."
        )


@pytest.mark.parametrize("seed", range(50))
def test_mix_is_within_one_cent_of_the_exact_fraction(seed: int) -> None:
    # Each rounding moves a flexed amount by at most half a cent, and an exact half cent always moves up, so the two
    # moves cannot differ by a full cent.
    case = json.loads(make_instance(seed)["payload"])
    got = sol.variance_decomposition(case)
    assert abs(Fraction(got["sales_mix"]) - oracle(case)["exact_mix"]) < 1, (
        "the flexed profit is taken to whole cents, so the mix differs from the exact fraction by less than one cent."
    )


def test_price_variance_is_favourable_when_price_rises() -> None:
    raised = copy.deepcopy(CASE)
    raised["products"][0]["actual_price_cents"] += 100
    before = sol.variance_decomposition(CASE)["sales_price"]
    after = sol.variance_decomposition(raised)["sales_price"]
    assert after - before == 100 * raised["products"][0]["actual_units"], (
        "a price rise must move the price variance by its units."
    )


def test_price_variance_is_unfavourable_when_every_price_falls() -> None:
    lowered = copy.deepcopy(CASE)
    for row in lowered["products"]:
        row["actual_price_cents"] = row["budget_price_cents"] - 50
    units = sum(r["actual_units"] for r in lowered["products"])
    got = sol.variance_decomposition(lowered)["sales_price"]
    assert got == -50 * units, (
        "every price below budget is an unfavourable price variance, the shortfall for each unit sold."
    )


def test_efficiency_is_positive_when_fewer_inputs_are_used() -> None:
    saved = copy.deepcopy(CASE)
    standard = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in saved["products"])
    saved["actual_inputs_used"] = standard - 100
    got = sol.variance_decomposition(saved)["efficiency"]
    assert got == 100 * INPUT_PRICE, "using fewer inputs than the standard allows is favourable, so positive."


def test_efficiency_is_negative_when_more_inputs_are_used() -> None:
    wasted = copy.deepcopy(CASE)
    standard = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in wasted["products"])
    wasted["actual_inputs_used"] = standard + 100
    assert sol.variance_decomposition(wasted)["efficiency"] == -100 * INPUT_PRICE, (
        "efficiency: using more inputs than the standard allows must give a negative variance."
    )


def test_efficiency_is_zero_at_the_standard_quantity() -> None:
    exact = copy.deepcopy(CASE)
    exact["actual_inputs_used"] = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in exact["products"])
    assert sol.variance_decomposition(exact)["efficiency"] == 0, (
        "efficiency: at exactly the standard quantity the variance must be zero."
    )


def test_all_variances_are_zero_when_actuals_equal_budget() -> None:
    same = copy.deepcopy(CASE)
    for row in same["products"]:
        row["actual_units"] = row["budget_units"]
        row["actual_price_cents"] = row["budget_price_cents"]
    same["actual_inputs_used"] = sum(r["standard_inputs_per_unit"] * r["budget_units"] for r in same["products"])
    got = sol.variance_decomposition(same)
    assert got["sales_volume"] == 0 and got["sales_mix"] == 0 and got["efficiency"] == 0 and got["total"] == 0, (
        "with actuals equal to budget, volume, mix, efficiency and total must all be zero."
    )


def test_mix_is_zero_when_the_actual_mix_equals_the_budgeted_mix() -> None:
    scaled = copy.deepcopy(CASE)
    for row in scaled["products"]:
        row["actual_units"] = 2 * row["budget_units"]
    scaled["actual_inputs_used"] = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in scaled["products"])
    got = sol.variance_decomposition(scaled)
    assert got["sales_mix"] == 0, "the same mix at a different total volume has no mix variance."
    assert got["sales_volume"] == oracle(scaled)["variances"]["sales_volume"], (
        "sales_volume: must equal the oracle's volume variance at the scaled total."
    )


def test_two_product_shift_to_lower_margin_is_unfavourable() -> None:
    rows = copy.deepcopy(PRODUCTS[:2])
    margins = [r["budget_price_cents"] - r["standard_inputs_per_unit"] * INPUT_PRICE for r in rows]
    low = min(range(2), key=lambda i: margins[i])
    for i, row in enumerate(rows):
        row["actual_units"] = row["budget_units"] * (3 if i == low else 1)
    case = with_products(rows, actual_inputs_used=sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in rows))
    got = sol.variance_decomposition(case)
    assert got["sales_mix"] == oracle(case)["variances"]["sales_mix"], (
        "sales_mix: must equal the oracle's mix variance for the shifted case."
    )
    if margins[0] == margins[1]:
        # Equal budgeted margins m: the exact flexed revenue and variable cost differ by AT*m, an integer, so their
        # whole-cent roundings differ by that same integer, and the whole-cent flexed profit equals the exact one.
        # The mix is therefore zero.
        assert got["sales_mix"] == 0, (
            "with equal budgeted margins, shifting volume between the two has no mix variance."
        )
    else:
        assert got["sales_mix"] < 0, "with two products, volume moved to the lower budgeted margin is unfavourable."


def test_two_product_shift_to_higher_margin_is_favourable() -> None:
    # Explicit products, so the sign does not depend on the seed: margins 5400 and 8000 cents at 200 cents an input.
    rows = [
        {
            "name": "Alpha",
            "budget_units": 500,
            "budget_price_cents": 6_000,
            "standard_inputs_per_unit": 3,
            "actual_units": 500,
            "actual_price_cents": 6_000,
        },
        {
            "name": "Beta",
            "budget_units": 500,
            "budget_price_cents": 9_000,
            "standard_inputs_per_unit": 5,
            "actual_units": 1_500,
            "actual_price_cents": 9_000,
        },
    ]
    case = with_products(rows, input_price_cents=200, actual_inputs_used=3 * 500 + 5 * 1_500)
    got = sol.variance_decomposition(case)
    assert got["sales_mix"] == oracle(case)["variances"]["sales_mix"], (
        "sales_mix: must equal the oracle's mix variance for the shift to the higher margin."
    )
    assert got["sales_mix"] > 0, "volume moved to the higher budgeted margin is favourable, so the mix is positive."


def test_three_products_with_equal_margins_have_no_mix_variance() -> None:
    # Each budgeted margin is 1000 cents: price = 200 x standard + 1000. The actual units differ from the budget.
    rows = [
        {
            "name": "Alpha",
            "budget_units": 100,
            "budget_price_cents": 1_400,
            "standard_inputs_per_unit": 2,
            "actual_units": 150,
            "actual_price_cents": 1_400,
        },
        {
            "name": "Beta",
            "budget_units": 200,
            "budget_price_cents": 1_600,
            "standard_inputs_per_unit": 3,
            "actual_units": 50,
            "actual_price_cents": 1_600,
        },
        {
            "name": "Gamma",
            "budget_units": 300,
            "budget_price_cents": 1_800,
            "standard_inputs_per_unit": 4,
            "actual_units": 400,
            "actual_price_cents": 1_800,
        },
    ]
    case = with_products(rows, input_price_cents=200, actual_inputs_used=2 * 150 + 3 * 50 + 4 * 400)
    got = sol.variance_decomposition(case)
    assert got["sales_mix"] == 0, "with equal budgeted margins no shift of units between products changes profit."
    assert got["sales_mix"] == oracle(case)["variances"]["sales_mix"], "sales_mix: must equal the oracle's value."


def test_price_change_on_an_unsold_product_has_no_price_variance() -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["actual_units"] = 0
    rows[0]["actual_price_cents"] = rows[0]["budget_price_cents"] + 700
    case = with_products(rows)
    got = sol.variance_decomposition(case)["sales_price"]
    assert got == sum((r["actual_price_cents"] - r["budget_price_cents"]) * r["actual_units"] for r in rows), (
        "sales_price: a product with no actual units contributes nothing to the price variance."
    )
    decomposition_matches(case)


def test_volume_variance_is_favourable_when_more_units_are_sold() -> None:
    more = copy.deepcopy(CASE)
    for row in more["products"]:
        row["actual_units"] = 2 * row["budget_units"]
    got = sol.variance_decomposition(more)["sales_volume"]
    assert got == oracle(more)["variances"]["sales_volume"], "sales_volume: must equal the oracle's volume variance."
    assert got > 0, "selling more units than budgeted, at the budgeted mix, is a favourable volume variance."


def test_volume_variance_is_unfavourable_when_fewer_units_are_sold() -> None:
    fewer = copy.deepcopy(CASE)
    for row in fewer["products"]:
        row["actual_units"] = row["budget_units"] // 2
    got = sol.variance_decomposition(fewer)["sales_volume"]
    assert got == oracle(fewer)["variances"]["sales_volume"], "sales_volume: must equal the oracle's volume variance."
    assert got < 0, "selling fewer units than budgeted, at the budgeted mix, is an unfavourable volume variance."


def test_one_budgeted_unit_in_total_is_a_valid_budget() -> None:
    row = {
        "name": "Only",
        "budget_units": 1,
        "budget_price_cents": 9_000,
        "standard_inputs_per_unit": 2,
        "actual_units": 1,
        "actual_price_cents": 9_100,
    }
    case = with_products([row], actual_inputs_used=2)
    assert sol.master_budget(case)["total_units"] == 1, "one budgeted unit in total is a valid budget, not an error."
    decomposition_matches(case)


def test_flexed_amount_below_half_a_cent_rounds_down() -> None:
    # Budgeted revenue 3 cents over 9 budgeted units: one unit flexes to 1/3 of a cent, which rounds down to 0.
    rows = [
        {
            "name": "Pen",
            "budget_units": 3,
            "budget_price_cents": 1,
            "standard_inputs_per_unit": 0,
            "actual_units": 1,
            "actual_price_cents": 1,
        },
        {
            "name": "Ink",
            "budget_units": 6,
            "budget_price_cents": 0,
            "standard_inputs_per_unit": 0,
            "actual_units": 0,
            "actual_price_cents": 0,
        },
    ]
    case = with_products(rows, actual_inputs_used=0)
    assert sol.flexible_budget(case, 1)["revenue_cents"] == 0, "a third of a cent must round down, not up."
    assert oracle(case)["flex_revenue"] == 0, "the test oracle must round a third of a cent down."
    decomposition_matches(case)


@pytest.mark.parametrize("field", ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"))
def test_zero_case_amount_is_a_valid_case(field: str) -> None:
    case = fresh(**{field: 0})
    assert sol.master_budget(case)["profit_cents"] == oracle(case)["master_profit"], (
        "master_budget: zero is a valid value for this case field."
    )
    decomposition_matches(case)


@pytest.mark.parametrize(
    "field",
    ("budget_price_cents", "standard_inputs_per_unit", "actual_price_cents", "actual_units"),
)
def test_zero_product_amount_is_a_valid_case(field: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0][field] = 0
    decomposition_matches(with_products(rows))


# ---------------------------------------------------------------- edge cases


def test_single_product_has_no_mix_variance() -> None:
    row = copy.deepcopy(PRODUCTS[0])
    case = with_products([row], actual_inputs_used=max(0, row["standard_inputs_per_unit"] * row["actual_units"] - 40))
    got = sol.variance_decomposition(case)
    assert got["sales_mix"] == 0, "with one product the mix cannot change."
    decomposition_matches(case)


def test_zero_actual_units_everywhere() -> None:
    rows = copy.deepcopy(PRODUCTS)
    for row in rows:
        row["actual_units"] = 0
    case = with_products(rows, actual_inputs_used=0)
    got = sol.variance_decomposition(case)
    assert got["sales_price"] == 0 and got["efficiency"] == 0 and got["sales_mix"] == 0, (
        "with no actual units, sales_price, efficiency and sales_mix must all be zero."
    )
    assert got["sales_volume"] == -FIXED - oracle(case)["master_profit"], (
        "sales_volume: with no output the volume variance must be the flexed profit less the master profit."
    )
    assert got["total"] == -FIXED - oracle(case)["master_profit"], (
        "total: with no output the total must be the actual profit less the master budget profit."
    )


def test_inputs_used_with_no_output() -> None:
    rows = copy.deepcopy(PRODUCTS)
    for row in rows:
        row["actual_units"] = 0
    case = with_products(rows, actual_inputs_used=250)
    assert sol.variance_decomposition(case)["efficiency"] == -250 * INPUT_PRICE, "inputs with no output are wasted."


def test_product_with_no_budgeted_units() -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows.append(
        {
            "name": "Launch",
            "budget_units": 0,
            "budget_price_cents": 7_000,
            "standard_inputs_per_unit": 3,
            "actual_units": 120,
            "actual_price_cents": 6_900,
        }
    )
    case = with_products(rows, actual_inputs_used=CASE["actual_inputs_used"] + 360)
    decomposition_matches(case)
    assert sol.master_budget(case)["units"]["Launch"] == 0, (
        "master_budget: a product with zero budgeted units must report zero units."
    )


# ---------------------------------------------------------------- every seed of the grader


@pytest.mark.parametrize("seed", range(50))
def test_every_grader_seed_reconciles_exactly(seed: int) -> None:
    case = json.loads(make_instance(seed)["payload"])
    decomposition_matches(case)
    got = sol.variance_decomposition(case)
    assert sum(got[k] for k in VARIANCES) == got["total"], "reconciliation must hold on every instance, exactly."


# ---------------------------------------------------------------- failure behaviour


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("field", ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"))
def test_missing_case_field_raises_value_error(name: str, field: str) -> None:
    case = fresh()
    del case[field]
    must_raise(_call_for(name, case), f"{name}: a case without {field}")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_negative_units_raise_value_error(name: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["budget_units"] = -1
    call = (
        (lambda: sol.flexible_budget(with_products(rows), 10))
        if name == "flexible_budget"
        else (lambda: getattr(sol, name)(with_products(rows)))
    )
    must_raise(call, "a negative budgeted unit count")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_float_money_raises_value_error(name: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["budget_price_cents"] = float(rows[0]["budget_price_cents"])
    call = (
        (lambda: sol.flexible_budget(with_products(rows), 10))
        if name == "flexible_budget"
        else (lambda: getattr(sol, name)(with_products(rows)))
    )
    must_raise(call, "money given as a float")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("field", ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"))
def test_boolean_input_raises_value_error(name: str, field: str) -> None:
    # A bool is an int in Python, so True would otherwise pass as one cent or one unit.
    case = fresh(**{field: True})
    must_raise(_call_for(name, case), f"{name}: {field} given as a boolean, where a whole number is required")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_zero_budgeted_units_raise_value_error(name: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    for row in rows:
        row["budget_units"] = 0
    call = (
        (lambda: sol.flexible_budget(with_products(rows), 10))
        if name == "flexible_budget"
        else (lambda: getattr(sol, name)(with_products(rows)))
    )
    must_raise(call, "a budget with no budgeted units")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_duplicate_product_names_raise_value_error(name: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[1]["name"] = rows[0]["name"]
    case = with_products(rows)
    call = (lambda: sol.flexible_budget(case, 10)) if name == "flexible_budget" else (lambda: getattr(sol, name)(case))
    must_raise(call, f"{name}: two products with the same name")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_empty_product_name_raises_value_error(name: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["name"] = ""
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product with an empty name")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_empty_product_list_raises_value_error(name: str) -> None:
    case = with_products([])
    call = (lambda: sol.flexible_budget(case, 10)) if name == "flexible_budget" else (lambda: getattr(sol, name)(case))
    must_raise(call, f"{name}: a case with no products")


def test_negative_actual_units_argument_raises_value_error() -> None:
    must_raise(lambda: sol.flexible_budget(CASE, -1), "a negative actual unit count")


def test_float_actual_units_argument_raises_value_error() -> None:
    wrong_type: Any = 100.0  # a float is not a whole number, whatever its value
    must_raise(lambda: sol.flexible_budget(CASE, wrong_type), "a float unit count")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("field", ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"))
@pytest.mark.parametrize("offset", (0.5, 0.0))
def test_case_field_not_a_whole_number_raises_value_error(name: str, field: str, offset: float) -> None:
    # offset 0.5 is a fraction; offset 0.0 is an integral float. Both are not whole numbers as the page states.
    case = fresh(**{field: CASE[field] + offset})
    must_raise(_call_for(name, case), f"{name}: {field} given as the non-whole number {CASE[field] + offset!r}")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize(
    "field",
    ("budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"),
)
@pytest.mark.parametrize("offset", (0.5, 0.0))
def test_product_field_not_a_whole_number_raises_value_error(name: str, field: str, offset: float) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0][field] = rows[0][field] + offset
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product's {field} given as a non-whole number")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize(
    "field",
    ("budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"),
)
def test_product_field_boolean_raises_value_error(name: str, field: str) -> None:
    # A bool is an int in Python, so True would otherwise pass as one unit or one cent.
    rows = copy.deepcopy(PRODUCTS)
    rows[0][field] = True
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product's {field} given as a boolean")


@pytest.mark.parametrize("offset", (0.5, 0.0))
def test_non_whole_actual_units_argument_raises_value_error(offset: float) -> None:
    total = sum(r["actual_units"] for r in PRODUCTS)
    must_raise(
        lambda: sol.flexible_budget(CASE, total + offset),
        "flexible_budget: an actual unit count that is not a whole number",
    )


def test_boolean_actual_units_argument_raises_value_error() -> None:
    must_raise(lambda: sol.flexible_budget(CASE, True), "flexible_budget: a boolean given as the actual unit count")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_negative_input_price_raises_value_error(name: str) -> None:
    must_raise(_call_for(name, fresh(input_price_cents=-1)), f"{name}: a negative input_price_cents")


def _call_for(name: str, case: Mapping[str, Any]) -> Callable[[], object]:
    """The call to make for a function, on a case: flexible_budget gets the actual total of 10 units."""
    if name == "flexible_budget":
        return lambda: sol.flexible_budget(case, 10)
    return lambda: getattr(sol, name)(case)


@pytest.mark.parametrize("name", FUNCTIONS)
def test_negative_fixed_overhead_raises_value_error(name: str) -> None:
    must_raise(_call_for(name, fresh(fixed_overhead_cents=-1)), f"{name}: a negative fixed overhead")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_negative_actual_inputs_raises_value_error(name: str) -> None:
    must_raise(_call_for(name, fresh(actual_inputs_used=-1)), f"{name}: a negative count of input units used")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("field", ("actual_units", "actual_price_cents"))
def test_negative_actual_product_field_raises_value_error(name: str, field: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0][field] = -1
    must_raise(_call_for(name, with_products(rows)), f"{name}: a negative {field} on a product")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize(
    "field",
    ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"),
)
def test_missing_product_field_raises_value_error(name: str, field: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    del rows[0][field]
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product without its {field} field")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_negative_budget_price_raises_value_error(name: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["budget_price_cents"] = -1
    must_raise(_call_for(name, with_products(rows)), f"{name}: a negative budget_price_cents on a product")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_negative_standard_inputs_raises_value_error(name: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["standard_inputs_per_unit"] = -1
    must_raise(_call_for(name, with_products(rows)), f"{name}: a negative standard_inputs_per_unit on a product")


def test_non_mapping_case_raises_value_error() -> None:
    not_a_case: Any = []
    must_raise(lambda: sol.master_budget(not_a_case), "a case that is a list")


# ---------------------------------------------------------------- one isolated refusal per condition


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("bad", ([], "case", None, list(CASE.items())), ids=["list", "text", "none", "pairs"])
def test_case_that_is_not_a_mapping_raises_value_error(name: str, bad: Any) -> None:
    must_raise(_call_for(name, bad), f"{name}: a case that is not a mapping")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_case_that_is_a_read_only_mapping_is_accepted(name: str) -> None:
    # The page says "a mapping", so a read-only mapping that is not a dict must give the dict's results.
    view = types.MappingProxyType(copy.deepcopy(CASE))
    if name == "flexible_budget":
        total = sum(r["actual_units"] for r in PRODUCTS)
        assert sol.flexible_budget(view, total) == sol.flexible_budget(CASE, total), (
            "flexible_budget: a case given as a read-only mapping must give the same result as the dict."
        )
    else:
        assert getattr(sol, name)(view) == getattr(sol, name)(CASE), (
            f"{name}: a case given as a read-only mapping must give the same result as the dict."
        )


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize(
    "bad",
    ({r["name"]: r for r in PRODUCTS}, "Alpha", tuple(copy.deepcopy(PRODUCTS)), None, 5),
    ids=["mapping", "text", "tuple", "none", "number"],
)
def test_products_that_are_not_a_list_raise_value_error(name: str, bad: Any) -> None:
    must_raise(_call_for(name, fresh(products=bad)), f"{name}: products given as a {type(bad).__name__}, not a list")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("bad", (["Alpha"], 5, None), ids=["list", "number", "none"])
def test_product_that_is_not_a_mapping_raises_value_error(name: str, bad: Any) -> None:
    rows: list[Any] = copy.deepcopy(PRODUCTS)
    rows[0] = bad
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product that is not a mapping")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("bad", (5, None, True), ids=["number", "none", "boolean"])
def test_product_name_that_is_not_text_raises_value_error(name: str, bad: Any) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["name"] = bad
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product name that is not text")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("field", ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"))
def test_case_field_that_is_none_raises_value_error(name: str, field: str) -> None:
    must_raise(_call_for(name, fresh(**{field: None})), f"{name}: {field} given as nothing, not a whole number")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize(
    "field",
    ("budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"),
)
def test_product_field_that_is_none_raises_value_error(name: str, field: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0][field] = None
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product's {field} given as nothing")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("field", ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"))
def test_case_number_given_as_text_raises_value_error(name: str, field: str) -> None:
    case = fresh(**{field: str(CASE[field])})
    must_raise(_call_for(name, case), f"{name}: {field} given as text, where a whole number is required")


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize(
    "field",
    ("budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"),
)
def test_product_number_given_as_text_raises_value_error(name: str, field: str) -> None:
    rows = copy.deepcopy(PRODUCTS)
    rows[0][field] = str(rows[0][field])
    must_raise(_call_for(name, with_products(rows)), f"{name}: a product's {field} given as text")


@pytest.mark.parametrize("bad", ("1500", None), ids=["text", "none"])
def test_actual_units_argument_that_is_not_a_number_raises_value_error(bad: Any) -> None:
    must_raise(lambda: sol.flexible_budget(CASE, bad), "flexible_budget: an actual unit count that is text or nothing")


# ---------------------------------------------------------------- the same refusals for a later product
#
# Most refusal tests above put the bad value in the first product. Each condition below is put in the middle or the last
# product instead, one condition per test, so that a check made only for the first product is caught.

LATER_PRODUCT_CONDITIONS: dict[str, Callable[[list[Any], int], None]] = {
    "negative budgeted units": lambda rows, i: rows[i].__setitem__("budget_units", -1),
    "boolean budgeted units": lambda rows, i: rows[i].__setitem__("budget_units", True),
    "negative actual units": lambda rows, i: rows[i].__setitem__("actual_units", -1),
    "float budgeted price": lambda rows, i: rows[i].__setitem__(
        "budget_price_cents", float(rows[i]["budget_price_cents"])
    ),
    "text input count": lambda rows, i: rows[i].__setitem__(
        "standard_inputs_per_unit", str(rows[i]["standard_inputs_per_unit"])
    ),
    "missing actual price": lambda rows, i: rows[i].pop("actual_price_cents"),
    "missing name": lambda rows, i: rows[i].pop("name"),
    "empty name": lambda rows, i: rows[i].__setitem__("name", ""),
    "name that is a number": lambda rows, i: rows[i].__setitem__("name", 5),
    "product that is a list": lambda rows, i: rows.__setitem__(i, ["Alpha"]),
}


@pytest.mark.parametrize("name", FUNCTIONS)
@pytest.mark.parametrize("position", (1, 2), ids=["middle-product", "last-product"])
@pytest.mark.parametrize("condition", tuple(LATER_PRODUCT_CONDITIONS))
def test_bad_later_product_raises_value_error(name: str, position: int, condition: str) -> None:
    rows: list[Any] = copy.deepcopy(PRODUCTS)
    LATER_PRODUCT_CONDITIONS[condition](rows, position)
    must_raise(_call_for(name, with_products(rows)), f"{name}: {condition} in product {position + 1} of {len(rows)}")


@pytest.mark.parametrize("name", FUNCTIONS)
def test_zero_budgeted_units_in_the_first_product_is_valid(name: str) -> None:
    # Only a budget with no budgeted units in total is refused. A first product that budgets no units is a valid case.
    rows = copy.deepcopy(PRODUCTS)
    rows[0]["budget_units"] = 0
    _call_for(name, with_products(rows))()
    decomposition_matches(with_products(rows))


@pytest.mark.parametrize("name", FUNCTIONS)
def test_first_product_name_repeated_in_the_last_position_raises_value_error(name: str) -> None:
    # The repeat is not adjacent: the last product repeats the first, and the middle product sits between them.
    rows = copy.deepcopy(PRODUCTS)
    rows[2]["name"] = rows[0]["name"]
    must_raise(
        _call_for(name, with_products(rows)), f"{name}: a product name that appears twice, not next to each other"
    )


# ---------------------------------------------------------------- purity and silence


@pytest.mark.parametrize("name", FUNCTIONS)
def test_functions_do_not_change_their_arguments(name: str) -> None:
    case = fresh()
    before = copy.deepcopy(case)
    if name == "flexible_budget":
        sol.flexible_budget(case, 900)
    else:
        getattr(sol, name)(case)
    assert case == before, "a function must never change its argument."


@pytest.mark.parametrize("name", FUNCTIONS)
def test_functions_are_silent(name: str) -> None:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        if name == "flexible_budget":
            sol.flexible_budget(CASE, 900)
        else:
            getattr(sol, name)(CASE)
    assert buffer.getvalue() == "", "a function must not print."


@pytest.mark.parametrize("name", FUNCTIONS)
def test_functions_do_not_reorder_their_products(name: str) -> None:
    # The generated products are already in name order, so a function that sorts its argument in place would pass
    # test_functions_do_not_change_their_arguments. The reversed list exposes it.
    case = with_products(copy.deepcopy(PRODUCTS[::-1]))
    before = copy.deepcopy(case)
    if name == "flexible_budget":
        sol.flexible_budget(case, 900)
    else:
        getattr(sol, name)(case)
    assert case == before, "a function must never change its argument, including the order of the products."


def test_results_do_not_depend_on_call_order() -> None:
    first = sol.variance_decomposition(CASE)
    sol.flexible_budget(CASE, 1)
    sol.master_budget(CASE)
    assert sol.variance_decomposition(CASE) == first, (
        "variance_decomposition: a result must not depend on earlier calls."
    )


def test_shared_case_is_unchanged_by_the_suite() -> None:
    # Runs last in the file: many tests before it have passed the shared CASE to the learner's functions.
    assert CASE == PRISTINE, (
        "the suite's shared case was changed by a function call; a function must never change its argument."
    )
