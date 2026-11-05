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
# its target by more than any fixed tolerance (the reference's relative error is 1.022 at seed 1093 with nu = 3).
# Over seeds 0 to 1999 the reference's largest relative error was 0.126 at nu = 5, 0.097 at nu = 6, 0.073 at nu = 7
# and 0.062 at nu = 8 (the unrounded maxima are 0.1259, 0.0967, 0.0728 and 0.0624, from the seed-by-seed sweep of the
# reference against make_instance). The tolerance 0.30 is about 2.4 times the largest of these (0.30 / 0.1259 = 2.38).
# Against a missing matched factor (an inflation of nu / (nu - 2), which is 1.67, 1.50, 1.40 and 1.33 at nu = 5 to 8),
# the check fails on every seed tested at nu = 5 and 6 (347 and 317 seeds, seeds 0 to 1999), and on 342 of 343 seeds
# at nu = 7 and 288 of 317 at nu = 8.
TOL_GAUSSIAN_VARIANCE = 0.10
TOL_T_VARIANCE = 0.30
MIN_NU_FOR_T_VARIANCE_CHECK = 5
# The Student-t cross term: two assets with correlation 0.8, 100,000 draws, nu of 5. The reference's largest relative
# error over seeds 0 to 49 is 0.024. A matched factor applied to the first asset only moves the cross term by 7 % to
# 9 %, and a separate chi-square variable for each asset after the first by 14 % to 16 % (both measured at seeds 0 to
# 9, relative error 0.068 to 0.086 and 0.141 to 0.161). The tolerance 0.05 lies above the reference's 0.024 and below
# both smallest mutant errors, 0.068 and 0.141.
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
    check(abs(sol.matched_scale(3) - (3 - 2) / 3) <= 1e-12, "matched_scale must return (nu - 2) / nu at nu = 3")


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


def test_student_t_mean_absolute_loss_matches_the_matched_scale() -> None:
    # For one position w with variance sigma^2, the loss is -w R with R = sqrt((nu - 2) / nu) sigma X_nu, where X_nu
    # is a Student-t variable. So E|loss| = w sigma sqrt((nu - 2) / nu) E|X_nu| for every nu of 3 to 8. This is
    # checked at nu = 3 and 4 too, where the variance is not checked: a matched factor left out there inflates
    # E|loss| by sqrt(nu / (nu - 2)), about 1.73 at nu = 3, far outside the 5 % tolerance over 20,000 draws.
    w = 1_000_000
    sigma = math.sqrt(4e-4)
    for nu in range(3, 9):
        target = w * sigma * math.sqrt((nu - 2) / nu) * _mean_abs_t(nu)
        losses = sol.simulate_losses([w], [[4e-4]], 20_000, SEED, "student_t", nu)
        measured = sum(abs(x) for x in losses) / len(losses)
        check(
            relative_error(measured, target) <= 0.05,
            "the student_t mean absolute loss must match the matched scale: check the factor (nu - 2) / nu",
        )


def _mean_abs_t(nu: int) -> float:
    """E|X| for a Student-t variable X with nu > 1 degrees of freedom, from the Gamma function."""
    return 2.0 * math.sqrt(nu) * math.gamma((nu + 1) / 2) / (math.sqrt(math.pi) * (nu - 1) * math.gamma(nu / 2))


def test_student_t_draws_do_not_share_chi_square() -> None:
    # Each Student-t draw has its own chi-square variable (Conventions item 5). Then every pair of draws one apart
    # (i, i + 1), two apart (i, i + 2) and three apart (i, i + 3) is independent, and P(both |loss| above the median)
    # is 1/4 for each pair. The pairs are taken in non-overlapping blocks: for lag d, the offsets 0 to 2d - 1 each give
    # the pairs (i, i + d) with i stepping by 2d. The test accepts 1/4 within five standard errors for every block of
    # lags 1 to 3, over 40,000 draws at nu = 3. The sharings measured on seeds 0 to 49 fail it as follows: draws 2k and
    # 2k + 1 sharing one variable fails on 50 of 50 seeds (lag 1), draws 4j and 4j + 2 on 50 of 50 (lag 2), and draws
    # 6j and 6j + 3 on 39 of 50 (lag 3). A sharing of one pair of draws at a lag of four or more is not read here:
    # disjoint pairs of that kind pass on all 50 seeds, while a chain with draws 4j and 4j + 4 sharing one variable
    # fails on 38 of 50.
    n = 40_000
    losses = sol.simulate_losses([1_000_000], [[4e-4]], n, SEED, "student_t", 3)
    magnitudes = [abs(x) for x in losses]
    median = sorted(magnitudes)[n // 2]
    above = [m > median for m in magnitudes]
    for lag in (1, 2, 3):
        for offset in range(2 * lag):
            pairs = [(above[i], above[i + lag]) for i in range(offset, n - lag, 2 * lag)]
            share = sum(a and b for a, b in pairs) / len(pairs)
            standard_error = math.sqrt(0.25 * 0.75 / len(pairs))
            check(
                abs(share - 0.25) <= 5 * standard_error,
                "each student_t draw must have its own chi-square variable: draws must not share one across pairs",
            )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_a_short_position_is_valid_and_reverses_its_loss(family: str, nu: int | None) -> None:
    # A negative position is a short position, and it is valid input (the Conditions). The loss is linear in the
    # positions and round() is symmetric about zero, so flipping every sign flips every loss exactly, for any seed.
    cov = [[4e-4, 1e-4], [1e-4, 9e-4]]
    long_pair = sol.simulate_losses([1_000, 2_000], cov, 300, SEED, family, nu)
    mixed = sol.simulate_losses([1_000, -2_000], cov, 300, SEED, family, nu)
    flipped = sol.simulate_losses([-1_000, -2_000], cov, 300, SEED, family, nu)
    mixed_flipped = sol.simulate_losses([-1_000, 2_000], cov, 300, SEED, family, nu)
    check(
        flipped == [-x for x in long_pair],
        "negating every position must negate every loss: a negative position is a valid short position",
    )
    check(
        mixed_flipped == [-x for x in mixed],
        "a short position must reverse its own contribution to the loss, with the other positions unchanged",
    )


def _lower_factor(cov: list[list[float]]) -> list[list[float]]:
    """The lower-triangular L with L L^T = cov, computed row by row, for the instance's positive definite covariance."""
    n = len(cov)
    factor = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            inner = sum(factor[i][k] * factor[j][k] for k in range(j))
            factor[i][j] = math.sqrt(cov[i][i] - inner) if i == j else (cov[i][j] - inner) / factor[j][j]
    return factor


def test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return() -> None:
    # Conventions item 5 fixes the Gaussian stream: draw d takes its n normals z in position order from
    # random.Random(seed).gauss(0, 1), and the loss is -sum_i w_i (L z)_i, rounded once. The unrounded loss is
    # recomputed here from the same stream, so each reported loss lies within half a cent of it. The loss with the
    # opposite sign lies about twice the weighted return away, so it fails.
    n = len(POSITIONS)
    losses = sol.simulate_losses(POSITIONS, COV, 3, SEED, "gaussian", None)
    rng = random.Random(SEED)
    factor = _lower_factor(COV)
    for loss in losses:
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        unrounded = -sum(POSITIONS[i] * sum(factor[i][k] * z[k] for k in range(i + 1)) for i in range(n))
        check(
            abs(loss - unrounded) <= 0.5 + 1e-6,
            "the gaussian losses must be -sum_i w_i (L z)_i from the frozen stream: check the sign and normal order",
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
    # well. quantile_99 runs on three losses, on one loss, on 100 losses and on 101 losses.
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


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_covariance_must_be_symmetric_at_a_tiny_scale(family: str, nu: int | None) -> None:
    # Entries of order 1e-14. The two off-diagonal entries differ by 1e-15, a tenth of the first variance, so the matrix
    # is asymmetric at this scale. Both pivots are positive, so only the symmetry condition is violated. A symmetry
    # check with an absolute tolerance above 1e-15 would accept it.
    cov = [[1e-14, 1e-15], [2e-15, 9e-14]]
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000], cov, 10, SEED, family, nu),
        "cov must be symmetric at every scale: entries of order 1e-14 that differ by a tenth are not symmetric",
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


@pytest.mark.parametrize(
    "cov",
    [
        # Only the last pivot fails: the first two are 1e-4 and 1e-4, above zero.
        [[1e-4, 0.0, 0.0], [0.0, 1e-4, 0.0], [0.0, 0.0, -1e-4]],
        # Only the last pivot fails: the first two are 1 and 1, the last is 1 - (1 + 1) = -1.
        [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
        # Singular: the last pivot is 2 - (1 + 1) = 0, which is not above zero.
        [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 2.0]],
    ],
)
@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_three_position_covariance_must_be_positive_definite(
    cov: list[list[float]], family: str, nu: int | None
) -> None:
    expect_value_error(
        lambda: sol.simulate_losses([1_000, 1_000, 1_000], cov, 10, SEED, family, nu),
        "cov must be positive definite: the last Cholesky pivot of a three-position covariance must be above zero",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
def test_three_position_positive_definite_covariance_is_accepted(family: str, nu: int | None) -> None:
    # Tridiagonal with diagonal 4e-4 and off-diagonal 1e-4: eigenvalues 4e-4 and 4e-4 +/- 1.41e-4, all positive.
    cov = [[4e-4, 1e-4, 0.0], [1e-4, 4e-4, 1e-4], [0.0, 1e-4, 4e-4]]
    losses = sol.simulate_losses([1_000, 1_000, 1_000], cov, 100, SEED, family, nu)
    check(
        len(losses) == 100 and all(type(x) is int for x in losses),
        "a 3 x 3 positive definite covariance must be accepted",
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
@pytest.mark.parametrize("variance", [1e-16, 1e-30])
def test_one_position_with_a_variance_of_1e_minus16_or_1e_minus30_is_accepted(
    family: str, nu: int | None, variance: float
) -> None:
    # A variance of 1e-16 or 1e-30 is positive, so the one-position portfolio is valid. A pivot check with an absolute
    # tolerance above these values (for example pivot > 1e-15) would wrongly reject it.
    losses = sol.simulate_losses([1_000_000], [[variance]], 100, SEED, family, nu)
    check(
        len(losses) == 100 and all(type(x) is int for x in losses),
        "a one-position covariance with a tiny positive variance must be accepted",
    )


@pytest.mark.parametrize("family, nu", FAMILY_CASES)
@pytest.mark.parametrize("scale", [1e-16, 1e-30])
def test_two_positions_with_covariance_of_order_1e_minus16_or_1e_minus30_are_accepted(
    family: str, nu: int | None, scale: float
) -> None:
    # Entries of order scale, both pivots (scale and 0.89 scale) positive: a valid input that a pivot tolerance above
    # 1e-15 would wrongly reject.
    off = scale / 10
    cov = [[scale, off], [off, 0.9 * scale]]
    losses = sol.simulate_losses([1_000_000, 1_000_000], cov, 100, SEED, family, nu)
    check(
        len(losses) == 100 and all(type(x) is int for x in losses),
        "a 2 x 2 positive definite covariance with tiny entries must be accepted",
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
    check(sol.quantile_99(list(range(1, 100))) == 99, "quantile_99 must use the ceiling index ceil(0.99 n) at n = 99")
    check(sol.quantile_99(list(range(1, 101))) == 99, "quantile_99 must use the ceiling index ceil(0.99 n) at n = 100")
    check(
        sol.quantile_99(list(range(1, 102))) == 100,
        "quantile_99 must use the ceiling index ceil(0.99 n) at n = 101, where the floor index is one lower",
    )
    check(sol.quantile_99(list(range(1, 3))) == 2, "quantile_99 must use the ceiling index ceil(0.99 n) at n = 2")


def test_quantile_99_returns_a_tied_value_when_losses_tie() -> None:
    check(sol.quantile_99([3, 3, 1, 3, 2]) == 3, "with ties the 99% loss is the tied value at the ceiling index")


def test_quantile_99_ignores_the_input_order() -> None:
    losses = sol.simulate_losses(POSITIONS, COV, 500, SEED, "gaussian", None)
    shuffled = losses[:]
    random.Random(SEED).shuffle(shuffled)
    check(sol.quantile_99(losses) == sol.quantile_99(shuffled), "quantile_99 must not depend on the order of the list")


def test_quantile_99_of_one_loss_is_that_loss() -> None:
    check(sol.quantile_99([7]) == 7, "quantile_99 of a list of one loss must return that loss")


def test_quantile_99_rejects_an_empty_list() -> None:
    expect_value_error(lambda: sol.quantile_99([]), "quantile_99 must reject an empty list")


@pytest.mark.parametrize("losses", [[1.0, 2], [True, 2], ["7"], [None], [5, 2.0], [5, None], [5, True]])
def test_quantile_99_rejects_non_whole_losses(losses: Any) -> None:
    expect_value_error(lambda: sol.quantile_99(losses), "quantile_99 must reject a float or a boolean loss")


def test_quantile_99_returns_an_int() -> None:
    result = sol.quantile_99(sol.simulate_losses(POSITIONS, COV, 300, SEED, "student_t", NU))
    check(type(result) is int, "quantile_99 must return an int number of cents")
