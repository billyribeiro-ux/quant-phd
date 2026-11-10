"""Pytest acceptance suite for S6: Policy-shock event study engine.

Runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable

import pytest

try:
    import event_study as es
except ImportError:
    import reference as es

from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: contract requires a ValueError naming the violated condition.")


# ---------------------------------------------------------------- Normal Model Tests


def test_fit_normal_model_market_exact() -> None:
    """Market model OLS returns exact slope and intercept on clean fixtures."""
    mkt = [1.0, 2.0, 3.0, 4.0, 5.0]
    # y = 2.0 + 3.0 * x
    stk = [5.0, 8.0, 11.0, 14.0, 17.0]
    alpha, beta, sig2 = es.fit_normal_model(stk, mkt)
    assert abs(alpha - 2.0) < 1e-10, "alpha must equal exact intercept 2.0"
    assert abs(beta - 3.0) < 1e-10, "beta must equal exact slope 3.0"
    assert abs(sig2 - 0.0) < 1e-10, "residual variance must be 0 for exact linear relation"


def test_fit_normal_model_divisor_l_minus_2() -> None:
    """Market model residual variance divides by L - 2 degrees of freedom."""
    mkt = [-2.0, -1.0, 0.0, 1.0, 2.0]  # L = 5
    # Let y = 1.0 + 2.0 * mkt + e with orthogonal residuals e = [1, -2, 0, 2, -1]
    # sum e = 0, sum e * mkt = 0, sum e^2 = 10.0
    stk = [-2.0, -3.0, 1.0, 5.0, 4.0]
    alpha, beta, sig2 = es.fit_normal_model(stk, mkt)
    assert abs(beta - 2.0) < 1e-10
    assert abs(alpha - 1.0) < 1e-10
    # Divisor must be L - 2 = 3, so sig2 = 10.0 / 3.0
    expected_sig2 = 10.0 / 3.0
    assert abs(sig2 - expected_sig2) < 1e-9, (
        f"sigma2 must be divided by L - 2 = 3; got {sig2}, expected {expected_sig2}"
    )


def test_fit_normal_model_constant_mean() -> None:
    """Constant-mean model sets beta=0 and divides residual sum of squares by L - 1."""
    stk = [2.0, 4.0, 6.0, 8.0]  # L = 4, mean = 5.0
    # SS = (2-5)^2 + (4-5)^2 + (6-5)^2 + (8-5)^2 = 9 + 1 + 1 + 9 = 20.0
    # Divisor L - 1 = 3 -> sig2 = 20.0 / 3 = 6.6666666667
    alpha, beta, sig2 = es.fit_normal_model(stk, None)
    assert abs(alpha - 5.0) < 1e-10, "alpha must equal sample mean 5.0"
    assert beta == 0.0, "beta must be exactly 0.0 in constant-mean model"
    expected_sig2 = 20.0 / 3.0
    assert abs(sig2 - expected_sig2) < 1e-9, f"constant-mean sigma2 must equal {expected_sig2}"


def test_fit_normal_model_exceptions() -> None:
    """fit_normal_model enforces input validation and raises ValueError."""
    must_raise(lambda: es.fit_normal_model([1.0], None), "constant-mean with L < 2")
    must_raise(lambda: es.fit_normal_model([1.0, 2.0], [1.0, 2.0]), "market model with L < 3")
    must_raise(lambda: es.fit_normal_model([1.0, 2.0, 3.0], [1.0, 2.0]), "unequal lengths")
    must_raise(
        lambda: es.fit_normal_model([1.0, 2.0, 3.0], [2.0, 2.0, 2.0]),
        "market series with zero variance",
    )


# ---------------------------------------------------------------- Abnormal Returns Tests


def test_abnormal_returns_calculation() -> None:
    """abnormal_returns evaluates AR = actual - (alpha + beta * market)."""
    stk = [0.05, -0.02, 0.08]
    mkt = [0.01, 0.00, 0.02]
    alpha, beta = 0.01, 1.2
    # expected:
    # 0.05 - (0.01 + 1.2 * 0.01) = 0.05 - 0.022 = 0.028
    # -0.02 - (0.01 + 1.2 * 0.00) = -0.02 - 0.01 = -0.030
    # 0.08 - (0.01 + 1.2 * 0.02) = 0.08 - 0.034 = 0.046
    ar = es.abnormal_returns(stk, mkt, alpha, beta)
    assert len(ar) == 3
    assert abs(ar[0] - 0.028) < 1e-9
    assert abs(ar[1] - (-0.030)) < 1e-9
    assert abs(ar[2] - 0.046) < 1e-9


def test_abnormal_returns_sign_check() -> None:
    """A positive shock yields a positive abnormal return, not negative."""
    stk = [0.10]
    mkt = [0.00]
    ar = es.abnormal_returns(stk, mkt, 0.0, 1.0)
    assert ar[0] > 0.0, "positive outperformance must yield positive AR"


def test_abnormal_returns_exceptions() -> None:
    """abnormal_returns raises ValueError on mismatched series lengths."""
    must_raise(
        lambda: es.abnormal_returns([0.01, 0.02], [0.01], 0.0, 1.0),
        "mismatched series lengths in abnormal_returns",
    )


# ---------------------------------------------------------------- Variance Tests


def test_abnormal_return_variance_formula() -> None:
    """Variance formula accounts for both residual risk and estimation error."""
    est_mkt = [0.0, 2.0, 4.0]  # L = 3, mean = 2.0, SS_m = (-2)^2 + 0^2 + 2^2 = 8.0
    ev_mkt = 6.0  # (ev - mean)^2 = (6 - 2)^2 = 16.0
    sig2 = 0.04
    # Var = sig2 * (1 + 1/3 + 16/8) = 0.04 * (1 + 0.333333333 + 2.0) = 0.04 * (10/3) = 0.40 / 3
    v = es.abnormal_return_variance(sig2, est_mkt, ev_mkt)
    expected = 0.04 * (1.0 + 1.0 / 3.0 + 16.0 / 8.0)
    assert abs(v - expected) < 1e-9, f"expected AR variance {expected}, got {v}"

    # Constant-mean case: event_market is None
    v_cm = es.abnormal_return_variance(sig2, est_mkt, None)
    expected_cm = sig2 * (1.0 + 1.0 / 3.0)
    assert abs(v_cm - expected_cm) < 1e-9, f"expected constant-mean variance {expected_cm}, got {v_cm}"


def test_abnormal_return_variance_exceptions() -> None:
    """abnormal_return_variance validates input preconditions."""
    must_raise(lambda: es.abnormal_return_variance(0.02, None, 0.01), "estimation_market is None")
    must_raise(lambda: es.abnormal_return_variance(0.02, [], None), "empty estimation_market")
    must_raise(
        lambda: es.abnormal_return_variance(0.02, [1.0, 1.0, 1.0], 2.0),
        "zero variance estimation market",
    )


# ---------------------------------------------------------------- CAR Tests


def test_car_aggregation() -> None:
    """car evaluates the exact cumulative sum of abnormal returns."""
    abnormal = [0.012, -0.004, 0.025, -0.001]
    expected = sum(abnormal)
    assert abs(es.car(abnormal) - expected) < 1e-12, "car must equal the exact sum"


def test_car_exceptions() -> None:
    """car raises ValueError on empty sequence."""
    must_raise(lambda: es.car([]), "empty abnormal sequence")


# ---------------------------------------------------------------- Event t-statistic Tests


def test_event_t_statistic_ddof_1() -> None:
    """event_t_statistic divides by sample standard error with ddof=1."""
    # K = 3, cars = [0.02, 0.04, 0.06], mean = 0.04
    # deviations: [-0.02, 0.0, 0.02], sum sq = 0.0004 + 0 + 0.0004 = 0.0008
    # sample var (ddof=1): 0.0008 / 2 = 0.0004, s = 0.02
    # standard error = 0.02 / sqrt(3)
    # t = 0.04 / (0.02 / sqrt(3)) = 2 * sqrt(3) = 3.464101615
    cars = [0.02, 0.04, 0.06]
    t_val = es.event_t_statistic(cars)
    expected_t = 2.0 * math.sqrt(3.0)
    assert abs(t_val - expected_t) < 1e-9, f"expected t {expected_t}, got {t_val}"


def test_event_t_statistic_exceptions() -> None:
    """event_t_statistic rejects inputs with K < 2 or zero variance."""
    must_raise(lambda: es.event_t_statistic([0.05]), "fewer than 2 CARs")
    must_raise(lambda: es.event_t_statistic([0.03, 0.03, 0.03]), "zero variance across CARs")


# ---------------------------------------------------------------- Clustered t-statistic Tests


def test_clustered_t_statistic_cr1_formula() -> None:
    """clustered_t_statistic computes CR1 cluster variance with G/(G-1) factor."""
    # 4 observations in 2 clusters:
    # Cluster A: obs 1 = 0.04, obs 2 = 0.06 (mean = 0.05)
    # Cluster B: obs 3 = -0.02, obs 4 = 0.00 (mean = -0.01)
    # Overall mean = 0.08 / 4 = 0.02
    # Cluster A sum of deviations: (0.04 - 0.02) + (0.06 - 0.02) = 0.02 + 0.04 = 0.06
    # Cluster B sum of deviations: (-0.02 - 0.02) + (0.00 - 0.02) = -0.04 - 0.02 = -0.06
    # Sum of squared cluster sums: 0.06^2 + (-0.06)^2 = 0.0036 + 0.0036 = 0.0072
    # G = 2, G / (G - 1) = 2 / 1 = 2
    # N = 4, N^2 = 16
    # V = 2 * (0.0072 / 16) = 2 * 0.00045 = 0.0009
    # SE = sqrt(0.009) = 0.03
    # t = 0.02 / 0.03 = 2/3 = 0.6666666667
    vals = [0.04, 0.06, -0.02, 0.00]
    clusters = ["A", "A", "B", "B"]
    t_val = es.clustered_t_statistic(vals, clusters)
    expected_t = 2.0 / 3.0
    assert abs(t_val - expected_t) < 1e-9, f"expected clustered t {expected_t}, got {t_val}"


def test_clustered_t_differs_from_iid() -> None:
    """Clustering across shared shocks alters standard errors compared to iid."""
    # Correlated within clusters
    vals = [0.05, 0.05, -0.01, -0.01]
    clusters = ["G1", "G1", "G2", "G2"]
    t_clustered = es.clustered_t_statistic(vals, clusters)
    # iid standard error would be much smaller because it ignores cluster correlation
    t_iid = es.event_t_statistic(vals)
    assert abs(t_clustered) < abs(t_iid), "clustered t-stat should reflect wider cluster variance"


def test_clustered_t_exceptions() -> None:
    """clustered_t_statistic validates inputs."""
    must_raise(lambda: es.clustered_t_statistic([], []), "empty sequence")
    must_raise(lambda: es.clustered_t_statistic([0.01, 0.02], ["A"]), "length mismatch")
    must_raise(lambda: es.clustered_t_statistic([0.01, 0.02], ["A", "A"]), "fewer than 2 clusters")


# ---------------------------------------------------------------- Placebo Dates Tests


def test_placebo_dates_exclusion_and_determinism() -> None:
    """placebo_dates respects half-window exclusion zones and is reproducible."""
    calendar_len = 100
    events = [20, 50, 80]
    half_w = 3
    count = 10
    p1 = es.placebo_dates(calendar_len, events, half_w, count, seed=42)
    p2 = es.placebo_dates(calendar_len, events, half_w, count, seed=42)
    assert p1 == p2, "placebo_dates must be deterministic for identical seed"
    assert len(p1) == count, f"must return exactly {count} placebo dates"
    assert len(set(p1)) == count, "all placebo dates must be distinct"

    # Invariant: no date within half_w of any event
    for p in p1:
        for e in events:
            assert abs(p - e) > half_w, f"placebo date {p} is within exclusion zone of event day {e}"


def test_placebo_dates_exceptions() -> None:
    """placebo_dates rejects negative half_window or impossible count."""
    must_raise(lambda: es.placebo_dates(50, [25], -1, 5, seed=1), "negative half_window in placebo_dates")
    must_raise(
        lambda: es.placebo_dates(10, [5], 4, 10, seed=1),
        "count exceeds eligible days in placebo_dates",
    )


# ---------------------------------------------------------------- Event Window CAR Tests


def test_event_window_car_instance_consistency() -> None:
    """event_window_car reproduces reference values for instance seed."""
    stk: list[float] = list(INST["stock"])
    mkt: list[float] = list(INST["market"])
    est_len: int = INST["est_len"]
    window: tuple[int, int] = INST["window"]
    ev_days: list[int] = list(INST["event_days"])
    exp_cars: list[float] = list(INST["cars"])
    exp_vars: list[float] = list(INST["car_vars"])

    for i, ev in enumerate(ev_days):
        c_val, c_var = es.event_window_car(stk, mkt, ev, est_len, window)
        assert abs(c_val - exp_cars[i]) < 1e-7, f"event {i} CAR mismatch: expected {exp_cars[i]}, got {c_val}"
        assert abs(c_var - exp_vars[i]) < 1e-7, f"event {i} CAR variance mismatch: expected {exp_vars[i]}, got {c_var}"


def test_event_window_car_shift_invariance_and_no_lookahead() -> None:
    """Shifting returns outside the estimation and event windows has zero effect."""
    stk: list[float] = list(INST["stock"])
    mkt: list[float] = list(INST["market"])
    est_len: int = INST["est_len"]
    window: tuple[int, int] = INST["window"]
    ev: int = INST["event_days"][0]

    c_base, v_base = es.event_window_car(stk, mkt, ev, est_len, window)

    # Modify stock returns on day 0 (which is well before estimation window of event 0)
    stk_mod = list(stk)
    stk_mod[0] += 10.0
    c_mod, v_mod = es.event_window_car(stk_mod, mkt, ev, est_len, window)
    assert abs(c_base - c_mod) < 1e-12, "irrelevant days outside window must not alter CAR"
    assert abs(v_base - v_mod) < 1e-12, "irrelevant days outside window must not alter CAR variance"

    # Shift all days in the event window by constant c = 0.05
    # Window length = b - a + 1 = 1 - (-1) + 1 = 3 days
    stk_shift = list(stk)
    shift_c = 0.05
    for t in range(ev + window[0], ev + window[1] + 1):
        stk_shift[t] += shift_c

    c_shifted, v_shifted = es.event_window_car(stk_shift, mkt, ev, est_len, window)
    expected_shift = 3 * shift_c
    assert abs((c_shifted - c_base) - expected_shift) < 1e-10, (
        "event window shift must change CAR by exactly (b - a + 1) * shift_c"
    )
    # Variance of AR depends on estimation window which was NOT modified
    assert abs(v_shifted - v_base) < 1e-10, "estimation window variance must be unaffected"


def test_event_window_car_exceptions() -> None:
    """event_window_car enforces bounds on windows."""
    stk = [0.01] * 50
    mkt = [0.01] * 50
    must_raise(lambda: es.event_window_car(stk, mkt, 30, 20, (2, 1)), "window start > window end")
    must_raise(
        lambda: es.event_window_car(stk, mkt, 10, 20, (-1, 1)),
        "estimation window starts before day 0",
    )
    must_raise(lambda: es.event_window_car(stk, mkt, 49, 10, (-1, 1)), "event window exceeds length")


# ---------------------------------------------------------------- End-to-End Pipeline Tests


def test_planted_shock_statistical_significance() -> None:
    """Planted announcement shock produces a statistically significant positive t-statistic."""
    cars: list[float] = list(INST["cars"])
    t_stat = es.event_t_statistic(cars)
    assert t_stat > 2.0, f"event t-statistic must detect planted positive shock with t > 2.0 (got {t_stat:.2f})"
