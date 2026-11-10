"""Acceptance test suite for CR3: Credit Cycles & Macro-Credit.

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    construct_credit_sentiment_index,
    decompose_credit_spread,
    evaluate_recession_forecasts,
    fit_recession_probit,
    predict_spread_reversals,
    simulate_leveraged_loan_waterfall,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
BOND_DATA: dict[str, list[float]] = {
    "spread_bps": INST["bond_spread_bps"],
    "duration": INST["bond_duration"],
    "coupon": INST["bond_coupon"],
    "amount_outstanding": INST["bond_amount_outstanding"],
    "merton_edf": INST["bond_merton_edf"],
    "industry_id": INST["bond_industry_id"],
}


# ============================================================================
# 1. Gilchrist-Zakrajšek (2012) Spread Decomposition & EBP
# ============================================================================


def test_ebp_decomposition_identity() -> None:
    """EBP must exactly equal GZ credit spread minus predicted default spread."""
    res = decompose_credit_spread(BOND_DATA)
    gz = res["gz_spread_bps"]
    pred = res["predicted_spread_bps"]
    ebp = res["ebp_bps"]

    assert abs(gz - pred - ebp) < 1e-3, f"Articulation failure: GZ ({gz}) - Pred ({pred}) != EBP ({ebp})"
    assert gz > 0.0, "GZ spread must be strictly positive"
    assert pred > 0.0, "Predicted default component must be strictly positive"


def test_ebp_regression_properties() -> None:
    """Log-spread regression must produce valid R^2 and positive residual std."""
    res = decompose_credit_spread(BOND_DATA)
    assert 0.0 <= res["r_squared"] <= 1.0, f"R^2 must be in [0, 1], got {res['r_squared']}"
    assert res["residual_std"] > 0.0, "Residual standard deviation must be positive"
    coefs = res["coefficients"]
    for k in ["intercept", "duration", "coupon", "log_amount", "log_edf"]:
        assert k in coefs, f"Missing coefficient: {k}"
        assert math.isfinite(coefs[k]), f"Coefficient {k} is non-finite"


def test_ebp_input_validation() -> None:
    """Function must reject negative spreads and mismatched lengths."""
    bad_data = {
        "spread_bps": [-10.0, 50.0, 100.0],
        "duration": [5.0, 5.0, 5.0],
        "coupon": [0.05, 0.05, 0.05],
        "amount_outstanding": [500.0, 500.0, 500.0],
        "merton_edf": [0.01, 0.01, 0.01],
        "industry_id": [0, 1, 2],
    }
    with pytest.raises(ValueError):
        decompose_credit_spread(bad_data)


# ============================================================================
# 2. Credit-Market Sentiment Index
# ============================================================================


def test_sentiment_index_properties() -> None:
    """Sentiment index must be mean zero and have bounded lag-1 autocorrelation."""
    res = construct_credit_sentiment_index(
        INST["hy_issuance_share"],
        INST["credit_spreads"],
        INST["ebp"],
        INST["weights"],
    )
    s_idx = res["sentiment_index"]
    assert len(s_idx) == len(INST["hy_issuance_share"])
    assert abs(sum(s_idx) / len(s_idx)) < 1e-3, "Standardized sentiment index should have approximately zero mean"
    assert -1.0 <= res["autocorrelation_lag1"] <= 1.0, "Autocorrelation must be in [-1, 1]"
    assert abs(sum(res["weights"]) - 1.0) < 1e-4, "Weights must sum to 1.0"
    for name, z in res["z_scores"].items():
        sample_std = float(np.std(z, ddof=1))
        assert abs(sample_std - 1.0) < 1e-2, (
            f"Component {name} z-score must have unit sample standard deviation, got {sample_std}"
        )


def test_sentiment_comparative_directionality() -> None:
    """High HY share increases sentiment; wide spreads or high EBP decrease sentiment."""
    hy = [0.10, 0.20, 0.30, 0.40, 0.25, 0.15, 0.35, 0.20, 0.22, 0.18]
    spr = [300.0, 250.0, 200.0, 150.0, 180.0, 280.0, 140.0, 220.0, 210.0, 260.0]
    ebp = [50.0, 20.0, -10.0, -40.0, -15.0, 40.0, -45.0, 0.0, -5.0, 30.0]

    res = construct_credit_sentiment_index(hy, spr, ebp)
    s = res["sentiment_index"]
    # Point 3 has highest HY share (0.40), lowest spread (150), and lowest EBP (-40)
    # Point 0 has lowest HY share (0.10), highest spread (300), and highest EBP (+50)
    assert s[3] > s[0], (
        "Bullish credit market conditions must produce strictly higher sentiment than depressed conditions"
    )


# ============================================================================
# 3. Predictable Spread Reversals
# ============================================================================


def test_spread_reversal_inference() -> None:
    """Reversal regression must return valid OLS and Newey-West HAC statistics."""
    res_sent = construct_credit_sentiment_index(
        INST["hy_issuance_share"],
        INST["credit_spreads"],
        INST["ebp"],
        INST["weights"],
    )
    res_rev = predict_spread_reversals(
        res_sent["sentiment_index"],
        INST["credit_spreads"],
        horizon_steps=INST["horizon_steps"],
    )

    assert math.isfinite(res_rev["beta_reversal"])
    assert math.isfinite(res_rev["intercept"])
    assert math.isfinite(res_rev["t_stat_hac"])
    assert 0.0 <= res_rev["p_value"] <= 1.0
    assert 0.0 <= res_rev["r_squared"] <= 1.0


def test_spread_reversal_directionality() -> None:
    """High sentiment must predict positive future spread widening (beta_rev > 0)."""
    t_len = 24
    horizon = 2
    sent = [1.0 if i % 4 < 2 else -1.0 for i in range(t_len)]
    spreads = [150.0 + (35.0 if (i - horizon) % 4 < 2 else -35.0) for i in range(t_len)]
    res = predict_spread_reversals(sent, spreads, horizon_steps=horizon)
    assert res["beta_reversal"] > 0.0, (
        f"beta_reversal must be positive when high sentiment leads widening spreads, got {res['beta_reversal']}"
    )


def test_spread_reversal_horizon_validation() -> None:
    """Reversal function must validate horizon parameters."""
    with pytest.raises(ValueError):
        predict_spread_reversals([1.0, 2.0, 3.0], [100.0, 120.0, 130.0], horizon_steps=0)
    with pytest.raises(ValueError):
        predict_spread_reversals([1.0, 2.0, 3.0], [100.0, 120.0, 130.0], horizon_steps=5)


# ============================================================================
# 4. Recession Probit / Logit Regression
# ============================================================================


def test_recession_probit_estimation() -> None:
    """Probit/logit regression must produce valid log-likelihood, pseudo-R^2, and probabilities."""
    res = fit_recession_probit(
        INST["credit_indicators"],
        INST["term_spreads"],
        INST["recession_flags"],
    )

    assert res["log_likelihood"] <= 0.0, "Log-likelihood must be non-positive"
    assert 0.0 <= res["pseudo_r_squared"] <= 1.0, "McFadden pseudo-R^2 must be in [0, 1]"

    probs = res["fitted_probabilities"]
    assert len(probs) == len(INST["recession_flags"])
    for p in probs:
        assert 0.0 < p < 1.0, f"Fitted probability must be in (0, 1), got {p}"


def test_recession_probit_covariates_impact() -> None:
    """Credit distress should increase recession risk; term spread steepness should reduce it."""
    indicators = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, -1.2, 0.2, 1.8, -0.8, 1.2, -1.0, 0.0, 1.0]
    term_spreads = [2.5, 2.0, 1.5, 1.0, 0.5, -0.5, -1.5, 2.0, 0.8, -1.2, 1.8, -0.8, 1.5, 0.5, -1.0]
    recessions = [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1]

    res = fit_recession_probit(indicators, term_spreads, recessions)
    b = res["beta"]
    assert b["credit_indicator"] > 0.0, "Credit distress should have a positive coefficient on recession probability"
    assert b["term_spread"] < 0.0, "Steeper term spread should have a negative coefficient on recession probability"


# ============================================================================
# 5. Out-of-Sample Forecast Evaluation
# ============================================================================


def test_forecast_evaluation_metrics() -> None:
    """Evaluation metrics must lie in valid probability / classification ranges."""
    res = evaluate_recession_forecasts(INST["eval_true"], INST["eval_prob"], threshold=0.5)

    assert 0.0 <= res["brier_score"] <= 1.0, "Brier score must be in [0, 1]"
    assert 0.0 <= res["auc_roc"] <= 1.0, "AUC-ROC must be in [0, 1]"
    assert 0.0 <= res["precision"] <= 1.0
    assert 0.0 <= res["recall"] <= 1.0
    assert 0.0 <= res["specificity"] <= 1.0

    cm = res["confusion_matrix"]
    total_samples = cm["tp"] + cm["fp"] + cm["tn"] + cm["fn"]
    assert total_samples == len(INST["eval_true"])


def test_forecast_evaluation_perfect_separation() -> None:
    """When predictions perfectly separate positive and negative classes, AUC-ROC must be 1.0."""
    y_true = [0, 0, 0, 1, 1, 1]
    y_prob = [0.1, 0.2, 0.3, 0.7, 0.8, 0.9]
    res = evaluate_recession_forecasts(y_true, y_prob)
    assert abs(res["auc_roc"] - 1.0) < 1e-9, "AUC-ROC must equal 1.0 for perfect ranking"
    assert res["brier_score"] < 0.10


# ============================================================================
# 6. Leveraged Loan & Private Credit Restructuring Waterfall
# ============================================================================


def test_leveraged_loan_covenant_and_recovery_bounds() -> None:
    """Waterfall recoveries must satisfy bounds and priority rules."""
    res = simulate_leveraged_loan_waterfall(
        INST["loan_debt"],
        INST["loan_ebitda"],
        INST["loan_addback"],
        INST["loan_senior_share"],
        INST["loan_cov_lite"],
        INST["loan_distress"],
    )

    assert 0.0 <= res["senior_recovery_rate"] <= 1.0
    assert 0.0 <= res["junior_recovery_rate"] <= 1.0
    assert 0.0 <= res["total_recovery_rate"] <= 1.0
    assert abs(res["total_recovery_rate"] + res["loss_given_default"] - 1.0) < 1e-5

    # Priority rule: senior recovery rate must be >= junior recovery rate
    assert res["senior_recovery_rate"] >= res["junior_recovery_rate"] - 1e-9, (
        f"Senior recovery ({res['senior_recovery_rate']}) must be >= junior ({res['junior_recovery_rate']})"
    )


def test_leveraged_loan_covlite_depresses_recovery() -> None:
    """Absence of maintenance covenants (cov-lite) allows equity burn, depressing recovery."""
    debt = 500.0
    ebitda = 80.0
    addback = 0.25
    senior_share = 0.75
    distress = 0.50

    maint = simulate_leveraged_loan_waterfall(debt, ebitda, addback, senior_share, False, distress)
    cov_lite = simulate_leveraged_loan_waterfall(debt, ebitda, addback, senior_share, True, distress)

    assert maint["covenant_breached"] is True, "Maintenance loan should trigger breach under 50% distress"
    assert cov_lite["covenant_breached"] is False, "Cov-lite loan has no maintenance covenant to breach"
    assert maint["enterprise_value"] > cov_lite["enterprise_value"], (
        "Early maintenance restructuring must preserve higher enterprise value than delayed cov-lite"
    )
    assert maint["total_recovery_rate"] >= cov_lite["total_recovery_rate"], (
        "Maintenance loan recovery must be >= cov-lite recovery"
    )
