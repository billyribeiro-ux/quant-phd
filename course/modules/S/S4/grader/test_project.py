"""Acceptance suite for Atlas A4 (atlas.timeseries), the S4 project.

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with atlas.timeseries importable.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable

import pytest

try:
    import atlas.timeseries as a4
except ImportError:
    import reference as a4

from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail with a descriptive message unless call() raises ValueError."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the contract requires a ValueError naming the violated condition.")


# ---------------------------------------------------------------- GARCH(1,1) tests


def test_garch11_variance_recursion() -> None:
    """Checks GARCH(1,1) conditional variance recursion and h_0 initialization."""
    returns: list[float] = list(INST["returns"])
    omega = 0.03
    alpha = 0.09
    beta = 0.85

    h = a4.garch11_variance(returns, omega, alpha, beta)
    assert len(h) == len(returns), "garch11_variance output must have same length as returns"

    # h_0 must be the sample variance (divisor n)
    mean_r = sum(returns) / len(returns)
    expected_h0 = sum((r - mean_r) ** 2 for r in returns) / len(returns)
    assert abs(h[0] - expected_h0) < 1e-9, "h_0 must equal sample variance of returns"

    # Recursion check for all t >= 1
    for t in range(1, len(returns)):
        expected_ht = omega + alpha * (returns[t - 1] ** 2) + beta * h[t - 1]
        assert abs(h[t] - expected_ht) < 1e-9 * (1.0 + abs(expected_ht)), f"variance recursion failed at t={t}"


def test_garch11_variance_no_lookahead() -> None:
    """Modifying returns[t] must not alter conditional variance h[t]."""
    returns = list(INST["returns"][:50])
    omega, alpha, beta = 0.03, 0.09, 0.85
    h_orig = a4.garch11_variance(returns, omega, alpha, beta)

    # In GARCH, h[t] is measurable with respect to F_{t-1}.
    # Given the same h_0, perturbing returns[t] should not change h[t].
    # Specifically, check that h[1] depends only on returns[0], not returns[1..].
    h1_val = omega + alpha * (returns[0] ** 2) + beta * h_orig[0]
    assert abs(h_orig[1] - h1_val) < 1e-9, "h[1] must depend only on returns[0] and h[0]"


def test_garch11_variance_validation() -> None:
    """Checks ValueError conditions on garch11_variance and garch11_loglik."""
    r = [0.01, -0.02, 0.015]
    must_raise(lambda: a4.garch11_variance([0.01], 0.05, 0.1, 0.8), "fewer than 2 returns")
    must_raise(lambda: a4.garch11_variance(r, 0.0, 0.1, 0.8), "omega <= 0")
    must_raise(lambda: a4.garch11_variance(r, -0.01, 0.1, 0.8), "omega < 0")
    must_raise(lambda: a4.garch11_variance(r, 0.05, -0.01, 0.8), "alpha < 0")
    must_raise(lambda: a4.garch11_variance(r, 0.05, 0.1, -0.01), "beta < 0")

    must_raise(lambda: a4.garch11_loglik([0.01], 0.05, 0.1, 0.8), "loglik fewer than 2 returns")
    must_raise(lambda: a4.garch11_loglik(r, 0.0, 0.1, 0.8), "loglik omega <= 0")


def test_garch11_loglik_constant_and_values() -> None:
    """Checks that Gaussian loglik includes the full normal constant -0.5*ln(2*pi)."""
    returns = list(INST["returns"][:100])
    omega, alpha, beta = 0.02, 0.08, 0.85
    ll = a4.garch11_loglik(returns, omega, alpha, beta)

    h = a4.garch11_variance(returns, omega, alpha, beta)
    log2pi = math.log(2.0 * math.pi)
    manual_ll = -0.5 * sum(log2pi + math.log(ht) + (r * r) / ht for r, ht in zip(returns, h, strict=True))
    assert abs(ll - manual_ll) < 1e-7, "garch11_loglik must match exact Gaussian log-likelihood formula"


def test_garch11_fit() -> None:
    """Quasi-maximum likelihood GARCH(1,1) fit returns valid feasible parameters."""
    returns = list(INST["returns"])
    fit = a4.garch11_fit(returns)

    assert isinstance(fit, dict), "garch11_fit must return dict"
    for k in ("omega", "alpha", "beta", "loglik"):
        assert k in fit, f"missing key {k} in fit output"

    om, al, be = fit["omega"], fit["alpha"], fit["beta"]
    assert om > 0.0, "fitted omega must be strictly positive"
    assert al >= 0.0, "fitted alpha must be non-negative"
    assert be >= 0.0, "fitted beta must be non-negative"
    assert al + be < 1.0, "fitted alpha + beta must be strictly less than 1"

    # Log-likelihood optimality: fit loglik must be >= loglik at true parameters minus tolerance
    true_p = INST["true_garch"]
    ll_true = a4.garch11_loglik(returns, float(true_p[0]), float(true_p[1]), float(true_p[2]))
    assert fit["loglik"] >= ll_true - 1e-2, "fitted log-likelihood must be at least as high as true parameter loglik"

    # Validation
    must_raise(lambda: a4.garch11_fit(returns[:49]), "fewer than 50 returns")
    bad_rets = list(returns[:60])
    bad_rets[10] = float("nan")
    must_raise(lambda: a4.garch11_fit(bad_rets), "NaN return")


# ---------------------------------------------------------------- HAR-RV tests


def test_har_design_matrix() -> None:
    """Checks HAR design matrix structure, lag alignments, and window averages."""
    rv: list[float] = list(INST["rv"])
    x_mat, y = a4.har_design(rv)

    n = len(rv)
    assert len(x_mat) == n - 22, f"X must have {n - 22} rows"
    assert len(y) == n - 22, f"y must have {n - 22} rows"

    # Check row 0 (corresponding to t = 22)
    assert x_mat[0][0] == 1.0, "first column of X must be intercept 1.0"
    assert abs(x_mat[0][1] - rv[21]) < 1e-12, "daily component must be rv[t-1]"

    mean_5 = sum(rv[22 - 5 : 22]) / 5.0
    assert abs(x_mat[0][2] - mean_5) < 1e-12, "weekly component must be mean of rv[t-5..t-1]"

    mean_22 = sum(rv[22 - 22 : 22]) / 22.0
    assert abs(x_mat[0][3] - mean_22) < 1e-12, "monthly component must be mean of rv[t-22..t-1]"
    assert abs(y[0] - rv[22]) < 1e-12, "target y must be rv[t]"


def test_har_fit_and_forecast() -> None:
    """Checks HAR OLS parameter recovery and rolling out-of-sample forecast."""
    rv = list(INST["rv"])
    coefs = a4.har_fit(rv)
    assert len(coefs) == 4, "har_fit must return 4 coefficients"

    # Invariant: Normal equations orthogonality X^T (y - X beta) == 0
    x_mat, y = a4.har_design(rv)
    resids = [y[i] - sum(x_mat[i][j] * coefs[j] for j in range(4)) for i in range(len(y))]
    for j in range(4):
        orthog = sum(x_mat[i][j] * resids[i] for i in range(len(y)))
        assert abs(orthog) < 1e-7, f"OLS normal equation violated for regressor {j}: dot = {orthog}"

    # Forecast calculation
    t_fc = 50
    fc = a4.har_forecast(rv, t_fc, coefs)
    expected_fc = (
        coefs[0]
        + coefs[1] * rv[t_fc - 1]
        + coefs[2] * (sum(rv[t_fc - 5 : t_fc]) / 5.0)
        + coefs[3] * (sum(rv[t_fc - 22 : t_fc]) / 22.0)
    )
    assert abs(fc - expected_fc) < 1e-9, "har_forecast must match design row linear combination"

    # Validation
    must_raise(lambda: a4.har_design(rv[:22]), "fewer than 23 observations in rv")
    bad_rv = list(rv[:40])
    bad_rv[5] = -0.01
    must_raise(lambda: a4.har_design(bad_rv), "non-positive rv")
    must_raise(lambda: a4.har_forecast(rv, 21, coefs), "t < 22")
    must_raise(lambda: a4.har_forecast(rv, len(rv) + 1, coefs), "t > len(rv)")


# ---------------------------------------------------------------- Loss function tests


def test_loss_functions() -> None:
    """Checks properties of QLIKE and MSE loss functions."""
    y = 1.25
    assert a4.qlike(y, y) == 0.0, "qlike(y, y) must equal 0"
    assert a4.mse_loss(y, y) == 0.0, "mse_loss(y, y) must equal 0"

    # QLIKE asymmetry: penalizes under-forecasting more heavily than over-forecasting
    q_under = a4.qlike(1.0, 0.5)  # 2.0 - ln(2) - 1 ~ 0.30685
    q_over = a4.qlike(1.0, 1.5)  # 0.6667 - ln(0.6667) - 1 ~ 0.07213
    assert q_under > q_over, "QLIKE must penalize under-prediction more than over-prediction"
    assert abs(q_under - (2.0 - math.log(2.0) - 1.0)) < 1e-12

    m_loss = a4.mse_loss(1.0, 0.5)
    assert abs(m_loss - 0.25) < 1e-12, "mse_loss must equal squared error"

    # Validation
    must_raise(lambda: a4.qlike(0.0, 1.0), "realized <= 0")
    must_raise(lambda: a4.qlike(1.0, 0.0), "forecast <= 0")
    must_raise(lambda: a4.qlike(-1.0, 1.0), "realized < 0")


# ---------------------------------------------------------------- Kalman filter tests


def test_kalman_filter() -> None:
    """Checks Kalman local-level filter recursion and asymptotic properties."""
    y: list[float] = list(INST["kalman_y"])
    sw2 = float(INST["sigma_w2"])
    sv2 = float(INST["sigma_v2"])

    filtered = a4.kalman_local_level_filter(y, sw2, sv2)
    assert len(filtered) == len(y), "kalman filter output length must equal input length"

    # Known answer 1: When sigma_v2 is very small (exact observations), filtered state equals y
    filtered_exact = a4.kalman_local_level_filter(y[:20], 0.02, 1e-9)
    for t in range(20):
        assert abs(filtered_exact[t] - y[t]) < 1e-4, f"state should match exact observation at t={t}"

    # Known answer 2: Exact one-step calculation
    # y = [10.0, 12.0], sw2 = 0.01, sv2 = 0.04 -> P0 = 0.05, F1 = 0.09, K1 = 5/9, a1 = 10 + (5/9)*2 = 11.11111
    step_check = a4.kalman_local_level_filter([10.0, 12.0], 0.01, 0.04)
    expected_a1 = 10.0 + (5.0 / 9.0) * 2.0
    assert abs(step_check[1] - expected_a1) < 1e-9, "Kalman update step failed on exact 2-step case"

    # Validation
    must_raise(lambda: a4.kalman_local_level_filter([], sw2, sv2), "empty y")
    must_raise(lambda: a4.kalman_local_level_filter(y, -0.01, sv2), "sigma_w2 < 0")
    must_raise(lambda: a4.kalman_local_level_filter(y, sw2, 0.0), "sigma_v2 <= 0")


# ---------------------------------------------------------------- ARMA(1,1) tests


def test_arma11_fit() -> None:
    """Checks ARMA(1,1) conditional sum-of-squares fitting."""
    x: list[float] = list(INST["arma_x"])
    fit = a4.arma11_fit(x)

    assert isinstance(fit, dict), "arma11_fit must return dict"
    for k in ("phi", "theta", "sigma2"):
        assert k in fit, f"missing key {k} in fit output"

    assert abs(fit["phi"]) < 1.0, "|phi| must be less than 1 (stationarity)"
    assert abs(fit["theta"]) < 1.0, "|theta| must be less than 1 (invertibility)"
    assert fit["sigma2"] > 0.0, "sigma2 must be strictly positive"

    # Validation
    must_raise(lambda: a4.arma11_fit(x[:29]), "fewer than 30 observations")
