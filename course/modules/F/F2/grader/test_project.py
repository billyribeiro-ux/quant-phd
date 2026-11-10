"""Acceptance suite for Module F2 Project: Factor-Model Horse Race.

Runs identically in Pyodide and locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest

try:
    import horse_race as proj
except ImportError:
    import reference as proj

from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)

MODELS: dict[str, np.ndarray] = {
    "CAPM": np.asarray(INST["factors_capm"], dtype=np.float64),
    "FF3": np.asarray(INST["factors_ff3"], dtype=np.float64),
    "Carhart": np.asarray(INST["factors_carhart"], dtype=np.float64),
    "FF5": np.asarray(INST["factors_ff5"], dtype=np.float64),
    "q_factor": np.asarray(INST["factors_q_factor"], dtype=np.float64),
}


def test_fit_factor_model_shapes_and_residuals() -> None:
    """Checks that fit_factor_model returns correct array shapes, OLS orthogonality, and unbiased sigma_eps."""
    test_returns = np.asarray(INST["test_returns"], dtype=np.float64)
    ff3_factors = MODELS["FF3"]

    t_obs, n_assets = test_returns.shape
    k_factors = ff3_factors.shape[1]

    fit = proj.fit_factor_model(test_returns, ff3_factors)

    alphas = np.asarray(fit["alphas"], dtype=np.float64)
    betas = np.asarray(fit["betas"], dtype=np.float64)
    residuals = np.asarray(fit["residuals"], dtype=np.float64)
    sigma_eps = np.asarray(fit["sigma_eps"], dtype=np.float64)
    r2 = np.asarray(fit["r2"], dtype=np.float64)

    assert alphas.shape == (n_assets,), f"alphas shape must be ({n_assets},), got {alphas.shape}"
    assert betas.shape == (n_assets, k_factors), f"betas shape must be ({n_assets}, {k_factors}), got {betas.shape}"
    assert residuals.shape == (t_obs, n_assets), f"residuals shape must be ({t_obs}, {n_assets}), got {residuals.shape}"
    assert sigma_eps.shape == (n_assets, n_assets), (
        f"sigma_eps shape must be ({n_assets}, {n_assets}), got {sigma_eps.shape}"
    )
    assert r2.shape == (n_assets,), f"r2 shape must be ({n_assets},), got {r2.shape}"

    # Residuals must be orthogonal to factors (sum(e * f_k) ~ 0) and have zero mean
    res_mean = np.mean(residuals, axis=0)
    assert np.all(np.abs(res_mean) < 1e-10), "OLS residuals must have zero mean per asset"

    ortho = residuals.T @ ff3_factors
    assert np.all(np.abs(ortho) < 1e-8), "OLS residuals must be orthogonal to explanatory factors"

    # Sigma_eps must be positive semi-definite and symmetric
    assert np.allclose(sigma_eps, sigma_eps.T, atol=1e-12), "Residual covariance matrix must be symmetric"
    eigvals = np.linalg.eigvalsh(sigma_eps)
    assert np.all(eigvals > 0), "Residual covariance matrix must be strictly positive definite"

    # Degrees of freedom divisor check: sum(e_i^2) / (T - K - 1)
    expected_s2_0 = np.sum(residuals[:, 0] ** 2) / float(t_obs - k_factors - 1)
    assert abs(sigma_eps[0, 0] - expected_s2_0) < 1e-10, (
        f"sigma_eps must divide by unbiased degrees of freedom (T - K - 1), got {sigma_eps[0, 0]} vs {expected_s2_0}"
    )


def test_grs_statistic_invariants_and_values() -> None:
    """Checks the GRS statistic formula, degrees of freedom, and exact numerical value."""
    test_returns = np.asarray(INST["test_returns"], dtype=np.float64)
    capm_factors = MODELS["CAPM"]

    t_obs, n_assets = test_returns.shape
    k_factors = capm_factors.shape[1]

    fit = proj.fit_factor_model(test_returns, capm_factors)
    grs = proj.compute_grs_statistic(fit["alphas"], capm_factors, fit["residuals"])

    stat = float(grs["stat"])
    p_value = float(grs["p_value"])
    df_num = int(grs["df_num"])
    df_denom = int(grs["df_denom"])

    assert stat >= 0.0, f"GRS F-statistic must be non-negative, got {stat}"
    assert 0.0 <= p_value <= 1.0, f"GRS p-value must be in [0, 1], got {p_value}"
    assert df_num == n_assets, f"Numerator degrees of freedom must be {n_assets}, got {df_num}"
    assert df_denom == (t_obs - n_assets - k_factors), (
        f"Denominator degrees of freedom must be {t_obs - n_assets - k_factors}, got {df_denom}"
    )

    # Invariant: If alphas are identically zero, GRS statistic must be exactly 0.0 and p-value 1.0
    zero_alphas = np.zeros(n_assets, dtype=np.float64)
    grs_zero = proj.compute_grs_statistic(zero_alphas, capm_factors, fit["residuals"])
    assert abs(float(grs_zero["stat"])) < 1e-14, "GRS statistic must be zero when pricing errors are zero"
    assert abs(float(grs_zero["p_value"]) - 1.0) < 1e-12, "GRS p-value must be 1.0 when pricing errors are zero"

    # Exact oracle comparison for GRS formula
    f_bar = np.mean(capm_factors, axis=0)
    sigma_f = np.cov(capm_factors, rowvar=False, ddof=1)
    sh2_f = float((f_bar[0] ** 2) / float(sigma_f))
    sigma_eps = (fit["residuals"].T @ fit["residuals"]) / float(t_obs - k_factors - 1)
    alpha_quad = float(fit["alphas"] @ np.linalg.inv(sigma_eps) @ fit["alphas"])
    expected_stat = ((t_obs - n_assets - k_factors) / n_assets) * (1.0 / (1.0 + sh2_f)) * alpha_quad
    assert abs(stat - expected_stat) < 1e-8, (
        f"GRS statistic {stat:.6f} differs from expected {expected_stat:.6f}; check factor quadratic form scaling"
    )


def test_max_sharpe_ratio_properties() -> None:
    """Checks Barillas-Shanken maximum squared Sharpe ratio metric properties."""
    capm_factors = MODELS["CAPM"]
    ff3_factors = MODELS["FF3"]
    ff5_factors = MODELS["FF5"]

    sh2_capm_ann = proj.compute_max_sharpe(capm_factors, annualize=True)
    sh2_capm_mth = proj.compute_max_sharpe(capm_factors, annualize=False)

    assert sh2_capm_ann >= 0.0, f"Squared Sharpe ratio must be non-negative, got {sh2_capm_ann}"
    assert abs(sh2_capm_ann - 12.0 * sh2_capm_mth) < 1e-10, (
        f"Annualized Sh^2(f) ({sh2_capm_ann:.6f}) must equal exactly 12 * monthly Sh^2(f) ({sh2_capm_mth:.6f})"
    )

    # Monotonicity under nested factors: Adding factors cannot decrease the maximum Sharpe ratio
    sh2_ff3_ann = proj.compute_max_sharpe(ff3_factors, annualize=True)
    sh2_ff5_ann = proj.compute_max_sharpe(ff5_factors, annualize=True)

    assert sh2_ff3_ann >= sh2_capm_ann - 1e-12, (
        f"FF3 max Sharpe ({sh2_ff3_ann:.4f}) must be >= CAPM max Sharpe ({sh2_capm_ann:.4f})"
    )
    assert sh2_ff5_ann >= sh2_ff3_ann - 1e-12, (
        f"FF5 max Sharpe ({sh2_ff5_ann:.4f}) must be >= FF3 max Sharpe ({sh2_ff3_ann:.4f})"
    )


def test_evaluate_model_horse_race_complete() -> None:
    """Checks full model horse race comparison table across all 5 candidate models."""
    test_returns = np.asarray(INST["test_returns"], dtype=np.float64)

    race = proj.evaluate_model_horse_race(test_returns, MODELS)

    expected_models = {"CAPM", "FF3", "Carhart", "FF5", "q_factor"}
    assert set(race.keys()) == expected_models, (
        f"Horse race must evaluate models {expected_models}, got {set(race.keys())}"
    )

    for model_name, metrics in race.items():
        assert "grs_stat" in metrics, f"Model {model_name} missing grs_stat"
        assert "p_value" in metrics, f"Model {model_name} missing p_value"
        assert "max_sharpe_sq" in metrics, f"Model {model_name} missing max_sharpe_sq"
        assert "mean_abs_alpha_ann" in metrics, f"Model {model_name} missing mean_abs_alpha_ann"
        assert "mean_r2" in metrics, f"Model {model_name} missing mean_r2"

        assert metrics["grs_stat"] >= 0.0, f"{model_name} GRS stat must be non-negative"
        assert 0.0 <= metrics["p_value"] <= 1.0, f"{model_name} p-value must be in [0, 1]"
        assert metrics["max_sharpe_sq"] >= 0.0, f"{model_name} max_sharpe_sq must be non-negative"
        assert metrics["mean_abs_alpha_ann"] >= 0.0, f"{model_name} mean_abs_alpha_ann must be non-negative"
        assert 0.0 <= metrics["mean_r2"] <= 1.0, f"{model_name} mean_r2 must be in [0, 1]"

        # Verify mean absolute alpha calculation
        fit = proj.fit_factor_model(test_returns, MODELS[model_name])
        expected_abs_alpha = float(np.mean(np.abs(fit["alphas"])) * 12.0 * 100.0)
        assert abs(metrics["mean_abs_alpha_ann"] - expected_abs_alpha) < 1e-8, (
            f"{model_name}: mean_abs_alpha_ann must be mean absolute pricing error, not signed mean"
        )


def test_out_of_sample_rmspe() -> None:
    """Checks out-of-sample root mean squared pricing error estimation and lookahead discipline."""
    test_returns = np.asarray(INST["test_returns"], dtype=np.float64)
    train_len = int(INST["train_len"])

    oos_res = proj.compute_out_of_sample_rmspe(test_returns, MODELS, train_len=train_len)

    expected_models = {"CAPM", "FF3", "Carhart", "FF5", "q_factor"}
    assert set(oos_res.keys()) == expected_models

    # Recompute oracle for CAPM
    r_train = test_returns[:train_len, :]
    r_test = test_returns[train_len:, :]
    r_bar_oos = np.mean(r_test, axis=0)

    for model_name, rmspe_val in oos_res.items():
        assert isinstance(rmspe_val, float), f"{model_name} RMSPE must be a float"
        assert rmspe_val > 0.0, f"{model_name} RMSPE must be positive, got {rmspe_val}"

        f_mat = MODELS[model_name]
        f_train = f_mat[:train_len, :]
        f_test = f_mat[train_len:, :]
        fit_is = proj.fit_factor_model(r_train, f_train)
        pred_mu = fit_is["betas"] @ np.mean(f_test, axis=0)
        expected_rmspe = float(np.sqrt(np.mean((r_bar_oos - pred_mu) ** 2)) * np.sqrt(12.0) * 100.0)
        assert abs(rmspe_val - expected_rmspe) < 1e-8, (
            f"{model_name}: RMSPE must use in-sample betas without full-sample lookahead"
        )
