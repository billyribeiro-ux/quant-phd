"""Acceptance suite for PR2 project: Atlas A11 portfolio construction (atlas/portfolio.py).

Runs identically in Pyodide and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
from atlas import portfolio as sol  # type: ignore[attr-defined]
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_shrinkage_covariance_properties() -> None:
    returns = np.asarray(INST["returns"], dtype=np.float64)
    shrunk = sol.shrinkage_covariance(returns, target="scaled_identity")

    assert isinstance(shrunk, np.ndarray), "Shrinkage covariance must return an ndarray"
    assert shrunk.shape == (INST["n_assets"], INST["n_assets"]), "Shrunk covariance shape mismatch"
    assert np.allclose(shrunk, shrunk.T, atol=1e-8), "Shrunk covariance must be symmetric"

    evals = np.linalg.eigvalsh(shrunk)
    assert np.all(evals > 1e-8), f"Shrunk covariance must be strictly positive definite, min eval={evals[0]}"
    assert np.all(np.diag(shrunk) > 0), "Diagonal variances must be strictly positive"

    # Shrunk covariance must differ from un-shrunk sample covariance
    sample_cov = np.cov(returns, rowvar=False, ddof=1)
    diff = float(np.max(np.abs(shrunk - sample_cov)))
    assert diff > 1e-5, f"Shrunk covariance must differ from raw sample covariance, got diff={diff:g}"

    # Test constant correlation target
    shrunk_cc = sol.shrinkage_covariance(returns, target="constant_correlation")
    assert shrunk_cc.shape == (INST["n_assets"], INST["n_assets"])
    assert np.allclose(shrunk_cc, shrunk_cc.T, atol=1e-8)


def test_euler_risk_decomposition() -> None:
    returns = np.asarray(INST["returns"], dtype=np.float64)
    cov = sol.shrinkage_covariance(returns)
    n = INST["n_assets"]
    weights = np.full(n, 1.0 / n, dtype=np.float64)

    mrc = sol.marginal_risk_contributions(weights, cov)
    trc = sol.component_risk_contributions(weights, cov)
    prc = sol.percent_risk_contributions(weights, cov)

    assert mrc.shape == (n,), "MRC must be 1D vector of length N"
    assert trc.shape == (n,), "TRC must be 1D vector of length N"
    assert prc.shape == (n,), "PRC must be 1D vector of length N"

    port_vol = float(np.sqrt(weights @ cov @ weights))

    # Invariant: TRC = w * MRC
    assert np.allclose(trc, weights * mrc, atol=1e-8), "TRC must equal w_i * MRC_i"

    # Euler theorem: sum(TRC) = sigma_p
    assert np.isclose(float(np.sum(trc)), port_vol, atol=1e-7), "Component risk contributions must sum to portfolio vol"

    # Invariant: sum(PRC) = 1.0
    assert np.isclose(float(np.sum(prc)), 1.0, atol=1e-7), "Percent risk contributions must sum to 1.0"
    assert np.allclose(prc, trc / port_vol, atol=1e-7), "PRC must equal TRC / sigma_p"


def test_risk_parity_weights() -> None:
    returns = np.asarray(INST["returns"], dtype=np.float64)
    cov = sol.shrinkage_covariance(returns)
    n = INST["n_assets"]

    # 1. Equal Risk Contribution (default budgets)
    w_erc = sol.risk_parity_weights(cov)
    assert len(w_erc) == n, "ERC weights length mismatch"
    assert np.all(w_erc > 0), "ERC weights must be strictly positive"
    assert np.isclose(float(np.sum(w_erc)), 1.0, atol=1e-6), "ERC weights must sum to 1.0"

    prc_erc = sol.percent_risk_contributions(w_erc, cov)
    expected_erc_prc = np.full(n, 1.0 / n)
    assert np.allclose(prc_erc, expected_erc_prc, atol=1e-3), (
        f"ERC risk contributions must all equal 1/N, got {prc_erc}"
    )

    # 2. General Risk Budgeting with instance budgets
    budgets = np.asarray(INST["budgets"], dtype=np.float64)
    w_rb = sol.risk_parity_weights(cov, budgets=budgets)
    assert np.isclose(float(np.sum(w_rb)), 1.0, atol=1e-6), "Risk budgeting weights must sum to 1.0"
    assert np.all(w_rb > 0), "Risk budgeting weights must be strictly positive"

    prc_rb = sol.percent_risk_contributions(w_rb, cov)
    assert np.allclose(prc_rb, budgets, atol=1e-3), (
        f"Risk budgeting PRC must match target budgets within tolerance, got {prc_rb} vs {budgets}"
    )


def test_mean_variance_weights() -> None:
    returns = np.asarray(INST["returns"], dtype=np.float64)
    cov = sol.shrinkage_covariance(returns)
    mean = np.asarray(INST["mean"], dtype=np.float64)
    gamma = float(INST["risk_aversion"])
    n = INST["n_assets"]

    # Unconstrained MV (sum(w) = 1)
    w_unc = sol.mean_variance_weights(mean, cov, risk_aversion=gamma, long_only=False)
    assert len(w_unc) == n
    assert np.isclose(float(np.sum(w_unc)), 1.0, atol=1e-6), "Unconstrained MV weights must sum to 1.0"

    # First-order condition: gamma * cov @ w - mu = lambda * 1
    grad = gamma * (cov @ w_unc) - mean
    assert np.allclose(grad, grad[0], atol=1e-5), "Gradient must be uniform across assets at unconstrained optimum"

    # Long-only MV
    w_lo = sol.mean_variance_weights(mean, cov, risk_aversion=gamma, long_only=True)
    assert len(w_lo) == n
    assert np.isclose(float(np.sum(w_lo)), 1.0, atol=1e-6), "Long-only MV weights must sum to 1.0"
    assert np.all(w_lo >= -1e-7), f"Long-only weights must be non-negative, got min={np.min(w_lo)}"


def test_volatility_targeting() -> None:
    returns = np.asarray(INST["returns"], dtype=np.float64)
    cov = sol.shrinkage_covariance(returns)
    w_base = sol.risk_parity_weights(cov)
    target_vol = float(INST["target_vol"])

    # Uncapped targeting
    w_vt = sol.volatility_target_weights(w_base, cov, target_vol=target_vol, max_leverage=None)
    realized_vol = float(np.sqrt(w_vt @ cov @ w_vt))
    assert np.isclose(realized_vol, target_vol, atol=1e-6), (
        f"Realized vol {realized_vol:g} must match target vol {target_vol:g}"
    )

    # Relative proportions preserved
    scale = realized_vol / float(np.sqrt(w_base @ cov @ w_base))
    assert np.allclose(w_vt, scale * w_base, atol=1e-6), "Vol targeting must scale weights proportionally"

    # Capped targeting
    high_target = target_vol * 10.0
    cap = float(INST["max_leverage"])
    w_capped = sol.volatility_target_weights(w_base, cov, target_vol=high_target, max_leverage=cap)
    gross_lev = float(np.sum(np.abs(w_capped)))
    assert gross_lev <= cap + 1e-6, f"Gross leverage {gross_lev:g} exceeded cap {cap:g}"
    assert np.isclose(gross_lev, cap, atol=1e-6), f"Binding leverage cap must be achieved, got {gross_lev:g} vs {cap:g}"


def test_benchmark_pipeline() -> None:
    res = sol.run_benchmark(INST)
    required_keys = {
        "shrunk_cov_diag",
        "risk_parity_weights",
        "risk_parity_prc",
        "mean_variance_long_only",
        "vol_target_weights",
        "vol_target_gross_leverage",
    }
    assert required_keys.issubset(res.keys()), f"Missing keys in benchmark result: {required_keys - set(res.keys())}"
    assert len(res["risk_parity_weights"]) == INST["n_assets"]
    assert res["vol_target_gross_leverage"] > 0


def test_input_validation_errors() -> None:
    cov_valid = np.eye(3)
    w_valid = np.array([1 / 3, 1 / 3, 1 / 3])

    # Non-finite returns
    bad_returns = np.array([[0.01, 0.02], [np.nan, 0.03], [0.02, 0.01]])
    with pytest.raises(ValueError):
        sol.shrinkage_covariance(bad_returns)

    # Unsupported shrinkage target
    with pytest.raises(ValueError):
        sol.shrinkage_covariance(np.ones((10, 3)), target="unsupported")

    # Mismatched dimensions
    with pytest.raises(ValueError):
        sol.marginal_risk_contributions(np.array([0.5, 0.5]), cov_valid)

    # Negative budgets
    with pytest.raises(ValueError):
        sol.risk_parity_weights(cov_valid, budgets=np.array([-0.2, 0.6, 0.6]))

    # Budgets not summing to 1.0
    with pytest.raises(ValueError):
        sol.risk_parity_weights(cov_valid, budgets=np.array([0.5, 0.5, 0.5]))

    # Negative target volatility
    with pytest.raises(ValueError):
        sol.volatility_target_weights(w_valid, cov_valid, target_vol=-0.05)

    # Negative risk aversion
    with pytest.raises(ValueError):
        sol.mean_variance_weights(np.array([0.05, 0.05, 0.05]), cov_valid, risk_aversion=-2.0)
