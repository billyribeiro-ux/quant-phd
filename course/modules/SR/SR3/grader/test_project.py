"""Acceptance suite for SR3 project: Atlas A19 Systemic-Risk Monitor (`atlas/systemic.py`).

Runs identically in Pyodide and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest

try:
    from atlas import systemic as sol  # type: ignore[attr-defined]
except ImportError:
    import reference as sol
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_quantile_regression_pinball_loss() -> None:
    """Validate linear quantile regression estimates and pinball loss optimality."""
    r_sys = np.asarray(INST["r_system"], dtype=np.float64)
    r_inst = np.asarray(INST["r_institutions"][0], dtype=np.float64)
    t_obs = len(r_sys)

    x = np.column_stack([np.ones(t_obs), r_inst])
    q = 0.05
    beta_q = sol.fit_linear_quantile_regression(r_sys, x, q=q)

    assert isinstance(beta_q, np.ndarray), "fit_linear_quantile_regression must return np.ndarray"
    assert beta_q.shape == (2,), f"Expected shape (2,), got {beta_q.shape}"

    # Verify pinball loss check function optimality against OLS baseline
    # Pinball loss: sum rho_q(u) where rho_q(u) = u * (q - (u < 0))
    def pinball(b: np.ndarray[Any, Any]) -> float:
        res = r_sys - x @ b
        return float(np.sum(res * (q - (res < 0).astype(np.float64))))

    loss_q = pinball(beta_q)
    # OLS coefficients
    beta_ols = np.linalg.lstsq(x, r_sys, rcond=None)[0]
    loss_ols = pinball(beta_ols)

    assert loss_q <= loss_ols + 1e-6, (
        f"Quantile regression pinball loss ({loss_q:.6f}) must be <= OLS loss ({loss_ols:.6f})"
    )


def test_covar_and_delta_covar() -> None:
    """Validate CoVaR, median CoVaR, and Delta-CoVaR with and without macro state conditioning."""
    r_sys = np.asarray(INST["r_system"], dtype=np.float64)
    r_inst = np.asarray(INST["r_institutions"][1], dtype=np.float64)
    macro = np.asarray(INST["macro_states"], dtype=np.float64)
    alpha = INST["alpha"]

    # 1. Static CoVaR
    res_static = sol.compute_covar(r_sys, r_inst, state_vars=None, alpha=alpha)
    for key in ("covar", "covar_median", "delta_covar", "beta_quantile", "var_institution"):
        assert key in res_static, f"Missing key '{key}' in static compute_covar output"

    # CoVaR at 5% crisis should be substantially lower (more negative return) than median CoVaR
    assert res_static["covar"] < res_static["covar_median"], (
        f"Crisis CoVaR ({res_static['covar']:.5f}) must be < median CoVaR ({res_static['covar_median']:.5f})"
    )
    assert res_static["delta_covar"] < 0.0, f"Delta-CoVaR must be negative, got {res_static['delta_covar']:.5f}"
    assert res_static["beta_quantile"] > 0.0, "Tail quantile regression slope must be positive"

    # 2. State-conditioned CoVaR
    res_macro = sol.compute_covar(r_sys, r_inst, state_vars=macro, alpha=alpha)
    assert res_macro["covar"] < res_macro["covar_median"], (
        f"State-conditioned crisis CoVaR must be < median CoVaR, got {res_macro['covar']:.5f}"
    )
    assert res_macro["delta_covar"] < 0.0, (
        f"State-conditioned Delta-CoVaR must be negative, got {res_macro['delta_covar']:.5f}"
    )


def test_marginal_expected_shortfall() -> None:
    """Validate Marginal Expected Shortfall (MES) against crisis returns."""
    r_sys = np.asarray(INST["r_system"], dtype=np.float64)
    r_inst = np.asarray(INST["r_institutions"][2], dtype=np.float64)
    alpha = INST["alpha"]

    mes = sol.compute_mes(r_sys, r_inst, alpha=alpha)
    assert isinstance(mes, float), "compute_mes must return a float"
    # MES is expressed as positive expected loss during crisis
    assert mes > 0.0, f"Expected institution loss during 5% systemic crisis should be positive, got {mes:.5f}"

    # Crisis days loss should exceed unconditional average loss
    unconditional_loss = float(-np.mean(r_inst))
    assert mes > unconditional_loss, (
        f"MES ({mes:.5f}) must strictly exceed unconditional average loss ({unconditional_loss:.5f})"
    )


def test_lrmes_and_srisk_formula() -> None:
    """Validate LRMES projection and closed-form SRISK capital shortfall."""
    r_sys = np.asarray(INST["r_system"], dtype=np.float64)
    r_inst = np.asarray(INST["r_institutions"][0], dtype=np.float64)
    crisis_drop = INST["crisis_drop"]

    lrmes = sol.compute_lrmes(r_sys, r_inst, alpha=0.05, crisis_drop=crisis_drop)
    assert isinstance(lrmes, float), "compute_lrmes must return a float"
    assert 0.0 < lrmes < 1.0, f"LRMES must lie in (0, 1), got {lrmes:.5f}"

    # Hand-checked SRISK instance:
    # W = 100.0, D = 900.0, k = 0.08, LRMES = 0.40
    # Required equity = 0.08 * (900.0 + (1 - 0.40)*100.0) = 0.08 * 960.0 = 76.8
    # Remaining equity = 60.0 ==> Capital Shortfall = 76.8 - 60.0 = 16.8
    srisk_hand = sol.compute_srisk(100.0, 900.0, 0.40, prudential_ratio=0.08)
    assert np.isclose(srisk_hand, 16.8, atol=1e-5), f"SRISK hand-check failed: expected 16.8, got {srisk_hand:.5f}"

    # A well-capitalized institution with zero debt has zero SRISK (non-negative clamp)
    srisk_solvent = sol.compute_srisk(500.0, 50.0, 0.20, prudential_ratio=0.08)
    # k * D - (1 - k)(1 - LRMES) * W = 0.08 * 50 - 0.92 * 0.8 * 500 = 4 - 368 < 0
    assert srisk_solvent == 0.0, f"Solvent institution SRISK must clamp to 0.0, got {srisk_solvent:.5f}"


def test_systemic_srisk_panel_and_contributions() -> None:
    """Validate multi-institution SRISK panel aggregation and percentage shares."""
    equities = np.asarray(INST["equities"], dtype=np.float64)
    debts = np.asarray(INST["debts"], dtype=np.float64)
    r_sys = np.asarray(INST["r_system"], dtype=np.float64)
    k = INST["prudential_ratio"]

    lrmes_list = [
        sol.compute_lrmes(r_sys, np.asarray(inst, dtype=np.float64), crisis_drop=INST["crisis_drop"])
        for inst in INST["r_institutions"]
    ]
    lrmes_arr = np.asarray(lrmes_list, dtype=np.float64)

    res = sol.compute_systemic_srisk_panel(equities, debts, lrmes_arr, prudential_ratio=k)

    for key in ("srisk_individual", "capital_shortfall", "total_srisk", "srisk_pct"):
        assert key in res, f"Missing key '{key}' in compute_systemic_srisk_panel output"

    srisk_ind = res["srisk_individual"]
    total_srisk = res["total_srisk"]
    srisk_pct = res["srisk_pct"]

    assert srisk_ind.shape == equities.shape, "srisk_individual shape mismatch"
    assert np.all(srisk_ind >= 0.0), "All individual SRISK values must be non-negative"
    assert np.isclose(total_srisk, float(np.sum(srisk_ind)), atol=1e-6), (
        "total_srisk must equal sum of individual SRISK"
    )

    if total_srisk > 1e-6:
        assert np.isclose(float(np.sum(srisk_pct)), 1.0, atol=1e-6), "SRISK percentage shares must sum to 1.0"
        assert np.all(srisk_pct >= 0.0), "SRISK shares must be non-negative"


def test_eisenberg_noe_clearing_vector() -> None:
    """Validate Eisenberg-Noe network clearing on solvent baseline system."""
    l_mat = np.asarray(INST["nominal_liabilities"], dtype=np.float64)
    z_vec = np.asarray(INST["external_assets"], dtype=np.float64)
    b_vec = np.asarray(INST["senior_liabilities"], dtype=np.float64)

    res = sol.compute_network_clearing(l_mat, z_vec, b_vec)

    for key in ("clearing_payments", "equity_values", "defaults", "default_count", "cascade_rounds", "total_shortfall"):
        assert key in res, f"Missing key '{key}' in compute_network_clearing output"

    p_star = res["clearing_payments"]
    p_bar = np.sum(l_mat, axis=1)

    assert np.all(p_star <= p_bar + 1e-8), "Clearing payments cannot exceed promised nominal liabilities"
    assert np.all(p_star >= 0.0), "Clearing payments cannot be negative"
    assert np.all(res["equity_values"] >= 0.0), "Firm equity values cannot be negative"


def test_network_cascade_shock_propagation() -> None:
    """Validate cascade contagion rounds and defaults under severe asset shock."""
    l_mat = np.asarray(INST["nominal_liabilities"], dtype=np.float64)
    z_stressed = np.asarray(INST["stressed_assets"], dtype=np.float64)
    b_vec = np.asarray(INST["senior_liabilities"], dtype=np.float64)

    res_shock = sol.compute_network_clearing(l_mat, z_stressed, b_vec)

    # Severe stress shock should induce at least 1 default and positive shortfall
    assert res_shock["default_count"] >= 1, "Stressed network should exhibit defaults"
    assert res_shock["total_shortfall"] > 0.0, "Stressed network should exhibit non-zero aggregate payment shortfall"
    assert res_shock["cascade_rounds"] >= 1, "Cascade clearing requires at least 1 round"


def test_systemic_risk_monitor_alerts() -> None:
    """Validate SystemicRiskMonitor alert thresholds and severity rating progression."""
    monitor = sol.SystemicRiskMonitor()

    # Normal calm market state
    calm_metrics = {
        "delta_covar": -0.005,  # calmer than -0.015 threshold
        "mes": 0.015,  # below 0.035 threshold
        "srisk_pct": 0.15,  # below 0.30 threshold
        "network_defaults": 0,  # below 1 threshold
    }
    calm_res = monitor.evaluate(calm_metrics)
    assert calm_res["severity"] == "NORMAL", f"Expected NORMAL, got {calm_res['severity']}"
    assert calm_res["total_breaches"] == 0, "No breaches expected in calm state"
    assert not calm_res["is_alert"], "No alert flag expected in calm state"

    # Critical systemic crisis state breaching all indicators
    crisis_metrics = {
        "delta_covar": -0.035,  # severe breach (< -0.015)
        "mes": 0.065,  # severe breach (> 0.035)
        "srisk_pct": 0.45,  # concentration breach (> 0.30)
        "network_defaults": 2,  # cascade breach (>= 1)
    }
    crisis_res = monitor.evaluate(crisis_metrics)
    assert crisis_res["severity"] == "CRITICAL", f"Expected CRITICAL, got {crisis_res['severity']}"
    assert crisis_res["total_breaches"] == 4, f"Expected 4 breaches, got {crisis_res['total_breaches']}"
    assert crisis_res["is_alert"], "Alert flag expected in crisis state"


def test_input_validation_and_invariants() -> None:
    """Validate error raising on domain and structural invariant violations."""
    # Invalid quantile level
    with pytest.raises(ValueError):
        sol.fit_linear_quantile_regression(np.array([1.0, 2.0]), np.ones((2, 1)), q=1.5)

    # Negative equity value in SRISK
    with pytest.raises(ValueError):
        sol.compute_srisk(-10.0, 100.0, 0.40)

    # Negative debt value in SRISK
    with pytest.raises(ValueError):
        sol.compute_srisk(100.0, -50.0, 0.40)

    # Non-zero diagonal in nominal liabilities matrix
    bad_l = np.array([[10.0, 20.0], [30.0, 0.0]])
    with pytest.raises(ValueError):
        sol.compute_network_clearing(bad_l, np.array([50.0, 50.0]))
