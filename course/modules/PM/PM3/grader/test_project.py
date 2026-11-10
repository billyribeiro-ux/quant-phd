"""Acceptance test suite for PM3: Private Credit & Infrastructure.

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    compute_risk_metrics,
    estimate_smoothing_parameter,
    estimate_systematic_risk,
    solve_project,
    unsmooth_returns_ar1,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_instance_validity() -> None:
    """Validate instance dimensions, finitude, and configuration structure."""
    reported = np.asarray(INST["reported_returns"], dtype=float)
    proxy = np.asarray(INST["public_proxy_returns"], dtype=float)
    rf_q = float(INST["rf_quarterly"])

    assert len(reported) == 40, f"Expected 40 quarters of reported returns, got {len(reported)}"
    assert len(proxy) == 40, f"Expected 40 quarters of proxy returns, got {len(proxy)}"
    assert np.all(np.isfinite(reported)), "Reported returns contain non-finite values"
    assert np.all(np.isfinite(proxy)), "Proxy returns contain non-finite values"
    assert 0.0 < rf_q < 0.05, f"Quarterly risk-free rate out of range: {rf_q}"


def test_phi_estimation_bounds() -> None:
    """Validate estimation of first-order autocorrelation parameter phi."""
    reported = np.asarray(INST["reported_returns"], dtype=float)
    phi = estimate_smoothing_parameter(reported)

    assert 0.0 <= phi <= 0.95, f"Estimated phi {phi} outside permitted bounds [0.0, 0.95]"
    assert phi > 0.05, f"Expected positive autocorrelation in private credit marks, got {phi}"

    # Synthetic white noise should produce phi near 0
    rng = np.random.default_rng(12345)
    white_noise = rng.normal(0.0, 0.02, size=50)
    phi_noise = estimate_smoothing_parameter(white_noise)
    assert abs(phi_noise) < 0.35, f"White noise produced excessive phi: {phi_noise}"


def test_unsmooth_inversion_and_identity() -> None:
    """Verify algebraic exactness of AR(1) smoothing inversion."""
    reported = np.asarray(INST["reported_returns"], dtype=float)

    # 1. Identity at phi = 0
    identity_ret = unsmooth_returns_ar1(reported, 0.0)
    assert np.allclose(identity_ret, reported, atol=1e-12), "Unsmoothing with phi=0 must be identity"

    # 2. Inversion conservation: forward smoothing recovered returns reproduces observed marks
    phi = estimate_smoothing_parameter(reported)
    unsmoothed = unsmooth_returns_ar1(reported, phi)
    assert len(unsmoothed) == len(reported)

    re_smoothed = np.zeros_like(reported)
    re_smoothed[0] = unsmoothed[0]
    for t in range(1, len(reported)):
        re_smoothed[t] = phi * reported[t - 1] + (1.0 - phi) * unsmoothed[t]

    assert np.allclose(re_smoothed, reported, atol=1e-10), (
        "Re-smoothing unobserved series does not reconstruct reported series exactly"
    )


def test_volatility_inflation_and_annualization() -> None:
    """Verify that quarterly volatility is scaled by sqrt(4) = 2.0 and expands upon de-smoothing."""
    reported = np.asarray(INST["reported_returns"], dtype=float)
    rf_q = float(INST["rf_quarterly"])

    phi = estimate_smoothing_parameter(reported)
    unsmoothed = unsmooth_returns_ar1(reported, phi)

    rep_stats = compute_risk_metrics(reported, rf_q)
    unsmooth_stats = compute_risk_metrics(unsmoothed, rf_q)

    # Annualization scaling check: quarterly std must be multiplied by sqrt(4) = 2.0
    expected_vol_rep = float(np.std(reported, ddof=1) * 2.0)
    assert np.isclose(rep_stats["volatility_annualized"], expected_vol_rep, atol=1e-8), (
        f"Annualized volatility must be scaled by sqrt(4)=2.0: expected {expected_vol_rep:.6f}, "
        f"got {rep_stats['volatility_annualized']:.6f}"
    )

    vol_rep = rep_stats["volatility_annualized"]
    vol_true = unsmooth_stats["volatility_annualized"]

    assert vol_true > vol_rep * 1.05, (
        f"De-smoothed volatility ({vol_true:.4f}) must exceed reported volatility ({vol_rep:.4f})"
    )

    # Autocorrelation should be suppressed in de-smoothed returns
    ac_rep = rep_stats["first_order_autocorr"]
    ac_true = unsmooth_stats["first_order_autocorr"]
    assert abs(ac_true) < ac_rep, (
        f"De-smoothed autocorrelation ({ac_true:.4f}) must be smaller than reported ({ac_rep:.4f})"
    )


def test_systematic_risk_and_beta_expansion() -> None:
    """Verify that appraisal smoothing understates market beta to leveraged loans."""
    reported = np.asarray(INST["reported_returns"], dtype=float)
    proxy = np.asarray(INST["public_proxy_returns"], dtype=float)

    phi = estimate_smoothing_parameter(reported)
    unsmoothed = unsmooth_returns_ar1(reported, phi)

    rep_sys = estimate_systematic_risk(reported, proxy)
    unsmooth_sys = estimate_systematic_risk(unsmoothed, proxy)

    beta_rep = rep_sys["beta"]
    beta_true = unsmooth_sys["beta"]

    assert beta_true > beta_rep * 1.05, (
        f"De-smoothed beta ({beta_true:.4f}) must expand relative to reported beta ({beta_rep:.4f})"
    )
    assert 0.0 <= rep_sys["r_squared"] <= 1.0, f"Invalid reported R2: {rep_sys['r_squared']}"
    assert 0.0 <= unsmooth_sys["r_squared"] <= 1.0, f"Invalid unsmoothed R2: {unsmooth_sys['r_squared']}"
    assert unsmooth_sys["tracking_error"] > 0.0, "Tracking error must be strictly positive"


def test_sharpe_deflation_and_drawdown_bounds() -> None:
    """Verify that de-smoothing deflates artificial Sharpe ratios and produces bounded drawdowns."""
    reported = np.asarray(INST["reported_returns"], dtype=float)
    rf_q = float(INST["rf_quarterly"])

    phi = estimate_smoothing_parameter(reported)
    unsmoothed = unsmooth_returns_ar1(reported, phi)

    rep_stats = compute_risk_metrics(reported, rf_q)
    unsmooth_stats = compute_risk_metrics(unsmoothed, rf_q)

    sharpe_rep = rep_stats["sharpe_ratio"]
    sharpe_true = unsmooth_stats["sharpe_ratio"]

    # When excess return is positive, higher volatility reduces Sharpe ratio
    assert sharpe_true < sharpe_rep, (
        f"True Sharpe ratio ({sharpe_true:.4f}) must be lower than smoothed Sharpe ratio ({sharpe_rep:.4f})"
    )

    dd_rep = rep_stats["max_drawdown"]
    dd_true = unsmooth_stats["max_drawdown"]
    assert 0.0 <= dd_rep <= 1.0, f"Invalid reported max drawdown: {dd_rep}"
    assert 0.0 <= dd_true <= 1.0, f"Invalid de-smoothed max drawdown: {dd_true}"


def test_full_pipeline_solution() -> None:
    """Verify master solve_project pipeline return structure and ratios."""
    res = solve_project(INST)

    required_keys = {
        "phi",
        "reported_metrics",
        "unsmoothed_metrics",
        "proxy_metrics",
        "reported_systematic",
        "unsmoothed_systematic",
        "volatility_ratio",
        "beta_ratio",
    }
    assert required_keys.issubset(res.keys()), f"Missing keys in pipeline output: {required_keys - set(res.keys())}"

    assert res["volatility_ratio"] > 1.05, f"Volatility ratio too low: {res['volatility_ratio']}"
    assert res["beta_ratio"] > 1.05, f"Beta ratio too low: {res['beta_ratio']}"
