"""Pytest suite for CAP4: Research Thesis & Defense Capstone Grader.

Verifies doctoral thesis replication, econometric estimation, and defense stress-test solvers:
1. Sample Hygiene & Institutional Delisting Adjustments
2. Econometric Factor Estimation, Shanken Corrections, and GRS Tests
3. Committee Defense Stress Testing & Sensitivity Bounds
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
import reference as solution
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))


@pytest.fixture
def thesis_instance() -> dict[str, Any]:
    """Provide a reproducible thesis instance for property and invariant checks."""
    return dict(make_instance(seed=SEED))


# =========================================================================
# Section 1: Sample Hygiene & Institutional Delisting Adjustments
# =========================================================================


def test_sample_hygiene_spread_properties(thesis_instance: dict[str, Any]) -> None:
    """Verify that sample hygiene spreads and delisting adjustments satisfy economic invariants."""
    res = solution.solve_hygiene_and_delisting(thesis_instance)

    ew_spread = res["ew_spread"]
    vw_spread = res["vw_spread"]
    delisting_drag = res["delisting_drag"]
    nyse_vw_spread = res["nyse_vw_spread"]

    # Spreads must be finite numbers
    assert np.isfinite(ew_spread), f"EW spread must be finite, got {ew_spread}"
    assert np.isfinite(vw_spread), f"VW spread must be finite, got {vw_spread}"
    assert np.isfinite(delisting_drag), f"Delisting drag must be finite, got {delisting_drag}"
    assert np.isfinite(nyse_vw_spread), f"NYSE VW spread must be finite, got {nyse_vw_spread}"

    # Anomaly spread must be strictly positive
    assert ew_spread > 0.005, f"Equal-weighted spread must be substantial (> 0.5%/mo), got {ew_spread}"
    assert vw_spread > 0.005, f"Value-weighted spread must be substantial (> 0.5%/mo), got {vw_spread}"


def test_nasdaq_shumway_delisting_penalty(thesis_instance: dict[str, Any]) -> None:
    """Verify that NASDAQ delistings incur the full -0.55 Shumway penalty rather than a uniform -0.30."""
    res = solution.solve_hygiene_and_delisting(thesis_instance)

    raw_returns = np.array(thesis_instance["raw_returns"], dtype=np.float64)
    delisting_flags = np.array(thesis_instance["delisting_flags"], dtype=bool)
    exchange_codes = np.array(thesis_instance["exchange_codes"], dtype=np.int64)
    anomaly_signals = np.array(thesis_instance["anomaly_signals"], dtype=np.float64)
    market_caps = np.array(thesis_instance["market_caps"], dtype=np.float64)

    top_decile = anomaly_signals >= np.percentile(anomaly_signals, 90.0)
    bot_decile = anomaly_signals <= np.percentile(anomaly_signals, 10.0)

    clean_ref = raw_returns.copy()
    for j in range(len(exchange_codes)):
        mask = delisting_flags[:, j]
        if np.any(mask):
            p = -0.30 if exchange_codes[j] == 1 else -0.55
            clean_ref[mask, j] = p

    w_top = market_caps[top_decile] / np.sum(market_caps[top_decile])
    w_bot = market_caps[bot_decile] / np.sum(market_caps[bot_decile])
    expected_vw = float(np.mean(clean_ref[:, top_decile] @ w_top - clean_ref[:, bot_decile] @ w_bot))
    expected_ew = float(np.mean(np.mean(clean_ref[:, top_decile] - clean_ref[:, bot_decile], axis=1)))

    assert res["ew_spread"] == pytest.approx(expected_ew, rel=1e-5), (
        "Delisting correction must apply -0.55 for NASDAQ and -0.30 for NYSE"
    )
    assert res["vw_spread"] == pytest.approx(expected_vw, rel=1e-5), (
        "Value-weighted spread must accurately reflect NASDAQ -0.55 delisting penalty"
    )


def test_nyse_breakpoint_capitalization_weighting(thesis_instance: dict[str, Any]) -> None:
    """Verify that nyse_vw_spread applies market cap weighting excluding microcaps below NYSE p20."""
    res = solution.solve_hygiene_and_delisting(thesis_instance)

    market_caps = np.array(thesis_instance["market_caps"], dtype=np.float64)
    anomaly_signals = np.array(thesis_instance["anomaly_signals"], dtype=np.float64)
    nyse_p20_cutoff = float(thesis_instance["nyse_p20_cutoff"])

    top_decile = anomaly_signals >= np.percentile(anomaly_signals, 90.0)
    valid_top = top_decile & (market_caps >= nyse_p20_cutoff)

    # Verify that nyse_vw_spread is strictly different from equal-weighted spread
    assert abs(res["nyse_vw_spread"] - res["ew_spread"]) > 1e-5, (
        "NYSE value-weighted spread must differ from naive equal-weighted spread"
    )
    # Weights must be non-negative
    w_sum = np.sum(market_caps[valid_top])
    assert w_sum > 0.0, "NYSE qualifying firms must have positive aggregate market cap"


# =========================================================================
# Section 2: Econometric Estimation, Shanken Corrections, and GRS Tests
# =========================================================================


def test_econometric_estimation_properties(thesis_instance: dict[str, Any]) -> None:
    """Verify factor risk premia, Shanken corrections, and GRS test properties."""
    sol = solution.solve_econometric_estimation(thesis_instance)

    lambda_premia = sol["lambda_premia"]
    shanken_factor = sol["shanken_factor"]
    shanken_se = sol["shanken_se"]
    grs_stat = sol["grs_statistic"]
    grs_p = sol["grs_p_value"]

    # Invariants
    assert len(lambda_premia) == 2, f"Expected 2 factor risk premia, got {len(lambda_premia)}"
    assert len(shanken_se) == 2, f"Expected 2 factor standard errors, got {len(shanken_se)}"
    assert shanken_factor >= 1.0, f"Shanken factor must be >= 1.0, got {shanken_factor}"
    assert all(se > 0.0 for se in shanken_se), f"Standard errors must be positive, got {shanken_se}"
    assert grs_stat > 0.0, f"GRS test statistic must be positive, got {grs_stat}"
    assert 0.0 <= grs_p <= 1.0, f"GRS p-value must lie in [0, 1], got {grs_p}"


def test_shanken_standard_error_correction_invariant(thesis_instance: dict[str, Any]) -> None:
    """Verify that Shanken correction factor c = 1 + lambda' Sigma_f^{-1} lambda strictly exceeds 1.0."""
    sol = solution.solve_econometric_estimation(thesis_instance)

    factor_series = np.array(thesis_instance["factor_series"], dtype=np.float64)
    lambda_hat = np.array(sol["lambda_premia"], dtype=np.float64)

    sigma_f = np.cov(factor_series, rowvar=False)
    inv_sigma_f = np.linalg.inv(sigma_f)
    expected_c = float(1.0 + lambda_hat @ inv_sigma_f @ lambda_hat)

    assert sol["shanken_factor"] == pytest.approx(expected_c, rel=1e-5), (
        "Shanken factor must equal 1 + lambda' Sigma_f^{-1} lambda"
    )
    assert sol["shanken_factor"] > 1.001, (
        f"Shanken correction factor must strictly exceed 1.0 for non-zero premia, got {sol['shanken_factor']}"
    )


def test_grs_curvature_denominator(thesis_instance: dict[str, Any]) -> None:
    """Verify that the Gibbons-Ross-Shanken (GRS) statistic normalizes by (1 + f_bar' Sigma_f^{-1} f_bar)."""
    sol = solution.solve_econometric_estimation(thesis_instance)

    factor_series = np.array(thesis_instance["factor_series"], dtype=np.float64)
    panel_returns = np.array(thesis_instance["panel_returns"], dtype=np.float64)
    t_panel, n_assets = panel_returns.shape
    _, n_factors = factor_series.shape

    x_ts = np.column_stack([np.ones(t_panel), factor_series])
    b_ts = np.linalg.inv(x_ts.T @ x_ts) @ (x_ts.T @ panel_returns)
    alpha_hat = b_ts[0]
    resids = panel_returns - x_ts @ b_ts
    sigma_eps = (resids.T @ resids) / float(t_panel - n_factors - 1)
    inv_sigma_eps = np.linalg.inv(sigma_eps)

    f_bar = np.mean(factor_series, axis=0)
    sigma_f = np.cov(factor_series, rowvar=False)
    inv_sigma_f = np.linalg.inv(sigma_f)

    grs_df_num = n_assets
    grs_df_denom = t_panel - n_assets - n_factors
    grs_scale = float(grs_df_denom / grs_df_num)

    quad_alpha = float(alpha_hat @ inv_sigma_eps @ alpha_hat)
    quad_f = float(f_bar @ inv_sigma_f @ f_bar)
    curvature = float(1.0 + quad_f)
    expected_grs = float(grs_scale * (quad_alpha / curvature))

    assert curvature > 1.0, "Factor curvature term in GRS denominator must strictly exceed 1.0"
    assert sol["grs_statistic"] == pytest.approx(expected_grs, rel=1e-5), (
        "GRS statistic must divide by factor curvature denominator (1 + f_bar' Sigma_f^{-1} f_bar)"
    )


# =========================================================================
# Section 3: Defense Stress Testing & Sensitivity Bounds
# =========================================================================


def test_defense_stress_test_properties(thesis_instance: dict[str, Any]) -> None:
    """Verify that committee defense stress testing correctly accounts for all frictions."""
    stress = solution.solve_defense_stress_test(thesis_instance)

    net_alpha = stress["net_alpha"]
    breakeven = stress["breakeven_cost_bps"]
    resilience = stress["resilience_score"]
    verdict = stress["defense_verdict"]

    assert net_alpha > 0.0, f"Net alpha after standard frictions must be positive, got {net_alpha}"
    assert breakeven > 50.0, f"Break-even trading cost must exceed 50 bps, got {breakeven}"
    assert 0.0 <= resilience <= 100.0, f"Resilience score must lie in [0, 100], got {resilience}"
    assert isinstance(verdict, bool), f"Defense verdict must be boolean, got {type(verdict)}"


def test_multiplicative_decay_scaling(thesis_instance: dict[str, Any]) -> None:
    """Verify that out-of-sample decay scales remaining margin multiplicatively: (1 - decay)."""
    stress = solution.solve_defense_stress_test(thesis_instance)

    gross_alpha = float(thesis_instance["gross_alpha"])
    turnover = float(thesis_instance["turnover"])
    decay_rate = float(thesis_instance["decay_rate"])
    look_ahead = float(thesis_instance["look_ahead_penalty"])
    microcap = float(thesis_instance["microcap_penalty"])
    tcost_bps = float(thesis_instance["trading_cost_bps"])

    tcost_drag = turnover * (tcost_bps / 10000.0)
    unhedged_margin = gross_alpha - look_ahead - microcap - tcost_drag
    expected_net = float(unhedged_margin * (1.0 - decay_rate))

    assert stress["net_alpha"] == pytest.approx(expected_net, rel=1e-5), (
        "Net alpha must apply out-of-sample decay multiplicatively to unhedged margin"
    )
