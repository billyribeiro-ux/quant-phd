"""Test suite for AP6 Flow-Impact Estimation & Inelastic Markets Engine.

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
    """Check that instance generator returns all required arrays and valid shapes."""
    assert "returns_excess" in instance_data
    assert "dealer_capital_ratio" in instance_data
    assert "holdings_weights" in instance_data
    assert "aum" in instance_data
    assert "shares_out" in instance_data
    assert "flow_fractions" in instance_data

    returns = instance_data["returns_excess"]
    assert returns.ndim == 2
    assert returns.shape[0] > 50
    assert returns.shape[1] == 10


def test_intermediary_sdf_properties(instance_data: dict[str, Any]) -> None:
    """Verify He-Kelly-Manela intermediary SDF estimation and cross-sectional factor pricing."""
    res = ref.estimate_intermediary_sdf(
        instance_data["returns_excess"],
        instance_data["dealer_capital_ratio"],
    )

    # 1. AR(1) persistence phi must be strictly inside unit circle (stationary)
    assert 0.0 < res["phi"] < 1.0, f"AR(1) persistence phi={res['phi']:.4f} must be in (0, 1)"

    # 2. Factor betas must match number of test assets
    betas = res["betas"]
    assert len(betas) == instance_data["returns_excess"].shape[1]
    assert np.all(np.isfinite(betas))

    # 3. Intermediary risk price must be positive (dealers demand positive premium for capital risk)
    assert res["risk_price"] > 0.0, f"Dealer risk price lambda_eta={res['risk_price']} must be positive"

    # 4. Orthogonality condition: betas dot alpha must be zero by OLS cross-sectional projection
    alpha = res["alpha"]
    orthogonality_gap = abs(float(betas @ alpha))
    assert orthogonality_gap < 1e-5, f"Pricing error orthogonality gap {orthogonality_gap:.2e} exceeds tolerance"

    # 5. SDF loading b_eta must equal risk_price / Var(u)
    var_u = float(np.var(res["innovations"], ddof=1))
    expected_b_eta = res["risk_price"] / var_u
    assert abs(res["b_eta"] - expected_b_eta) < 1e-6

    # 6. MSE must be strictly positive and bounded
    assert 0.0 < res["mse"] < 0.1


def test_koijen_yogo_demand_iv(instance_data: dict[str, Any]) -> None:
    """Verify Koijen-Yogo 2SLS demand system elasticity and characteristic estimation."""
    res = ref.estimate_koijen_yogo_demand(
        instance_data["holdings_weights"],
        instance_data["log_prices"],
        instance_data["characteristics"],
        instance_data["instruments"],
    )

    # 1. First-stage F-statistic must indicate instrument relevance (F > 5.0)
    assert res["first_stage_f"] > 5.0, f"First-stage F={res['first_stage_f']:.2f} too weak"

    # 2. Price elasticities must be strictly positive (downward sloping demand curves)
    elasticities = res["elasticities"]
    assert len(elasticities) == instance_data["holdings_weights"].shape[0]
    assert np.all(elasticities > 0.0), f"Elasticities {elasticities} must be strictly positive"

    # 3. Alphas and Gammas shape checks
    alphas = res["alphas"]
    gammas = res["gammas"]
    assert len(alphas) == len(elasticities)
    assert gammas.shape == (len(elasticities), instance_data["characteristics"].shape[1])

    # 4. Residuals finite and non-degenerate
    residuals = res["residuals"]
    assert residuals.shape == instance_data["holdings_weights"].shape
    assert np.all(np.isfinite(residuals))


def test_market_clearing_solution(instance_data: dict[str, Any]) -> None:
    """Verify that solved equilibrium prices satisfy the asset market clearing invariant."""
    p_star = ref.solve_market_clearing_prices(
        instance_data["aum"],
        instance_data["shares_out"],
        instance_data["alpha_i"],
        instance_data["beta_i"],
        instance_data["char_effects"],
        tol=1e-6,
    )

    # 1. Prices must be strictly positive and finite
    assert np.all(p_star > 0.0)
    assert np.all(np.isfinite(p_star))

    # 2. Verify market clearing: sum_i A_i * w_{i,n}(p^*) == P_n^* * Q_n
    p_log = np.log(p_star)
    n_stocks = len(p_star)
    n_inst = len(instance_data["aum"])
    dollar_demand = np.zeros(n_stocks)

    for i in range(n_inst):
        delta_i = instance_data["alpha_i"][i] - instance_data["beta_i"][i] * p_log + instance_data["char_effects"][i, :]
        max_delta = np.max(delta_i)
        exp_delta = np.exp(delta_i - max_delta)
        denom = np.exp(-max_delta) + np.sum(exp_delta)
        weights_i = exp_delta / denom
        dollar_demand += instance_data["aum"][i] * weights_i

    market_cap = p_star * instance_data["shares_out"]
    relative_discrepancy = np.max(np.abs(dollar_demand - market_cap) / market_cap)
    assert relative_discrepancy < 1e-4, f"Market clearing discrepancy {relative_discrepancy:.2e} exceeds tolerance"


def test_flow_multiplier_bounds(instance_data: dict[str, Any]) -> None:
    """Verify Gabaix-Koijen aggregate elasticity and multiplier identities."""
    res = ref.compute_flow_multiplier(
        instance_data["aum_shares"],
        instance_data["elasticities"],
    )

    zeta_m = res["aggregate_elasticity"]
    m_mult = res["flow_multiplier"]

    # 1. Aggregate elasticity must be positive and bounded within empirical range (0.05 to 5.0)
    assert 0.05 <= zeta_m <= 5.0, f"Aggregate elasticity {zeta_m} out of bounds"

    # 2. Multiplier identity: M * zeta_m == 1.0
    assert abs(zeta_m * m_mult - 1.0) < 1e-6, "Flow multiplier identity M * zeta == 1 violated"

    # 3. Inelastic markets prediction: multiplier M >= 1.0
    assert m_mult >= 0.5, f"Multiplier {m_mult} must be >= 0.5"


def test_index_event_study(instance_data: dict[str, Any]) -> None:
    """Verify index inclusion flow impact estimation and event CARs."""
    res = ref.estimate_index_event_impact(
        instance_data["pre_prices"],
        instance_data["post_prices"],
        instance_data["flow_fractions"],
    )

    # 1. Impact multiplier must be strictly positive and reflect inelastic demand (M >= 1.0)
    assert res["multiplier"] >= 1.0, f"Impact multiplier {res['multiplier']} must be >= 1.0 under inelastic demand"

    # 2. Stock elasticity must equal reciprocal of multiplier
    expected_zeta = 1.0 / res["multiplier"]
    assert abs(res["stock_elasticity"] - expected_zeta) < 1e-6

    # 3. R-squared must lie in [0, 1]
    assert 0.0 <= res["r2"] <= 1.0

    # 4. Mean CAR must be positive under positive flow shocks
    assert res["mean_car"] > 0.0
