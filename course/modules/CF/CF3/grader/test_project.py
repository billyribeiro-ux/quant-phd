"""Acceptance test suite for CF3 project: Governance Scorecard (governance_scorecard.py).

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable
from typing import Any

import pytest
from governance_scorecard import (  # type: ignore[import-not-found, unused-ignore]
    compute_e_index,
    compute_g_index,
    compute_tobins_q,
    cross_sectional_ols,
    governance_regression,
    score_firm_panel,
    statistical_power_t_test,
)
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def _assert_close(a: float, b: float, tol: float = 1e-6, msg: str = "") -> None:
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


def _make_caller(p: dict[str, int]) -> Callable[[], Any]:
    return lambda: compute_e_index(p)


# 1. Test E-index boundary values and core provision counting
def test_e_index_all_zeros_and_ones() -> None:
    all_zeros = {k: 0 for k in INST["core_provisions"]}
    all_ones = {k: 1 for k in INST["core_provisions"]}
    assert compute_e_index(all_zeros) == 0
    assert compute_e_index(all_ones) == 6

    subset = {k: (1 if i % 2 == 0 else 0) for i, k in enumerate(INST["core_provisions"])}
    assert compute_e_index(subset) == 3


def test_e_index_missing_key_raises() -> None:
    for key in INST["core_provisions"]:
        provisions = {k: 1 for k in INST["core_provisions"] if k != key}
        _must_raise(_make_caller(provisions), f"missing key {key}")


def test_e_index_non_binary_value_raises() -> None:
    for bad_val in [-1, 2, 5]:
        provisions = {k: 1 for k in INST["core_provisions"]}
        provisions["poison_pill"] = bad_val
        _must_raise(_make_caller(provisions), f"non-binary value {bad_val}")


# 2. Test G-index counting and validation
def test_g_index_sum() -> None:
    sample = {"p1": 1, "p2": 0, "p3": 1, "p4": 1}
    assert compute_g_index(sample) == 3


def test_g_index_empty_or_invalid_raises() -> None:
    _must_raise(lambda: compute_g_index({}), "empty provisions dict")
    _must_raise(lambda: compute_g_index({"p1": 2}), "invalid provision value 2")


# 3. Test Tobin's Q calculation
def test_tobins_q_standard_calculation() -> None:
    # Assets: $1,000, Debt: $300, Book Equity: $700, Market Equity: $900
    # Q = (1,000 - 700 + 900) / 1,000 = 1,200 / 1,000 = 1.20
    q = compute_tobins_q(
        assets_cents=100_000_00,
        debt_cents=30_000_00,
        market_equity_cents=90_000_00,
        book_equity_cents=70_000_00,
    )
    _assert_close(q, 1.20, tol=1e-6, msg="Tobin's Q calculation")


def test_tobins_q_invalid_inputs_raise() -> None:
    _must_raise(
        lambda: compute_tobins_q(0, 30_000, 90_000, 70_000),
        "zero assets",
    )
    _must_raise(
        lambda: compute_tobins_q(-10_000, 30_000, 90_000, 70_000),
        "negative assets",
    )
    _must_raise(
        lambda: compute_tobins_q(100_000, -1, 90_000, 70_000),
        "negative debt",
    )
    _must_raise(
        lambda: compute_tobins_q(100_000, 30_000, 0, 70_000),
        "zero market equity",
    )


# 4. Test Bivariate OLS properties
def test_ols_recovers_known_linear_parameters() -> None:
    # y = 2.50 - 0.15 * x
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    y = [2.50 - 0.15 * xi for xi in x]
    res = cross_sectional_ols(x, y)
    _assert_close(res["alpha"], 2.50, tol=1e-6, msg="OLS intercept")
    _assert_close(res["beta"], -0.15, tol=1e-6, msg="OLS slope")
    _assert_close(res["r_squared"], 1.0, tol=1e-6, msg="OLS R^2 for exact line")
    _assert_close(res["rss"], 0.0, tol=1e-6, msg="OLS RSS for exact line")


def test_ols_bessel_correction_n_minus_2() -> None:
    # Distinct y values with known residuals
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.2, 1.8, 3.1, 3.9, 5.1]
    res = cross_sectional_ols(x, y)
    rss = res["rss"]
    expected_s2 = rss / (len(x) - 2)
    _assert_close(res["s_squared"], expected_s2, tol=1e-6, msg="Degrees of freedom n-2 normalization")


def test_ols_slope_sign() -> None:
    # Positive slope
    x = [1.0, 2.0, 3.0, 4.0]
    y = [2.0, 4.0, 6.0, 8.0]
    res = cross_sectional_ols(x, y)
    assert res["beta"] > 0.0, "Beta must be positive for positive relation"

    # Negative slope
    y_neg = [8.0, 6.0, 4.0, 2.0]
    res_neg = cross_sectional_ols(x, y_neg)
    assert res_neg["beta"] < 0.0, "Beta must be negative for negative relation"


def test_ols_invalid_inputs_raise() -> None:
    _must_raise(lambda: cross_sectional_ols([1.0, 2.0], [1.0, 2.0, 3.0]), "length mismatch")
    _must_raise(lambda: cross_sectional_ols([1.0, 2.0], [1.0, 2.0]), "too few observations (n < 3)")
    _must_raise(lambda: cross_sectional_ols([2.0, 2.0, 2.0, 2.0], [1.0, 2.0, 3.0, 4.0]), "zero variance in x")


# 5. Test statistical power calculations
def test_power_null_hypothesis() -> None:
    # When true_slope = 0, power should equal alpha_sig (0.05)
    power = statistical_power_t_test(n=10, true_slope=0.0, se_slope=0.05, alpha_sig=0.05)
    _assert_close(power, 0.05, tol=1e-3, msg="Power under H0 must equal alpha")


def test_power_large_effect() -> None:
    # When true_slope is 10 standard errors from 0, power should approach 1.0
    power = statistical_power_t_test(n=10, true_slope=0.50, se_slope=0.05, alpha_sig=0.05)
    assert power > 0.999, f"Power should approach 1.0 for t = 10, got {power}"


def test_power_two_sided_symmetry() -> None:
    # Two-sided power should be symmetric for beta and -beta
    p_pos = statistical_power_t_test(n=10, true_slope=0.10, se_slope=0.08, alpha_sig=0.05)
    p_neg = statistical_power_t_test(n=10, true_slope=-0.10, se_slope=0.08, alpha_sig=0.05)
    _assert_close(p_pos, p_neg, tol=1e-6, msg="Two-sided power must be symmetric in sign")


def test_power_invalid_inputs_raise() -> None:
    _must_raise(lambda: statistical_power_t_test(n=2, true_slope=0.1, se_slope=0.05), "n < 3")
    _must_raise(lambda: statistical_power_t_test(n=10, true_slope=0.1, se_slope=0.0), "se_slope <= 0")
    _must_raise(lambda: statistical_power_t_test(n=10, true_slope=0.1, se_slope=0.05, alpha_sig=0.0), "alpha <= 0")
    _must_raise(lambda: statistical_power_t_test(n=10, true_slope=0.1, se_slope=0.05, alpha_sig=1.0), "alpha >= 1")


# 6. Test panel scoring and full pipeline
def test_score_firm_panel_seeded_instance() -> None:
    raw_firms = INST["firms"]
    scored = score_firm_panel(raw_firms)
    assert len(scored) == len(raw_firms)
    for firm in scored:
        assert "e_index" in firm
        assert "g_index" in firm
        assert "tobins_q" in firm
        assert 0 <= firm["e_index"] <= 6
        assert 0 <= firm["g_index"] <= len(INST["all_provisions"])
        assert firm["tobins_q"] > 0.5


def test_governance_regression_seeded_instance() -> None:
    scored = score_firm_panel(INST["firms"])
    reg_e = governance_regression(scored, index_key="e_index")
    reg_g = governance_regression(scored, index_key="g_index")

    for reg in (reg_e, reg_g):
        assert "alpha" in reg
        assert "beta" in reg
        assert "se_beta" in reg
        assert "t_stat" in reg
        assert "r_squared" in reg
        assert "power" in reg
        assert 0.0 <= reg["power"] <= 1.0
        assert 0.0 <= reg["r_squared"] <= 1.0
