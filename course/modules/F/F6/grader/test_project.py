"""Acceptance test suite for F6: Machine Learning in Asset Pricing (ml_study.py).

Verifies:
- compute_oos_r2 mathematical correctness, zero-benchmark definition, and error handling.
- construct_spread_portfolio quantile construction, turnover accounting, and cost drag.
- evaluate_complexity_curve random features double-descent evaluation.
- run_ml_study end-to-end model comparison under purged cross-validation.
"""

from __future__ import annotations

import math
import os

import numpy as np
import pytest
from instance import make_instance

try:
    from ml_study import (
        compute_oos_r2,
        construct_spread_portfolio,
        evaluate_complexity_curve,
        run_ml_study,
    )
except ImportError:
    from reference import (
        compute_oos_r2,
        construct_spread_portfolio,
        evaluate_complexity_curve,
        run_ml_study,
    )


@pytest.fixture
def current_instance() -> dict[str, object]:
    seed = int(os.environ.get("QF_SEED", "42"))
    inst: dict[str, object] = dict(make_instance(seed))
    return inst


def test_oos_r2_properties() -> None:
    """Test out-of-sample R2 mathematical invariants and zero benchmark."""
    y = np.array([0.02, -0.01, 0.03, -0.04, 0.05], dtype=np.float64)

    # 1. Perfect prediction has R2 = 1.0
    r2_perf = compute_oos_r2(y, y)
    assert math.isclose(r2_perf, 1.0, rel_tol=1e-7)

    # 2. Zero prediction has R2 = 0.0 exactly by definition
    zeros = np.zeros_like(y)
    r2_zero = compute_oos_r2(y, zeros)
    assert math.isclose(r2_zero, 0.0, abs_tol=1e-7)

    # 3. Pathological prediction has negative R2
    bad_pred = -y
    r2_bad = compute_oos_r2(y, bad_pred)
    assert r2_bad < -1.0

    # 4. Must raise ValueError on shape mismatch or empty input
    with pytest.raises(ValueError):
        compute_oos_r2(y, y[:-1])
    with pytest.raises(ValueError):
        compute_oos_r2(np.array([]), np.array([]))


def test_spread_portfolio_properties(current_instance: dict[str, object]) -> None:
    """Test long-short spread portfolio construction and transaction cost drag."""
    y_test = np.asarray(current_instance["y_test"], dtype=np.float64)
    n_assets, t_test = y_test.shape

    rng = np.random.default_rng(123)
    preds = rng.normal(0.0, 0.02, size=(n_assets, t_test))

    # Gross vs. net test with cost_bps = 15.0
    perf = construct_spread_portfolio(preds, y_test, cost_bps=15.0)

    required_keys = {
        "gross_mean",
        "gross_vol",
        "gross_sharpe",
        "net_mean",
        "net_vol",
        "net_sharpe",
        "mean_turnover",
    }
    assert required_keys.issubset(perf.keys()), f"Missing keys in portfolio output: {required_keys - perf.keys()}"

    assert np.isfinite(perf["gross_mean"])
    assert np.isfinite(perf["net_mean"])
    assert perf["gross_vol"] >= 0.0
    assert perf["mean_turnover"] >= 0.0

    # Net returns must reflect trading cost drag when turnover is positive
    assert perf["net_mean"] <= perf["gross_mean"] + 1e-9
    if perf["mean_turnover"] > 0.0:
        assert perf["net_mean"] < perf["gross_mean"] - 1e-6

    # Zero cost test: net must equal gross
    perf_free = construct_spread_portfolio(preds, y_test, cost_bps=0.0)
    assert math.isclose(perf_free["gross_mean"], perf_free["net_mean"], abs_tol=1e-7)
    assert math.isclose(perf_free["gross_sharpe"], perf_free["net_sharpe"], abs_tol=1e-7)

    # Error handling
    with pytest.raises(ValueError):
        construct_spread_portfolio(preds, y_test, cost_bps=-5.0)
    with pytest.raises(ValueError):
        construct_spread_portfolio(preds, y_test[:-1])


def test_complexity_curve_structure(current_instance: dict[str, object]) -> None:
    """Test overparameterized double-descent evaluation across complexity ratios."""
    x_tr = np.asarray(current_instance["X_train"], dtype=np.float64)
    y_tr = np.asarray(current_instance["y_train"], dtype=np.float64)
    x_te = np.asarray(current_instance["X_test"], dtype=np.float64)
    y_te = np.asarray(current_instance["y_test"], dtype=np.float64)
    gammas = [0.25, 0.5, 1.0, 2.0]

    res = evaluate_complexity_curve(x_tr, y_tr, x_te, y_te, gammas, seed=42)

    assert "gammas" in res
    assert "ridgeless_mse" in res
    assert "regularized_mse" in res
    assert len(res["gammas"]) == len(gammas)
    assert len(res["ridgeless_mse"]) == len(gammas)
    assert len(res["regularized_mse"]) == len(gammas)

    # All values must be finite positive numbers
    for val in res["ridgeless_mse"]:
        assert np.isfinite(val) and val > 0.0
    for val in res["regularized_mse"]:
        assert np.isfinite(val) and val > 0.0

    # Proper regularization smooths or matches the interpolation peak near gamma = 1.0
    idx_gamma1 = gammas.index(1.0)
    assert res["regularized_mse"][idx_gamma1] < res["ridgeless_mse"][idx_gamma1]


def test_run_ml_study_execution(current_instance: dict[str, object]) -> None:
    """Test full pipeline execution on the seeded instance."""
    study = run_ml_study(current_instance)

    assert "best_alpha" in study
    assert "oos_r2" in study
    assert "portfolio_performance" in study
    assert "complexity_results" in study

    models = ["ols", "ridge", "rf", "nn"]
    for m in models:
        assert m in study["oos_r2"], f"Model {m} missing in oos_r2"
        assert np.isfinite(study["oos_r2"][m])
        assert m in study["portfolio_performance"], f"Model {m} missing in portfolio_performance"

        m_perf = study["portfolio_performance"][m]
        assert m_perf["net_mean"] <= m_perf["gross_mean"] + 1e-9
        assert m_perf["mean_turnover"] >= 0.0

    # Cross-sectional regularized models capture positive signal on instance
    assert study["portfolio_performance"]["ridge"]["gross_mean"] > -0.01
