"""Acceptance test suite for PR3 Growth-Optimal Sizing autograded project.

Tests property invariants, closed-form formulas, KKT and stationary conditions,
estimation shrinkage under parameter uncertainty, and drawdown control.
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance
from sizing import (
    binary_kelly,
    continuous_kelly,
    drawdown_constrained_multiplier,
    drawdown_probability,
    growth_rate,
    multivariate_kelly,
    optimal_shrinkage_factor,
    simulate_wealth,
    sizing_policy,
)

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_binary_kelly_properties() -> None:
    p = INST["p"]
    b = INST["b"]
    f = binary_kelly(p, b)

    assert isinstance(f, float), "binary_kelly must return a float"
    assert 0.0 <= f <= 1.0, f"Binary Kelly fraction must lie in [0, 1], got {f}"

    expected = max(0.0, (b * p - (1.0 - p)) / b)
    assert math.isclose(f, expected, rel_tol=1e-7, abs_tol=1e-7), (
        f"binary_kelly({p}, {b})={f} did not match expected {expected}"
    )

    # Edge cases
    assert binary_kelly(0.4, 1.0) == 0.0, "Negative edge bet must return 0.0"
    assert binary_kelly(1.0, 2.0) == 1.0, "Certain win must return 1.0"
    # Specific known value: p=0.6, b=2.0 -> (1.2 - 0.4)/2 = 0.40
    assert math.isclose(binary_kelly(0.6, 2.0), 0.40, abs_tol=1e-7), (
        "binary_kelly(0.6, 2.0) must be 0.40 (checks denominator is b, not b+1)"
    )

    with pytest.raises(ValueError):
        binary_kelly(-0.1, 1.0)
    with pytest.raises(ValueError):
        binary_kelly(1.1, 1.0)
    with pytest.raises(ValueError):
        binary_kelly(0.5, 0.0)


def test_continuous_kelly_properties() -> None:
    mu = INST["mu"]
    r = INST["r"]
    sigma = INST["sigma"]
    f_star = continuous_kelly(mu, r, sigma)

    assert isinstance(f_star, float), "continuous_kelly must return a float"
    expected = (mu - r) / (sigma**2)
    assert math.isclose(f_star, expected, rel_tol=1e-7, abs_tol=1e-7)

    # Invariant: doubling volatility must reduce leverage by a factor of 4 (quadratic scaling)
    f_double_vol = continuous_kelly(mu, r, 2.0 * sigma)
    assert math.isclose(f_double_vol, f_star / 4.0, rel_tol=1e-6), (
        "continuous_kelly must scale inversely with sigma^2, not linear sigma"
    )

    with pytest.raises(ValueError):
        continuous_kelly(mu, r, 0.0)
    with pytest.raises(ValueError):
        continuous_kelly(mu, r, -0.1)


def test_multivariate_kelly_properties() -> None:
    mu = np.array(INST["mu_vec"], dtype=np.float64)
    r = INST["r"]
    cov = np.array(INST["cov_mat"], dtype=np.float64)

    w = multivariate_kelly(mu, r, cov)
    assert isinstance(w, np.ndarray), "multivariate_kelly must return an ndarray"
    assert w.shape == (len(mu),), "multivariate_kelly output shape mismatch"

    # Invariant: Sigma * w* == mu - r * 1 (Euler first-order optimality condition)
    excess_mu = mu - r
    cov_w = cov @ w
    assert np.allclose(cov_w, excess_mu, atol=1e-6), (
        "Multivariate Kelly weights must satisfy the first-order condition Sigma * w* = mu - r"
    )


def test_growth_rate_properties() -> None:
    mu = INST["mu"]
    r = INST["r"]
    sigma = INST["sigma"]
    f_star = continuous_kelly(mu, r, sigma)

    # Invariant 1: Zero allocation yields risk-free growth rate
    assert math.isclose(growth_rate(0.0, mu, r, sigma), r, abs_tol=1e-9)

    # Invariant 2: Growth rate is maximized at f_star
    g_opt = growth_rate(f_star, mu, r, sigma)
    g_sub = growth_rate(0.9 * f_star, mu, r, sigma)
    g_sup = growth_rate(1.1 * f_star, mu, r, sigma)
    assert g_opt > g_sub, "f_star must achieve strictly higher growth rate than 0.9 * f_star"
    assert g_opt > g_sup, "f_star must achieve strictly higher growth rate than 1.1 * f_star"

    # Invariant 3: Double Kelly yields zero excess growth (g(2*f*) == r)
    g_double = growth_rate(2.0 * f_star, mu, r, sigma)
    assert math.isclose(g_double, r, rel_tol=1e-6, abs_tol=1e-7), (
        "Double Kelly must yield zero excess growth rate above risk-free rate"
    )

    # Invariant 4: Half Kelly yields exactly 75% of maximum excess growth
    g_half = growth_rate(0.5 * f_star, mu, r, sigma)
    excess_opt = g_opt - r
    excess_half = g_half - r
    assert math.isclose(excess_half, 0.75 * excess_opt, rel_tol=1e-6), (
        "Half-Kelly must capture exactly 75% of optimal excess growth rate"
    )


def test_drawdown_probability_properties() -> None:
    # Closed form check for half-Kelly (c = 0.5) and 50% drawdown (d = 0.5):
    # exponent = 2/0.5 - 1 = 3 -> (1 - 0.5)^3 = 0.125
    p_half = drawdown_probability(0.5, 0.5)
    assert math.isclose(p_half, 0.125, abs_tol=1e-7), f"Drawdown prob for c=0.5, d=0.5 must be 0.125, got {p_half}"

    # Full Kelly (c = 1.0): exponent = 2/1 - 1 = 1 -> (1 - d)^1 = 1 - d
    p_full = drawdown_probability(1.0, 0.3)
    assert math.isclose(p_full, 0.70, abs_tol=1e-7), f"Drawdown prob for c=1.0, d=0.3 must be 0.70, got {p_full}"

    # Overbetting (c >= 2.0) guarantees 100% drawdown probability
    assert drawdown_probability(2.0, 0.5) == 1.0
    assert drawdown_probability(2.5, 0.2) == 1.0
    assert drawdown_probability(0.0, 0.5) == 0.0

    with pytest.raises(ValueError):
        drawdown_probability(0.5, 0.0)
    with pytest.raises(ValueError):
        drawdown_probability(0.5, 1.0)


def test_optimal_shrinkage_factor_properties() -> None:
    t_obs = INST["t_obs"]
    excess = INST["mu"] - INST["r"]
    sharpe = excess / INST["sigma"]

    alpha = optimal_shrinkage_factor(sharpe, t_obs)
    assert 0.0 < alpha < 1.0, f"alpha* must be strictly in (0, 1), got {alpha}"

    # Asymptotic behavior
    alpha_inf = optimal_shrinkage_factor(sharpe, 10_000_000)
    assert math.isclose(alpha_inf, 1.0, abs_tol=1e-4), "alpha* must approach 1.0 as sample size approaches infinity"

    alpha_small = optimal_shrinkage_factor(sharpe, 5)
    assert alpha_small < alpha, "alpha* must be smaller for smaller sample sizes"

    assert optimal_shrinkage_factor(0.0, t_obs) == 0.0, "Zero Sharpe must yield zero allocation"
    with pytest.raises(ValueError):
        optimal_shrinkage_factor(sharpe, 0)


def test_drawdown_constrained_multiplier_accuracy() -> None:
    max_d = INST["max_drawdown"]
    max_p = INST["max_drawdown_prob"]

    c_dd = drawdown_constrained_multiplier(max_d, max_p)
    assert 0.0 < c_dd < 2.0, f"c_dd must lie in (0, 2), got {c_dd}"

    # Verify that drawdown_probability(c_dd, max_d) exactly matches max_p
    implied_prob = drawdown_probability(c_dd, max_d)
    assert math.isclose(implied_prob, max_p, rel_tol=1e-6, abs_tol=1e-7), (
        f"Drawdown probability at c_dd must equal max_p: got {implied_prob}, expected {max_p}"
    )

    with pytest.raises(ValueError):
        drawdown_constrained_multiplier(0.0, 0.1)
    with pytest.raises(ValueError):
        drawdown_constrained_multiplier(0.5, 1.0)


def test_sizing_policy_applies_shrinkage() -> None:
    mu = INST["mu"]
    r = INST["r"]
    sigma = INST["sigma"]
    t_obs = INST["t_obs"]
    max_d = INST["max_drawdown"]
    max_p = INST["max_drawdown_prob"]

    pol = sizing_policy(mu, r, sigma, t_obs, max_d, max_p)

    required_keys = {
        "f_raw",
        "sharpe",
        "alpha_shrinkage",
        "c_drawdown",
        "c_recommended",
        "f_recommended",
        "raw_growth",
        "expected_growth",
    }
    assert required_keys <= pol.keys(), f"sizing_policy missing keys: {required_keys - pol.keys()}"

    # Shrinkage check: alpha_shrinkage must be strictly less than 1.0 under finite sample
    assert pol["alpha_shrinkage"] < 1.0, "alpha_shrinkage must reflect estimation error and be < 1.0"

    # c_recommended must be min(alpha_shrinkage, c_drawdown)
    expected_c = min(pol["alpha_shrinkage"], pol["c_drawdown"])
    assert math.isclose(pol["c_recommended"], expected_c, rel_tol=1e-7), (
        f"c_recommended {pol['c_recommended']} must equal min(alpha, c_dd) {expected_c}"
    )

    # f_recommended must equal c_recommended * f_raw
    expected_f = pol["c_recommended"] * pol["f_raw"]
    assert math.isclose(pol["f_recommended"], expected_f, rel_tol=1e-7), (
        f"f_recommended {pol['f_recommended']} must equal c_recommended * f_raw {expected_f}"
    )


def test_simulate_wealth_invariants() -> None:
    mu = INST["mu"]
    r = INST["r"]
    sigma = INST["sigma"]
    f_star = continuous_kelly(mu, r, sigma)

    # Simulate 500 paths over 3 years
    res = simulate_wealth(0.5 * f_star, mu, r, sigma, t_years=3.0, n_steps=60, n_paths=400, seed=INST["seed"])

    assert res["median_terminal_wealth"] > 0.0, "Median terminal wealth must be positive"
    assert 0.0 <= res["prob_loss"] <= 1.0, "Loss probability must lie in [0, 1]"
    # Half-Kelly should have positive empirical growth rate when excess return is positive
    assert res["empirical_growth_rate"] > r, "Empirical growth rate must exceed risk-free rate"
