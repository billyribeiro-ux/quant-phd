"""Autograder test suite for GM2: Regimes & the Business Cycle.

Runs identically in native pytest and Pyodide:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any, cast

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    backtest_regime_strategy,
    classify_regimes_realtime,
    estimate_regime_moments,
    optimize_regime_allocation,
)

pytestmark = pytest.mark.filterwarnings("error")


def _get_instance() -> dict[str, Any]:
    """Retrieve test instance seeded by environment SEED or fallback to 0."""
    seed_env = os.environ.get("SEED", "0")
    try:
        seed = int(seed_env)
    except ValueError:
        seed = 0
    return cast(dict[str, Any], make_instance(seed))


def test_realtime_classification_causality() -> None:
    """Property 1: Verify causality. Modifying future data must not alter past regime classifications."""
    inst = _get_instance()
    growth = np.copy(inst["growth"])
    inflation = np.copy(inst["inflation"])
    lookback = inst["lookback"]
    burn_in = inst["burn_in"]

    regimes_base, probs_base = classify_regimes_realtime(growth, inflation, lookback, burn_in)

    # Mutate data in the final quarter of history
    cutoff = len(growth) - 30
    growth_mut = np.copy(growth)
    inflation_mut = np.copy(inflation)
    growth_mut[cutoff:] += 0.05
    inflation_mut[cutoff:] -= 0.03

    regimes_mut, probs_mut = classify_regimes_realtime(growth_mut, inflation_mut, lookback, burn_in)

    # Past classifications prior to cutoff must be strictly identical
    np.testing.assert_array_equal(
        regimes_base[:cutoff],
        regimes_mut[:cutoff],
        err_msg="Causality violation: modifying future data changed earlier regime classifications",
    )
    np.testing.assert_allclose(
        probs_base[:cutoff],
        probs_mut[:cutoff],
        atol=1e-12,
        err_msg="Causality violation: modifying future data changed earlier regime probabilities",
    )


def test_regime_probabilities_simplex() -> None:
    """Property 2: Filtered regime probability vectors must lie strictly on the probability simplex."""
    inst = _get_instance()
    growth = inst["growth"]
    inflation = inst["inflation"]
    _, probs = classify_regimes_realtime(growth, inflation, inst["lookback"], inst["burn_in"])

    assert probs.shape == (len(growth), 4), f"Expected shape ({len(growth)}, 4), got {probs.shape}"
    assert np.all(probs >= -1e-12), "Found negative probability values"
    sums = np.sum(probs, axis=1)
    np.testing.assert_allclose(sums, 1.0, atol=1e-10, err_msg="Regime probabilities must sum to 1.0 at every period")


def test_regime_classification_properties() -> None:
    """Property 3: Verify deterministic mapping of quadrant signs to discrete regimes."""
    # Construct synthetic series where values clearly sit in quadrants
    n = 60
    growth = np.zeros(n)
    inflation = np.zeros(n)
    # Set history to establish mean ~ 0, std ~ 1
    for t in range(n):
        growth[t] = 0.01 if t % 2 == 0 else -0.01
        inflation[t] = 0.01 if t % 2 == 0 else -0.01

    # Inject definitive quadrant tests at t=50, 51, 52, 53
    # 50: Goldilocks (g > 0, pi < 0) -> Regime 0
    growth[50] = 0.08
    inflation[50] = -0.08
    # 51: Reflation (g > 0, pi > 0) -> Regime 1
    growth[51] = 0.08
    inflation[51] = 0.08
    # 52: Stagflation (g < 0, pi > 0) -> Regime 2
    growth[52] = -0.08
    inflation[52] = 0.08
    # 53: Deflation (g < 0, pi < 0) -> Regime 3
    growth[53] = -0.08
    inflation[53] = -0.08

    regimes, _ = classify_regimes_realtime(growth, inflation, lookback=24, burn_in=20)
    assert regimes[50] == 0, f"Expected Goldilocks regime 0 at t=50, got {regimes[50]}"
    assert regimes[51] == 1, f"Expected Reflation regime 1 at t=51, got {regimes[51]}"
    assert regimes[52] == 2, f"Expected Stagflation regime 2 at t=52, got {regimes[52]}"
    assert regimes[53] == 3, f"Expected Deflation regime 3 at t=53, got {regimes[53]}"


def test_regime_moments_shapes_and_invariants() -> None:
    """Property 4: Regime moments must have correct dimensions, symmetry, and positive definiteness."""
    inst = _get_instance()
    returns = inst["asset_returns"]
    growth = inst["growth"]
    inflation = inst["inflation"]
    regimes, _ = classify_regimes_realtime(growth, inflation, inst["lookback"], inst["burn_in"])

    expected_returns, cov_matrices, se_returns = estimate_regime_moments(returns, regimes)

    n_assets = returns.shape[1]
    assert expected_returns.shape == (4, n_assets), f"Wrong shape {expected_returns.shape}"
    assert cov_matrices.shape == (4, n_assets, n_assets), f"Wrong cov shape {cov_matrices.shape}"
    assert se_returns.shape == (4, n_assets), f"Wrong se shape {se_returns.shape}"
    assert np.all(se_returns >= 0.0), "Standard errors must be non-negative"

    for k in range(4):
        cov_k = cov_matrices[k]
        # Check symmetry
        np.testing.assert_allclose(
            cov_k, cov_k.T, atol=1e-10, err_msg=f"Covariance matrix for regime {k} is not symmetric"
        )
        # Check positive definiteness (eigenvalues > 0)
        eigvals = np.linalg.eigvalsh(cov_k)
        assert np.all(eigvals > 0.0), f"Covariance matrix for regime {k} is not positive definite: min eig {eigvals[0]}"


def test_regime_moments_values() -> None:
    """Property 5: Verify annualized expected returns and standard errors match empirical definitions."""
    inst = _get_instance()
    returns = inst["asset_returns"]
    growth = inst["growth"]
    inflation = inst["inflation"]
    regimes, _ = classify_regimes_realtime(growth, inflation, inst["lookback"], inst["burn_in"])

    expected_returns, _, _se_returns = estimate_regime_moments(returns, regimes, min_obs=10)

    for k in range(4):
        mask = regimes == k
        if np.sum(mask) >= 10:
            direct_mean = np.mean(returns[mask], axis=0) * 12.0
            np.testing.assert_allclose(
                expected_returns[k],
                direct_mean,
                rtol=1e-5,
                atol=1e-5,
                err_msg=f"Expected returns in regime {k} differ from empirical mean",
            )


def test_portfolio_weights_budget() -> None:
    """Property 6: Portfolio weights must satisfy budget constraints (sum to 1.0, non-negative)."""
    inst = _get_instance()
    returns = inst["asset_returns"]
    growth = inst["growth"]
    inflation = inst["inflation"]
    regimes, probs = classify_regimes_realtime(growth, inflation, inst["lookback"], inst["burn_in"])
    expected_returns, cov_matrices, _ = estimate_regime_moments(returns, regimes)

    weights = optimize_regime_allocation(probs, expected_returns, cov_matrices, risk_aversion=3.0)

    assert weights.shape == returns.shape, f"Weights shape {weights.shape} != returns shape {returns.shape}"
    # Non-negativity
    assert np.all(weights >= -1e-6), "Found negative portfolio weights"
    # Budget constraint
    weight_sums = np.sum(weights, axis=1)
    np.testing.assert_allclose(weight_sums, 1.0, atol=1e-5, err_msg="Portfolio weights must sum to 1.0 at every period")


def test_portfolio_optimization_objective() -> None:
    """Property 7: Under equal diagonal risk, assets must be strictly ordered by expected return."""
    # Create simple diagonal covariance matrix for 4 assets
    cov_matrices = np.zeros((4, 4, 4))
    for k in range(4):
        cov_matrices[k] = 0.04 * np.eye(4)  # 20% annualized vol each, zero correlation

    expected_returns = np.array(
        [
            [0.12, 0.04, 0.02, 0.06],  # Asset 0 (12%) > Asset 3 (6%) > Asset 1 (4%) > Asset 2 (2%)
            [0.10, 0.04, 0.02, 0.06],
            [0.10, 0.04, 0.02, 0.06],
            [0.10, 0.04, 0.02, 0.06],
        ]
    )

    # In pure regime 0 with conservative risk aversion ensuring positive allocations
    p0 = np.array([1.0, 0.0, 0.0, 0.0])
    w = optimize_regime_allocation(p0, expected_returns, cov_matrices, risk_aversion=10.0)

    assert w[0] > w[3], f"Asset 0 weight ({w[0]:.3f}) should exceed Asset 3 ({w[3]:.3f})"
    assert w[3] > w[1], f"Asset 3 weight ({w[3]:.3f}) should exceed Asset 1 ({w[1]:.3f})"
    assert w[1] > w[2], f"Asset 1 weight ({w[1]:.3f}) should exceed Asset 2 ({w[2]:.3f})"
    assert np.all(w > 0.0), "All weights should be strictly positive"


def test_backtest_accounting_articulation() -> None:
    """Property 8: Articulation test: equity curve must equal cumulative product of (1 + net_return)."""
    inst = _get_instance()
    returns = inst["asset_returns"]
    growth = inst["growth"]
    inflation = inst["inflation"]
    regimes, probs = classify_regimes_realtime(growth, inflation, inst["lookback"], inst["burn_in"])
    expected_returns, cov_matrices, _ = estimate_regime_moments(returns, regimes)
    weights = optimize_regime_allocation(probs, expected_returns, cov_matrices)

    res = backtest_regime_strategy(returns, weights, transaction_cost_bps=10.0, burn_in=inst["burn_in"])

    net_returns = res["net_returns"]
    equity_curve = res["equity_curve"]

    calculated_curve = np.cumprod(1.0 + net_returns)
    np.testing.assert_allclose(
        equity_curve,
        calculated_curve,
        rtol=1e-10,
        atol=1e-10,
        err_msg="Equity curve articulation failed: does not equal cumulative product of net returns",
    )


def test_backtest_performance_metrics() -> None:
    """Property 9: Increasing transaction costs must strictly decrease cumulative return and Sharpe ratio."""
    inst = _get_instance()
    returns = inst["asset_returns"]
    growth = inst["growth"]
    inflation = inst["inflation"]
    regimes, probs = classify_regimes_realtime(growth, inflation, inst["lookback"], inst["burn_in"])
    expected_returns, cov_matrices, _ = estimate_regime_moments(returns, regimes)
    weights = optimize_regime_allocation(probs, expected_returns, cov_matrices)

    res_low_tc = backtest_regime_strategy(returns, weights, transaction_cost_bps=5.0, burn_in=inst["burn_in"])
    res_high_tc = backtest_regime_strategy(returns, weights, transaction_cost_bps=50.0, burn_in=inst["burn_in"])

    assert res_low_tc["annualized_return"] > res_high_tc["annualized_return"], (
        "Higher transaction costs must reduce annualized net return"
    )
    assert res_low_tc["sharpe_ratio"] > res_high_tc["sharpe_ratio"], (
        "Higher transaction costs must reduce net Sharpe ratio"
    )
    assert res_low_tc["equity_curve"][-1] > res_high_tc["equity_curve"][-1], (
        "Terminal equity must be strictly lower under higher transaction frictions"
    )


def test_end_to_end_regime_strategy() -> None:
    """Property 10: End-to-end strategy verification across instance parameters."""
    inst = _get_instance()
    returns = inst["asset_returns"]
    growth = inst["growth"]
    inflation = inst["inflation"]
    regimes, probs = classify_regimes_realtime(growth, inflation, inst["lookback"], inst["burn_in"])
    expected_returns, cov_matrices, _ = estimate_regime_moments(returns, regimes)
    weights = optimize_regime_allocation(probs, expected_returns, cov_matrices)
    res = backtest_regime_strategy(returns, weights, transaction_cost_bps=inst["transaction_cost_bps"])

    assert 0.0 <= res["max_drawdown"] <= 1.0, f"Max drawdown out of bounds: {res['max_drawdown']}"
    assert res["annualized_volatility"] > 0.0, "Annualized volatility must be strictly positive"
    assert res["annualized_turnover"] >= 0.0, "Turnover must be non-negative"
    assert np.isfinite(res["sharpe_ratio"]), "Sharpe ratio must be finite"
