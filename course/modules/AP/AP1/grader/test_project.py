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


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail with a message naming the violated condition unless call() raises ValueError."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError naming the violated condition.")


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
        "x* must price every training payoff exactly in sample: E_T[x* x] = p (L08, the sample pricing identity)."
    )


def test_x_star_matches_the_projection_formula() -> None:
    b = np.asarray(sol.x_star_weights(TRAIN, PRICES))
    assert close(TRAIN @ b, sample_x_star(TRAIN, PRICES)), (
        "x* is the unique SDF in the payoff space: x' E[x x']^{-1} p (L05, Theorem on existence and uniqueness)."
    )


def test_sdf_values_are_the_payoff_combination() -> None:
    b = np.asarray(sol.x_star_weights(TRAIN, PRICES))
    assert close(sol.sdf_values(TEST, b), TEST @ b), "sdf_values must return x' b in every observed state."


def test_x_star_is_invariant_to_units() -> None:
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    scaled = sol.sdf_values(3.0 * TRAIN, sol.x_star_weights(3.0 * TRAIN, 3.0 * PRICES))
    assert close(scaled, m), (
        "Measuring every payoff and price in other units (x -> c x, p -> c p) cannot change the SDF (L05)."
    )


def test_x_star_depends_only_on_the_payoff_space() -> None:
    rng = np.random.default_rng(SEED + 101)
    n = TRAIN.shape[1]
    a = rng.normal(0.0, 1.0, (n, n)) + 3.0 * np.eye(n)  # an invertible repackaging of the assets
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    repackaged = sol.sdf_values(TRAIN @ a, sol.x_star_weights(TRAIN @ a, a.T @ PRICES))
    assert close(repackaged, m, 1e-7), (
        "Repackaging the assets into portfolios (x -> A'x, priced by the law of one price at A'p) spans the same "
        "payoff space, so x* must not change: it is unique in the payoff space (L01 and L05)."
    )


def test_x_star_has_the_smallest_second_moment() -> None:
    rng = np.random.default_rng(SEED + 202)
    m = sol.sdf_values(TRAIN, sol.x_star_weights(TRAIN, PRICES))
    for _ in range(5):
        other = m + 0.3 * orthogonal_noise(TRAIN, rng)
        assert close(TRAIN.T @ other / TRAIN.shape[0], PRICES, 1e-8), "internal: the comparison SDF prices the payoffs"
        assert np.mean(m**2) <= np.mean(other**2) + 1e-12, (
            "Every SDF is x* plus a noise orthogonal to the payoffs, so x* has the smallest second moment (L06)."
        )


def test_population_x_star_is_the_projection_of_the_true_sdf() -> None:
    x_star = np.asarray(sol.population_x_star(PROBS, PAYOFFS, PRICES))
    m_true = INST["m_true"]
    resid = m_true - x_star
    assert close(PAYOFFS.T @ (PROBS * resid), np.zeros(PAYOFFS.shape[1]), 1e-9), (
        "The true SDF minus x* must be orthogonal to every payoff under the state probabilities: x* is the "
        "projection of any SDF onto the payoff space (L05, L06)."
    )
    assert float(PROBS @ x_star**2) <= float(PROBS @ m_true**2) + 1e-12, (
        "x* has a smaller second moment than the true SDF that generated the prices (L06)."
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
            "With a riskless payoff of 1 traded at price p_0, every SDF that prices it has mean p_0 = 1/R_f (L02)."
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
            "Among SDFs with a given mean that price the payoffs, the one in span{1, x} has the least variance (L06)."
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
        "x* minimizes E[m^2] over all SDFs, so at its own mean it is the minimum-variance SDF (L06)."
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
                "sigma(m) >= E(m) |E(R^e)| / sigma(R^e) for every excess return: the variance bound of L06 "
                "(Theorem 4.4) must hold for the minimum-variance SDF."
            )


# ---------------------------------------------------------------- recovery and out-of-sample errors


def test_recover_sdf_reports_in_and_out_of_sample_errors() -> None:
    out = sol.recover_sdf(TRAIN, TEST, PRICES)
    b = np.linalg.solve(TRAIN.T @ TRAIN / TRAIN.shape[0], PRICES)
    assert close(out.weights, b, 1e-7), "recover_sdf must estimate the x* weights on the training sample only."
    assert close(out.in_sample_errors, np.zeros(PRICES.size), 1e-9), "x* prices the training sample exactly."
    expected = TEST.T @ (TEST @ b) / TEST.shape[0] - PRICES
    assert close(out.out_of_sample_errors, expected, 1e-7), (
        "Out-of-sample errors must be E_test[m x] - p with the weights estimated on the training sample (L08)."
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
        "test_share_negative is the share of test observations in which x* is negative: x* need not be positive (L06)."
    )


def test_out_of_sample_errors_are_not_identically_zero() -> None:
    out = sol.recover_sdf(TRAIN, TEST, PRICES)
    assert out.out_of_sample_rms > 1e-6, (
        "On a fresh sample x* does not price the payoffs exactly: estimate on train, evaluate on test (L08)."
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
    ],
)
def test_invalid_input_raises(bad: Callable[[], object], condition: str) -> None:
    must_raise(bad, condition)


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
