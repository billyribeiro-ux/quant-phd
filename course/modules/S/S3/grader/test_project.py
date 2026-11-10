"""Acceptance suite for the S3 project: Pairs-trading audit.

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Each test checks econometric properties, exact numbers, invariance principles,
boundary edge cases, or named exception conditions.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable
from typing import Any

import pytest
from instance import make_instance

try:
    import pairs_audit as pa
except ImportError:
    import reference as pa  # type: ignore[no-redef]

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail with a descriptive message unless call() raises ValueError."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"Missing required ValueError for condition: {condition}")


def is_close(a: float, b: float, tol: float = 1e-7) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol * (1.0 + abs(b))


def test_alpha_beta_exact() -> None:
    """Test 1: alpha_beta recovers exact planted alpha and beta on noise-free pair."""
    pair = INST["pairs"][0]
    alpha, beta = pa.alpha_beta(pair["y"], pair["x"])
    assert is_close(alpha, pair["true_alpha"], tol=1e-8), (
        "alpha_beta failed to recover exact intercept on noise-free data."
    )
    assert is_close(beta, pair["true_beta"], tol=1e-8), "alpha_beta failed to recover exact slope on noise-free data."


def test_adf_t_invariance() -> None:
    """Test 2: adf_t is invariant to constant shifts and positive scaling."""
    series = INST["pairs"][1]["y"]
    base_t = pa.adf_t(series, lags=1)
    shifted = [val + 42.5 for val in series]
    scaled = [val * 3.14 for val in series]
    shift_scale = [(val + 10.0) * 2.5 for val in series]

    assert is_close(pa.adf_t(shifted, lags=1), base_t, tol=1e-6), "adf_t is not invariant to adding a constant."
    assert is_close(pa.adf_t(scaled, lags=1), base_t, tol=1e-6), "adf_t is not invariant to positive scaling."
    assert is_close(pa.adf_t(shift_scale, lags=1), base_t, tol=1e-6), "adf_t is not invariant to affine scaling."


def test_adf_t_stationary_vs_random_walk() -> None:
    """Test 3: adf_t distinguishes stationary spread from unit root."""
    # Cointegrated residuals in formation are stationary -> stat < df_critical
    y_coint = INST["pairs"][1]["y"][: INST["split"]]
    x_coint = INST["pairs"][1]["x"][: INST["split"]]
    a, b = pa.alpha_beta(y_coint, x_coint)
    u_coint = [y_coint[t] - a - b * x_coint[t] for t in range(len(y_coint))]
    stat_stationary = pa.adf_t(u_coint, lags=1)

    # Independent random walk -> stat > df_critical
    rw_series = INST["pairs"][3]["y"][: INST["split"]]
    stat_rw = pa.adf_t(rw_series, lags=1)

    df_crit = INST["df_critical_5pct"]
    assert stat_stationary < df_crit, (
        f"Stationary residual failed to reject unit root: stat={stat_stationary} >= crit={df_crit}"
    )
    assert stat_rw > df_crit, f"Independent random walk spuriously rejected unit root: stat={stat_rw} <= crit={df_crit}"


def test_eg_t_cointegrated_vs_random_walk() -> None:
    """Test 4: eg_t rejects for cointegrated pair and fails to reject for random walks."""
    coint = INST["pairs"][1]
    rw1 = INST["pairs"][3]
    rw2 = INST["pairs"][4]
    eg_crit = INST["eg_critical_5pct"]

    stat_coint = pa.eg_t(coint["y"], coint["x"], INST["split"], lags=1)
    stat_rw1 = pa.eg_t(rw1["y"], rw1["x"], INST["split"], lags=1)
    stat_rw2 = pa.eg_t(rw2["y"], rw2["x"], INST["split"], lags=1)

    assert stat_coint < eg_crit, (
        f"eg_t failed to detect cointegration on planted cointegrated pair: stat={stat_coint} >= crit={eg_crit}"
    )
    assert stat_rw1 > eg_crit, (
        f"eg_t falsely detected cointegration on independent random walk 1: stat={stat_rw1} <= crit={eg_crit}"
    )
    assert stat_rw2 > eg_crit, (
        f"eg_t falsely detected cointegration on independent random walk 2: stat={stat_rw2} <= crit={eg_crit}"
    )


def test_eg_t_no_intercept_convention() -> None:
    """Test 5: eg_t matches independent residual ADF with no intercept."""
    coint = INST["pairs"][1]
    split = INST["split"]
    a, b = pa.alpha_beta(coint["y"][:split], coint["x"][:split])
    u = [coint["y"][t] - a - b * coint["x"][t] for t in range(split)]

    # Compute residual ADF without intercept manually
    m = len(u)
    du = [u[i] - u[i - 1] for i in range(1, m)]
    y_dep = du[1:]
    x0 = [u[t - 1] for t in range(2, m)]
    x1 = [du[t - 2] for t in range(2, m)]
    n_obs = len(y_dep)

    s00 = sum(x0[r] * x0[r] for r in range(n_obs))
    s01 = sum(x0[r] * x1[r] for r in range(n_obs))
    s11 = sum(x1[r] * x1[r] for r in range(n_obs))
    det = s00 * s11 - s01 * s01
    inv00 = s11 / det
    inv01 = -s01 / det
    sy0 = sum(x0[r] * y_dep[r] for r in range(n_obs))
    sy1 = sum(x1[r] * y_dep[r] for r in range(n_obs))
    gamma = inv00 * sy0 + inv01 * sy1
    delta = inv01 * sy0 + (s00 / det) * sy1

    res = [y_dep[r] - gamma * x0[r] - delta * x1[r] for r in range(n_obs)]
    rss = sum(r * r for r in res)
    sigma2 = rss / (n_obs - 2)
    se_gamma = math.sqrt(sigma2 * inv00)
    expected_stat = gamma / se_gamma

    actual_stat = pa.eg_t(coint["y"], coint["x"], split, lags=1)
    assert is_close(actual_stat, expected_stat, tol=1e-7), (
        "eg_t did not match residual ADF specification without intercept."
    )


def test_half_life_exact_exponential() -> None:
    """Test 6: half_life on noiseless exponential decay s_t = 0.9^t equals ln(2)/(-ln(0.9))."""
    path = [0.9**t for t in range(60)]
    expected_hl = math.log(2.0) / (-math.log(0.9))
    actual_hl = pa.half_life(path)
    assert is_close(actual_hl, expected_hl, tol=1e-8), (
        f"half_life on exact exponential path returned {actual_hl}, expected {expected_hl}"
    )


def test_half_life_linear_returns_inf() -> None:
    """Test 7: half_life on linear ramp s_t = float(t) returns math.inf."""
    path = [float(t) for t in range(50)]
    assert pa.half_life(path) == math.inf, "half_life on linear path (unit root) must return math.inf"


def test_half_life_negative_phi_raises() -> None:
    """Test 8: half_life on alternating path s_t = (-0.5)^t raises ValueError."""
    path = [(-0.5) ** t for t in range(40)]
    must_raise(lambda: pa.half_life(path), "half_life with phi <= 0 must raise ValueError")


def test_half_life_shift_scale_invariance() -> None:
    """Test 9: half_life is invariant to shift and positive scale."""
    path = [0.85**t for t in range(50)]
    base_hl = pa.half_life(path)
    shifted = [val + 15.0 for val in path]
    scaled = [val * 4.0 for val in path]
    shift_scale = [(val + 5.0) * 2.0 for val in path]

    assert is_close(pa.half_life(shifted), base_hl, tol=1e-6), "half_life is not invariant to shift."
    assert is_close(pa.half_life(scaled), base_hl, tol=1e-6), "half_life is not invariant to positive scaling."
    assert is_close(pa.half_life(shift_scale), base_hl, tol=1e-6), "half_life is not invariant to affine scaling."


def test_trading_spread_no_lookahead() -> None:
    """Test 10: trading_spread estimates alpha and beta on formation only."""
    pair = INST["pairs"][1]
    split = INST["split"]
    y = list(pair["y"])
    x = list(pair["x"])

    spread_orig = pa.trading_spread(y, x, split)
    a_orig, b_orig = pa.alpha_beta(y[:split], x[:split])

    # Perturb the trading window values
    y_perturbed = list(y)
    x_perturbed = list(x)
    for t in range(split, len(y)):
        y_perturbed[t] += 5.0
        x_perturbed[t] += 2.0

    spread_perturbed = pa.trading_spread(y_perturbed, x_perturbed, split)

    # Point-wise check: trading spread must use original alpha and beta
    for idx, t in enumerate(range(split, len(y))):
        expected_orig = y[t] - a_orig - b_orig * x[t]
        expected_pert = y_perturbed[t] - a_orig - b_orig * x_perturbed[t]
        assert is_close(spread_orig[idx], expected_orig, tol=1e-8), "trading_spread returned incorrect baseline value."
        assert is_close(spread_perturbed[idx], expected_pert, tol=1e-8), (
            "trading_spread lookahead defect: hedge ratio changed when trading window data was altered."
        )


def test_survives_decision_rules() -> None:
    """Test 11: survives requires both eg_stat < eg_critical and finite half-life."""
    eg_crit = INST["eg_critical_5pct"]

    # Cointegrated pair with finite half-life survives
    coint = INST["pairs"][1]
    split = INST["split"]
    stat_coint = pa.eg_t(coint["y"], coint["x"], split, lags=1)
    spread_coint = pa.trading_spread(coint["y"], coint["x"], split)
    hl_coint = pa.half_life(spread_coint)
    assert pa.survives(stat_coint, eg_crit, hl_coint) is True, "Planted cointegrated pair must survive audit."

    # Break pair: passes EG in formation, but trading half-life is inf -> fails survival
    bp = INST["pairs"][5]
    stat_bp = pa.eg_t(bp["y"], bp["x"], split, lags=1)
    spread_bp = pa.trading_spread(bp["y"], bp["x"], split)
    hl_bp = pa.half_life(spread_bp)
    assert stat_bp < eg_crit, "Break pair was expected to pass EG in formation window."
    assert hl_bp == math.inf, "Break pair was expected to have infinite trading half-life."
    assert pa.survives(stat_bp, eg_crit, hl_bp) is False, "Break pair with infinite half-life must NOT survive."

    # Marginal pair: stat is between eg_crit and df_crit -> fails survival under eg_crit
    mp = INST["pairs"][2]
    stat_mp = pa.eg_t(mp["y"], mp["x"], split, lags=1)
    assert eg_crit < stat_mp, "Marginal pair stat was expected to be above eg_critical."
    assert pa.survives(stat_mp, eg_crit, 5.0) is False, "Pair with eg_stat > eg_critical must NOT survive."

    # Explicit threshold tests
    assert pa.survives(eg_crit - 0.01, eg_crit, 10.0) is True
    assert pa.survives(eg_crit + 0.01, eg_crit, 10.0) is False
    assert pa.survives(eg_crit - 0.01, eg_crit, math.inf) is False


def test_named_value_errors() -> None:
    """Test 12: functions raise ValueError for the five named error conditions."""
    split = INST["split"]
    valid_y = INST["pairs"][1]["y"]
    valid_x = INST["pairs"][1]["x"]

    # (i) Length mismatch
    must_raise(lambda: pa.alpha_beta(valid_y, valid_x[:-1]), "alpha_beta length mismatch")
    must_raise(lambda: pa.trading_spread(valid_y, valid_x[:-1], split), "trading_spread length mismatch")
    must_raise(lambda: pa.eg_t(valid_y, valid_x[:-1], split, lags=1), "eg_t length mismatch")

    # (ii) Negative lags
    must_raise(lambda: pa.adf_t(valid_y, lags=-1), "adf_t negative lags")
    must_raise(lambda: pa.eg_t(valid_y, valid_x, split, lags=-1), "eg_t negative lags")

    # lags=0 is a valid edge case
    stat_lags0 = pa.adf_t(valid_y, lags=0)
    assert math.isfinite(stat_lags0), "adf_t with lags=0 should be finite"

    # (iii) split out of bounds (<30 or > n-30)
    must_raise(lambda: pa.trading_spread(valid_y, valid_x, 25), "trading_spread split < 30")
    must_raise(lambda: pa.trading_spread(valid_y, valid_x, len(valid_y) - 20), "trading_spread split > n - 30")
    must_raise(lambda: pa.eg_t(valid_y, valid_x, 25, lags=1), "eg_t split < 30")

    # (iv) Non-finite inputs
    nan_series = list(valid_y)
    nan_series[5] = float("nan")
    must_raise(lambda: pa.adf_t(nan_series, lags=1), "adf_t with NaN")
    must_raise(lambda: pa.alpha_beta(nan_series, valid_x), "alpha_beta with NaN")
    must_raise(lambda: pa.trading_spread(nan_series, valid_x, split), "trading_spread with NaN")
    must_raise(lambda: pa.eg_t(nan_series, valid_x, split, lags=1), "eg_t with NaN")
    must_raise(lambda: pa.half_life(nan_series), "half_life with NaN")

    inf_series = list(valid_y)
    inf_series[10] = float("inf")
    must_raise(lambda: pa.half_life(inf_series), "half_life with inf")


def test_split_bounds_edge_cases() -> None:
    """Test 13: split boundary edge cases at 30 and n-30."""
    valid_y = INST["pairs"][1]["y"]
    valid_x = INST["pairs"][1]["x"]
    n = len(valid_y)

    # Valid boundary cases
    sp_lower = pa.trading_spread(valid_y, valid_x, 30)
    assert len(sp_lower) == n - 30
    sp_upper = pa.trading_spread(valid_y, valid_x, n - 30)
    assert len(sp_upper) == 30

    eg_lower = pa.eg_t(valid_y, valid_x, 30, lags=1)
    assert math.isfinite(eg_lower)
    eg_upper = pa.eg_t(valid_y, valid_x, n - 30, lags=1)
    assert math.isfinite(eg_upper)

    # Invalid boundary cases (one step over)
    must_raise(lambda: pa.trading_spread(valid_y, valid_x, 29), "split=29 rejected")
    must_raise(lambda: pa.trading_spread(valid_y, valid_x, n - 29), "split=n-29 rejected")
    must_raise(lambda: pa.eg_t(valid_y, valid_x, 29, lags=1), "split=29 rejected in eg_t")
    must_raise(lambda: pa.eg_t(valid_y, valid_x, n - 29, lags=1), "split=n-29 rejected in eg_t")
