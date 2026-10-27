"""Acceptance suite for the AP1 project: recovering the minimum-variance SDF (sdf_recovery.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your sdf_recovery.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number against the definitions of the AP1 lessons and the project
specification. A failure names the property it checks and the idea to revisit; it never prints the
expected value.
"""

from __future__ import annotations

import ast
import contextlib
import io
import math
import os
import sys
import warnings
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pytest
import sdf_recovery as sol
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
TRAIN: np.ndarray = INST["train"]
TEST: np.ndarray = INST["test"]
PRICES: np.ndarray = INST["prices"]
PROBS: np.ndarray = INST["probs"]
PAYOFFS: np.ndarray = INST["payoffs"]
WITH_NAN = TRAIN.copy()
WITH_NAN[1, 0] = np.nan
TEST_WITH_NAN = TEST.copy()
TEST_WITH_NAN[0, 0] = np.nan
WITH_INF = np.where(np.isnan(WITH_NAN), np.inf, WITH_NAN)
PRICES_WITH_NAN = np.where(np.arange(PRICES.size) == 0, np.nan, PRICES)
RISKY = TRAIN[:, 1:] if INST["riskless"] else TRAIN  # without the riskless payoff the SDF mean is free
RISKY_P = PRICES[1:] if INST["riskless"] else PRICES
ZERO_PROB = PROBS.copy()  # sums to one, with one state of probability zero
ZERO_PROB[0], ZERO_PROB[1] = 0.0, PROBS[0] + PROBS[1]
TEST_WITH_INF = TEST.copy()
TEST_WITH_INF[0, 0] = np.inf
PAYOFFS_WITH_NAN = PAYOFFS.copy()
PAYOFFS_WITH_NAN[0, 0] = np.nan
PAYOFFS_WITH_INF = PAYOFFS.copy()
PAYOFFS_WITH_INF[0, 0] = np.inf
PRICES_WITH_INF = np.where(np.arange(PRICES.size) == 0, np.inf, PRICES)
RISKY_WITH_NAN = RISKY.copy()  # built from RISKY, so the NaN is never dropped by the riskless column selection
RISKY_WITH_NAN[1, 0] = np.nan
RISKY_WITH_INF = np.where(np.isnan(RISKY_WITH_NAN), np.inf, RISKY_WITH_NAN)
RISKY_P_WITH_NAN = np.where(np.arange(RISKY_P.size) == 0, np.nan, RISKY_P)
RISKY_P_WITH_INF = np.where(np.arange(RISKY_P.size) == 0, np.inf, RISKY_P)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError: the grader checks the exception type."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError.")


def close(a: object, b: object, tol: float = 1e-8) -> bool:
    x, y = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return x.shape == y.shape and bool(np.all(np.isfinite(x))) and bool(np.allclose(x, y, rtol=tol, atol=tol))


def sample_x_star(x: np.ndarray, p: np.ndarray) -> np.ndarray:
    """The test's own x* values: x' b with E_T[x x'] b = p, solved by least squares."""
    b = np.linalg.lstsq(x.T @ x / x.shape[0], p, rcond=None)[0]
    return np.asarray(x @ b)


def orthogonal_noise(x: np.ndarray, rng: np.random.Generator, with_constant: bool = False) -> np.ndarray:
    """A random vector over the T observations with E_T[eps x] = 0 (and E_T[eps] = 0 if asked)."""
    basis = np.column_stack([np.ones(x.shape[0]), x]) if with_constant else x
    raw = rng.normal(0.0, 1.0, x.shape[0])
    coef = np.linalg.lstsq(basis, raw, rcond=None)[0]
    return np.asarray(raw - basis @ coef)


# ---------------------------------------------------------------- moments and x*


def test_second_moment_matrix_definition() -> None:
    s = sol.second_moment_matrix(TRAIN)
    assert close(s, TRAIN.T @ TRAIN / TRAIN.shape[0]), (
        "second_moment_matrix must be the equally weighted sample average of x x' (divide by T, not T - 1)."
    )
    assert close(s, s.T), "a second-moment matrix is symmetric."


def test_x_star_prices_the_training_sample_exactly() -> None:
    b = sol.x_star_weights(TRAIN, PRICES)
    m = TRAIN @ np.asarray(b)
    assert close(TRAIN.T @ m / TRAIN.shape[0], PRICES, 1e-9), (
        "x* must price every training payoff exactly in sample: E_T[x* x] = p (L07, Proposition 2.1)."
    )


def test_x_star_matches_the_projection_formula() -> None:
    b = np.asarray(sol.x_star_weights(TRAIN, PRICES))
    assert close(TRAIN @ b, sample_x_star(TRAIN, PRICES)), (
        "x* is the unique SDF in the payoff space: x' E[x x']^{-1} p (L04, Theorem 3.2)."
    )


def test_sdf_values_are_the_payoff_combination() -> None:
    b = np.asarray(sol.x_star_weights(TRAIN, PRICES))
    assert close(sol.sdf_values(TEST, b), TEST @ b), "sdf_values must return x' b in every observed state."


def test_x_star_is_invariant_to_units() -> None:
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    scaled = sol.sdf_values(3.0 * TRAIN, sol.x_star_weights(3.0 * TRAIN, 3.0 * PRICES))
    assert close(scaled, m), (
        "Measuring every payoff and price in other units (x -> c x, p -> c p) cannot change the SDF (L04, Theorem 3.2)."
    )


def test_x_star_accepts_small_units() -> None:
    c = 1e-5  # small units: the redundancy test must not depend on the absolute size of the payoffs
    m_small = sol.sdf_values(c * TRAIN, sol.x_star_weights(c * TRAIN, c * PRICES))
    m_unit = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    assert close(m_small, m_unit, 1e-7), (
        "Measuring every payoff and price in small units (x -> c x, p -> c p) cannot change the SDF, so a "
        "redundancy check must not depend on the absolute size of the payoffs (L04, Theorem 3.2)."
    )


def test_x_star_accepts_as_many_observations_as_assets() -> None:
    square = PAYOFFS[: PRICES.size]  # T = N: the payoffs of N states, linearly independent on every seed
    b = np.asarray(sol.x_star_weights(square, PRICES))
    assert close(square.T @ (square @ b) / square.shape[0], PRICES, 1e-9), (
        "With T = N observations and independent payoffs, x* still prices every payoff: only fewer observations "
        "than assets is invalid (L07, Proposition 2.1)."
    )


def test_x_star_depends_only_on_the_payoff_space() -> None:
    rng = np.random.default_rng(SEED + 101)
    n = TRAIN.shape[1]
    a = rng.normal(0.0, 1.0, (n, n)) + 3.0 * np.eye(n)  # an invertible repackaging of the assets
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    repackaged = sol.sdf_values(TRAIN @ a, sol.x_star_weights(TRAIN @ a, a.T @ PRICES))
    assert close(repackaged, m, 1e-7), (
        "Repackaging the assets into portfolios (x -> A'x, priced by the law of one price at A'p) spans the same "
        "payoff space, so x* must not change: it is unique in the payoff space (L01 and L04)."
    )


def test_x_star_has_the_smallest_second_moment() -> None:
    rng = np.random.default_rng(SEED + 202)
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    for _ in range(5):
        other = m + 0.3 * orthogonal_noise(TRAIN, rng)
        assert close(TRAIN.T @ other / TRAIN.shape[0], PRICES, 1e-8), "internal: the comparison SDF prices the payoffs"
        assert np.mean(m**2) <= np.mean(other**2) + 1e-12, (
            "Every SDF is x* plus a noise orthogonal to the payoffs, so x* has the smallest second moment "
            "(L04, Theorem 4.1)."
        )


def test_population_x_star_is_the_projection_of_the_true_sdf() -> None:
    x_star = np.asarray(sol.population_x_star(PROBS, PAYOFFS, PRICES))
    m_true = INST["m_true"]
    resid = m_true - x_star
    assert close(PAYOFFS.T @ (PROBS * resid), np.zeros(PAYOFFS.shape[1]), 1e-9), (
        "The true SDF minus x* must be orthogonal to every payoff under the state probabilities: x* is the "
        "projection of any SDF onto the payoff space (L04, Theorem 4.1)."
    )
    assert float(PROBS @ x_star**2) <= float(PROBS @ m_true**2) + 1e-12, (
        "x* has a smaller second moment than the true SDF that generated the prices (L04, Theorem 4.1)."
    )


def test_population_x_star_weights_the_states_by_their_probabilities() -> None:
    x_star = np.asarray(sol.population_x_star(PROBS, PAYOFFS, PRICES))
    uniform = np.asarray(sol.population_x_star(np.full(PROBS.size, 1.0 / PROBS.size), PAYOFFS, PRICES))
    assert close(PAYOFFS.T @ (PROBS * x_star), PRICES, 1e-9), (
        "population_x_star must price every payoff under the given state probabilities: E[x* x] = p."
    )
    assert not close(x_star, uniform, 1e-6), (
        "population_x_star must weight each state by its probability, not equally (E is the expectation under probs)."
    )


def test_riskless_payoff_pins_the_mean_of_x_star() -> None:
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    if INST["riskless"]:
        assert math.isclose(float(m.mean()), float(PRICES[0]), rel_tol=1e-9, abs_tol=1e-12), (
            "With a riskless payoff of 1 traded at price p_0, every SDF that prices it has mean p_0 = 1/R_f "
            "(L05, Proposition 1.2)."
        )
    else:
        assert np.all(np.isfinite(m)), "x* must be finite."


# ---------------------------------------------------------------- pricing errors


def test_pricing_error_sign_and_value() -> None:
    m = np.ones(TEST.shape[0])
    errors = sol.pricing_errors(TEST, PRICES, m)
    assert close(errors, TEST.mean(axis=0) - PRICES), (
        "pricing_errors must be E_T[m x] - p: positive when the SDF values a payoff above its price."
    )


def test_pricing_errors_vanish_for_x_star_in_sample() -> None:
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    assert close(sol.pricing_errors(TRAIN, PRICES, m), np.zeros(PRICES.size), 1e-9), (
        "In sample, x* prices every payoff, so its pricing errors are zero up to rounding."
    )


# ---------------------------------------------------------------- minimum-variance SDFs and the variance bound


def test_min_variance_sdf_needs_a_nonsingular_covariance() -> None:
    if INST["riskless"]:
        must_raise(
            lambda: sol.min_variance_sdf(TRAIN, PRICES, 0.99),
            "min_variance_sdf when a riskless (constant) payoff makes the payoff covariance matrix singular",
        )
        must_raise(
            lambda: sol.min_sdf_std(TRAIN, PRICES, 0.99),
            "min_sdf_std when a riskless (constant) payoff makes the payoff covariance matrix singular",
        )
    else:
        a, b = sol.min_variance_sdf(TRAIN, PRICES, 0.99)
        assert math.isfinite(a) and np.all(np.isfinite(b)), "min_variance_sdf must return finite (a, b)."


@pytest.mark.parametrize("mean", [0.9, 0.97, 1.02])
def test_min_variance_sdf_has_its_mean_and_prices_the_sample(mean: float) -> None:
    x = TRAIN[:, 1:] if INST["riskless"] else TRAIN  # without the riskless payoff the mean is free
    p = PRICES[1:] if INST["riskless"] else PRICES
    a, b = sol.min_variance_sdf(x, p, mean)
    m = a + x @ np.asarray(b)
    assert math.isclose(float(m.mean()), mean, rel_tol=1e-9), "the minimum-variance SDF must have the requested mean."
    assert close(x.T @ m / x.shape[0], p, 1e-9), "the minimum-variance SDF must price every payoff in the sample."


@pytest.mark.parametrize("mean", [0.9, 0.97, 1.02])
def test_min_variance_sdf_beats_every_other_sdf_with_its_mean(mean: float) -> None:
    x = TRAIN[:, 1:] if INST["riskless"] else TRAIN
    p = PRICES[1:] if INST["riskless"] else PRICES
    a, b = sol.min_variance_sdf(x, p, mean)
    m = a + x @ np.asarray(b)
    rng = np.random.default_rng(SEED + 303)
    for _ in range(5):
        other = m + 0.2 * orthogonal_noise(x, rng, with_constant=True)
        assert other.std() >= m.std() - 1e-12, (
            "Among SDFs with a given mean that price the payoffs, the one in span{1, x} has the least variance "
            "(L05, Theorem 2.1)."
        )
    assert math.isclose(sol.min_sdf_std(x, p, mean), float(m.std()), rel_tol=1e-8), (
        "min_sdf_std must equal the standard deviation (divide by T) of the minimum-variance SDF with that mean."
    )


def test_x_star_is_the_minimum_variance_sdf_at_its_own_mean() -> None:
    x = TRAIN[:, 1:] if INST["riskless"] else TRAIN
    p = PRICES[1:] if INST["riskless"] else PRICES
    m_star = x @ np.asarray(sol.x_star_weights(x, p))
    a, b = sol.min_variance_sdf(x, p, float(m_star.mean()))
    assert close(a + x @ np.asarray(b), m_star, 1e-7), (
        "x* minimizes E[m^2] over all SDFs, so at its own mean it is the minimum-variance SDF (L05, Proposition 2.3)."
    )


def test_variance_bound_dominates_every_sharpe_ratio() -> None:
    x = TRAIN[:, 1:] if INST["riskless"] else TRAIN
    p = PRICES[1:] if INST["riskless"] else PRICES
    gross = x / p  # gross returns: each payoff per unit of its price
    rng = np.random.default_rng(SEED + 404)
    for mean in (0.95, 1.0):
        bound = sol.min_sdf_std(x, p, mean)
        for _ in range(8):
            w = rng.normal(0.0, 1.0, gross.shape[1])
            v = rng.normal(0.0, 1.0, gross.shape[1])
            excess = gross @ (w / w.sum()) - gross @ (v / v.sum())  # a zero-price payoff
            sd = float(excess.std())
            if sd == 0.0:
                continue
            assert bound >= mean * abs(float(excess.mean())) / sd - 1e-9, (
                "sigma(m) >= E(m) |E(R^e)| / sigma(R^e) for every excess return: the variance bound of L05 "
                "(Theorem 2.4) must hold for the minimum-variance SDF."
            )


# ---------------------------------------------------------------- recovery and out-of-sample errors


def test_recover_sdf_reports_in_and_out_of_sample_errors() -> None:
    out = sol.recover_sdf(TRAIN, TEST, PRICES)
    b = np.linalg.solve(TRAIN.T @ TRAIN / TRAIN.shape[0], PRICES)
    assert close(out.weights, b, 1e-7), "recover_sdf must estimate the x* weights on the training sample only."
    assert close(out.in_sample_errors, np.zeros(PRICES.size), 1e-9), "x* prices the training sample exactly."
    expected = TEST.T @ (TEST @ b) / TEST.shape[0] - PRICES
    assert close(out.out_of_sample_errors, expected, 1e-7), (
        "Out-of-sample errors must be E_test[m x] - p with the weights estimated on the training sample "
        "(L07, Definition 4.1)."
    )
    assert math.isclose(out.out_of_sample_rms, float(np.sqrt(np.mean(expected**2))), rel_tol=1e-7), (
        "out_of_sample_rms is the root mean square of the out-of-sample pricing errors."
    )


def test_recover_sdf_summary_statistics() -> None:
    out = sol.recover_sdf(TRAIN, TEST, PRICES)
    b = np.linalg.solve(TRAIN.T @ TRAIN / TRAIN.shape[0], PRICES)
    m_train, m_test = TRAIN @ b, TEST @ b
    assert math.isclose(out.train_mean, float(m_train.mean()), rel_tol=1e-8), "train_mean is E_train[x*]."
    assert math.isclose(out.train_std, float(m_train.std()), rel_tol=1e-8), (
        "train_std is the standard deviation of x* on the training sample, dividing by T."
    )
    assert math.isclose(out.test_share_negative, float(np.mean(m_test < 0.0)), abs_tol=1e-12), (
        "test_share_negative is the share of test observations in which x* is negative: x* need not be positive "
        "(L04, Example 5.1)."
    )


def test_share_negative_counts_test_rows() -> None:
    mirrored = np.vstack([TEST, -TEST])  # the mirrored rows make about half of x*'s test values negative, on every seed
    out = sol.recover_sdf(TRAIN, mirrored, PRICES)
    m = mirrored @ np.linalg.solve(TRAIN.T @ TRAIN / TRAIN.shape[0], PRICES)
    assert math.isclose(out.test_share_negative, float(np.mean(m < 0.0)), abs_tol=1e-12), (
        "test_share_negative is the share of TEST observations with x* < 0, computed with the training weights; "
        "x* need not be positive (L04, Example 5.1)."
    )


def test_share_negative_uses_the_training_weights() -> None:
    rng = np.random.default_rng(SEED + 505)
    # Random signs make the share depend on the weights; the zero row has x* = 0, which is not negative.
    probe = np.vstack([rng.normal(0.0, 1.0, (200, TRAIN.shape[1])), np.zeros((1, TRAIN.shape[1]))])
    out = sol.recover_sdf(TRAIN, probe, PRICES)
    m = probe @ np.linalg.solve(TRAIN.T @ TRAIN / TRAIN.shape[0], PRICES)
    assert math.isclose(out.test_share_negative, float(np.mean(m < 0.0)), abs_tol=1e-12), (
        "test_share_negative counts test observations with x* < 0 (strictly), using the weights estimated on the "
        "training sample only (L07, Definition 4.1; L04, Example 5.1)."
    )


def test_out_of_sample_errors_are_not_identically_zero() -> None:
    out = sol.recover_sdf(TRAIN, TEST, PRICES)
    assert out.out_of_sample_rms > 1e-6, (
        "On a fresh sample x* does not price the payoffs exactly: estimate on train, evaluate on test "
        "(L07, Definition 4.1)."
    )


def test_recover_sdf_result_is_frozen() -> None:
    out = sol.recover_sdf(TRAIN, TEST, PRICES)
    with pytest.raises((AttributeError, TypeError)):
        out.out_of_sample_rms = 0.0  # type: ignore[misc]


# ---------------------------------------------------------------- failure behaviour


@pytest.mark.parametrize(
    ("bad", "condition"),
    [
        pytest.param(lambda: sol.x_star_weights(TRAIN[:, 0], PRICES[:1]), "one-dimensional payoffs", id="1d"),
        pytest.param(lambda: sol.x_star_weights(WITH_NAN, PRICES), "a payoff sample with a NaN", id="nan"),
        pytest.param(lambda: sol.second_moment_matrix(WITH_NAN), "a payoff sample with a NaN", id="nan-moments"),
        pytest.param(
            lambda: sol.pricing_errors(WITH_NAN, PRICES, np.ones(WITH_NAN.shape[0])),
            "a payoff sample with a NaN",
            id="nan-errors",
        ),
        pytest.param(lambda: sol.recover_sdf(TRAIN, TEST_WITH_NAN, PRICES), "a test sample with a NaN", id="nan-test"),
        pytest.param(lambda: sol.x_star_weights(WITH_INF, PRICES), "a payoff sample with an infinite value", id="inf"),
        pytest.param(
            lambda: sol.second_moment_matrix(WITH_INF), "a payoff sample with an infinite value", id="inf-moments"
        ),
        pytest.param(lambda: sol.x_star_weights(TRAIN, PRICES_WITH_NAN), "a NaN price", id="nan-price"),
        pytest.param(
            lambda: sol.min_sdf_std(
                TRAIN[:, 1:] if INST["riskless"] else TRAIN, PRICES[1:] if INST["riskless"] else PRICES, float("nan")
            ),
            "a NaN mean",
            id="nan-mean-std",
        ),
        pytest.param(
            lambda: sol.population_x_star(np.where(np.arange(PROBS.size) == 0, np.nan, PROBS), PAYOFFS, PRICES),
            "a NaN state probability",
            id="nan-probs",
        ),
        pytest.param(lambda: sol.sdf_values(TEST, np.full(TEST.shape[1], np.nan)), "NaN weights", id="nan-weights"),
        pytest.param(
            lambda: sol.pricing_errors(TEST, PRICES, np.where(np.arange(TEST.shape[0]) == 0, np.nan, 1.0)),
            "an SDF with a NaN value",
            id="nan-sdf",
        ),
        pytest.param(
            lambda: sol.x_star_weights(TRAIN, np.where(np.arange(PRICES.size) == 0, np.inf, PRICES)),
            "an infinite price",
            id="inf-price",
        ),
        pytest.param(lambda: sol.min_sdf_std(RISKY, RISKY_P, float("inf")), "an infinite mean", id="inf-mean-std"),
        pytest.param(
            lambda: sol.min_variance_sdf(
                np.column_stack([RISKY, RISKY[:, 0] * 0.3 + RISKY[:, 1] * 0.7]),
                np.append(RISKY_P, RISKY_P[0] * 0.3 + RISKY_P[1] * 0.7),
                0.97,
            ),
            "a redundant combination of risky payoffs, whose covariance matrix is singular",
            id="redundant-cov",
        ),
        pytest.param(
            lambda: sol.x_star_weights(
                np.column_stack([TRAIN, TRAIN[:, 0] + TRAIN[:, 1]]), np.append(PRICES, PRICES[0] + PRICES[1])
            ),
            "a redundant payoff (the sum of two others), whose second-moment matrix is singular",
            id="redundant-sum",
        ),
        pytest.param(lambda: sol.x_star_weights(TRAIN, PRICES[:-1]), "one price too few", id="short-prices"),
        pytest.param(
            lambda: sol.x_star_weights(np.column_stack([TRAIN, TRAIN[:, 0]]), np.append(PRICES, PRICES[0])),
            "a redundant payoff (duplicate column), whose second-moment matrix is singular",
            id="redundant",
        ),
        pytest.param(
            lambda: sol.x_star_weights(TRAIN[: TRAIN.shape[1] - 1], PRICES), "fewer observations than assets", id="few"
        ),
        pytest.param(
            lambda: sol.recover_sdf(TRAIN, TEST[:, :-1], PRICES), "train and test with different assets", id="cols"
        ),
        pytest.param(
            lambda: sol.pricing_errors(TEST, PRICES, np.ones(TEST.shape[0] - 1)),
            "an SDF of the wrong length",
            id="m-len",
        ),
        pytest.param(
            lambda: sol.population_x_star(-PROBS, PAYOFFS, PRICES), "negative state probabilities", id="neg-probs"
        ),
        pytest.param(
            lambda: sol.population_x_star(2.0 * PROBS, PAYOFFS, PRICES),
            "probabilities that do not sum to one",
            id="sum",
        ),
        pytest.param(lambda: sol.min_variance_sdf(TRAIN, PRICES, float("nan")), "a NaN mean", id="nan-mean"),
        pytest.param(lambda: sol.min_variance_sdf(RISKY, RISKY_P, float("inf")), "an infinite mean", id="inf-mean-var"),
        pytest.param(lambda: sol.second_moment_matrix(TRAIN[:, 0]), "a one-dimensional payoff sample", id="1d-moments"),
        pytest.param(
            lambda: sol.population_x_star(ZERO_PROB, PAYOFFS, PRICES), "a zero state probability", id="zero-probs"
        ),
        pytest.param(
            lambda: sol.population_x_star(np.array([1.0]), PAYOFFS, PRICES),
            "probabilities of the wrong length",
            id="probs-len",
        ),
        pytest.param(
            lambda: sol.population_x_star(np.where(np.arange(PROBS.size) == 0, np.inf, PROBS), PAYOFFS, PRICES),
            "an infinite state probability",
            id="inf-probs",
        ),
        pytest.param(
            lambda: sol.pricing_errors(TEST, PRICES, np.where(np.arange(TEST.shape[0]) == 0, np.inf, 1.0)),
            "an SDF with an infinite value",
            id="inf-sdf",
        ),
        pytest.param(
            lambda: sol.sdf_values(TEST, np.where(np.arange(TEST.shape[1]) == 0, np.inf, 1.0)),
            "infinite weights",
            id="inf-weights",
        ),
        pytest.param(
            lambda: sol.pricing_errors(WITH_INF, PRICES, np.ones(WITH_INF.shape[0])),
            "a payoff sample with an infinite value",
            id="inf-errors",
        ),
        pytest.param(
            lambda: sol.recover_sdf(TRAIN, TEST_WITH_INF, PRICES), "a test sample with an infinite value", id="inf-test"
        ),
        pytest.param(
            lambda: sol.population_x_star(PROBS, PAYOFFS_WITH_INF, PRICES),
            "a payoff sample with an infinite value",
            id="inf-population",
        ),
        pytest.param(
            lambda: sol.population_x_star(PROBS, PAYOFFS_WITH_NAN, PRICES),
            "a payoff sample with a NaN",
            id="nan-population",
        ),
        pytest.param(lambda: sol.sdf_values(TRAIN[:, 0], np.ones(1)), "one-dimensional payoffs", id="1d-sdf"),
        pytest.param(
            lambda: sol.pricing_errors(TRAIN[:, 0], PRICES[:1], np.ones(TRAIN.shape[0])),
            "one-dimensional payoffs",
            id="1d-errors",
        ),
        pytest.param(
            lambda: sol.recover_sdf(TRAIN[:, 0], TEST, PRICES[:1]), "one-dimensional training payoffs", id="1d-train"
        ),
        pytest.param(lambda: sol.recover_sdf(TRAIN, TEST[:, 0], PRICES), "one-dimensional test payoffs", id="1d-test"),
        pytest.param(
            lambda: sol.population_x_star(PROBS, PAYOFFS[:, 0], PRICES[:1]),
            "one-dimensional payoffs",
            id="1d-population",
        ),
        pytest.param(
            lambda: sol.min_variance_sdf(TRAIN[:, 0], PRICES[:1], 0.97), "one-dimensional payoffs", id="1d-minvar"
        ),
        pytest.param(lambda: sol.min_sdf_std(TRAIN[:, 0], PRICES[:1], 0.97), "one-dimensional payoffs", id="1d-minstd"),
        pytest.param(
            lambda: sol.min_sdf_std(np.column_stack([RISKY, np.ones(RISKY.shape[0])]), np.append(RISKY_P, 1.0), 0.97),
            "a riskless (constant) payoff, whose covariance matrix is singular",
            id="constant-std",
        ),
        pytest.param(
            lambda: sol.min_variance_sdf(
                np.column_stack([RISKY, np.ones(RISKY.shape[0])]), np.append(RISKY_P, 1.0), 0.97
            ),
            "a riskless (constant) payoff, whose covariance matrix is singular",
            id="constant-var",
        ),
        pytest.param(
            lambda: sol.pricing_errors(TEST, PRICES_WITH_NAN, np.ones(TEST.shape[0])),
            "a NaN price",
            id="nan-price-errors",
        ),
        pytest.param(
            lambda: sol.sdf_values(TEST_WITH_NAN, np.ones(TEST.shape[1])),
            "a payoff sample with a NaN",
            id="nan-sdf-values",
        ),
        pytest.param(
            lambda: sol.sdf_values(TEST_WITH_INF, np.ones(TEST.shape[1])),
            "a payoff sample with an infinite value",
            id="inf-sdf-values",
        ),
        pytest.param(
            lambda: sol.min_variance_sdf(RISKY_WITH_NAN, RISKY_P, 0.97),
            "a payoff sample with a NaN",
            id="nan-payoffs-minvar",
        ),
        pytest.param(
            lambda: sol.min_variance_sdf(RISKY_WITH_INF, RISKY_P, 0.97),
            "a payoff sample with an infinite value",
            id="inf-payoffs-minvar",
        ),
        pytest.param(
            lambda: sol.min_sdf_std(RISKY_WITH_NAN, RISKY_P, 0.97),
            "a payoff sample with a NaN",
            id="nan-payoffs-minstd",
        ),
        pytest.param(
            lambda: sol.min_sdf_std(RISKY_WITH_INF, RISKY_P, 0.97),
            "a payoff sample with an infinite value",
            id="inf-payoffs-minstd",
        ),
        pytest.param(
            lambda: sol.recover_sdf(WITH_NAN, TEST, PRICES),
            "a training sample with a NaN",
            id="nan-train-recover",
        ),
        pytest.param(
            lambda: sol.recover_sdf(WITH_INF, TEST, PRICES),
            "a training sample with an infinite value",
            id="inf-train-recover",
        ),
        pytest.param(
            lambda: sol.pricing_errors(TEST, PRICES_WITH_INF, np.ones(TEST.shape[0])),
            "an infinite price",
            id="inf-price-errors",
        ),
        pytest.param(lambda: sol.recover_sdf(TRAIN, TEST, PRICES_WITH_NAN), "a NaN price", id="nan-price-recover"),
        pytest.param(
            lambda: sol.recover_sdf(TRAIN, TEST, PRICES_WITH_INF), "an infinite price", id="inf-price-recover"
        ),
        pytest.param(
            lambda: sol.population_x_star(PROBS, PAYOFFS, PRICES_WITH_NAN), "a NaN price", id="nan-price-population"
        ),
        pytest.param(
            lambda: sol.population_x_star(PROBS, PAYOFFS, PRICES_WITH_INF),
            "an infinite price",
            id="inf-price-population",
        ),
        pytest.param(lambda: sol.min_variance_sdf(RISKY, RISKY_P_WITH_NAN, 0.97), "a NaN price", id="nan-price-minvar"),
        pytest.param(
            lambda: sol.min_variance_sdf(RISKY, RISKY_P_WITH_INF, 0.97), "an infinite price", id="inf-price-minvar"
        ),
        pytest.param(lambda: sol.min_sdf_std(RISKY, RISKY_P_WITH_NAN, 0.97), "a NaN price", id="nan-price-minstd"),
        pytest.param(
            lambda: sol.min_sdf_std(RISKY, RISKY_P_WITH_INF, 0.97), "an infinite price", id="inf-price-minstd"
        ),
        pytest.param(
            lambda: sol.min_sdf_std(
                np.column_stack([RISKY, RISKY[:, 0] * 0.3 + RISKY[:, 1] * 0.7]),
                np.append(RISKY_P, RISKY_P[0] * 0.3 + RISKY_P[1] * 0.7),
                0.97,
            ),
            "a redundant combination of risky payoffs, whose covariance matrix is singular",
            id="redundant-cov-std",
        ),
    ],
)
def test_invalid_input_raises(bad: Callable[[], object], condition: str) -> None:
    must_raise(bad, condition)


def test_min_sdf_std_does_not_change_its_prices() -> None:
    p = np.asarray(RISKY_P, dtype=np.float64).copy()
    before = p.copy()
    sol.min_sdf_std(RISKY, p, 0.97)
    assert np.array_equal(p, before), (
        "Functions must not modify their arguments (min_sdf_std must not form p - v E[x] in place)."
    )


def test_functions_do_not_mutate_or_print() -> None:
    train, test, prices = TRAIN.copy(), TEST.copy(), PRICES.copy()
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        sol.second_moment_matrix(train)
        b = sol.x_star_weights(train, prices)
        sol.sdf_values(test, b)
        sol.pricing_errors(test, prices, np.ones(test.shape[0]))
        sol.recover_sdf(train, test, prices)
        sol.population_x_star(PROBS.copy(), PAYOFFS.copy(), prices)
    assert buffer.getvalue() == "", "Functions must not print."
    assert np.array_equal(train, TRAIN) and np.array_equal(test, TEST) and np.array_equal(prices, PRICES), (
        "Functions must not modify their arguments."
    )


def call_every_public_function(
    train: np.ndarray,
    test: np.ndarray,
    prices: np.ndarray,
    probs: np.ndarray,
    payoffs: np.ndarray,
    sdf: np.ndarray,
    weights: np.ndarray,
    risky: np.ndarray,
    risky_p: np.ndarray,
) -> None:
    """Call each of the eight public functions once on valid inputs."""
    sol.second_moment_matrix(payoffs)
    sol.x_star_weights(train, prices)
    sol.sdf_values(test, weights)
    sol.pricing_errors(test, prices, sdf)
    sol.population_x_star(probs, payoffs, prices)
    sol.min_variance_sdf(risky, risky_p, 0.97)
    sol.min_sdf_std(risky, risky_p, 0.97)
    sol.recover_sdf(train, test, prices)


def test_every_public_function_is_silent_and_pure() -> None:
    args = (
        TRAIN.copy(),
        TEST.copy(),
        PRICES.copy(),
        PROBS.copy(),
        PAYOFFS.copy(),
        np.ones(TEST.shape[0]),
        np.full(TEST.shape[1], 0.1),
        RISKY.copy(),
        RISKY_P.copy(),
    )
    names = ("train", "test", "prices", "probs", "payoffs", "sdf", "weights", "risky", "risky_p")
    before = [a.copy() for a in args]
    out, err = io.StringIO(), io.StringIO()
    with (
        warnings.catch_warnings(record=True) as caught,
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(err),
    ):
        warnings.simplefilter("always")
        call_every_public_function(*args)
    assert out.getvalue() == "", "Functions must not print to standard output."
    assert err.getvalue() == "", "Functions must not write to standard error."
    assert not caught, "Functions must not warn on valid inputs."
    for name, a, b in zip(names, args, before, strict=True):
        assert np.array_equal(a, b), f"Functions must not modify their arguments: {name} changed."


def test_ill_conditioned_payoffs_emit_no_warning() -> None:
    rng = np.random.default_rng(20260501)  # fixed, independent of the seed: the sample is the same on every seed
    x = rng.normal(0.0, 1.0, (200, 3)) * np.array(
        [1.0, 1.0, 1e-4]
    )  # full rank, but the second moments are ill-conditioned
    assert np.linalg.cond(x.T @ x / x.shape[0]) > 1e6, "internal: the second-moment matrix must be ill-conditioned"
    p = np.array([1.0, 0.99, 1e-4])
    probs = np.full(x.shape[0], 1.0 / x.shape[0])
    sdf, weights = np.ones(x.shape[0]), np.full(x.shape[1], 0.1)
    out, err = io.StringIO(), io.StringIO()
    with (
        warnings.catch_warnings(record=True) as caught,
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(err),
    ):
        warnings.simplefilter("always")
        call_every_public_function(x, x, p, probs, x, sdf, weights, x, p)
    assert not caught, "A valid but ill-conditioned payoff sample must not trigger a warning from any function."
    assert out.getvalue() == "" and err.getvalue() == "", "Functions must not print or write to stderr."


@pytest.mark.parametrize("delta", [5e-4, 1e-6], ids=["sum-1.0005", "sum-1-plus-1e-6"])
def test_probabilities_off_one_beyond_rounding_raise(delta: float) -> None:
    q = PROBS.copy()
    q[0] += delta
    must_raise(
        lambda: sol.population_x_star(q, PAYOFFS, PRICES),
        "probabilities whose sum differs from one by more than float rounding",
    )


def test_probability_rounding_is_accepted() -> None:
    x_star = np.asarray(sol.population_x_star(PROBS, PAYOFFS, PRICES))
    for delta in (1e-12, -1e-12):
        q = PROBS.copy()
        q[0] += delta
        out = np.asarray(sol.population_x_star(q, PAYOFFS, PRICES))
        assert close(out, x_star, 1e-7), "Probabilities that sum to one up to float rounding must be accepted."


def test_negative_sdf_values_are_legal_and_silent() -> None:
    b = -np.ones(TEST.shape[1])  # the weights are unconstrained, so the SDF values may be negative
    args = (TEST.copy(), PRICES.copy(), b.copy())
    out, err = io.StringIO(), io.StringIO()
    with (
        warnings.catch_warnings(record=True) as caught,
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(err),
    ):
        warnings.simplefilter("always")
        values = np.asarray(sol.sdf_values(args[0], args[2]))
        errors = np.asarray(sol.pricing_errors(args[0], args[1], values))
    assert np.any(values < 0.0), "internal: the check needs negative SDF values"
    assert not caught and out.getvalue() == "" and err.getvalue() == "", (
        "A negative SDF value is legal: functions must neither warn nor print on it."
    )
    assert close(values, TEST @ b), "sdf_values must return x' b in every state, negative or not."
    assert close(errors, TEST.T @ values / TEST.shape[0] - PRICES), (
        "pricing_errors must be E_T[m x] - p for any finite SDF values, negative or not."
    )


@pytest.mark.parametrize("scale", [1e-11, 1e11], ids=["tiny-units", "huge-units"])
def test_rank_check_is_scale_invariant(scale: float) -> None:
    unit = np.asarray(sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES)))
    small = np.asarray(sol.sdf_values(scale * TRAIN, sol.x_star_weights(scale * TRAIN, scale * PRICES)))
    assert close(small, unit, 1e-7), (
        "Measuring payoffs and prices in other units cannot change x*, so the redundancy check must not depend on "
        "the absolute size of the payoffs (L04, Theorem 3.2)."
    )
    pop_unit = np.asarray(sol.population_x_star(PROBS, PAYOFFS, PRICES))
    pop = np.asarray(sol.population_x_star(PROBS, scale * PAYOFFS, scale * PRICES))
    assert close(pop, pop_unit, 1e-7), "population_x_star must not depend on the absolute size of the payoffs."
    out = sol.recover_sdf(scale * TRAIN, scale * TEST, scale * PRICES)
    assert close(scale * np.asarray(out.weights), np.asarray(sol.x_star_weights(TRAIN, PRICES)), 1e-7), (
        "recover_sdf must not depend on the absolute size of the payoffs."
    )


def test_share_negative_counts_states_just_below_zero() -> None:
    b = np.asarray(sol.x_star_weights(TRAIN, PRICES))
    v = -1e-10 * b / (b @ b)  # a legal payoff state whose x* is -1e-10: negative, though tiny
    probe = np.vstack([TEST, v])
    m = probe @ b
    assert -1e-9 < m[-1] < 0.0, "internal: the probe state's x* must be negative and within 1e-9 of zero"
    out = sol.recover_sdf(TRAIN, probe, PRICES)
    assert math.isclose(out.test_share_negative, float(np.mean(m < 0.0)), abs_tol=1e-12), (
        "test_share_negative counts every test observation with x* < 0, however small in size (L04, Example 5.1)."
    )


def test_ill_conditioned_full_rank_payoffs_are_accepted() -> None:
    rng = np.random.default_rng(20260502)  # fixed: the same sample on every seed
    x = rng.normal(0.0, 1.0, (50, 3)) * np.array([1.0, 1.0, 1e-7])  # full rank, with a second-moment matrix near 1e14
    p = np.array([1.0, 0.99, 1e-7])
    assert np.linalg.cond(x.T @ x / x.shape[0]) > 1e12, "internal: the second-moment matrix must be ill-conditioned"
    b = np.asarray(sol.x_star_weights(x, p))
    assert np.all(np.isfinite(b)), "x_star_weights must return finite weights for a full-rank payoff sample."
    residual = x.T @ (x @ b) / x.shape[0] - p
    assert np.max(np.abs(residual)) <= 1e-10 * np.max(np.abs(p)), (
        "x* must still price every payoff in sample: a backward-stable solve leaves a residual of rounding size, "
        "not one that grows with the condition number (L07, Proposition 2.1)."
    )


def test_imports_only_numpy_and_the_standard_library() -> None:
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
                f"sdf_recovery may import only NumPy and the standard library, not {name}."
            )
