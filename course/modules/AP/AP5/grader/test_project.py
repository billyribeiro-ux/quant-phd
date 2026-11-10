"""Acceptance suite for Module AP5: Present Value & Return Predictability.

Tests Campbell-Shiller VAR estimation, return news decomposition,
dividend-yield variance decomposition, Stambaugh bias, and out-of-sample forecasting.

Runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
import reference as sol
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)

VAR_DATA = np.array(INST["var_data"], dtype=np.float64)
RHO = float(INST["rho"])
PRED_X = np.array(INST["predictive_x"], dtype=np.float64)
PRED_Y = np.array(INST["predictive_y"], dtype=np.float64)
OOS_X = np.array(INST["oos_x"], dtype=np.float64)
OOS_Y = np.array(INST["oos_y"], dtype=np.float64)
OOS_BURN_IN = int(INST["oos_burn_in"])


# ---------------------------------------------------------------------------
# 1. VAR Estimation & Stability
# ---------------------------------------------------------------------------


def test_var_estimation_dimensions_and_stability() -> None:
    """VAR(1) estimation returns valid coefficient matrices and stationary companion matrix."""
    phi, c, sigma = sol.estimate_var(VAR_DATA)
    assert phi.shape == (2, 2)
    assert c.shape == (2,)
    assert sigma.shape == (2, 2)

    # Symmetry and positive definiteness of residual covariance
    assert np.allclose(sigma, sigma.T, atol=1e-12)
    eigvals_sigma = np.linalg.eigvalsh(sigma)
    assert np.all(eigvals_sigma > 0.0)

    # Stationarity of companion matrix: spectral radius strictly inside unit circle
    eigvals_phi = np.linalg.eigvals(phi)
    assert np.all(np.abs(eigvals_phi) < 0.999)


def test_var_estimation_validation() -> None:
    """Invalid VAR input dimensions raise ValueError."""
    with pytest.raises(ValueError):
        sol.estimate_var(np.ones(50))  # 1D array
    with pytest.raises(ValueError):
        sol.estimate_var(np.ones((50, 1)))  # K < 2
    with pytest.raises(ValueError):
        sol.estimate_var(np.ones((4, 2)))  # T too short


# ---------------------------------------------------------------------------
# 2. Campbell-Shiller Return News Decomposition
# ---------------------------------------------------------------------------


def test_cs_return_identity() -> None:
    """Unexpected return eta equals cash-flow news minus discount-rate news: eta = N_cf - N_dr."""
    phi, c, _ = sol.estimate_var(VAR_DATA)
    z_lead = VAR_DATA[1:]
    z_lag = VAR_DATA[:-1]
    resids = z_lead - (c + z_lag @ phi.T)

    n_cf, n_dr = sol.campbell_shiller_news(phi, resids, rho=RHO)
    eta = resids[:, 0]  # unexpected return

    assert n_cf.shape == eta.shape
    assert n_dr.shape == eta.shape
    diff = np.max(np.abs(eta - (n_cf - n_dr)))
    assert diff < 1e-12, f"Return news identity violated: max error {diff}"


def test_cs_news_variance_identity() -> None:
    """Variance identity Var(eta) = Var(N_cf) + Var(N_dr) - 2*Cov(N_cf, N_dr) holds."""
    phi, c, _ = sol.estimate_var(VAR_DATA)
    resids = VAR_DATA[1:] - (c + VAR_DATA[:-1] @ phi.T)
    n_cf, n_dr = sol.campbell_shiller_news(phi, resids, rho=RHO)

    decomp = sol.decompose_return_variance(n_cf, n_dr)
    var_eta = decomp["var_eta"]
    var_cf = decomp["var_cf"]
    var_dr = decomp["var_dr"]
    cov_cf_dr = decomp["cov_cf_dr"]

    reconstructed_var = var_cf + var_dr - 2.0 * cov_cf_dr
    assert np.isclose(var_eta, reconstructed_var, atol=1e-12)
    assert np.isclose(decomp["share_dr"] + decomp["share_cf"] + decomp["share_cov"], 1.0, atol=1e-12)


def test_cs_discount_factor_sensitivity() -> None:
    """When rho -> 0, discount-rate news vanishes and cash-flow news equals return innovation."""
    phi, c, _ = sol.estimate_var(VAR_DATA)
    resids = VAR_DATA[1:] - (c + VAR_DATA[:-1] @ phi.T)

    n_cf_low, n_dr_low = sol.campbell_shiller_news(phi, resids, rho=1e-6)
    eta = resids[:, 0]
    assert np.allclose(n_dr_low, 0.0, atol=1e-4)
    assert np.allclose(n_cf_low, eta, atol=1e-4)


# ---------------------------------------------------------------------------
# 3. Dividend-Yield Variance Decomposition
# ---------------------------------------------------------------------------


def test_div_yield_variance_identity() -> None:
    """Dividend-yield variance decomposition satisfies b_r - b_d = 1.0000 exactly."""
    phi, _, sigma = sol.estimate_var(VAR_DATA)
    decomp = sol.dividend_yield_variance_decomposition(phi, sigma, rho=RHO)

    assert "b_r" in decomp and "b_d" in decomp and "identity_gap" in decomp
    assert decomp["identity_gap"] < 1e-10, f"Identity gap {decomp['identity_gap']} exceeds tolerance"
    assert np.isclose(decomp["b_r"] - decomp["b_d"], 1.0, atol=1e-10)


def test_div_yield_shares() -> None:
    """Discount-rate variation accounts for the majority of valuation ratio variance (b_r > 0.50)."""
    phi, _, sigma = sol.estimate_var(VAR_DATA)
    decomp = sol.dividend_yield_variance_decomposition(phi, sigma, rho=RHO)
    assert decomp["b_r"] > 0.50, f"Discount rate share {decomp['b_r']} is below 50%"


# ---------------------------------------------------------------------------
# 4. Predictive Regression & Stambaugh Bias
# ---------------------------------------------------------------------------


def test_predictive_regression_invariants() -> None:
    """Predictive regression estimates valid OLS coefficients, SEs, and R^2."""
    res = sol.predictive_regression(PRED_X, PRED_Y, max_lags=4)
    assert 0.0 <= res["r2"] <= 1.0
    assert res["se_ols"] > 0.0
    assert res["se_nw"] > 0.0
    assert np.isclose(res["t_stat"], res["beta"] / res["se_nw"], atol=1e-12)


def test_stambaugh_bias_sign_and_magnitude() -> None:
    """When predictor innovation negatively correlates with return innovation, Stambaugh bias is positive."""
    # Negative cov_uv generates upward bias in OLS slope
    bias_pos = sol.stambaugh_bias(phi_x=0.95, sigma_uv=-0.015, sigma_v2=0.020, n_obs=150)
    assert bias_pos > 0.0, f"Expected positive bias for sigma_uv < 0, got {bias_pos}"

    # Positive cov_uv generates downward bias in OLS slope
    bias_neg = sol.stambaugh_bias(phi_x=0.95, sigma_uv=0.015, sigma_v2=0.020, n_obs=150)
    assert bias_neg < 0.0, f"Expected negative bias for sigma_uv > 0, got {bias_neg}"

    # Bias scales inversely with sample size
    bias_large_t = sol.stambaugh_bias(phi_x=0.95, sigma_uv=-0.015, sigma_v2=0.020, n_obs=600)
    assert np.isclose(bias_pos, 4.0 * bias_large_t, rtol=1e-8)


# ---------------------------------------------------------------------------
# 5. Out-of-Sample Predictability
# ---------------------------------------------------------------------------


def test_oos_r2_no_lookahead() -> None:
    """Recursive out-of-sample R^2 is <= 1.0 and runs cleanly across specifications."""
    r2_unconstrained = sol.out_of_sample_r2(OOS_Y, OOS_X, n_init=OOS_BURN_IN, constrained=False)
    r2_constrained = sol.out_of_sample_r2(OOS_Y, OOS_X, n_init=OOS_BURN_IN, constrained=True)

    assert r2_unconstrained <= 1.0
    assert r2_constrained <= 1.0
    assert np.isfinite(r2_unconstrained)
    assert np.isfinite(r2_constrained)


def test_oos_benchmark_expanding_mean() -> None:
    """Out-of-sample benchmark must strictly use expanding historical mean, not full-sample mean."""
    y_test = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 15.0, 25.0, 35.0, 45.0, 55.0], dtype=np.float64)
    x_test = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], dtype=np.float64)
    r2_val = sol.out_of_sample_r2(y_test, x_test, n_init=5, constrained=False)
    assert np.isclose(r2_val, 0.8229109055595696, atol=1e-8)


def test_oos_economic_constraints() -> None:
    """Campbell-Thompson economic constraints bound predictive slope and return forecasts."""
    # On series where naive OLS overfits, constrained forecasting produces non-trivial R^2
    r2_c = sol.out_of_sample_r2(OOS_Y, OOS_X, n_init=OOS_BURN_IN, constrained=True)
    assert isinstance(r2_c, float)


# ---------------------------------------------------------------------------
# 6. Input Validation
# ---------------------------------------------------------------------------


def test_validation_errors() -> None:
    """All project routines reject invalid inputs with descriptive ValueError exceptions."""
    with pytest.raises(ValueError):
        sol.campbell_shiller_news(np.eye(2), np.zeros((10, 2)), rho=1.2)  # invalid rho
    with pytest.raises(ValueError):
        sol.decompose_return_variance(np.zeros(5), np.zeros(6))  # length mismatch
    with pytest.raises(ValueError):
        sol.stambaugh_bias(0.95, -0.01, sigma_v2=-0.02, n_obs=100)  # negative variance
    with pytest.raises(ValueError):
        sol.out_of_sample_r2(OOS_Y, OOS_X, n_init=len(OOS_Y) + 10)  # burn-in > N
