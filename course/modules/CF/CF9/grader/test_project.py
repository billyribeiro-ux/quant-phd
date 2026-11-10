"""Acceptance test suite for CF9 Corporate Hedging Program project.

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    compute_cfar,
    compute_net_transaction_exposure,
    compute_usd_exposure,
    cross_border_npv,
    evaluate_hedge_effectiveness,
    hedge_accounting_test,
    minimum_variance_hedge_ratio,
    portfolio_cash_flow_variance,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def _assert_close(a: float, b: float, tol: float = 1e-5, msg: str = "") -> None:
    __tracebackhide__ = True
    if not math.isfinite(a) or abs(a - b) > tol:
        pytest.fail(f"Value mismatch: {msg} got {a} expected {b}")


def _must_raise(func: Callable[[], Any], condition_name: str) -> None:
    __tracebackhide__ = True
    try:
        func()
    except ValueError:
        return
    pytest.fail(f"Failed to raise ValueError for invalid condition: {condition_name}")


# 1. Transaction exposure tests
def test_net_transaction_exposure_calculation() -> None:
    rec = {"EUR": 30.0, "JPY": 3000.0, "GBP": 20.0}
    pay = {"EUR": 10.0, "JPY": 1000.0, "GBP": 5.0}
    net = compute_net_transaction_exposure(rec, pay)
    assert net["EUR"] == 20.0
    assert net["JPY"] == 2000.0
    assert net["GBP"] == 15.0


def test_net_transaction_exposure_validation() -> None:
    _must_raise(lambda: compute_net_transaction_exposure({}, {}), "empty dicts")
    _must_raise(
        lambda: compute_net_transaction_exposure({"EUR": 10.0}, {"JPY": 5.0}),
        "mismatched currency keys",
    )
    _must_raise(
        lambda: compute_net_transaction_exposure({"EUR": -5.0}, {"EUR": 5.0}),
        "negative cash flow",
    )


def test_usd_exposure_translation() -> None:
    net_fc = {"EUR": 10.0, "JPY": 1000.0}
    spots = {"EUR": 1.10, "JPY": 0.0070}
    usd_exp = compute_usd_exposure(net_fc, spots)
    _assert_close(usd_exp["EUR"], 11.0, tol=1e-5, msg="EUR USD translation")
    _assert_close(usd_exp["JPY"], 7.0, tol=1e-5, msg="JPY USD translation")

    _must_raise(lambda: compute_usd_exposure(net_fc, {"EUR": -1.10, "JPY": 0.007}), "negative spot")
    _must_raise(lambda: compute_usd_exposure(net_fc, {"EUR": 1.10}), "missing spot currency")


# 2. Minimum-variance hedge ratio tests
def test_minimum_variance_hedge_ratio_formula() -> None:
    # h* = Cov / Var
    h = minimum_variance_hedge_ratio(cov_cf_f=12.0, var_f=16.0)
    _assert_close(h, 0.75, tol=1e-6, msg="Minimum-variance hedge ratio")

    # Negative covariance implies negative hedge ratio (long futures)
    h_neg = minimum_variance_hedge_ratio(cov_cf_f=-8.0, var_f=16.0)
    _assert_close(h_neg, -0.50, tol=1e-6, msg="Negative hedge ratio")


def test_minimum_variance_hedge_ratio_validation() -> None:
    _must_raise(lambda: minimum_variance_hedge_ratio(10.0, 0.0), "zero futures variance")
    _must_raise(lambda: minimum_variance_hedge_ratio(10.0, -4.0), "negative futures variance")


# 3. Portfolio variance and covariance tests
def test_portfolio_cash_flow_variance_formula() -> None:
    w = [10.0, 20.0]
    # Covariance matrix: [ [0.04, 0.02], [0.02, 0.09] ]
    cov = [[0.04, 0.02], [0.02, 0.09]]
    # Var = 10^2 * 0.04 + 20^2 * 0.09 + 2 * 10 * 20 * 0.02 = 4 + 36 + 8 = 48.0
    var = portfolio_cash_flow_variance(w, cov)
    _assert_close(var, 48.0, tol=1e-6, msg="Portfolio cash flow variance")


def test_portfolio_variance_covariance_sensitivity() -> None:
    # Test that off-diagonal covariance is strictly included (kills mutant omitting cov)
    w = [10.0, 10.0]
    cov_uncorr = [[0.04, 0.0], [0.0, 0.04]]
    cov_corr = [[0.04, 0.03], [0.03, 0.04]]

    var_uncorr = portfolio_cash_flow_variance(w, cov_uncorr)
    var_corr = portfolio_cash_flow_variance(w, cov_corr)
    # Correlation must strictly increase portfolio variance for positive weights
    assert var_corr > var_uncorr + 5.0, "Portfolio variance must incorporate cross-currency covariance"


def test_portfolio_variance_dimension_mismatch() -> None:
    _must_raise(lambda: portfolio_cash_flow_variance([1.0, 2.0], [[1.0]]), "dimension mismatch")
    _must_raise(lambda: portfolio_cash_flow_variance([], []), "empty exposure list")


# 4. Cash-Flow-at-Risk (CFaR) tests
def test_cfar_calculation() -> None:
    mean_cf = 100.0
    std_cf = 20.0
    # 95% confidence -> z = 1.644853
    res = compute_cfar(mean_cf=mean_cf, std_cf=std_cf, alpha=0.05, hurdle=65.0)
    expected_cfar = 1.6448536269514722 * 20.0
    _assert_close(res["cfar"], expected_cfar, tol=1e-4, msg="95% CFaR amount")
    _assert_close(res["worst_case_cf"], mean_cf - expected_cfar, tol=1e-4, msg="Worst case CF")

    # Shortfall prob below hurdle 65: z = (65 - 100) / 20 = -1.75
    # Normal cdf(-1.75) ~ 0.040059
    _assert_close(res["prob_shortfall"], 0.040059, tol=1e-3, msg="Shortfall probability")


def test_cfar_validation() -> None:
    _must_raise(lambda: compute_cfar(100.0, -5.0), "negative std_cf")
    _must_raise(lambda: compute_cfar(100.0, 10.0, alpha=0.0), "alpha zero")
    _must_raise(lambda: compute_cfar(100.0, 10.0, alpha=0.6), "alpha >= 0.5")


# 5. Hedge effectiveness tests
def test_hedge_effectiveness_bounds() -> None:
    # 50% variance reduction
    he = evaluate_hedge_effectiveness(var_unhedged=100.0, var_hedged=50.0)
    _assert_close(he, 0.50, tol=1e-6, msg="50% hedge effectiveness")

    # Perfect hedge
    he_perfect = evaluate_hedge_effectiveness(var_unhedged=100.0, var_hedged=0.0)
    _assert_close(he_perfect, 1.0, tol=1e-6, msg="100% hedge effectiveness")


def test_hedge_effectiveness_validation() -> None:
    _must_raise(lambda: evaluate_hedge_effectiveness(0.0, 10.0), "zero unhedged variance")
    _must_raise(lambda: evaluate_hedge_effectiveness(100.0, -5.0), "negative hedged variance")


# 6. Hedge accounting compliance tests (ASC 815 / IFRS 9)
def test_hedge_accounting_corridor() -> None:
    # Within 80% to 125%
    h_80 = hedge_accounting_test(delta_derivative=8.0, delta_exposure=-10.0)
    assert h_80["is_qualified"] is True
    _assert_close(float(h_80["dollar_offset_ratio"]), 0.80, tol=1e-6)

    h_125 = hedge_accounting_test(delta_derivative=12.5, delta_exposure=-10.0)
    assert h_125["is_qualified"] is True
    _assert_close(float(h_125["dollar_offset_ratio"]), 1.25, tol=1e-6)

    # Outside corridor (< 0.80 or > 1.25)
    h_79 = hedge_accounting_test(delta_derivative=7.9, delta_exposure=-10.0)
    assert h_79["is_qualified"] is False

    h_126 = hedge_accounting_test(delta_derivative=12.6, delta_exposure=-10.0)
    assert h_126["is_qualified"] is False


def test_hedge_accounting_validation() -> None:
    _must_raise(lambda: hedge_accounting_test(10.0, 0.0), "zero delta exposure")


# 7. Cross-border capital budgeting tests
def test_cross_border_npv_method_equivalence() -> None:
    initial_fc = 50.0
    cfs_fc = [15.0, 20.0, 25.0, 20.0]
    s0 = 1.10
    wacc_home = 0.10
    r_home = 0.05
    r_foreign = 0.03

    npv_foreign = cross_border_npv(
        initial_outlay_foreign=initial_fc,
        foreign_cfs=cfs_fc,
        spot_fx=s0,
        wacc_home=wacc_home,
        r_home=r_home,
        r_foreign=r_foreign,
        method="foreign",
    )
    npv_home = cross_border_npv(
        initial_outlay_foreign=initial_fc,
        foreign_cfs=cfs_fc,
        spot_fx=s0,
        wacc_home=wacc_home,
        r_home=r_home,
        r_foreign=r_foreign,
        method="home",
    )

    _assert_close(npv_foreign, npv_home, tol=1e-5, msg="Foreign and Home currency NPV parity equivalence")
    assert npv_foreign > 0.0, "Project NPV must be positive"


def test_cross_border_npv_validation() -> None:
    _must_raise(lambda: cross_border_npv(50.0, [10.0], -1.10, 0.10, 0.05, 0.03), "negative spot rate")
    _must_raise(lambda: cross_border_npv(50.0, [10.0], 1.10, -1.2, 0.05, 0.03), "invalid discount rate")
    _must_raise(
        lambda: cross_border_npv(50.0, [10.0], 1.10, 0.10, 0.05, 0.03, method="invalid"),
        "invalid method string",
    )


# 8. Full seeded instance test
def test_seeded_instance_pipeline() -> None:
    currencies = INST["currencies"]
    rec = dict(zip(currencies, INST["receivables"], strict=True))
    pay = dict(zip(currencies, INST["payables"], strict=True))
    spots = dict(zip(currencies, INST["spot_rates"], strict=True))
    cov_matrix = INST["covariance_matrix"]

    net_fc = compute_net_transaction_exposure(rec, pay)
    usd_exp = compute_usd_exposure(net_fc, spots)

    exp_vector = [usd_exp[c] for c in currencies]

    total_var = portfolio_cash_flow_variance(exp_vector, cov_matrix)
    std_cf = math.sqrt(total_var)
    mean_cf = sum(exp_vector) - INST["domestic_costs_usd"]

    cfar_res = compute_cfar(mean_cf=mean_cf, std_cf=std_cf, alpha=0.05, hurdle=INST["hurdle_cash_flow"])

    assert total_var > 0.0
    assert cfar_res["cfar"] > 0.0
    assert 0.0 <= cfar_res["prob_shortfall"] <= 1.0

    ha_res = hedge_accounting_test(
        delta_derivative=INST["delta_derivative"],
        delta_exposure=INST["delta_exposure"],
    )
    assert isinstance(ha_res["is_qualified"], bool)

    npv_f = cross_border_npv(
        initial_outlay_foreign=INST["initial_outlay_eur"],
        foreign_cfs=INST["project_cfs_eur"],
        spot_fx=spots["EUR"],
        wacc_home=INST["wacc_usd"],
        r_home=INST["r_usd"],
        r_foreign=INST["r_eur"],
        method="foreign",
    )
    npv_h = cross_border_npv(
        initial_outlay_foreign=INST["initial_outlay_eur"],
        foreign_cfs=INST["project_cfs_eur"],
        spot_fx=spots["EUR"],
        wacc_home=INST["wacc_usd"],
        r_home=INST["r_usd"],
        r_foreign=INST["r_eur"],
        method="home",
    )
    _assert_close(npv_f, npv_h, tol=1e-4, msg="Seeded instance cross-border NPV parity")
