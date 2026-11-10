"""Test suite for AP7 Sentiment-Index Replication.

Executes under pytest both locally and in Pyodide.
Reads QF_SEED environment variable (default 0) to obtain deterministic test instance.
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
import reference as ref  # type: ignore[import-not-found]
from instance import make_instance  # type: ignore[import-not-found]


@pytest.fixture
def instance_data() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "0"))
    data: dict[str, Any] = make_instance(seed)
    return data


def test_instance_structure(instance_data: dict[str, Any]) -> None:
    """Verify instance dictionary keys, array shapes, and finite values."""
    required_keys = [
        "raw_proxies",
        "macro_controls",
        "test_assets_returns",
        "market_returns",
        "proxy_names",
        "asset_names",
    ]
    for key in required_keys:
        assert key in instance_data, f"Missing key {key} in instance data"

    raw_proxies = instance_data["raw_proxies"]
    macro = instance_data["macro_controls"]
    test_assets = instance_data["test_assets_returns"]
    market = instance_data["market_returns"]

    assert raw_proxies.ndim == 2 and raw_proxies.shape == (180, 6)
    assert macro.ndim == 2 and macro.shape == (180, 4)
    assert test_assets.ndim == 2 and test_assets.shape == (180, 8)
    assert market.ndim == 1 and market.shape == (180,)
    assert np.all(np.isfinite(raw_proxies))
    assert np.all(np.isfinite(macro))
    assert np.all(np.isfinite(test_assets))
    assert np.all(np.isfinite(market))


def test_proxy_standardization_and_orthogonalization(instance_data: dict[str, Any]) -> None:
    """Verify that proxy standardization and macroeconomic orthogonalization satisfy OLS invariants."""
    raw = instance_data["raw_proxies"]
    macro = instance_data["macro_controls"]

    # 1. Standardization
    std_proxies = ref.standardize_proxies(raw)
    assert std_proxies.shape == raw.shape
    means = np.mean(std_proxies, axis=0)
    stds = np.std(std_proxies, axis=0, ddof=1)
    assert np.all(np.abs(means) < 1e-7), f"Standardized proxy means {means} must be zero"
    assert np.all(np.abs(stds - 1.0) < 1e-7), f"Standardized proxy standard deviations {stds} must equal 1.0"

    # 2. Orthogonalization
    ortho_proxies = ref.orthogonalize_proxies(std_proxies, macro)
    assert ortho_proxies.shape == raw.shape

    # Orthogonality condition: Residuals must be strictly orthogonal to macro controls and constant
    t_obs = len(macro)
    x_mat = np.column_stack([np.ones(t_obs), macro])
    projection_gap = np.abs(x_mat.T @ ortho_proxies)
    assert np.all(projection_gap < 1e-4), (
        f"Orthogonality projection condition violated; max gap = {np.max(projection_gap):.2e}"
    )

    # Cross-correlations between orthogonalized proxies and each macro control must be zero
    for m in range(macro.shape[1]):
        for k in range(raw.shape[1]):
            corr_val = np.corrcoef(ortho_proxies[:, k], macro[:, m])[0, 1]
            assert abs(corr_val) < 1e-5, f"Proxy {k} not orthogonalized against macro control {m}: corr={corr_val:.4f}"


def test_sentiment_index_properties(instance_data: dict[str, Any]) -> None:
    """Verify principal component extraction, sign anchor normalization, and variance explained."""
    std_proxies = ref.standardize_proxies(instance_data["raw_proxies"])
    ortho_proxies = ref.orthogonalize_proxies(std_proxies, instance_data["macro_controls"])

    # Extract with sign anchor on NIPO (index 2)
    sent_res = ref.extract_sentiment_index(ortho_proxies, sign_anchor_idx=2)

    assert "index" in sent_res
    assert "loadings" in sent_res
    assert "var_explained" in sent_res
    assert "eigenvalues" in sent_res

    index = sent_res["index"]
    loadings = sent_res["loadings"]
    var_exp = sent_res["var_explained"]

    # 1. Shape and standardization
    assert len(index) == 180
    assert abs(float(np.mean(index))) < 1e-7
    assert abs(float(np.std(index, ddof=1)) - 1.0) < 1e-7

    # 2. Sign anchor normalization: NIPO loading must be strictly positive
    assert loadings[2] > 0.0, f"Anchor proxy loading {loadings[2]:.4f} must be positive"

    # 3. Leading eigenvalue dominance: 30% to 90% of proxy variance explained
    assert 0.30 < var_exp < 0.90, f"Variance explained {var_exp:.2%} outside expected range [30%, 90%]"

    # 4. Orthogonality to macro factors preserved in aggregate index
    macro = instance_data["macro_controls"]
    for m in range(macro.shape[1]):
        corr_m = abs(float(np.corrcoef(index, macro[:, m])[0, 1]))
        assert corr_m < 1e-4, f"Aggregate sentiment index correlates with macro factor {m}: corr={corr_m:.4f}"


def test_newey_west_hac_properties(instance_data: dict[str, Any]) -> None:
    """Verify Newey-West HAC covariance estimation and Bartlett kernel weighting."""
    y = instance_data["market_returns"]
    t_obs = len(y)
    x = np.column_stack([np.ones(t_obs), np.sin(np.linspace(0, 3 * np.pi, t_obs))])

    # Run HAC with 4 lags
    lags = 4
    res = ref.newey_west_hac(x, y, lags=lags)

    assert len(res["beta"]) == 2
    assert len(res["se"]) == 2
    assert len(res["t_stats"]) == 2
    assert np.all(res["se"] > 0.0)

    # Verify t-stat identity: t = beta / se
    for k in range(2):
        expected_t = res["beta"][k] / res["se"][k]
        assert abs(res["t_stats"][k] - expected_t) < 1e-6

    # Verify OLS R^2 identity
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    ss_res = float(np.sum(res["residuals"] ** 2))
    expected_r2 = 1.0 - ss_res / ss_tot
    assert abs(res["r2"] - expected_r2) < 1e-6

    # Check against analytical Bartlett weights
    xtx_inv = np.linalg.inv(x.T @ x)
    u_x = res["residuals"][:, None] * x
    s_mat = u_x.T @ u_x
    for lag_idx in range(1, lags + 1):
        weight = 1.0 - (lag_idx / (lags + 1.0))
        gamma_lag = u_x[lag_idx:].T @ u_x[:-lag_idx]
        s_mat += weight * (gamma_lag + gamma_lag.T)
    expected_var = xtx_inv @ s_mat @ xtx_inv
    expected_se = np.sqrt(np.diag(expected_var))
    assert np.all(np.abs(res["se"] - expected_se) < 1e-6)


def test_predictive_regression_lag_alignment(instance_data: dict[str, Any]) -> None:
    """Verify predictive multi-horizon forecasting structure and non-contemporaneous alignment."""
    # 1. Exact lag alignment verification: y_{t+1} = 2.5 * x_t + noise
    rng_check = np.random.default_rng(999)
    n_check = 100
    x_iid = rng_check.normal(0.0, 1.0, size=n_check)
    y_forward = np.zeros(n_check)
    y_forward[1:] = 2.5 * x_iid[:-1] + rng_check.normal(0.0, 0.05, size=n_check - 1)

    synth_reg = ref.estimate_predictive_regression(y_forward, x_iid, horizon=1, lags=1)
    assert abs(synth_reg["beta"] - 2.5) < 0.15, (
        f"Predictive regression must align sentiment at t with forward returns starting at t+1; "
        f"estimated beta={synth_reg['beta']:.4f} violates lag structure"
    )

    std_proxies = ref.standardize_proxies(instance_data["raw_proxies"])
    ortho_proxies = ref.orthogonalize_proxies(std_proxies, instance_data["macro_controls"])
    sent_res = ref.extract_sentiment_index(ortho_proxies, sign_anchor_idx=2)
    sentiment = sent_res["index"]

    hard_ret = np.mean(instance_data["test_assets_returns"][:, :4], axis=1)

    # 1-month horizon
    reg_h1 = ref.estimate_predictive_regression(hard_ret, sentiment, horizon=1, lags=1)
    assert np.isfinite(reg_h1["beta"])
    assert reg_h1["se_hac"] > 0.0
    assert abs(reg_h1["t_stat"] - reg_h1["beta"] / reg_h1["se_hac"]) < 1e-5

    # 3-month cumulative horizon
    reg_h3 = ref.estimate_predictive_regression(hard_ret, sentiment, horizon=3, lags=3)
    assert np.isfinite(reg_h3["beta"])
    assert reg_h3["se_hac"] > 0.0
    # Overlapping 3-month returns have larger HAC standard error than 1-month
    assert reg_h3["se_hac"] > reg_h1["se_hac"]


def test_cross_sectional_sentiment_asymmetry(instance_data: dict[str, Any]) -> None:
    """Verify Baker & Wurgler (2006) cross-sectional asymmetry: speculative stocks underperform post-high sentiment."""
    std_proxies = ref.standardize_proxies(instance_data["raw_proxies"])
    ortho_proxies = ref.orthogonalize_proxies(std_proxies, instance_data["macro_controls"])
    sent_res = ref.extract_sentiment_index(ortho_proxies, sign_anchor_idx=2)
    sentiment = sent_res["index"]

    asym_res = ref.test_cross_sectional_asymmetry(instance_data["test_assets_returns"], sentiment)

    # 1. Predictive slope on spread must be significantly negative:
    # High sentiment at t forecasts low speculative-minus-safe spread at t+1
    assert asym_res["beta_spread"] < 0.0, (
        f"Predictive slope beta_spread={asym_res['beta_spread']:.4f} must be negative (BW 2006 hypothesis)"
    )
    assert asym_res["t_stat_spread"] < -1.60, (
        f"HAC t-stat {asym_res['t_stat_spread']:.2f} must be statistically negative (< -1.60)"
    )

    # 2. Asymmetry difference: Low sentiment subsequent spread > High sentiment subsequent spread
    assert asym_res["asymmetry_diff"] > 0.0, (
        f"Asymmetry diff {asym_res['asymmetry_diff']:.4f} must be positive (low sentiment spread exceeds high)"
    )
    assert asym_res["mean_spread_low"] > asym_res["mean_spread_high"]

    # 3. Spread return series length
    assert len(asym_res["spread"]) == 179
