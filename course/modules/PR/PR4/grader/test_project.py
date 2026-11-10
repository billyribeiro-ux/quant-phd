"""Acceptance suite for PR4 project: Atlas A12 Quantitative Risk Engine (atlas/risk.py).

Runs identically in Pyodide and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
from atlas import risk as sol  # type: ignore[attr-defined]
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_historical_var_and_es() -> None:
    losses = np.asarray(INST["losses"], dtype=np.float64)
    alpha = INST["alpha"]

    var_95 = sol.historical_var(losses, 0.95)
    var_99 = sol.historical_var(losses, alpha)
    es_99 = sol.historical_es(losses, alpha)

    assert isinstance(var_99, float), "historical_var must return float"
    assert isinstance(es_99, float), "historical_es must return float"
    assert var_99 > var_95, f"VaR must be strictly increasing in confidence level: got {var_99} <= {var_95}"
    assert es_99 >= var_99, f"Expected Shortfall must be >= VaR: got ES={es_99:g} < VaR={var_99:g}"

    # Hand-checked sample quantile invariance
    expected_q99 = float(np.quantile(losses, alpha, method="linear"))
    assert np.isclose(var_99, expected_q99, atol=1e-8), "Historical VaR does not match quantile"


def test_parametric_normal_and_student_t() -> None:
    losses = np.asarray(INST["losses"], dtype=np.float64)
    alpha = INST["alpha"]

    norm_var, norm_es = sol.parametric_normal_var_es(losses, alpha)
    stud_var, stud_es = sol.parametric_student_t_var_es(losses, alpha, df=4)

    assert norm_es > norm_var, "Normal ES must strictly exceed Normal VaR"
    assert stud_es > stud_var, "Student-t ES must strictly exceed Student-t VaR"

    # For heavy-tailed distributions at 99% confidence, Student-t risk measures must exceed Gaussian
    assert stud_var > norm_var, f"Student-t VaR ({stud_var:g}) must exceed Normal VaR ({norm_var:g}) under fat tails"
    assert stud_es > norm_es, f"Student-t ES ({stud_es:g}) must exceed Normal ES ({norm_es:g}) under fat tails"


def test_evt_gpd_var_and_es() -> None:
    losses = np.asarray(INST["losses"], dtype=np.float64)
    threshold = INST["threshold"]
    alpha = INST["alpha"]

    var_evt, es_evt, xi, beta = sol.evt_gpd_var_es(losses, threshold, alpha)

    assert isinstance(var_evt, float)
    assert isinstance(es_evt, float)
    assert isinstance(xi, float)
    assert isinstance(beta, float)

    assert beta > 0.0, f"GPD scale parameter beta must be positive, got {beta}"
    assert es_evt > var_evt, f"EVT ES ({es_evt:g}) must strictly exceed EVT VaR ({var_evt:g})"
    assert var_evt > threshold, f"EVT VaR ({var_evt:g}) must exceed the POT threshold ({threshold:g})"


def test_kupiec_pof_test() -> None:
    # 1. Null case: 2 exceptions out of 250 trading days at 99% confidence (nominal rate 1% -> 2.5 exceptions)
    lr_null, p_null, rej_null = sol.kupiec_pof_test(2, 250, 0.99)
    assert lr_null >= 0.0, "Likelihood ratio statistic must be non-negative"
    assert 0.0 <= p_null <= 1.0, "p-value must be in [0, 1]"
    assert not rej_null, f"Expected non-rejection of accurate model under H0, got p={p_null:g}"

    # 2. Reject case: 12 exceptions out of 250 trading days (nearly 5x the nominal rate)
    _lr_alt, p_alt, rej_alt = sol.kupiec_pof_test(12, 250, 0.99)
    assert rej_alt, f"Model with 12/250 exceptions must be rejected at 5% significance, got p={p_alt:g}"
    assert p_alt < 0.01, f"Severe failure rate must have p < 0.01, got {p_alt:g}"


def test_christoffersen_test() -> None:
    hits_iid = np.asarray(INST["hits_iid"], dtype=np.int64)
    hits_clustered = np.asarray(INST["hits_clustered"], dtype=np.int64)

    # Invariant: LR_cc = LR_uc + LR_ind exactly
    res_iid = sol.christoffersen_test(hits_iid, 0.99)
    lr_uc, _, lr_ind, _, lr_cc, _ = res_iid
    assert np.isclose(lr_cc, lr_uc + lr_ind, atol=1e-8), "LR_cc must equal LR_uc + LR_ind"

    # Clustered exceptions should lead to substantial independence LR statistic
    res_clust = sol.christoffersen_test(hits_clustered, 0.99)
    _lr_uc_c, _p_uc_c, lr_ind_c, p_ind_c, _lr_cc_c, _p_cc_c = res_clust

    assert lr_ind_c > 3.0, f"Clustered hits must produce substantial independence LR statistic, got {lr_ind_c:g}"
    assert p_ind_c < 0.10, f"Independence test must indicate clustering risk, got p_ind={p_ind_c:g}"


def test_stress_scenario_pnl() -> None:
    weights = np.asarray(INST["weights"], dtype=np.float64)
    shocks = np.asarray(INST["stress_shocks"], dtype=np.float64)
    pv = float(INST["portfolio_value"])

    pnl = sol.stress_scenario_pnl(weights, pv, shocks)
    assert isinstance(pnl, float)

    expected_pnl = pv * float(np.dot(weights, shocks))
    assert np.isclose(pnl, expected_pnl, atol=1e-4), "Stress P&L calculation does not match linear dot product"


def test_gaussian_copula_tail_metrics() -> None:
    corr = np.asarray(INST["corr_matrix"], dtype=np.float64)
    jp, tail_proxy = sol.gaussian_copula_tail_metrics(corr, threshold=0.95, n_sims=50000, seed=42)

    assert 0.0 <= jp <= 0.05, f"Joint exceedance probability at q=0.95 must be <= 0.05, got {jp}"
    assert 0.0 <= tail_proxy <= 1.0, f"Tail dependence proxy must be in [0, 1], got {tail_proxy}"
    # Under positive correlation, joint probability exceeds independent product (0.05 * 0.05 = 0.0025)
    assert jp > 0.0025, f"With positive correlation, joint exceedance must exceed independent level, got {jp}"


def test_input_validation() -> None:
    with pytest.raises(ValueError):
        sol.historical_var(np.array([1.0, 2.0]), 0.99)  # too short
    with pytest.raises(ValueError):
        sol.historical_var(np.array([1.0, 2.0, 3.0, 4.0, 5.0]), 1.5)  # invalid alpha
    with pytest.raises(ValueError):
        sol.parametric_student_t_var_es(np.array([1.0, 2.0, 3.0, 4.0, 5.0]), 0.99, df=2)  # invalid df <= 2
    with pytest.raises(ValueError):
        sol.kupiec_pof_test(10, 5, 0.99)  # exceptions > total_obs
    with pytest.raises(ValueError):
        sol.christoffersen_test(np.array([0, 1, 2, 0, 1]), 0.99)  # non-binary hits
