"""Autograder for the M4 tail-risk simulator (tail_risk.py). All inputs are SIMULATED.

Run in the browser or locally with the flags the page shows:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Every test checks a property the page states, or a condition the page names. Failure messages name the property and
give a concept hint; they never print a computed value or the answer.
"""

from __future__ import annotations

import math
import os
import random
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import pytest
import tail_risk as sol
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
POSITIONS: list[int] = INST["positions_cents"]
COV: list[list[float]] = INST["cov"]
NU: int = INST["nu"]
N_DRAWS: int = INST["n_draws"]

# Relative tolerances on the loss variance. The Gaussian is held tight. The Student-t variance is checked only for
# nu of 5 or more: the fourth moment of the Student-t is infinite at nu = 3 and 4, so a sample variance there can miss
# its target by more than any fixed tolerance (the reference fails at seed 1093 with nu = 3). Over seeds 0 to 1999 the
# reference's largest relative error was 0.126 at nu = 5, 0.097 at nu = 6, 0.073 at nu = 7 and 0.062 at nu = 8 (the
# unrounded maxima are 0.1259, 0.0967, 0.0728 and 0.0624, from the seed-by-seed sweep of the reference against
# make_instance). The tolerance 0.30 is about 2.4 times the largest of these (0.30 / 0.1259 = 2.38). Against a missing
# matched factor (an inflation of nu / (nu - 2), which is 1.67, 1.50, 1.40 and 1.33 at nu = 5 to 8), the check fails on
# every seed tested at nu = 5 and 6 (347 and 317 seeds, seeds 0 to 1999), and on 342 of 343 seeds at nu = 7 and 288 of
# 317 at nu = 8.
TOL_GAUSSIAN_VARIANCE = 0.10
TOL_T_VARIANCE = 0.30
MIN_NU_FOR_T_VARIANCE_CHECK = 5
# The Student-t cross term: two assets with correlation 0.8, 100,000 draws, nu of 5. The reference's largest relative
# error over seeds 0 to 49 is 0.024. A matched factor applied to one asset only, or one chi-square variable per asset,
# moves the cross term by about 29 % and 15 % (measured at seeds 0 to 9). The tolerance 0.05 lies between them.
CROSS_TERM_NU = 5
CROSS_TERM_DRAWS = 100_000
TOL_CROSS_TERM = 0.05


def check(condition: bool, message: str) -> None:
    """Fail with message when condition is false. The message names the property; it never shows a value."""
    __tracebackhide__ = True
    if not condition:
        raise AssertionError(message)


def expect_value_error(call: Callable[[], object], message: str) -> None:
    """Pass only when call raises ValueError. Any other exception, or no exception, fails with message."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    except Exception:
        raise AssertionError(message + " (a different exception type was raised)") from None
    raise AssertionError(message)


def sample_variance(xs: list[Any]) -> float:
    """The unbiased sample variance of a list of numbers, summed with math.fsum."""
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def portfolio_variance() -> float:
    """w' Sigma w in cents squared, from the instance's positions and covariance."""
    n = len(POSITIONS)
    return math.fsum(POSITIONS[i] * POSITIONS[j] * COV[i][j] for i in range(n) for j in range(n))


def relative_error(measured: float, target: float) -> float:
    """The absolute relative error |measured / target - 1|."""
    return abs(measured / target - 1.0)


# The input conditions of simulate_losses apply to both families, so each of them is tested for both. The Student-t
# case uses nu = 5, a valid degrees of freedom, so that only the condition under test is violated.
FAMILY_CASES = [("gaussian", None), ("student_t", 5)]


# --- the instance -----------------------------------------------------------------------------------------------


def test_instance_is_simulated_and_in_range() -> None:
    check(INST["label"] == "SIMULATED", "the instance must be labelled SIMULATED")
    check(3 <= NU <= 8, "the instance's degrees of freedom must lie between 3 and 8")
    check(
        N_DRAWS <= 20_000 and N_DRAWS % 100 != 0,
        "the instance's draw count must be at most 20,000 and not a multiple of 100",
    )
    check(all(type(w) is int and w > 0 for w in POSITIONS), "the instance's positions must be positive whole cents")


# --- matched_scale ------------------------------------------------------------------------------------------------


def test_matched_scale_is_nu_minus_two_over_nu() -> None:
    for nu in range(3, 9):
        got = sol.matched_scale(nu)
        check(abs(got - (nu - 2) / nu) <= 1e-12, "matched_scale must return (nu - 2) / nu for nu above 2")


def test_matched_scale_accepts_nu_just_above_two() -> None:
    check(abs(sol.matched_scale(3) - 1 / 3) <= 1e-12, "matched_scale(3) must return 1/3, the boundary above nu = 2")


def test_matched_scale_rejects_nu_equal_to_two() -> None:
    expect_value_error(lambda: sol.matched_scale(2), "matched_scale must raise ValueError at nu = 2")


@pytest.mark.parametrize("nu", [1, 0, -3])
def test_matched_scale_rejects_nu_below_two(nu: int) -> None:
    expect_value_error(lambda: sol.matched_scale(nu), "matched_scale must raise ValueError for nu below 2")


@pytest.mark.parametrize("nu", [3.0, True, "3", None])
def test_matched_scale_rejects_a_value_that_is_not_a_whole_number(nu: Any) -> None:
    expect_value_error(lambda: sol.matched_scale(nu), "matched_scale must reject a value that is not a whole number")


# --- simulate_losses: shape, moments, determinism -------------------------------------------------------------------


def test_gaussian_returns_one_whole_cent_loss_per_draw() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, N_DRAWS, SEED, "gaussian", None)
    check(len(losses) == N_DRAWS, "simulate_losses must return one loss per draw")
    check(all(type(x) is int for x in losses), "every gaussian loss must be an int number of cents, not a float")


def test_student_t_returns_one_whole_cent_loss_per_draw() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, N_DRAWS, SEED, "student_t", NU)
    check(len(losses) == N_DRAWS, "simulate_losses must return one loss per draw")
    check(all(type(x) is int for x in losses), "every student_t loss must be an int number of cents, not a float")


def test_gaussian_loss_variance_matches_portfolio_covariance() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, N_DRAWS, SEED, "gaussian", None)
    target = portfolio_variance()
    check(
        relative_error(sample_variance(losses), target) <= TOL_GAUSSIAN_VARIANCE,
        "the gaussian losses' variance must match w' Sigma w: check that the draws use the covariance factor L",
    )


def test_student_t_loss_variance_matches_matched_covariance() -> None:
    if NU < MIN_NU_FOR_T_VARIANCE_CHECK:
        pytest.skip("the Student-t variance is checked only for nu of 5 or more (the page states this)")
    losses = sol.simulate_losses(POSITIONS, COV, N_DRAWS, SEED, "student_t", NU)
    target = portfolio_variance()
    check(
        relative_error(sample_variance(losses), target) <= TOL_T_VARIANCE,
        "the student_t losses' variance must match w' Sigma w: the Student-t draws need the matched factor",
    )


def test_student_t_cross_term_matches_matched_covariance() -> None:
    # Positions (w1, w2) and (w1, -w2) with the same seed share their draws, so the difference of their sample
    # variances is 4 w1 w2 Cov(R1, R2) for the returns. The Conventions give R = sqrt((nu - 2) / W) L Z for every asset,
    # with one W per draw, so Cov(R1, R2) = Sigma_12. Whole-cent rounding is negligible at 10^6 cents.
    w1, w2 = 1_000_000, 1_000_000
    cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
    target = 4.0 * w1 * w2 * cov[0][1]
    plus = sol.simulate_losses([w1, w2], cov, CROSS_TERM_DRAWS, SEED, "student_t", CROSS_TERM_NU)
    minus = sol.simulate_losses([w1, -w2], cov, CROSS_TERM_DRAWS, SEED, "student_t", CROSS_TERM_NU)
    measured = sample_variance(plus) - sample_variance(minus)
    check(
        relative_error(measured, target) <= TOL_CROSS_TERM,
        "the student_t returns must share the matched factor across the assets of a draw: check each asset's return",
    )


def test_same_seed_gives_the_same_losses() -> None:
    for family, nu in (("gaussian", None), ("student_t", NU)):
        first = sol.simulate_losses(POSITIONS, COV, 500, SEED, family, nu)
        second = sol.simulate_losses(POSITIONS, COV, 500, SEED, family, nu)
        check(first == second, "the same seed must give the same losses (determinism)")


@pytest.mark.parametrize("family, nu", [("gaussian", None), ("student_t", NU)])
def test_different_seed_gives_different_losses(family: str, nu: int | None) -> None:
    first = sol.simulate_losses(POSITIONS, COV, 500, SEED, family, nu)
    other = sol.simulate_losses(POSITIONS, COV, 500, SEED + 1, family, nu)
    check(first != other, "a different seed must give different draws")


# --- simulate_losses: named conditions -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "family", ["Gaussian", "t", "student-t", " gaussian", "gaussian ", "student_t ", "student_tx", "", None]
)
def test_unknown_family_is_rejected(family: Any) -> None:
    expect_value_error(
        lambda: sol.simulate_losses(POSITIONS, COV, 10, SEED, family, NU),
        'family must be "gaussian" or "student_t"',
    )


def test_gaussian_accepts_no_degrees_of_freedom() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, 10, SEED, "gaussian", None)
    check(len(losses) == 10, "the gaussian family must accept nu = None")


@pytest.mark.parametrize("nu", [5, 3.0, False, True, "3", 0, 2])
def test_gaussian_rejects_a_degrees_of_freedom(nu: Any) -> None:
    expect_value_error(
        lambda: sol.simulate_losses(POSITIONS, COV, 10, SEED, "gaussian", nu),
        "the gaussian family must reject a non-None nu",
    )


def test_student_t_requires_degrees_of_freedom() -> None:
    expect_value_error(
        lambda: sol.simulate_losses(POSITIONS, COV, 10, SEED, "student_t", None),
        "the student_t family must reject nu = None",
    )


@pytest.mark.parametrize("nu", [2, 1, 0, -3])
def test_student_t_rejects_nu_at_or_below_two(nu: int) -> None:
    expect_value_error(
        lambda: sol.simulate_losses(POSITIONS, COV, 10, SEED, "student_t", nu),
        "the student_t family must reject nu of 2 or less",
    )


def test_student_t_accepts_nu_just_above_two() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, 10, SEED, "student_t", 3)
    check(len(losses) == 10, "the student_t family must accept nu = 3")


@pytest.mark.parametrize("n_draws", [0, -1, -5])
@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_draw_count_of_zero_or_less_is_rejected(n_draws: int, family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses(POSITIONS, COV, n_draws, SEED, family, nu),
        "n_draws must be 1 or more: zero or a negative draw count must raise ValueError",
    )


def test_gaussian_losses_are_rounded_once_not_truncated() -> None:
    # One position of 100 cents on a return with sd 2 %, so the loss is normal with variance 4 cents squared. Rounding
    # to the nearest cent adds about 1/12 to the variance, to 4 + 1/12 (about 4.08). Truncating toward zero instead
    # gives a variance of about 2.7, which is far from 4 + 1/12.
    losses = sol.simulate_losses([100], [[4e-4]], 20_000, SEED, "gaussian", None)
    check(
        abs(sample_variance(losses) - (4.0 + 1.0 / 12.0)) <= 0.3,
        "losses must be rounded once to the nearest cent with round(), not truncated",
    )


def test_loss_is_rounded_once_for_the_portfolio_not_per_position() -> None:
    # Two positions of 1000 cents, the same seed and draw count in every call. The loss of the pair is round(-(w . R)),
    # rounded once. Rounding each position's loss first and then adding is a different rule, and the two rules give
    # different values on some draws. The test needs only that the pair's loss differs from the sum of the single-
    # position losses on at least one draw; it does not depend on the random stream order.
    cov = [[4e-4, 1e-4], [1e-4, 9e-4]]
    both = sol.simulate_losses([1_000, 1_000], cov, 2_000, SEED, "gaussian", None)
    first = sol.simulate_losses([1_000, 0], cov, 2_000, SEED, "gaussian", None)
    second = sol.simulate_losses([0, 1_000], cov, 2_000, SEED, "gaussian", None)
    check(
        any(b != f + s for b, f, s in zip(both, first, second, strict=True)),
        "the portfolio loss must be rounded once: rounding each position's loss and then adding is not the rule",
    )


def test_no_function_prints(capsys: pytest.CaptureFixture[str]) -> None:
    # Every function runs at the sizes the instances use and at the edges they can reach: the instance's own draw count
    # for both families, 50 draws and 100 draws (a multiple of 100), and every nu of 3 to 8 in simulate_losses and
    # matched_scale, so a print that shows only on long runs, on a multiple of 100 draws, or at one nu is caught as
    # well. quantile_99 runs on one loss, on 100 losses and on 101 losses.
    for nu in range(3, 9):
        sol.matched_scale(nu)
        sol.simulate_losses(POSITIONS, COV, 50, SEED, "student_t", nu)
    sol.simulate_losses(POSITIONS, COV, N_DRAWS, SEED, "gaussian", None)
    sol.simulate_losses(POSITIONS, COV, N_DRAWS, SEED, "student_t", NU)
    sol.simulate_losses(POSITIONS, COV, 50, SEED, "gaussian", None)
    sol.simulate_losses(POSITIONS, COV, 100, SEED, "gaussian", None)
    sol.simulate_losses(POSITIONS, COV, 100, SEED, "student_t", 5)
    sol.quantile_99([3, 1, 2])
    sol.quantile_99([7])
    sol.quantile_99(list(range(100)))
    sol.quantile_99(list(range(101)))
    captured = capsys.readouterr()
    check(captured.out == "" and captured.err == "", "no function may print: the functions return their values only")


def test_one_draw_is_accepted() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, 1, SEED, "gaussian", None)
    check(len(losses) == 1, "n_draws = 1 must return one loss, the boundary above zero")


@pytest.mark.parametrize("n_draws", [10.0, True, False, "10", None])
@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_draw_count_must_be_a_whole_number(n_draws: Any, family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses(POSITIONS, COV, n_draws, SEED, family, nu),
        "n_draws must be a whole number, and a float or a boolean is not",
    )


@pytest.mark.parametrize("positions", [[1.0, 2], [True, 2], [1000, "1000"], [1000, 1.0], [1000, True], [None, 1000]])
@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_positions_must_be_whole_cents(positions: Any, family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses(positions, [[1e-4, 0.0], [0.0, 1e-4]], 10, SEED, family, nu),
        "position_cents must hold whole numbers of cents: a float or a boolean is rejected",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_positions_must_not_be_empty(family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([], [], 10, SEED, family, nu),
        "position_cents must not be empty",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_covariance_must_match_the_number_of_positions(family: str, nu: int | None) -> None:
    three_by_three = [[4e-4, 0.0, 0.0], [0.0, 4e-4, 0.0], [0.0, 0.0, 4e-4]]
    expect_value_error(
        lambda: sol.simulate_losses(POSITIONS[:2], three_by_three, 10, SEED, family, nu),
        "cov must have one row and one column per position",
    )


@pytest.mark.parametrize("skew", [[[4e-4, 1e-4], [2e-4, 9e-4]], [[4e-4, 2e-4], [1e-4, 9e-4]]])
@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_covariance_must_be_symmetric(skew: list[list[float]], family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000], skew, 10, SEED, family, nu),
        "cov must be symmetric",
    )


@pytest.mark.parametrize("pair", [(0, 1), (0, 2), (1, 2)])
@pytest.mark.parametrize("upper", [True, False])
def test_covariance_symmetry_is_checked_for_every_pair(pair: tuple[int, int], upper: bool) -> None:
    # Three positions. Only one entry of one off-diagonal pair is set, so the matrix is asymmetric in that pair alone.
    # The pair (1, 2) is the one a check of the first row alone would miss.
    cov = [[4e-4, 0.0, 0.0], [0.0, 4e-4, 0.0], [0.0, 0.0, 4e-4]]
    i, j = pair
    if upper:
        cov[i][j] = 1e-5
    else:
        cov[j][i] = 1e-5
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000, 1_000], cov, 10, SEED, "gaussian", None),
        "cov must be symmetric in every pair of entries, not only the first row",
    )


@pytest.mark.parametrize(
    "ragged",
    [
        [[4e-4]],
        [[4e-4, 0.0], [0.0]],
        [[4e-4, 0.0, 0.0], [0.0, 4e-4]],
        [[4e-4, 0.0], [0.0, 4e-4], [0.0, 0.0]],
        [[4e-4, 0.0], [0.0, 4e-4, 0.0]],
    ],
)
@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_covariance_must_be_square_with_one_row_per_position(
    ragged: list[list[float]], family: str, nu: int | None
) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000], ragged, 10, SEED, family, nu),
        "cov must be a square matrix with one row and one column per position",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_indefinite_covariance_is_rejected(family: str, nu: int | None) -> None:
    indefinite = [[1.0, 2.0], [2.0, 1.0]]
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000], indefinite, 10, SEED, family, nu),
        "cov must be positive definite: a pivot is not above zero",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_negative_second_pivot_is_rejected(family: str, nu: int | None) -> None:
    # The first pivot is 4e-4 (above zero) and the second is -9e-4 (below zero): the check must read every pivot.
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000], [[4e-4, 0.0], [0.0, -9e-4]], 10, SEED, family, nu),
        "cov must be positive definite: a negative second pivot is not above zero",
    )


def test_two_position_positive_definite_covariance_is_accepted() -> None:
    # The boundary on the other side: a symmetric matrix whose pivots are all above zero must not be rejected.
    losses = sol.simulate_losses([1_000, 1_000], [[4e-4, 1e-4], [1e-4, 9e-4]], 100, SEED, "gaussian", None)
    check(len(losses) == 100 and all(type(x) is int for x in losses), "a 2 x 2 positive definite cov must be accepted")


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_singular_covariance_is_rejected(family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([1_000], [[0.0]], 10, SEED, family, nu),
        "cov must be positive definite: a zero pivot is not above zero",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_singular_covariance_with_a_zero_second_pivot_is_rejected(family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000], [[1.0, 1.0], [1.0, 1.0]], 10, SEED, family, nu),
        "cov must be positive definite: the second pivot is zero",
    )


@pytest.mark.parametrize("cov", [[[0.0, 0.0], [0.0, 4e-4]], [[-4e-4, 0.0], [0.0, 4e-4]]])
@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_first_pivot_must_be_positive(cov: list[list[float]], family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000], cov, 10, SEED, family, nu),
        "cov must be positive definite: the first pivot must be above zero",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_negative_variance_is_rejected(family: str, nu: int | None) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([1_000], [[-4e-4]], 10, SEED, family, nu),
        "cov must be positive definite: a negative variance is not positive",
    )


def test_one_position_with_positive_variance_is_accepted() -> None:
    losses = sol.simulate_losses([1_000_000], [[4e-4]], 100, SEED, "gaussian", None)
    check(len(losses) == 100 and all(type(x) is int for x in losses), "a positive 1 x 1 covariance must be accepted")


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_one_position_with_a_tiny_positive_variance_is_accepted(family: str, nu: int | None) -> None:
    # A variance of 1e-14 is positive, so the one-position portfolio is valid: a pivot check with an absolute
    # tolerance above 1e-14 would wrongly reject it.
    losses = sol.simulate_losses([1_000_000], [[1e-14]], 100, SEED, family, nu)
    check(
        len(losses) == 100 and all(type(x) is int for x in losses),
        "a one-position covariance with a tiny positive variance must be accepted",
    )


def test_one_position_with_a_tiny_positive_variance_has_the_right_loss_variance() -> None:
    # Position 10^13 cents and variance 1e-14: the loss has variance (10^13)^2 x 1e-14 = 10^12 cents squared, a sd of
    # 10^6 cents, so rounding to the whole cent does not move the sample variance.
    losses = sol.simulate_losses([10**13], [[1e-14]], 20_000, SEED, "gaussian", None)
    check(
        relative_error(sample_variance(losses), 1e12) <= TOL_GAUSSIAN_VARIANCE,
        "the loss variance of a one-position portfolio must be w' Sigma w, also for a tiny positive variance",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_two_positions_with_tiny_positive_covariance_are_accepted(family: str, nu: int | None) -> None:
    # Symmetric, with both pivots (1e-14 and about 9e-14) positive: a valid input that must not be rejected.
    losses = sol.simulate_losses([1_000, 1_000], [[1e-14, 1e-15], [1e-15, 9e-14]], 100, SEED, family, nu)
    check(
        len(losses) == 100 and all(type(x) is int for x in losses),
        "a 2 x 2 positive definite covariance with entries of order 1e-14 must be accepted",
    )


# --- quantile_99 -----------------------------------------------------------------------------------------------------


def test_quantile_99_is_the_exact_order_statistic() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, N_DRAWS, SEED, "gaussian", None)
    k = math.ceil(Fraction(99, 100) * len(losses))
    check(
        sol.quantile_99(losses) == sorted(losses)[k - 1],
        "quantile_99 must be the order statistic with index ceil(0.99 n)",
    )


def test_quantile_99_convention_on_small_lists() -> None:
    check(sol.quantile_99(list(range(1, 100))) == 99, "for n = 99 the index is ceil(98.01) = 99, the largest value")
    check(sol.quantile_99(list(range(1, 101))) == 99, "for n = 100 the index is ceil(99) = 99, the 99th smallest")
    check(sol.quantile_99(list(range(1, 102))) == 100, "for n = 101 the index is ceil(99.99) = 100, not 99")
    check(sol.quantile_99(list(range(1, 3))) == 2, "for n = 2 the index is ceil(1.98) = 2, the largest value")


def test_quantile_99_returns_a_tied_value_when_losses_tie() -> None:
    check(sol.quantile_99([3, 3, 1, 3, 2]) == 3, "with ties the 99% loss is the tied value at the ceiling index")


def test_quantile_99_ignores_the_input_order() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, 500, SEED, "gaussian", None)
    shuffled = losses[:]
    random.Random(SEED).shuffle(shuffled)
    check(sol.quantile_99(losses) == sol.quantile_99(shuffled), "quantile_99 must not depend on the order of the list")


def test_quantile_99_of_one_loss_is_that_loss() -> None:
    check(sol.quantile_99([7]) == 7, "for n = 1 the index is ceil(0.99) = 1, the only value")


def test_quantile_99_rejects_an_empty_list() -> None:
    expect_value_error(lambda: sol.quantile_99([]), "quantile_99 must reject an empty list")


@pytest.mark.parametrize("losses", [[1.0, 2], [True, 2], ["7"], [None], [5, 2.0], [5, None], [5, True]])
def test_quantile_99_rejects_non_whole_losses(losses: Any) -> None:
    expect_value_error(lambda: sol.quantile_99(losses), "quantile_99 must reject a float or a boolean loss")


def test_quantile_99_returns_an_int() -> None:
    result = sol.quantile_99(sol.simulate_losses(POSITIONS, COV, 300, SEED, "student_t", NU))
    check(type(result) is int, "quantile_99 must return an int number of cents")
