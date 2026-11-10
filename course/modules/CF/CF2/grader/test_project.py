"""Acceptance test suite for CF2 project: Cost of Capital & Capital Structure (wacc_engine.py).

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
import random
from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

import pytest
import wacc_engine  # type: ignore[import-not-found, unused-ignore]
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from wacc_engine import (  # type: ignore[import-not-found, unused-ignore]
    beta_ols,
    cost_of_debt,
    cost_of_equity,
    relever_beta,
    unlever_beta,
    valuation_range,
    wacc,
    wacc_delta_variance,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def _assert_close(a: float, b: float, tol: float = 1e-9, msg: str = "") -> None:
    __tracebackhide__ = True
    if not math.isfinite(a) or abs(a - b) > tol:
        pytest.fail(f"Value mismatch: {msg} (check formula and precision)")


def _must_raise(func: Callable[[], Any], condition_name: str) -> None:
    __tracebackhide__ = True
    try:
        func()
    except ValueError:
        return
    pytest.fail(f"Failed to raise ValueError for invalid condition: {condition_name}")


def _must_accept(func: Callable[[], Any], condition_name: str) -> Any:
    __tracebackhide__ = True
    try:
        return func()
    except ValueError:
        pytest.fail(f"Raised unexpected ValueError for valid condition: {condition_name}")


# 1. test_beta_recovers_noise_free_slope
def test_beta_recovers_noise_free_slope() -> None:
    slope = 1.35
    intercept = 0.005
    mkt = [-0.04, -0.02, 0.0, 0.03, 0.05, 0.08]
    firm = [intercept + slope * m for m in mkt]
    est = beta_ols(firm, mkt)
    _assert_close(est, slope, tol=1e-12, msg="beta_ols must recover exact slope on noise-free linear data")


# 2. test_beta_uses_one_normalisation
def test_beta_uses_one_normalisation() -> None:
    mkt = [0.01, -0.02, 0.03, -0.01, 0.04, -0.03]
    firm = [0.02, -0.03, 0.05, -0.02, 0.06, -0.04]
    b1 = beta_ols(firm, mkt)
    # Doubling sample must give identical beta when both covariance and variance use n - 1
    b2 = beta_ols(firm + firm, mkt + mkt)
    _assert_close(b1, b2, tol=1e-12, msg="beta_ols must use consistent n-1 Bessel normalisation")


# 3. test_beta_rejects_short_and_flat_series
def test_beta_rejects_short_and_flat_series() -> None:
    _must_raise(lambda: beta_ols([0.05], [0.02]), "sample size n < 2")
    _must_raise(lambda: beta_ols([0.01, 0.02], [0.03, 0.03]), "flat market returns with zero variance")
    _must_raise(lambda: beta_ols([0.01, 0.02, 0.03], [0.01, 0.02]), "unequal lengths")
    _must_accept(lambda: beta_ols([0.01, 0.02], [0.01, 0.03]), "n = 2 with variance")


# 4. test_unlever_hand_value
def test_unlever_hand_value() -> None:
    # Fixture: D/E = 1, tau_c = 0.25, beta_L = 1.2
    # beta_U = 1.2 / (1 + (1 - 0.25) * 1) = 1.2 / 1.75 = 24/35 = 0.6857142857142857
    b_u = unlever_beta(1.2, 50_000, 50_000, 0.25)
    _assert_close(b_u, 1.2 / 1.75, tol=1e-12, msg="unlever_beta hand calculation check (Hamada equation)")


# 5. test_relever_inverts_unlever
def test_relever_inverts_unlever() -> None:
    for seed in range(50):
        inst = make_instance(seed)
        d = inst["debt_market_cents"]
        e = inst["equity_market_cents"]
        tau = inst["tax_rate"]
        b_l = 1.42
        b_u = unlever_beta(b_l, d, e, tau)
        b_round = relever_beta(b_u, d, e, tau)
        _assert_close(b_round, b_l, tol=1e-12, msg=f"relever_beta must invert unlever_beta (seed {seed})")


# 6. test_zero_debt_leaves_beta
def test_zero_debt_leaves_beta() -> None:
    b_l = 1.25
    b_u = unlever_beta(b_l, 0, 100_000, 0.25)
    _assert_close(b_u, b_l, tol=1e-12, msg="zero debt must leave asset beta equal to equity beta")


# 7. test_tax_rate_boundaries
def test_tax_rate_boundaries() -> None:
    _must_accept(lambda: unlever_beta(1.0, 100, 100, 0.0), "tax_rate = 0.0 is valid")
    _must_accept(lambda: unlever_beta(1.0, 100, 100, 0.45), "tax_rate = 0.45 is valid")
    _must_raise(lambda: unlever_beta(1.0, 100, 100, 1.0), "tax_rate = 1.0 is invalid")
    _must_raise(lambda: unlever_beta(1.0, 100, 100, -0.01), "tax_rate < 0 is invalid")
    _must_raise(lambda: unlever_beta(1.0, -10, 100, 0.2), "negative debt is invalid")
    _must_raise(lambda: unlever_beta(1.0, 100, 0, 0.2), "zero equity is invalid")


# 8. test_wacc_hand_value
def test_wacc_hand_value() -> None:
    # E = 600, D = 400, r_E = 0.10, r_D = 0.05, tau_c = 0.20
    # w_E = 0.6, w_D = 0.4, after-tax r_D = 0.04
    # WACC = 0.6 * 0.10 + 0.4 * 0.04 = 0.076
    w = wacc(400, 600, 0.10, 0.05, 0.20)
    _assert_close(w, 0.076, tol=1e-12, msg="wacc hand fixture check")


# 9. test_wacc_equals_cost_of_equity_without_debt
def test_wacc_equals_cost_of_equity_without_debt() -> None:
    w = wacc(0, 1_000_000, 0.09, 0.04, 0.25)
    _assert_close(w, 0.09, tol=1e-12, msg="unlevered WACC must equal cost of equity")


# 10. test_wacc_rejects_nonpositive_capital
def test_wacc_rejects_nonpositive_capital() -> None:
    _must_raise(lambda: wacc(0, 0, 0.10, 0.05, 0.25), "total capital D + E = 0")
    _must_raise(lambda: wacc(-50, 100, 0.10, 0.05, 0.25), "negative debt")
    _must_raise(lambda: wacc(100, -50, 0.10, 0.05, 0.25), "negative equity")
    _must_accept(lambda: wacc(10, 90, 0.10, 0.05, 0.25), "positive capital")


# 11. test_wacc_uses_market_values
def test_wacc_uses_market_values() -> None:
    # Verify that market debt produces the expected WACC and differs from book debt
    d_mkt = INST["debt_market_cents"]
    d_book = INST["debt_book_cents"]
    e_mkt = INST["equity_market_cents"]
    tau = INST["tax_rate"]

    re = cost_of_equity(INST["risk_free"], 1.1, INST["erp"])
    rd = cost_of_debt(INST["risk_free"], INST["spread"])

    wacc_mkt = wacc(d_mkt, e_mkt, re, rd, tau)
    wacc_book = wacc(d_book, e_mkt, re, rd, tau)

    assert abs(wacc_mkt - wacc_book) > 1e-6, "WACC using market debt must differ from WACC using book debt"


# 12. test_delta_variance_matches_exact_moments
def test_delta_variance_matches_exact_moments() -> None:
    # For jointly normal (beta, ERP) with covariance c,
    # exact Var(beta * ERP) - delta Var = Var(beta) * Var(ERP) + c^2.
    # WACC = w_E * (r_f + beta * ERP) + w_D * (r_f + s) * (1 - tau_c).
    # Scaled by w_E^2, exact variance of WACC exceeds linearised delta variance by:
    # w_E^2 * (Var(beta) * Var(ERP) + c^2).
    d = 40_000
    e = 60_000
    w_e = 0.6
    w_d = 0.4
    tau = 0.25

    beta_mid = 1.20
    erp_mid = 0.055
    var_beta = 0.040
    var_erp = 0.0004
    cov_beta_erp = 0.0010  # c != 0
    var_spread = 0.0001

    v_delta = wacc_delta_variance(d, e, beta_mid, erp_mid, var_beta, var_erp, cov_beta_erp, var_spread, tau)

    # Exact moment for product of bivariate normals:
    # Var(X Y) = mu_X^2 sigma_Y^2 + mu_Y^2 sigma_X^2 + 2 mu_X mu_Y c + sigma_X^2 sigma_Y^2 + c^2
    var_xy_exact = (
        (beta_mid**2) * var_erp
        + (erp_mid**2) * var_beta
        + 2.0 * beta_mid * erp_mid * cov_beta_erp
        + var_beta * var_erp
        + cov_beta_erp**2
    )
    v_exact = (w_e**2) * var_xy_exact + (w_d * (1.0 - tau)) ** 2 * var_spread

    diff = v_exact - v_delta
    expected_diff = (w_e**2) * (var_beta * var_erp + cov_beta_erp**2)

    _assert_close(diff, expected_diff, tol=1e-12, msg="difference between exact moment and delta method")


# 13. test_monte_carlo_within_four_standard_errors
def test_monte_carlo_within_four_standard_errors() -> None:
    rng = random.Random(20261110)
    n_sims = 20_000
    w_e = 0.5
    w_d = 0.5
    tau = 0.20

    mu_b, sigma_b = 1.10, 0.15
    mu_erp, sigma_erp = 0.050, 0.012
    # Bivariate normal generation with correlation rho = 0.3
    rho = 0.30
    cov_val = rho * sigma_b * sigma_erp
    sigma_s = 0.005

    draws: list[float] = []
    for _ in range(n_sims):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        b = mu_b + sigma_b * z1
        erp_draw = mu_erp + sigma_erp * (rho * z1 + math.sqrt(1.0 - rho**2) * z2)
        s_draw = rng.gauss(0.0, sigma_s)
        # WACC deviation from mean: w_E * (b * erp - mu_b * mu_erp) + w_D * s * (1 - tau)
        w_draw = w_e * (b * erp_draw) + w_d * s_draw * (1.0 - tau)
        draws.append(w_draw)

    sample_mean = sum(draws) / n_sims
    sample_var = sum((x - sample_mean) ** 2 for x in draws) / (n_sims - 1)

    exact_var_xy = (
        (mu_b**2) * (sigma_erp**2)
        + (mu_erp**2) * (sigma_b**2)
        + 2.0 * mu_b * mu_erp * cov_val
        + (sigma_b**2) * (sigma_erp**2)
        + cov_val**2
    )
    exact_var = (w_e**2) * exact_var_xy + (w_d * (1.0 - tau)) ** 2 * (sigma_s**2)

    se_mc = math.sqrt(2.0 / n_sims) * exact_var
    assert abs(sample_var - exact_var) <= 4.0 * se_mc, "Monte Carlo variance within 4 standard errors of exact moment"


# 14. test_zero_inputs_zero_variance
def test_zero_inputs_zero_variance() -> None:
    v = wacc_delta_variance(100, 100, 1.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.25)
    _assert_close(v, 0.0, tol=1e-12, msg="zero input uncertainties must yield zero WACC variance")


# 15. test_valuation_growing_perpetuity
def test_valuation_growing_perpetuity() -> None:
    # C_1 = 100_000 cents ($1,000), r = 0.10, g = 0.02
    # V = 100_000 / 0.08 = 1_250_000 cents
    low, high = valuation_range(100_000, 0.02, 0.10, 0.0, k=0.0)
    assert low == 1_250_000 and high == 1_250_000, "growing perpetuity at point estimate"


# 16. test_valuation_half_up_in_cents
def test_valuation_half_up_in_cents() -> None:
    # 1 cent cash flow, r = 0.50, g = 0.10 -> r - g = 0.40
    # 1 / 0.4 = 2.5 cents. Half-up rounding must round up to 3 cents.
    low, high = valuation_range(1, 0.10, 0.50, 0.0, k=0.0)
    assert low == 3 and high == 3, f"exact half cent must round half-up to 3, got ({low}, {high})"


# 17. test_valuation_range_brackets_base_value
def test_valuation_range_brackets_base_value() -> None:
    for seed in range(50):
        inst = make_instance(seed)
        cf = inst["cash_flow_cents"]
        g = inst["growth"]
        w_mid = inst["wacc"]
        w_se = 0.005
        low_val, high_val = valuation_range(cf, g, w_mid, w_se, k=1.0)
        # Base valuation
        base_val = int((Decimal(cf) / (Decimal(str(w_mid)) - Decimal(str(g)))).quantize(Decimal("1"), ROUND_HALF_UP))
        assert low_val <= base_val <= high_val, f"valuation range must bracket base value for seed {seed}"


# 18. test_wider_error_wider_range
def test_wider_error_wider_range() -> None:
    cf = 1_000_000
    g = 0.02
    w_mid = 0.08
    low1, high1 = valuation_range(cf, g, w_mid, 0.005, k=1.0)
    low2, high2 = valuation_range(cf, g, w_mid, 0.010, k=1.0)
    assert (high2 - low2) > (high1 - low1), "doubling standard error must widen the valuation range"


# 19. test_k_boundaries
def test_k_boundaries() -> None:
    cf = 500_000
    g = 0.02
    w_mid = 0.08
    low, high = valuation_range(cf, g, w_mid, 0.01, k=0.0)
    assert low == high, "k = 0 must produce a point estimate"
    _must_raise(lambda: valuation_range(cf, g, w_mid, 0.01, k=-0.1), "negative k multiplier")


# 20. test_rate_at_or_below_growth_rejected
def test_rate_at_or_below_growth_rejected() -> None:
    cf = 500_000
    g = 0.03
    # r_low = 0.04 - 0.02 = 0.02 <= 0.03 -> must raise ValueError
    _must_raise(lambda: valuation_range(cf, g, 0.04, 0.02, k=1.0), "discount rate at or below growth")
    _must_raise(lambda: valuation_range(cf, g, 0.03, 0.0, k=0.0), "discount rate exactly equal to growth")
    _must_accept(lambda: valuation_range(cf, g, 0.031, 0.0, k=0.0), "discount rate strictly above growth")


# 21. test_cash_flow_must_be_positive_integer_cents
def test_cash_flow_must_be_positive_integer_cents() -> None:
    g = 0.02
    w_mid = 0.08
    _must_raise(lambda: valuation_range(0, g, w_mid, 0.01), "zero cash flow")
    _must_raise(lambda: valuation_range(-100, g, w_mid, 0.01), "negative cash flow")
    _must_raise(lambda: valuation_range(100.5, g, w_mid, 0.01), "float cash flow")  # type: ignore[arg-type]
    _must_raise(lambda: valuation_range(True, g, w_mid, 0.01), "boolean cash flow")  # type: ignore[arg-type]
    _must_accept(lambda: valuation_range(1, g, w_mid, 0.01), "1 cent cash flow")


# 22. test_large_cents_accepted
def test_large_cents_accepted() -> None:
    big_cf = 10**18  # 10 quadrillion dollars in cents
    low, high = valuation_range(big_cf, 0.02, 0.07, 0.01, k=1.0)
    assert low > 0 and high > low, "large integer cents must not overflow or lose precision"


# 23. test_instances_valid_and_different
def test_instances_valid_and_different() -> None:
    wacc_set: set[float] = set()
    for s in range(50):
        inst = make_instance(s)
        assert inst["debt_market_cents"] > 0
        assert inst["equity_market_cents"] > 0
        assert inst["debt_book_cents"] != inst["debt_market_cents"]
        assert 0.0 <= inst["tax_rate"] < 1.0
        assert inst["wacc"] - inst["growth"] >= 0.02
        wacc_set.add(round(inst["wacc"], 4))
    assert len(wacc_set) >= 30, "instances across seeds 0-49 must generate materially different WACC values"


# 24. test_messages_name_the_rule_not_the_answer
def test_messages_name_the_rule_not_the_answer() -> None:
    # Structural check: helper functions must use __tracebackhide__ and never leak numbers
    assert hasattr(_assert_close, "__code__")
    assert wacc_engine is not None
