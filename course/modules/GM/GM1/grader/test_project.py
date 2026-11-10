"""Acceptance test suite for Atlas A18 Nowcasting & Macro Dashboard (atlas.macro).

Tests dynamic factor model estimation, ragged-edge Kalman filtering,
news decomposition identities, surprise index construction, regime classification,
and cross-asset sensitivity monitoring.
"""

from __future__ import annotations

import math
import os
from typing import Any, cast

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

try:
    from atlas.macro import (  # type: ignore[import-not-found, unused-ignore]
        DynamicFactorNowcaster,
        build_surprise_index,
        calculate_surprises,
        classify_growth_inflation_regime,
        compute_regime_probabilities,
        cross_asset_macro_sensitivity,
        decompose_news,
    )
except ImportError:
    try:
        from macro import (  # type: ignore[import-not-found, unused-ignore]
            DynamicFactorNowcaster,
            build_surprise_index,
            calculate_surprises,
            classify_growth_inflation_regime,
            compute_regime_probabilities,
            cross_asset_macro_sensitivity,
            decompose_news,
        )
    except ImportError:
        from reference import (  # type: ignore[import-not-found, unused-ignore]
            DynamicFactorNowcaster,
            build_surprise_index,
            calculate_surprises,
            classify_growth_inflation_regime,
            compute_regime_probabilities,
            cross_asset_macro_sensitivity,
            decompose_news,
        )


@pytest.fixture(scope="module")
def seed() -> int:
    return int(os.environ.get("QF_SEED", "0"))


@pytest.fixture(scope="module")
def inst(seed: int) -> dict[str, Any]:
    return cast(dict[str, Any], make_instance(seed))


# --- 1. Dynamic Factor Model & Estimation Tests ---


def test_dfm_fit_properties(inst: dict[str, Any]) -> None:
    x_bal = inst["x_balanced"]
    n_factors = inst["n_factors"]
    target = inst["target_balanced"]

    model = DynamicFactorNowcaster(n_factors=n_factors)
    fitted = model.fit(x_bal, y_target=target)
    assert fitted is model

    # Check loadings
    assert model.loadings_ is not None
    assert model.loadings_.shape == (x_bal.shape[1], n_factors)

    # Check VAR(1) transition matrix stability
    assert model.trans_a_ is not None
    assert model.trans_a_.shape == (n_factors, n_factors)
    eigvals = np.linalg.eigvals(model.trans_a_)
    assert np.all(np.abs(eigvals) < 1.0), "VAR(1) transition matrix must be stationary (spectral radius < 1)"

    # Check covariance matrices
    assert model.trans_q_ is not None
    assert model.trans_q_.shape == (n_factors, n_factors)
    assert np.all(np.linalg.eigvalsh(model.trans_q_) > 0.0), "Q must be positive definite"

    assert model.meas_r_ is not None
    assert model.meas_r_.shape == (x_bal.shape[1], x_bal.shape[1])
    assert np.all(np.diag(model.meas_r_) > 0.0), "Measurement error variance must be strictly positive"


def test_dfm_validation_errors() -> None:
    model = DynamicFactorNowcaster(n_factors=2)
    # n_factors <= 0
    with pytest.raises(ValueError):
        DynamicFactorNowcaster(n_factors=0)

    # 1D array
    with pytest.raises(ValueError):
        model.fit(np.array([1.0, 2.0, 3.0]))

    # Array with NaN
    x_nan = np.ones((50, 5))
    x_nan[2, 2] = np.nan
    with pytest.raises(ValueError):
        model.fit(x_nan)

    # n_factors >= N
    with pytest.raises(ValueError):
        DynamicFactorNowcaster(n_factors=6).fit(np.ones((50, 4)))


# --- 2. Ragged-Edge Kalman Filtering Tests ---


def test_kalman_filter_ragged(inst: dict[str, Any]) -> None:
    x_bal = inst["x_balanced"]
    x_ragged = inst["x_ragged_old"]
    n_factors = inst["n_factors"]

    model = DynamicFactorNowcaster(n_factors=n_factors).fit(x_bal)
    factors, covs = model.filter_ragged(x_ragged)

    t_len = x_ragged.shape[0]
    assert factors.shape == (t_len, n_factors)
    assert covs.shape == (t_len, n_factors, n_factors)
    assert np.all(np.isfinite(factors)), "Filtered factors must be finite despite ragged edge"

    # Covariance matrices must be symmetric positive semi-definite
    for t in range(t_len):
        cov_t = covs[t]
        assert np.allclose(cov_t, cov_t.T, atol=1e-8), f"Covariance at t={t} not symmetric"
        eigs = np.linalg.eigvalsh(cov_t)
        assert np.all(eigs >= -1e-8), f"Covariance at t={t} has negative eigenvalue {np.min(eigs)}"


def test_nowcast_precision(inst: dict[str, Any]) -> None:
    x_bal = inst["x_balanced"]
    x_ragged = inst["x_ragged_old"]
    target = inst["target_balanced"]
    n_factors = inst["n_factors"]

    model = DynamicFactorNowcaster(n_factors=n_factors).fit(x_bal, y_target=target)
    pred = model.nowcast(x_ragged)
    assert isinstance(pred, float)
    assert math.isfinite(pred)

    # Identical call gives identical answer
    pred2 = model.nowcast(x_ragged)
    assert pred == pred2


# --- 3. News Decomposition Tests ---


def test_news_decomposition_articulation(inst: dict[str, Any]) -> None:
    x_bal = inst["x_balanced"]
    x_old = inst["x_ragged_old"]
    x_new = inst["x_ragged_new"]
    target = inst["target_balanced"]
    n_factors = inst["n_factors"]

    model = DynamicFactorNowcaster(n_factors=n_factors).fit(x_bal, y_target=target)
    decomp = decompose_news(model, x_old, x_new)

    assert "old_nowcast" in decomp
    assert "new_nowcast" in decomp
    assert "total_revision" in decomp
    assert "contributions" in decomp

    old_val = decomp["old_nowcast"]
    new_val = decomp["new_nowcast"]
    tot_rev = decomp["total_revision"]
    contribs = decomp["contributions"]

    assert tot_rev == pytest.approx(new_val - old_val, abs=1e-9)
    # The fundamental Giannone-Reichlin-Small identity: sum(contributions) == total_revision
    assert np.sum(contribs) == pytest.approx(tot_rev, abs=1e-7)


# --- 4. Economic Surprise Index Tests ---


def test_calculate_surprises_formula() -> None:
    actuals = np.array([[105.0, 2.4], [102.0, 2.1]])
    consensus = np.array([[100.0, 2.0], [104.0, 2.3]])
    hist_std = np.array([2.5, 0.2])

    surp = calculate_surprises(actuals, consensus, hist_std)
    # Row 0: [(105 - 100)/2.5, (2.4 - 2.0)/0.2] = [2.0, 2.0]
    # Row 1: [(102 - 104)/2.5, (2.1 - 2.3)/0.2] = [-0.8, -1.0]
    assert np.allclose(surp[0], [2.0, 2.0])
    assert np.allclose(surp[1], [-0.8, -1.0])

    # Validation: negative standard deviation
    with pytest.raises(ValueError):
        calculate_surprises(actuals, consensus, np.array([2.5, -0.2]))


def test_build_surprise_index_properties(inst: dict[str, Any]) -> None:
    actuals = inst["actuals"]
    consensus = inst["consensus"]
    hist_std = inst["historical_std"]
    weights = inst["surprise_weights"]

    surp = calculate_surprises(actuals, consensus, hist_std)
    esi = build_surprise_index(surp, weights, half_life=20.0, normalize=True)

    assert len(esi) == len(actuals)
    assert np.mean(esi) == pytest.approx(0.0, abs=1e-7)
    assert np.std(esi, ddof=1) == pytest.approx(1.0, abs=1e-7)

    # Half life validation
    with pytest.raises(ValueError):
        build_surprise_index(surp, weights, half_life=0.0)


# --- 5. Macro Regime Classifier Tests ---


def test_regime_classification_quadrants() -> None:
    # Quadrant 1: Growth >= 0, Inflation < 0 -> Goldilocks
    assert classify_growth_inflation_regime(1.5, -0.5) == "Goldilocks"
    # Quadrant 2: Growth >= 0, Inflation >= 0 -> Reflation
    assert classify_growth_inflation_regime(1.5, 0.8) == "Reflation"
    # Quadrant 3: Growth < 0, Inflation >= 0 -> Stagflation
    assert classify_growth_inflation_regime(-1.0, 1.2) == "Stagflation"
    # Quadrant 4: Growth < 0, Inflation < 0 -> Deflation
    assert classify_growth_inflation_regime(-1.0, -0.7) == "Deflation"

    # Array classification
    g = np.array([1.0, 1.0, -1.0, -1.0])
    inf = np.array([-0.5, 0.5, 0.5, -0.5])
    labels = classify_growth_inflation_regime(g, inf)
    assert list(labels) == ["Goldilocks", "Reflation", "Stagflation", "Deflation"]


def test_regime_probabilities_sum_to_one(inst: dict[str, Any]) -> None:
    growth = inst["growth_signal"]
    inflation = inst["inflation_signal"]

    probs = compute_regime_probabilities(growth, inflation, bandwidth=1.0)
    assert probs.shape == (len(growth), 4)
    assert np.all(probs >= 0.0)
    assert np.all(probs <= 1.0)
    assert np.allclose(np.sum(probs, axis=1), 1.0, atol=1e-8)


# --- 6. Cross-Asset Macro Monitor Tests ---


def test_cross_asset_monitor(inst: dict[str, Any]) -> None:
    asset_rets = inst["asset_returns"]
    macro_sig = inst["macro_signals"]
    growth = inst["growth_signal"]
    inflation = inst["inflation_signal"]

    regime_labels = classify_growth_inflation_regime(growth, inflation)
    results = cross_asset_macro_sensitivity(asset_rets, macro_sig, regime_labels)

    assert "betas" in results
    assert "regime_mean_returns" in results
    assert "regime_sharpe" in results

    betas = results["betas"]
    assert betas.shape == (asset_rets.shape[1], macro_sig.shape[1])

    # Regimes present
    for reg in ["Goldilocks", "Reflation", "Stagflation", "Deflation"]:
        assert reg in results["regime_mean_returns"]
        assert len(results["regime_mean_returns"][reg]) == asset_rets.shape[1]
