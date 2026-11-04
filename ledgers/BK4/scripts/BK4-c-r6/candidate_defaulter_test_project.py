"""Acceptance suite for the BK4 project: the clearing-house simulator (clearing_house.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your clearing_house.py next to this file. Warnings are failures, as in the browser.

Each test checks one property or one number against the conventions of the project page. Money is compared exactly:
the page fixes integer cents and the layer order, so a correct implementation returns the same integers. Only the
conditions the page names with ValueError are required to raise it, and each named condition has its own test on
both sides of its limit. Any other invalid input may raise any exception or return. A failing test names the property
it checks and the idea to revisit, and it never prints an expected value: each expected value is held in a named
variable, so a failing line shows the name and not the value.
"""

from __future__ import annotations

import dataclasses
import functools
import math
import os
import random
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import clearing_house as sol  # type: ignore[import-not-found]  # the learner's module, beside this file at run time
import pytest
from instance import make_instance  # type: ignore[import-not-found]  # beside this file; not on the repository's path

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)  # a second case, so a fixed answer for one seed must also match
TARGETS: tuple[int, ...] = (9_000, 9_500, 9_750)


# ---------------------------------------------------------------------------------------------------------------------
# Helpers. Each oracle is written separately from the reference and uses only the page's rules.
# ---------------------------------------------------------------------------------------------------------------------


def as_maps(case: dict[str, Any]) -> tuple[dict[int, int], dict[int, int]]:
    """The initial margins and default funds of a case, keyed by member id."""
    ids = case["member_ids"]
    return dict(zip(ids, case["initial_margin_cents"], strict=True)), dict(
        zip(ids, case["default_fund_cents"], strict=True)
    )


def waterfall_of(case: dict[str, Any], loss: int) -> Any:
    margins, funds = as_maps(case)
    return sol.waterfall(loss, case["defaulter_id"], margins, funds, case["ccp_capital_cents"])


def oracle_waterfall(
    loss: int, defaulter: int, margins: dict[int, int], funds: dict[int, int], capital: int
) -> tuple[int, int, int, dict[int, int], int]:
    """The layers, the survivors' payments and the uncovered loss, by the page's rules."""
    from_margin = min(loss, margins[defaulter])
    from_fund = min(loss - from_margin, funds[defaulter])
    from_capital = min(loss - from_margin - from_fund, capital)
    residual = loss - from_margin - from_fund - from_capital
    survivors = sorted(m for m in funds if m != defaulter)
    pool = sum(funds[m] for m in survivors)
    if residual >= pool:
        return from_margin, from_fund, from_capital, {m: funds[m] for m in survivors}, residual - pool
    shares = {m: (residual * funds[m]) // pool for m in survivors}
    owed = residual - sum(shares.values())
    for m in survivors:
        if owed > 0 and funds[m] > 0:
            shares[m] += 1
            owed -= 1
    return from_margin, from_fund, from_capital, shares, 0


def oracle_sorted_margin(losses: list[int], target: int) -> int:
    """The margin by the order statistic: the k-th smallest loss, k the least integer with k * 10000 >= target * S."""
    count = len(losses)
    index = math.ceil(Fraction(target * count, 10_000))
    return sorted(losses)[index - 1]


def brute_minimal_margin(losses: list[int], target: int) -> int:
    """The least integer margin whose cover, 10000 * (losses at or below it) // S, reaches the target. Tabulated."""
    top = max(losses)
    tally = [0] * (top + 1)
    for loss in losses:
        tally[loss] += 1
    count = len(losses)
    covered = 0
    for margin in range(top + 1):
        covered += tally[margin]
        if 10_000 * covered // count >= target:
            return margin
    raise AssertionError("the largest loss covers every scenario, so the search must have returned")


def oracle_cover(losses: list[int], margin: int) -> int:
    return 10_000 * sum(1 for loss in losses if loss <= margin) // len(losses)


def must_refuse(call: Callable[[], object], condition: str, naming: str | None = None) -> None:
    """Fail unless call() raises ValueError. If naming is given, the message must contain it."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as exc:
        if naming is not None and naming not in str(exc):
            pytest.fail(f"{condition}: the ValueError must name {naming}, so the learner sees which input failed.")
        return
    pytest.fail(f"{condition}: the page requires a ValueError for this input, and none was raised.")


def must_accept(call: Callable[[], object], condition: str) -> object:
    """Fail if call() raises. Used for the boundary values the page allows."""
    __tracebackhide__ = True
    try:
        return call()
    except NotImplementedError:
        raise
    except Exception:
        pytest.fail(f"{condition}: the page allows this input, and the call raised an exception.")


def checked_int(value: object, prop: str) -> int:
    __tracebackhide__ = True
    if isinstance(value, bool) or not isinstance(value, int):
        pytest.fail(f"{prop}: a money output must be an int in cents, not a float or a bool.")
    return int(value)


def check_waterfall(result: Any, expected: tuple[int, int, int, dict[int, int], int], prop: str) -> None:
    """Compare every field of a Waterfall with its expected value; the names of the fields are the ones on the page."""
    __tracebackhide__ = True
    margin, fund, capital, survivors, uncovered = expected
    got = (
        checked_int(result.margin_cents, f"{prop}: margin_cents"),
        checked_int(result.default_fund_cents, f"{prop}: default_fund_cents"),
        checked_int(result.ccp_capital_cents, f"{prop}: ccp_capital_cents"),
        {int(k): checked_int(v, f"{prop}: survivor_cents") for k, v in result.survivor_cents.items()},
        checked_int(result.uncovered_cents, f"{prop}: uncovered_cents"),
    )
    if got[:3] != (margin, fund, capital):
        pytest.fail(
            f"{prop}: a layer's amount differs from the fixture. The layers are used in order (the defaulter's "
            "margin, then its default fund, then the CCP capital), and each takes only what the layer before left."
        )
    if got[3] != survivors:
        pytest.fail(
            f"{prop}: the survivors' payments differ from the fixture. The residual is shared pro rata to the default "
            "funds, and the leftover cents go one each to the first survivors with a positive contribution."
        )
    if got[4] != uncovered:
        pytest.fail(f"{prop}: the uncovered loss differs from the fixture: the residual above the survivors' total.")


# Layer-order fixture (hand-computed on the project page, not seed-derived): defaulter 3 with margin 100 and default
# fund 50; the CCP capital is 30; the survivors' default funds are 40 (member 1) and 60 (member 2).
FIX_MARGINS = {1: 500, 2: 500, 3: 100}
FIX_FUNDS = {1: 40, 2: 60, 3: 50}
FIX_CAPITAL = 30


def fixture(loss: int) -> Any:
    return sol.waterfall(loss, 3, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL)


def expect_fixture(loss: int, layers: tuple[int, int, int], survivors: tuple[int, int], uncovered: int) -> None:
    __tracebackhide__ = True
    result = fixture(loss)
    check_waterfall(
        result,
        (*layers, {1: survivors[0], 2: survivors[1]}, uncovered),
        f"fixture with loss {loss}",
    )


# ---------------------------------------------------------------------------------------------------------------------
# Waterfall: conservation, shape and arguments
# ---------------------------------------------------------------------------------------------------------------------


def test_waterfall_returns_plain_int_money() -> None:
    """Every money field of the waterfall is an int in cents, not a float or a bool."""
    __tracebackhide__ = True
    result = waterfall_of(INST, INST["losses_cents"][0])
    for name in ("margin_cents", "default_fund_cents", "ccp_capital_cents", "uncovered_cents"):
        checked_int(getattr(result, name), f"Waterfall.{name}")
    for member, amount in result.survivor_cents.items():
        checked_int(member, "Waterfall.survivor_cents key")
        checked_int(amount, "Waterfall.survivor_cents value")


def test_waterfall_is_a_frozen_dataclass_with_the_named_fields() -> None:
    """Waterfall is a frozen dataclass whose fields are the five named on the project page."""
    __tracebackhide__ = True
    cls: Any = sol.Waterfall
    is_dataclass_class = dataclasses.is_dataclass(cls)
    assert is_dataclass_class, "Waterfall must be a dataclass"
    names = {field.name for field in dataclasses.fields(cls)}
    assert names == {
        "margin_cents",
        "default_fund_cents",
        "ccp_capital_cents",
        "survivor_cents",
        "uncovered_cents",
    }, "Waterfall must have exactly the five fields named on the project page"
    sample: Any = cls(0, 0, 0, {}, 0)
    try:
        sample.margin_cents = 1
    except dataclasses.FrozenInstanceError:
        return
    pytest.fail("Waterfall must be frozen: assigning to a field must raise FrozenInstanceError.")


def test_survivor_keys_are_the_members_other_than_the_defaulter() -> None:
    """survivor_cents has one entry for every surviving member, zero allowed, and none for the defaulter."""
    __tracebackhide__ = True
    result = waterfall_of(INST, INST["losses_cents"][0])
    expected = sorted(m for m in INST["member_ids"] if m != INST["defaulter_id"])
    assert sorted(result.survivor_cents) == expected, (
        "survivor_cents must hold every surviving member, including those who pay zero, and not the defaulter"
    )


def test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario() -> None:
    """The conservation invariant: margin + default fund + capital + survivors + uncovered = loss, on each scenario."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        for loss in case["losses_cents"]:
            result = waterfall_of(case, loss)
            total = (
                result.margin_cents
                + result.default_fund_cents
                + result.ccp_capital_cents
                + sum(result.survivor_cents.values())
                + result.uncovered_cents
            )
            assert total == loss, (
                "the layers, the survivors' payments and the uncovered loss must add up to the loss exactly; "
                "check each layer's residual and the remainder rule"
            )


def test_each_scenario_matches_the_oracle_on_both_instances() -> None:
    """Every scenario of both instances gives the layers, survivors and uncovered loss the page's rules give."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        margins, funds = as_maps(case)
        for loss in case["losses_cents"]:
            expected = oracle_waterfall(loss, case["defaulter_id"], margins, funds, case["ccp_capital_cents"])
            check_waterfall(waterfall_of(case, loss), expected, f"seeded scenario with loss {loss}")


def test_waterfall_does_not_change_its_arguments() -> None:
    """The waterfall reads its dictionaries and never writes to them."""
    __tracebackhide__ = True
    margins, funds = as_maps(INST)
    before = (dict(margins), dict(funds))
    loss = INST["losses_cents"][2]
    sol.waterfall(loss, INST["defaulter_id"], margins, funds, INST["ccp_capital_cents"])
    assert (margins, funds) == before, "waterfall must not change the dictionaries it is given"


def test_zero_loss_pays_nothing_and_leaves_nothing_uncovered() -> None:
    """A loss of zero cents uses no layer and no survivor pays."""
    __tracebackhide__ = True
    result = fixture(0)
    want = (0, 0, 0, {1: 0, 2: 0}, 0)
    check_waterfall(result, want, "a zero loss")


# ---------------------------------------------------------------------------------------------------------------------
# Waterfall: layer order and boundaries (hand-computed fixtures)
# ---------------------------------------------------------------------------------------------------------------------


def test_fixture_loss_80_is_paid_by_the_margin_alone() -> None:
    """A loss inside the defaulter's margin uses the margin and nothing else."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (80, 0, 0), (0, 0), 0
    expect_fixture(80, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_100_equal_to_the_margin_is_covered_by_the_margin() -> None:
    """A loss equal to the defaulter's margin is paid by the margin in full; the default fund is not touched."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 0, 0), (0, 0), 0
    expect_fixture(100, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_120_reaches_the_default_fund() -> None:
    """Once the margin is exhausted, the default fund pays the next layer."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 20, 0), (0, 0), 0
    expect_fixture(120, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_150_equal_to_margin_plus_fund_leaves_capital_untouched() -> None:
    """At margin plus default fund, the CCP capital pays nothing; the boundary of the default fund."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 0), (0, 0), 0
    expect_fixture(150, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_151_is_the_first_cent_of_capital() -> None:
    """One cent past the default fund is the first cent the CCP capital pays."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 1), (0, 0), 0
    expect_fixture(151, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_170_uses_part_of_the_capital_and_no_survivor_pays() -> None:
    """The capital pays only what the loss still needs; survivors pay nothing while the capital covers the loss."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 20), (0, 0), 0
    expect_fixture(170, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_180_exhausts_the_capital_exactly() -> None:
    """At 180 the three layers pay 180 in full and no survivor is called: the lower boundary of the survivors."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 30), (0, 0), 0
    expect_fixture(180, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_181_is_the_first_cent_for_the_survivors() -> None:
    """One cent past the capital: the residual goes to the first survivor with a positive default fund."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 30), (1, 0), 0
    expect_fixture(181, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_200_shares_the_residual_pro_rata() -> None:
    """A residual split pro rata between two default funds with no remainder cents."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 30), (8, 12), 0
    expect_fixture(200, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_205_shares_the_residual_pro_rata() -> None:
    """A larger residual split pro rata between the same two default funds, again with no remainder cents."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 30), (10, 15), 0
    expect_fixture(205, want_layers, want_survivors, want_uncovered)


def test_fixture_loss_300_reports_the_uncovered_loss() -> None:
    """A residual above the survivors' total: each survivor pays its whole default fund, and the excess is uncovered."""
    __tracebackhide__ = True
    want_layers, want_survivors, want_uncovered = (100, 50, 30), (40, 60), 20
    expect_fixture(300, want_layers, want_survivors, want_uncovered)


# ---------------------------------------------------------------------------------------------------------------------
# Waterfall: the remainder rule, zero contributions and the uncovered loss
# ---------------------------------------------------------------------------------------------------------------------

REMAINDER_MARGINS = {1: 1, 2: 1, 3: 1, 4: 0}
REMAINDER_FUNDS = {1: 1, 2: 1, 3: 1, 4: 0}


def remainder_case(loss: int) -> Any:
    """Defaulter 4 has no margin, fund or capital, so the residual is the loss; survivors 1, 2, 3 have 1 cent each."""
    return sol.waterfall(loss, 4, REMAINDER_MARGINS, REMAINDER_FUNDS, 0)


def test_remainder_of_one_cent_goes_to_the_first_survivor() -> None:
    """A residual of 1 against three equal default funds goes to member 1, the lowest id, and to no other member."""
    __tracebackhide__ = True
    want = {1: 1, 2: 0, 3: 0}
    result = remainder_case(1)
    assert result.survivor_cents == want, (
        "the leftover cent goes to the first surviving member in ascending id order; the others receive zero"
    )


def test_remainder_of_two_cents_goes_to_the_first_two_survivors() -> None:
    """A residual of 2 cents gives the leftover cents one each to the first two survivors in ascending id order."""
    __tracebackhide__ = True
    want = {1: 1, 2: 1, 3: 0}
    result = remainder_case(2)
    assert result.survivor_cents == want, (
        "leftover cents go one each, in ascending id order, to the surviving members with a positive contribution"
    )


def test_residual_equal_to_the_total_fund_pays_every_fund_in_full() -> None:
    """A residual equal to the survivors' total: each pays its default fund and nothing is uncovered."""
    __tracebackhide__ = True
    want_survivors, want_uncovered = {1: 1, 2: 1, 3: 1}, 0
    result = remainder_case(3)
    assert result.survivor_cents == want_survivors and result.uncovered_cents == want_uncovered, (
        "when the residual equals the total default fund, each survivor pays its whole fund and nothing is uncovered"
    )


def test_residual_above_the_total_fund_reports_one_cent_uncovered() -> None:
    """A residual one cent above the survivors' total: all pay in full, and that one cent is uncovered."""
    __tracebackhide__ = True
    want_survivors, want_uncovered = {1: 1, 2: 1, 3: 1}, 1
    result = remainder_case(4)
    assert result.survivor_cents == want_survivors and result.uncovered_cents == want_uncovered, (
        "a residual above the total default fund leaves the excess uncovered, and the survivors pay in full"
    )


def test_a_member_with_no_default_fund_is_skipped_by_the_remainder_rule() -> None:
    """Member 1 contributes nothing, so the leftover cent goes to member 2, the first survivor with a positive fund."""
    __tracebackhide__ = True
    want = {1: 0, 2: 1, 3: 0}
    result = sol.waterfall(1, 4, {1: 0, 2: 1, 3: 1, 4: 0}, {1: 0, 2: 1, 3: 1, 4: 0}, 0)
    assert result.survivor_cents == want, (
        "a member whose default fund is zero pays nothing; the remainder goes to the first member with a positive fund"
    )


def test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order() -> None:
    """The dictionaries list members 3, 1, 2, 4; the leftover cent still goes to member 1, the lowest id, not to 3."""
    __tracebackhide__ = True
    margins = {3: 1, 1: 1, 2: 1, 4: 0}
    funds = {3: 1, 1: 1, 2: 1, 4: 0}
    result = sol.waterfall(1, 4, margins, funds, 0)
    assert result.survivor_cents == {1: 1, 2: 0, 3: 0}, (
        "the leftover cent goes to the first survivor in ascending id order, whatever the order of the dictionaries"
    )


def test_no_survivor_has_a_fund_so_the_whole_residual_is_uncovered() -> None:
    """With every survivor's default fund at zero, the residual is entirely uncovered and each survivor pays zero."""
    __tracebackhide__ = True
    want_survivors, want_uncovered = {1: 0, 2: 0}, 5
    result = sol.waterfall(5, 4, {1: 0, 2: 0, 4: 0}, {1: 0, 2: 0, 4: 0}, 0)
    assert result.survivor_cents == want_survivors and result.uncovered_cents == want_uncovered, (
        "with no default fund among the survivors, the residual above zero is uncovered"
    )


def test_large_cent_shares_are_floored_in_integers() -> None:
    """Survivor shares are exact integer floors, leftover cent to the first survivor; residual * fund exceeds 2**53."""
    __tracebackhide__ = True
    margins = {1: 0, 2: 0, 3: 0}
    funds = {1: 6_692_931_089_932_558, 2: 585_467_024_498_971, 3: 0}
    loss = 6_585_696_953_829_388
    want_survivors = {1: 6_055_950_114_045_320, 2: 529_746_839_784_068}
    want = (0, 0, 0, want_survivors, 0)
    result = sol.waterfall(loss, 3, margins, funds, 0)
    check_waterfall(result, want, "a scenario whose products exceed 2**53")


# ---------------------------------------------------------------------------------------------------------------------
# Waterfall: the named conditions, each on both sides of its limit
# ---------------------------------------------------------------------------------------------------------------------


def test_negative_loss_is_refused_and_the_message_names_the_loss() -> None:
    """A negative loss is refused, and the message names loss_cents."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.waterfall(-1, INST["defaulter_id"], *as_maps(INST), INST["ccp_capital_cents"]),
        "waterfall with a negative loss",
        naming="loss_cents",
    )


def test_zero_loss_is_accepted() -> None:
    """A loss of exactly zero is a valid scenario, so the boundary on the accepted side is tested."""
    __tracebackhide__ = True
    must_accept(lambda: fixture(0), "waterfall with loss 0")


def test_negative_initial_margin_is_refused_and_the_message_names_it() -> None:
    """A negative initial margin for any member is refused, and the message names initial_margin_cents."""
    __tracebackhide__ = True
    margins = {1: -1, 2: 500, 3: 100}
    must_refuse(
        lambda: sol.waterfall(10, 3, margins, FIX_FUNDS, FIX_CAPITAL),
        "waterfall with a negative initial margin",
        naming="initial_margin_cents",
    )


def test_negative_initial_margin_of_the_defaulter_is_refused() -> None:
    """The defaulter's own negative initial margin is refused, and the message names initial_margin_cents."""
    __tracebackhide__ = True
    margins = {1: 500, 2: 500, 3: -1}
    must_refuse(
        lambda: sol.waterfall(10, 3, margins, FIX_FUNDS, FIX_CAPITAL),
        "waterfall with a negative initial margin for the defaulter",
        naming="initial_margin_cents",
    )


def test_zero_initial_margin_is_accepted() -> None:
    """An initial margin of zero is a valid input, so the boundary on the accepted side is tested."""
    __tracebackhide__ = True
    margins = {1: 0, 2: 500, 3: 0}
    must_accept(lambda: sol.waterfall(10, 3, margins, FIX_FUNDS, FIX_CAPITAL), "waterfall with a zero initial margin")


def test_negative_default_fund_is_refused_and_the_message_names_it() -> None:
    """A negative default fund for any member is refused, and the message names default_fund_cents."""
    __tracebackhide__ = True
    funds = {1: 40, 2: -1, 3: 50}
    must_refuse(
        lambda: sol.waterfall(10, 3, FIX_MARGINS, funds, FIX_CAPITAL),
        "waterfall with a negative default fund",
        naming="default_fund_cents",
    )


def test_negative_default_fund_of_the_defaulter_is_refused() -> None:
    """The defaulter's own negative default fund is refused, and the message names default_fund_cents."""
    __tracebackhide__ = True
    funds = {1: 40, 2: 60, 3: -1}
    must_refuse(
        lambda: sol.waterfall(10, 3, FIX_MARGINS, funds, FIX_CAPITAL),
        "waterfall with a negative default fund for the defaulter",
        naming="default_fund_cents",
    )


def test_zero_default_fund_is_accepted() -> None:
    """A default fund of zero is a valid input, so the boundary on the accepted side is tested."""
    __tracebackhide__ = True
    funds = {1: 0, 2: 60, 3: 50}
    must_accept(lambda: sol.waterfall(10, 3, FIX_MARGINS, funds, FIX_CAPITAL), "waterfall with a zero default fund")


def test_negative_ccp_capital_is_refused_and_the_message_names_it() -> None:
    """A negative CCP capital is refused, and the message names ccp_capital_cents."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.waterfall(10, 3, FIX_MARGINS, FIX_FUNDS, -1),
        "waterfall with a negative CCP capital",
        naming="ccp_capital_cents",
    )


def test_zero_ccp_capital_is_accepted() -> None:
    """A CCP capital of zero is a valid input, so the boundary on the accepted side is tested."""
    __tracebackhide__ = True
    must_accept(lambda: sol.waterfall(10, 3, FIX_MARGINS, FIX_FUNDS, 0), "waterfall with zero CCP capital")


def test_defaulter_that_is_not_a_member_is_refused_and_the_message_names_it() -> None:
    """A defaulter id that is not among the member ids is refused, and the message names defaulter_id."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.waterfall(10, 9, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL),
        "waterfall with a defaulter that is not a member",
        naming="defaulter_id",
    )


def test_defaulter_below_the_member_ids_is_refused_and_the_message_names_it() -> None:
    """A defaulter id below the lowest member id is not a member: it is refused, and the message names defaulter_id."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.waterfall(10, 0, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL),
        "waterfall with a defaulter id of 0, below the member ids",
        naming="defaulter_id",
    )


def test_defaulter_inside_the_id_range_but_not_a_member_is_refused() -> None:
    """Member ids need not be contiguous: id 3 lies between the members 1, 2 and 4, but it is not a member."""
    __tracebackhide__ = True
    margins = {1: 500, 2: 500, 4: 100}
    funds = {1: 40, 2: 60, 4: 50}
    must_refuse(
        lambda: sol.waterfall(10, 3, margins, funds, FIX_CAPITAL),
        "waterfall with a defaulter id inside the id range that is not a member",
        naming="defaulter_id",
    )


def test_defaulter_that_is_a_member_of_a_non_contiguous_set_is_accepted() -> None:
    """In the same non-contiguous set, id 4 is a member, so it is accepted: the accepted side of that limit."""
    __tracebackhide__ = True
    margins = {1: 500, 2: 500, 4: 100}
    funds = {1: 40, 2: 60, 4: 50}
    must_accept(
        lambda: sol.waterfall(10, 4, margins, funds, FIX_CAPITAL),
        "waterfall with a defaulter that is the highest of non-contiguous member ids",
    )


def test_defaulter_at_the_smallest_and_largest_member_id_is_accepted() -> None:
    """The defaulter may be the lowest or the highest member id; both are valid, so both boundaries are tested."""
    __tracebackhide__ = True
    must_accept(lambda: sol.waterfall(10, 1, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL), "defaulter at the lowest id")
    must_accept(lambda: sol.waterfall(10, 3, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL), "defaulter at the highest id")


# ---------------------------------------------------------------------------------------------------------------------
# margin_for_cover: sizing against the order statistic and against a brute-force search
# ---------------------------------------------------------------------------------------------------------------------


def test_margin_matches_the_order_statistic_on_both_instances() -> None:
    """For each target, the margin is the k-th smallest loss with k = ceil(target * S / 10000), on both instances."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        for target in TARGETS:
            got = checked_int(sol.margin_for_cover(case["losses_cents"], target), "margin_for_cover")
            want = oracle_sorted_margin(case["losses_cents"], target)
            assert got == want, (
                f"margin_for_cover at target {target} differs from the order statistic: the index is the ceiling of "
                "target * S / 10000, counted from the smallest loss"
            )


def test_margin_equals_the_brute_force_minimum_on_both_instances() -> None:
    """For each target, the margin equals the least integer margin whose cover reaches the target, found by search."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        for target in TARGETS:
            got = checked_int(sol.margin_for_cover(case["losses_cents"], target), "margin_for_cover")
            want = brute_minimal_margin(case["losses_cents"], target)
            assert got == want, (
                f"margin_for_cover at target {target} is not the least margin that reaches the target: check the "
                "index and the strictness of the cover count"
            )


def test_fixture_five_losses_at_8000_bps_uses_the_ceiling_index() -> None:
    """Five scenarios and a target of 8000 bps: the ceiling index is exact, and the margin is the loss at that place."""
    __tracebackhide__ = True
    losses = [10, 20, 30, 40, 50]
    want = 40
    got = sol.margin_for_cover(losses, 8_000)
    assert got == want, (
        "the margin must be the loss at the position the ceiling of target * S gives, counted from the smallest loss"
    )


def test_fixture_five_losses_at_8001_bps_needs_the_next_loss() -> None:
    """A target just above the exact position needs the next loss in the sorted order."""
    __tracebackhide__ = True
    losses = [10, 20, 30, 40, 50]
    want = 50
    got = sol.margin_for_cover(losses, 8_001)
    assert got == want, (
        "a target just above the exact position needs the next loss; the index is a ceiling, not a floor"
    )


def test_fixture_five_losses_at_10000_bps_gives_the_largest_loss() -> None:
    """Full cover needs every scenario, so the margin is the largest loss."""
    __tracebackhide__ = True
    losses = [10, 20, 30, 40, 50]
    want = 50
    got = sol.margin_for_cover(losses, 10_000)
    assert got == want, "the full target covers every scenario, so the margin is the largest loss"


def test_fixture_four_losses_at_5000_bps_uses_the_exact_position() -> None:
    """Half of four scenarios is an exact position, so the margin is that loss in the sorted order, not the next one."""
    __tracebackhide__ = True
    losses = [10, 20, 30, 40]
    want = 20
    got = sol.margin_for_cover(losses, 5_000)
    assert got == want, "half of four scenarios is an exact position, and a strict count gives a different margin"


def test_repeated_losses_each_count_as_a_scenario_in_the_sizing() -> None:
    """A repeated loss is one scenario per occurrence, so the count S includes every repeat, not the distinct losses."""
    __tracebackhide__ = True
    got_four = sol.margin_for_cover([5, 5, 10, 20], 5_000)
    got_five = sol.margin_for_cover([5, 5, 5, 9, 12], 6_000)
    assert got_four == 5, (
        "the scenario count S counts every occurrence of a loss, repeats included: k is the ceiling of "
        "target * S / 10000, counted from the smallest of all S losses"
    )
    assert got_five == 5, (
        "the scenario count S counts every occurrence of a loss, repeats included: k is the ceiling of "
        "target * S / 10000, counted from the smallest of all S losses"
    )


def test_zero_losses_are_scenarios_in_the_sizing() -> None:
    """A zero loss is one of the S scenarios, so the sizing counts it: with four scenarios, k = 2 gives the second."""
    __tracebackhide__ = True
    got = sol.margin_for_cover([0, 10, 20, 30], 5_000)
    assert got == 10, (
        "a zero loss is a scenario: S counts it, and the margin is the k-th smallest of all S losses, zeros included"
    )


def test_a_single_scenario_gives_that_scenario_at_every_target() -> None:
    """With one scenario, every target needs that one loss: the boundary S = 1."""
    __tracebackhide__ = True
    want = 7
    at_one = sol.margin_for_cover([7], 1)
    at_full = sol.margin_for_cover([7], 10_000)
    assert at_one == want, "with one scenario the only loss is the margin, at any target"
    assert at_full == want, "with one scenario the only loss is the margin, at any target"


def test_the_smallest_target_gives_the_smallest_loss() -> None:
    """At one basis point, one scenario in the set is needed, so the margin is the smallest loss."""
    __tracebackhide__ = True
    want = 3
    got = sol.margin_for_cover([9, 3, 5], 1)
    assert got == want, "one basis point of cover needs the smallest loss"


def test_the_order_of_the_losses_does_not_change_the_margin() -> None:
    """Shuffling the scenarios does not change the margin: the answer depends only on the set of losses."""
    __tracebackhide__ = True
    shuffled = list(INST["losses_cents"])
    random.Random(SEED).shuffle(shuffled)
    for target in TARGETS:
        assert sol.margin_for_cover(shuffled, target) == sol.margin_for_cover(INST["losses_cents"], target), (
            "margin_for_cover must depend only on the set of losses, not on their order"
        )


def test_margin_is_non_decreasing_in_the_target() -> None:
    """A higher target cover never needs a smaller margin, on both instances."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        previous = -1
        for target in range(1, 10_001, 250):
            got = checked_int(sol.margin_for_cover(case["losses_cents"], target), "margin_for_cover")
            assert got >= previous, "a higher target cover must never need a smaller margin"
            previous = got


def test_the_margin_is_an_int_in_cents() -> None:
    """The margin is an int number of cents."""
    __tracebackhide__ = True
    checked_int(sol.margin_for_cover(INST["losses_cents"], 9_950), "margin_for_cover")


# ---------------------------------------------------------------------------------------------------------------------
# cover_bps: the cover in basis points
# ---------------------------------------------------------------------------------------------------------------------


def test_one_of_three_scenarios_covered_is_floored() -> None:
    """One covered scenario of three is a share with a fraction; the cover is that share, floored, in basis points."""
    __tracebackhide__ = True
    want = 3_333
    got = sol.cover_bps([1, 5, 9], 4)
    assert got == want, "the cover of one scenario of three is the floor of its share in basis points"


def test_two_of_three_scenarios_covered_is_floored_not_rounded() -> None:
    """Two covered scenarios of three is a share with a repeating fraction; the cover is floored, not rounded."""
    __tracebackhide__ = True
    want = 6_666
    got = sol.cover_bps([1, 2, 9], 2)
    assert got == want, "the cover is a floored integer, not a rounded one"


def test_no_scenario_covered_is_zero_bps() -> None:
    """A margin below every loss covers nothing."""
    __tracebackhide__ = True
    want = 0
    got = sol.cover_bps([5, 6], 4)
    assert got == want, "a margin below every loss covers no scenario"


def test_loss_equal_to_the_margin_is_covered() -> None:
    """A loss equal to the margin counts as covered: the comparison is at most, not strictly below."""
    __tracebackhide__ = True
    want = 10_000
    got = sol.cover_bps([50], 50)
    assert got == want, "a loss equal to the margin is covered in full"


def test_loss_one_cent_above_the_margin_is_not_covered() -> None:
    """A loss one cent above the margin is not covered."""
    __tracebackhide__ = True
    want = 0
    got = sol.cover_bps([51], 50)
    assert got == want, "a loss one cent above the margin is not covered"


def test_full_margin_covers_every_scenario() -> None:
    """A margin at the largest loss covers every scenario, so the cover is full."""
    __tracebackhide__ = True
    want = 10_000
    got = sol.cover_bps(INST["losses_cents"], max(INST["losses_cents"]))
    assert got == want, "a margin at the largest loss covers every scenario"


def test_repeated_losses_each_count_in_the_cover() -> None:
    """Each of the S scenarios counts once, repeats included: two of four scenarios at or below 5 cents is 5000 bps."""
    __tracebackhide__ = True
    got = sol.cover_bps([5, 5, 10, 20], 5)
    assert got == 5_000, "the cover counts every scenario, repeated losses included, and divides by all S scenarios"


def test_zero_losses_are_in_the_cover_denominator() -> None:
    """A zero loss is a scenario: two zero losses of four scenarios, at a zero margin, give a cover of 5000 bps."""
    __tracebackhide__ = True
    got = sol.cover_bps([0, 0, 5, 9], 0)
    assert got == 5_000, "the cover divides by all S scenarios, and the zero losses are among them, so they count"


def test_cover_matches_the_oracle_on_both_instances() -> None:
    """The cover at several margins on both instances equals the floored count of covered scenarios."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        top = max(case["losses_cents"])
        for margin in (0, top // 4, top // 2, top, top + 1):
            got = checked_int(sol.cover_bps(case["losses_cents"], margin), "cover_bps")
            assert got == oracle_cover(case["losses_cents"], margin), (
                "cover_bps must count the scenarios at or below the margin and floor 10000 times that share"
            )


def test_cover_is_non_decreasing_in_the_margin() -> None:
    """A larger margin never covers fewer scenarios."""
    __tracebackhide__ = True
    losses = INST["losses_cents"]
    previous = -1
    for margin in range(0, max(losses) + 1, 997):
        got = checked_int(sol.cover_bps(losses, margin), "cover_bps")
        assert got >= previous, "a larger margin must never cover fewer scenarios"
        previous = got


def test_chosen_margin_reaches_the_target_and_one_cent_less_does_not() -> None:
    """At the margin for each target, the cover reaches the target; one cent less falls short."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        for target in TARGETS:
            margin = sol.margin_for_cover(case["losses_cents"], target)
            assert sol.cover_bps(case["losses_cents"], margin) >= target, (
                f"at the margin for target {target}, cover_bps must reach the target"
            )
            assert sol.cover_bps(case["losses_cents"], margin - 1) < target, (
                f"one cent below the margin for target {target}, cover_bps must fall short of the target"
            )


def test_cover_bps_is_an_int() -> None:
    """The cover is an int in basis points."""
    __tracebackhide__ = True
    checked_int(sol.cover_bps(INST["losses_cents"], 1_000), "cover_bps")


# ---------------------------------------------------------------------------------------------------------------------
# The named conditions of the sizing and cover functions, each on both sides of its limit
# ---------------------------------------------------------------------------------------------------------------------


def test_empty_losses_are_refused_in_margin_for_cover_with_the_scenario_message() -> None:
    """An empty scenario set is refused, and the message says that at least one scenario is needed."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.margin_for_cover([], 9_950),
        "margin_for_cover with no scenarios",
        naming="at least one scenario is needed",
    )


def test_one_scenario_is_accepted_in_margin_for_cover() -> None:
    """A set of one scenario is accepted: the boundary on the accepted side."""
    __tracebackhide__ = True
    must_accept(lambda: sol.margin_for_cover([0], 9_950), "margin_for_cover with one scenario")


def test_target_of_zero_is_refused_in_margin_for_cover() -> None:
    """A target of zero basis points is outside the range 1 to 10000, and the message names target_bps."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.margin_for_cover([10, 20], 0),
        "margin_for_cover with target 0",
        naming="target_bps",
    )


def test_target_of_one_is_accepted_in_margin_for_cover() -> None:
    """A target of 1 basis point is the lowest valid target, so the boundary on the accepted side is tested."""
    __tracebackhide__ = True
    must_accept(lambda: sol.margin_for_cover([10, 20], 1), "margin_for_cover with target 1")


def test_target_of_10001_is_refused_in_margin_for_cover() -> None:
    """A target above 10000 basis points is outside the range, and the message names target_bps."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.margin_for_cover([10, 20], 10_001),
        "margin_for_cover with target 10001",
        naming="target_bps",
    )


def test_target_of_10000_is_accepted_in_margin_for_cover() -> None:
    """A target of 10000 basis points, full cover, is the highest valid target."""
    __tracebackhide__ = True
    must_accept(lambda: sol.margin_for_cover([10, 20], 10_000), "margin_for_cover with target 10000")


def test_negative_loss_is_refused_in_margin_for_cover() -> None:
    """A negative loss is refused, and the message says losses cannot be negative."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.margin_for_cover([10, -1], 9_950),
        "margin_for_cover with a negative loss",
        naming="losses cannot be negative",
    )


def test_zero_loss_is_accepted_in_margin_for_cover() -> None:
    """A loss of zero is valid: the boundary on the accepted side."""
    __tracebackhide__ = True
    must_accept(lambda: sol.margin_for_cover([0, 0], 9_950), "margin_for_cover with a zero loss")


def test_empty_losses_are_refused_in_cover_bps_with_the_scenario_message() -> None:
    """An empty scenario set is refused in cover_bps as well, with the same message."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.cover_bps([], 10),
        "cover_bps with no scenarios",
        naming="at least one scenario is needed",
    )


def test_one_scenario_is_accepted_in_cover_bps() -> None:
    """A set of one scenario is accepted by cover_bps: the boundary on the accepted side."""
    __tracebackhide__ = True
    must_accept(lambda: sol.cover_bps([3], 3), "cover_bps with one scenario")


def test_negative_loss_is_refused_in_cover_bps() -> None:
    """A negative loss is refused in cover_bps, and the message says losses cannot be negative."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.cover_bps([10, -1], 5),
        "cover_bps with a negative loss",
        naming="losses cannot be negative",
    )


def test_zero_loss_is_accepted_in_cover_bps() -> None:
    """A loss of zero is valid in cover_bps: the boundary on the accepted side."""
    __tracebackhide__ = True
    must_accept(lambda: sol.cover_bps([0, 0], 0), "cover_bps with a zero loss")


# ---------------------------------------------------------------------------------------------------------------------
# The seeded cases, the module's silence and purity
# ---------------------------------------------------------------------------------------------------------------------


def test_seeded_cases_are_valid() -> None:
    """Each case has member ids 1..N, positive default funds, non-negative margins and capital, and 40 to 80 losses."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        ids = case["member_ids"]
        assert ids == list(range(1, len(ids) + 1)), "member ids run 1 to N"
        assert 4 <= len(ids) <= 6, "a case has four to six members"
        assert case["defaulter_id"] in ids, "the defaulter is a member"
        assert all(f >= 1 for f in case["default_fund_cents"]), "every default fund is at least one cent"
        assert all(m >= 0 for m in case["initial_margin_cents"]), "every initial margin is non-negative"
        assert case["ccp_capital_cents"] >= 0, "the CCP capital is non-negative"
        assert 40 <= len(case["losses_cents"]) <= 80, "a case has 40 to 80 scenarios"
        assert all(isinstance(x, int) and x >= 0 for x in case["losses_cents"]), "losses are non-negative ints"
        assert case["target_bps"] in TARGETS, "the target is one of 9000, 9500 and 9750 bps"


def test_each_seeded_case_has_a_loss_in_each_region_the_waterfall_separates() -> None:
    """Each case has one loss inside the margin, one inside the default fund, and one past every defaulter layer."""
    __tracebackhide__ = True
    for case in (INST, INST2):
        margins, funds = as_maps(case)
        d = case["defaulter_id"]
        losses = case["losses_cents"]
        assert any(0 <= x <= margins[d] for x in losses), "a case needs a loss inside the defaulter's margin"
        assert any(margins[d] < x <= margins[d] + funds[d] for x in losses), (
            "a case needs a loss inside the defaulter's default fund"
        )
        assert any(x > margins[d] + funds[d] + case["ccp_capital_cents"] for x in losses), (
            "a case needs a loss past every defaulter layer and the CCP capital"
        )


def test_seeded_cases_give_different_margins_across_seeds() -> None:
    """Across seeds 0 to 49, the sizing answers take at least three distinct values, so a fixed answer fails."""
    __tracebackhide__ = True
    answers = set()
    for seed in range(50):
        case = make_instance(seed)
        answers.add(oracle_sorted_margin(case["losses_cents"], case["target_bps"]))
    assert len(answers) >= 3, "the seeded cases must give several different margins, so that a fixed answer fails"


def test_the_module_prints_nothing_on_valid_inputs(capsys: pytest.CaptureFixture[str]) -> None:
    """The module prints nothing and warns nothing on valid inputs, including a waterfall with an uncovered loss."""
    __tracebackhide__ = True
    sol.waterfall(120, 3, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL)
    sol.waterfall(300, 3, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL)
    sol.margin_for_cover(INST["losses_cents"], 9_950)
    sol.cover_bps(INST["losses_cents"], 1_000)
    captured = capsys.readouterr()
    assert captured.out == "" and captured.err == "", "a valid call must print nothing"


def test_refused_inputs_print_nothing_before_they_raise(capsys: pytest.CaptureFixture[str]) -> None:
    """Each named refusal in the list below raises ValueError and prints nothing on the way."""
    __tracebackhide__ = True
    refusals: list[tuple[str, Callable[[], object]]] = [
        ("margin_for_cover with no scenarios", lambda: sol.margin_for_cover([], 9_950)),
        ("margin_for_cover with target 0", lambda: sol.margin_for_cover([1], 0)),
        ("margin_for_cover with target 10001", lambda: sol.margin_for_cover([1], 10_001)),
        ("margin_for_cover with a negative loss", lambda: sol.margin_for_cover([10, -1], 9_950)),
        ("cover_bps with no scenarios", lambda: sol.cover_bps([], 10)),
        ("cover_bps with a negative loss", lambda: sol.cover_bps([10, -1], 5)),
        ("waterfall with a negative loss", lambda: sol.waterfall(-1, 3, FIX_MARGINS, FIX_FUNDS, FIX_CAPITAL)),
        (
            "waterfall with a negative initial margin for a survivor",
            lambda: sol.waterfall(10, 3, {1: -1, 2: 500, 3: 100}, FIX_FUNDS, FIX_CAPITAL),
        ),
        (
            "waterfall with a negative initial margin for the defaulter",
            lambda: sol.waterfall(10, 3, {1: 500, 2: 500, 3: -1}, FIX_FUNDS, FIX_CAPITAL),
        ),
        (
            "waterfall with a negative default fund for a survivor",
            lambda: sol.waterfall(10, 3, FIX_MARGINS, {1: 40, 2: -1, 3: 50}, FIX_CAPITAL),
        ),
        (
            "waterfall with a negative default fund for the defaulter",
            lambda: sol.waterfall(10, 3, FIX_MARGINS, {1: 40, 2: 60, 3: -1}, FIX_CAPITAL),
        ),
        ("waterfall with a negative CCP capital", lambda: sol.waterfall(10, 3, FIX_MARGINS, FIX_FUNDS, -1)),
        ("waterfall with a defaulter above the members", lambda: sol.waterfall(10, 9, FIX_MARGINS, FIX_FUNDS, 30)),
        ("waterfall with a defaulter below the members", lambda: sol.waterfall(10, 0, FIX_MARGINS, FIX_FUNDS, 30)),
        (
            "waterfall with a defaulter between two members",
            lambda: sol.waterfall(10, 3, {1: 500, 2: 500, 4: 100}, {1: 40, 2: 60, 4: 50}, 30),
        ),
    ]
    for condition, call in refusals:
        must_refuse(call, condition)
        captured = capsys.readouterr()
        assert captured.out == "" and captured.err == "", f"{condition}: a refused input must print nothing"


def test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument() -> None:
    """The sizing and the cover read their scenario list and never reorder it or write to it."""
    __tracebackhide__ = True
    losses = [30, 10, 20]
    sol.margin_for_cover(losses, 5_000)
    sol.cover_bps(losses, 20)
    assert losses == [30, 10, 20], "margin_for_cover and cover_bps must not change the list they are given"


def test_repeated_calls_agree() -> None:
    """The functions are pure: the same call gives the same answer each time."""
    __tracebackhide__ = True
    losses = INST["losses_cents"]
    assert sol.margin_for_cover(losses, 9_950) == sol.margin_for_cover(losses, 9_950), (
        "margin_for_cover must give the same answer on every call"
    )
    assert sol.cover_bps(losses, 2_000) == oracle_cover(losses, 2_000), (
        "cover_bps must give the same answer on every call"
    )
    first = waterfall_of(INST, losses[2])
    second = waterfall_of(INST, losses[2])
    assert first == second, "waterfall must give the same result on every call"


# ---------------------------------------------------------------------------------------------------------------------
# Every test names a failure in terms of the property, never with a traceback from a missing implementation
# ---------------------------------------------------------------------------------------------------------------------


def _named_when_unimplemented(test: Callable[..., None]) -> Callable[..., None]:
    """Turn the student module's NotImplementedError into a failure that names the property, with no traceback."""

    @functools.wraps(test)
    def run(*args: object, **kwargs: object) -> None:
        try:
            test(*args, **kwargs)
        except NotImplementedError as missing:
            name = str(missing)
        else:
            return
        # Failing outside the except block keeps the NotImplementedError out of the report, so no traceback shows.
        # The summary names the test, and never repeats its docstring.
        pytest.fail(
            f"{test.__name__}: the student module has no implementation for {name} yet; write it in clearing_house.py.",
            pytrace=False,
        )

    return run


for _name, _value in list(globals().items()):
    if _name.startswith("test_") and callable(_value):
        globals()[_name] = _named_when_unimplemented(_value)


def test_defaulter_in_margins_but_not_in_funds_is_refused_and_the_message_names_it() -> None:
    """Candidate test (verifier round 6): member ids are the keys of default_fund_cents, so id 3 is not a member."""
    __tracebackhide__ = True
    must_refuse(
        lambda: sol.waterfall(10, 3, {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60}, 30),
        "waterfall with a defaulter present in the margins only",
        naming="defaulter_id",
    )
