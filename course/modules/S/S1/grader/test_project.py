"""Autograder test suite for module S1 project: Power analysis for a strategy.

All tests check properties, invariants, and exact conditions on the instance.
No expected numbers are hard-coded in failure messages.
"""

from __future__ import annotations

import math
import os
import random
import statistics
from collections.abc import Callable

try:
    import sharpe_power as sol  # type: ignore[import-not-found]
except ImportError:
    try:
        from . import reference as sol  # type: ignore[import-not-found, no-redef]
    except ImportError:
        import reference as sol  # type: ignore[import-not-found, no-redef]

try:
    from instance import make_instance  # type: ignore[import-not-found]
except ImportError:
    from .instance import make_instance  # type: ignore[import-not-found]

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
SR_ANN: float = INST["sr_ann"]
PERIODS_PER_YEAR: int = INST["periods_per_year"]
ALPHA: float = INST["alpha"]
POWER: float = INST["power"]
SR_PER_PERIOD: float = INST["sr_per_period"]
RETURNS: list[float] = INST["returns"]


def check(condition: bool, message: str) -> None:
    """Fail with message when condition is false. The message names the property; it never shows a value."""
    __tracebackhide__ = True
    if not condition:
        raise AssertionError(message)


def expect_value_error(call: Callable[[], object], message: str) -> None:
    """Pass only when call raises ValueError. Any other exception or no exception fails with message."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    except Exception:
        raise AssertionError(message + " (a different exception type was raised)") from None
    raise AssertionError(message + " (no ValueError was raised)")


# --- Instance sanity --------------------------------------------------------------------------------------------


def test_instance_is_simulated() -> None:
    check(INST.get("label") == "SIMULATED", "instance must be labelled SIMULATED")
    check(0.20 <= SR_ANN <= 2.0, "instance annualized Sharpe ratio must lie in [0.20, 2.0]")
    check(PERIODS_PER_YEAR in (12, 52, 252), "instance periods per year must be one of {12, 52, 252}")
    check(0.0 < ALPHA < 1.0, "instance alpha must lie strictly in (0, 1)")
    check(0.50 <= POWER < 1.0, "instance power must lie in [0.50, 1.0)")
    check(len(RETURNS) == 30, "instance sample returns must have length 30")


# --- sharpe_hat tests -------------------------------------------------------------------------------------------


def test_sharpe_hat_exact_rational() -> None:
    # Compute mean and unbiased sample variance in high precision
    n = len(RETURNS)
    mean_val = sum(RETURNS) / n
    var_val = sum((r - mean_val) ** 2 for r in RETURNS) / (n - 1)
    expected = mean_val / math.sqrt(var_val)

    actual = sol.sharpe_hat(RETURNS)
    check(isinstance(actual, float), "sharpe_hat must return a float")

    # Kills divisor mutant (dividing by n instead of n-1)
    biased_var = sum((r - mean_val) ** 2 for r in RETURNS) / n
    biased_val = mean_val / math.sqrt(biased_var)

    check(abs(actual - expected) < 1e-11 * max(1.0, abs(expected)), "sharpe_hat must use sample std with divisor n-1")
    check(abs(actual - biased_val) > 1e-6, "sharpe_hat must not divide by n in sample variance (divisor n mutant)")


def test_sharpe_hat_raises_on_fewer_than_two_returns() -> None:
    expect_value_error(lambda: sol.sharpe_hat([]), "sharpe_hat must raise ValueError on empty return list")
    expect_value_error(lambda: sol.sharpe_hat([0.05]), "sharpe_hat must raise ValueError on single return")


def test_sharpe_hat_raises_on_zero_variance() -> None:
    expect_value_error(
        lambda: sol.sharpe_hat([0.02, 0.02, 0.02]),
        "sharpe_hat must raise ValueError when sample variance is zero",
    )


# --- analytic_years tests ---------------------------------------------------------------------------------------


def test_analytic_years_solves_power_equation() -> None:
    years = sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)
    check(isinstance(years, float), "analytic_years must return a float")
    check(years > 0.0, "analytic_years must return a strictly positive duration")

    # Verify that the returned years solves the power equation
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - ALPHA)
    t_periods = years * PERIODS_PER_YEAR
    sr_period = SR_ANN / math.sqrt(PERIODS_PER_YEAR)
    inflation = math.sqrt(1.0 + (sr_period**2) / 2.0)

    # Power achieved by test sqrt(T)*hSR >= z_alpha:
    # 1 - Phi((z_alpha - sqrt(T)*SR) / inflation)
    z_stat = (z_alpha - math.sqrt(t_periods) * sr_period) / inflation
    solved_power = 1.0 - dist.cdf(z_stat)

    check(
        abs(solved_power - POWER) < 1e-8,
        "analytic_years does not satisfy the asymptotic power equation (kills naive variance or missing inflation)",
    )


def test_analytic_years_kills_naive_variance_mutant() -> None:
    # Naive variance without inflation factor 1 + SR^2/2
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - ALPHA)
    z_power = dist.inv_cdf(POWER)
    naive_years = ((z_alpha + z_power) ** 2) / (SR_ANN**2)

    actual = sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)
    # The inflation factor is sqrt(1 + SR^2/2) > 1, so actual years must strictly exceed naive years
    check(
        actual > naive_years + 1e-6,
        "analytic_years must account for variance inflation under the alternative (naive variance mutant)",
    )


def test_analytic_years_kills_periods_for_years_mutant() -> None:
    actual = sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)
    # If periods were returned instead of years, it would differ by a factor of PERIODS_PER_YEAR
    check(
        actual < actual * PERIODS_PER_YEAR * 0.5 or PERIODS_PER_YEAR == 1,
        "analytic_years must return duration in years, not in periods (periods for years mutant)",
    )


def test_analytic_years_error_conditions() -> None:
    expect_value_error(
        lambda: sol.analytic_years(0.0, PERIODS_PER_YEAR, ALPHA, POWER),
        "analytic_years must raise ValueError when sr_ann is zero",
    )
    expect_value_error(
        lambda: sol.analytic_years(-0.5, PERIODS_PER_YEAR, ALPHA, POWER),
        "analytic_years must raise ValueError when sr_ann is negative",
    )
    expect_value_error(
        lambda: sol.analytic_years(SR_ANN, 0, ALPHA, POWER),
        "analytic_years must raise ValueError when periods_per_year < 1",
    )
    expect_value_error(
        lambda: sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, 0.0, POWER),
        "analytic_years must raise ValueError when alpha is zero",
    )
    expect_value_error(
        lambda: sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, 1.0, POWER),
        "analytic_years must raise ValueError when alpha is 1",
    )
    expect_value_error(
        lambda: sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, ALPHA, 0.0),
        "analytic_years must raise ValueError when power is zero",
    )
    expect_value_error(
        lambda: sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, ALPHA, 1.0),
        "analytic_years must raise ValueError when power is 1",
    )


# --- required_periods tests -------------------------------------------------------------------------------------


def test_required_periods_type_and_ceiling() -> None:
    years = sol.analytic_years(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)
    expected_periods = math.ceil(years * PERIODS_PER_YEAR)

    actual = sol.required_periods(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)
    check(type(actual) is int, "required_periods must return an int, not a float")
    check(actual == expected_periods, "required_periods must be ceil(years * periods_per_year)")


def test_required_periods_achieves_power() -> None:
    actual = sol.required_periods(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)

    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - ALPHA)
    sr_period = SR_ANN / math.sqrt(PERIODS_PER_YEAR)
    inflation = math.sqrt(1.0 + (sr_period**2) / 2.0)

    # Power at actual periods
    z_stat = (z_alpha - math.sqrt(actual) * sr_period) / inflation
    power_at_actual = 1.0 - dist.cdf(z_stat)
    check(
        power_at_actual >= POWER - 1e-12,
        "required_periods must achieve at least the target power",
    )

    # Power at actual - 1 must fall strictly below target (kills floor / off-by-one mutant)
    if actual > 1:
        z_stat_prev = (z_alpha - math.sqrt(actual - 1) * sr_period) / inflation
        power_at_prev = 1.0 - dist.cdf(z_stat_prev)
        check(
            power_at_prev < POWER,
            "required_periods minus one must not reach target power (smallest integer condition)",
        )


def test_required_periods_monotonicity() -> None:
    # A strategy with 25% higher Sharpe ratio requires strictly fewer or equal periods
    periods_low = sol.required_periods(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)
    periods_high = sol.required_periods(SR_ANN * 1.25, PERIODS_PER_YEAR, ALPHA, POWER)
    check(
        periods_high <= periods_low,
        "required_periods must be non-increasing in sr_ann (monotonicity condition)",
    )


def test_required_periods_error_conditions() -> None:
    expect_value_error(
        lambda: sol.required_periods(0.0, PERIODS_PER_YEAR, ALPHA, POWER),
        "required_periods must raise ValueError when sr_ann is zero",
    )
    expect_value_error(
        lambda: sol.required_periods(SR_ANN, 0, ALPHA, POWER),
        "required_periods must raise ValueError when periods_per_year < 1",
    )
    expect_value_error(
        lambda: sol.required_periods(SR_ANN, PERIODS_PER_YEAR, -0.05, POWER),
        "required_periods must raise ValueError when alpha is outside (0, 1)",
    )
    expect_value_error(
        lambda: sol.required_periods(SR_ANN, PERIODS_PER_YEAR, ALPHA, 1.2),
        "required_periods must raise ValueError when power is outside (0, 1)",
    )


# --- simulated_power tests --------------------------------------------------------------------------------------


def test_simulated_power_null_size() -> None:
    # Under H0: sr_per_period = 0, rejection rate should match alpha within 4 binomial standard errors
    n_sims = 1000
    periods = 60
    rejection_rate = sol.simulated_power(periods, 0.0, ALPHA, n_sims, seed=SEED + 100)

    se = math.sqrt(ALPHA * (1.0 - ALPHA) / n_sims)
    check(
        abs(rejection_rate - ALPHA) <= 4.0 * se + 0.01,
        "simulated_power under the null must be within 4 binomial SEs of alpha (kills single-path mutant)",
    )


def test_simulated_power_power_band() -> None:
    # At the instance's required periods, simulated power should match target power within sampling error
    n_sims = 1000
    periods = sol.required_periods(SR_ANN, PERIODS_PER_YEAR, ALPHA, POWER)
    sim_power = sol.simulated_power(periods, SR_PER_PERIOD, ALPHA, n_sims, seed=SEED + 200)

    se = math.sqrt(POWER * (1.0 - POWER) / n_sims)
    # Measured finite-T approximation tolerance is <= 0.035 across all seeds
    band = 4.0 * se + 0.035
    check(
        abs(sim_power - POWER) <= band,
        "simulated_power at required_periods must lie within the confidence band around target power",
    )


def test_simulated_power_determinism_and_independence_from_global_random() -> None:
    # Must produce identical result for identical seed regardless of global random state
    random.seed(999999)
    run1 = sol.simulated_power(50, 0.1, 0.05, 200, seed=12345)

    random.seed(111111)
    _ = random.random()
    run2 = sol.simulated_power(50, 0.1, 0.05, 200, seed=12345)

    check(run1 == run2, "simulated_power must be deterministic and independent of global random state")


def test_simulated_power_error_conditions() -> None:
    expect_value_error(
        lambda: sol.simulated_power(1, 0.1, 0.05, 100, seed=1),
        "simulated_power must raise ValueError when periods < 2",
    )
    expect_value_error(
        lambda: sol.simulated_power(50, 0.1, 0.05, 0, seed=1),
        "simulated_power must raise ValueError when n_sims < 1",
    )
    expect_value_error(
        lambda: sol.simulated_power(50, 0.1, 0.0, 100, seed=1),
        "simulated_power must raise ValueError when alpha is zero",
    )
    expect_value_error(
        lambda: sol.simulated_power(50, 0.1, 1.0, 100, seed=1),
        "simulated_power must raise ValueError when alpha is 1",
    )


def test_large_instance_acceptance() -> None:
    # Kills threshold mutants that arbitrarily reject large valid inputs
    val = sol.simulated_power(1000, 0.05, 0.05, 1, seed=42)
    check(isinstance(val, float), "simulated_power must accept periods=1000, n_sims=1")
