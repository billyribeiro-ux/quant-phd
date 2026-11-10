"""Acceptance test suite for the FC3 project: Fund-skill test.

Tests properties, numbers, exception handling, and bootstrap skill recovery.
Runs identically in Pyodide and under pytest:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any, cast

import fund_skill as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def _closed_form_oracle(returns: list[float], factor: list[float]) -> tuple[float, float]:
    """Independent oracle for OLS alpha and t-statistic with explicit loops."""
    n = len(returns)
    sum_f = 0.0
    sum_r = 0.0
    for t in range(n):
        sum_f += factor[t]
        sum_r += returns[t]
    m_f = sum_f / n
    m_r = sum_r / n

    s_ff = 0.0
    s_fr = 0.0
    for t in range(n):
        df = factor[t] - m_f
        dr = returns[t] - m_r
        s_ff += df * df
        s_fr += df * dr

    beta = s_fr / s_ff
    alpha = m_r - beta * m_f

    rss = 0.0
    for t in range(n):
        res = returns[t] - (alpha + beta * factor[t])
        rss += res * res

    s2 = rss / (n - 2)
    var_a = s2 * (1.0 / n + (m_f * m_f) / s_ff)
    se_a = math.sqrt(var_a)
    t_stat = alpha / se_a
    return alpha, t_stat


def test_alpha_and_t_oracle_match() -> None:
    """Check that alpha_and_t matches the closed-form oracle within tolerance 1e-9."""
    __tracebackhide__ = True
    factor = cast(list[float], INST["factor"])
    returns = cast(list[list[float]], INST["returns"])

    for i in range(min(5, len(returns))):
        fund_ret = returns[i]
        exp_a, exp_t = _closed_form_oracle(fund_ret, factor)
        act_a, act_t = sol.alpha_and_t(fund_ret, factor)

        tol_a = 1e-9 * (1.0 + abs(exp_a))
        tol_t = 1e-9 * (1.0 + abs(exp_t))
        assert abs(act_a - exp_a) <= tol_a, "alpha estimate does not match closed-form OLS formula"
        assert abs(act_t - exp_t) <= tol_t, "t-statistic does not match closed-form standard error formula"


def test_alpha_zero_constructed() -> None:
    """Check that an asset with zero true intercept yields alpha == 0.0 within numerical noise."""
    __tracebackhide__ = True
    # Symmetric factor and noise such that sum(factor) = 0, sum(noise) = 0, and dot(factor, noise) = 0
    sym_factor = [0.02, -0.02, 0.04, -0.04, 0.06, -0.06]
    sym_noise = [0.01, 0.01, -0.02, -0.02, 0.01, 0.01]
    sym_returns = [0.8 * sym_factor[t] + sym_noise[t] for t in range(6)]
    act_a, act_t = sol.alpha_and_t(sym_returns, sym_factor)
    assert abs(act_a) < 1e-12, "zero-alpha asset yielded non-zero alpha intercept"
    assert abs(act_t) < 1e-12, "zero-alpha asset yielded non-zero t-statistic"


def test_alpha_and_t_sign_consistency() -> None:
    """Check that the t-statistic strictly shares the sign of the alpha intercept."""
    __tracebackhide__ = True
    factor = [0.01, 0.02, -0.01, 0.03, -0.02]
    # Add non-zero residual noise so RSS > 0
    noise = [0.001, -0.001, 0.002, -0.002, 0.000]
    pos_returns = [f + 0.05 + n for f, n in zip(factor, noise, strict=True)]
    neg_returns = [f - 0.05 + n for f, n in zip(factor, noise, strict=True)]

    pos_a, pos_t = sol.alpha_and_t(pos_returns, factor)
    neg_a, neg_t = sol.alpha_and_t(neg_returns, factor)

    assert pos_a > 0.0 and pos_t > 0.0, "positive alpha must produce positive t-statistic"
    assert neg_a < 0.0 and neg_t < 0.0, "negative alpha must produce negative t-statistic"


def test_chance_count_properties() -> None:
    """Check strict inequality, monotonicity, and empty list handling of chance_count."""
    __tracebackhide__ = True
    t_stats = [1.0, 1.645, 2.0, 2.5]
    # Strict inequality: critical=2.0 counts only 2.5 (1 fund), not 2.0
    assert sol.chance_count(t_stats, 2.0) == 1, "chance_count must use strict inequality (t > critical)"
    assert sol.chance_count(t_stats, 1.0) == 3, "chance_count must strictly exclude boundary value"
    assert sol.chance_count([], 1.645) == 0, "empty t-statistics list must return 0"

    # Monotonicity check
    c1 = sol.chance_count(t_stats, 0.5)
    c2 = sol.chance_count(t_stats, 1.5)
    c3 = sol.chance_count(t_stats, 2.2)
    assert c1 >= c2 >= c3, "chance_count must be monotone non-increasing in critical value"


def test_bootstrap_output_structure() -> None:
    """Check that bootstrap_skilled_set returns a sorted list of valid fund indices without duplicates."""
    __tracebackhide__ = True
    returns = cast(list[list[float]], INST["returns"])
    factor = cast(list[float], INST["factor"])
    n_funds = len(returns)

    skilled = sol.bootstrap_skilled_set(returns, factor, level=0.05, n_boot=200, seed=SEED + 100)
    assert isinstance(skilled, list), "bootstrap_skilled_set must return a list"
    assert skilled == sorted(skilled), "output fund indices must be in ascending order"
    assert len(skilled) == len(set(skilled)), "output fund indices must contain no duplicates"
    for idx in skilled:
        assert 0 <= idx < n_funds, f"returned fund index {idx} out of universe bounds"


def test_bootstrap_superset_chain() -> None:
    """Check that higher significance levels produce nested supersets of skilled funds."""
    __tracebackhide__ = True
    returns = cast(list[list[float]], INST["returns"])
    factor = cast(list[float], INST["factor"])
    seed = SEED + 555

    s_01 = set(sol.bootstrap_skilled_set(returns, factor, level=0.01, n_boot=200, seed=seed))
    s_05 = set(sol.bootstrap_skilled_set(returns, factor, level=0.05, n_boot=200, seed=seed))
    s_20 = set(sol.bootstrap_skilled_set(returns, factor, level=0.20, n_boot=200, seed=seed))

    assert s_01.issubset(s_05), "skilled set at level 0.01 must be a subset of skilled set at level 0.05"
    assert s_05.issubset(s_20), "skilled set at level 0.05 must be a subset of skilled set at level 0.20"


def test_bootstrap_planted_recovery() -> None:
    """Check that all planted skilled funds are detected at the 5% level."""
    __tracebackhide__ = True
    returns = cast(list[list[float]], INST["returns"])
    factor = cast(list[float], INST["factor"])
    planted = set(cast(list[int], INST["planted_skill"]))

    skilled = set(sol.bootstrap_skilled_set(returns, factor, level=0.05, n_boot=200, seed=SEED + 1000))
    assert planted.issubset(skilled), "bootstrap test failed to recover all planted skilled funds at 5% level"


def test_bootstrap_zero_skill_false_positive_control() -> None:
    """Check that the number of false discoveries among zero-skill funds is strictly bounded."""
    __tracebackhide__ = True
    returns = cast(list[list[float]], INST["returns"])
    factor = cast(list[float], INST["factor"])
    planted = set(cast(list[int], INST["planted_skill"]))

    skilled = set(sol.bootstrap_skilled_set(returns, factor, level=0.05, n_boot=200, seed=SEED + 1000))
    false_positives = skilled - planted
    assert len(false_positives) <= 2, "excessive false discoveries among zero-skill funds under max-t bootstrap"


def test_bootstrap_determinism() -> None:
    """Check that identical seeds give identical results while different seeds yield reproducible draws."""
    __tracebackhide__ = True
    returns = cast(list[list[float]], INST["returns"])
    factor = cast(list[float], INST["factor"])

    run1 = sol.bootstrap_skilled_set(returns, factor, level=0.05, n_boot=200, seed=42)
    run2 = sol.bootstrap_skilled_set(returns, factor, level=0.05, n_boot=200, seed=42)
    assert run1 == run2, "bootstrap procedure must be strictly deterministic given a fixed seed"


def test_edge_cases() -> None:
    """Check edge cases: single fund universe and n_boot = 1."""
    __tracebackhide__ = True
    factor = cast(list[float], INST["factor"])
    single_fund = [cast(list[list[float]], INST["returns"])[0]]

    res = sol.bootstrap_skilled_set(single_fund, factor, level=0.05, n_boot=1, seed=123)
    assert isinstance(res, list), "n_boot=1 on single fund must return a list"
    assert set(res).issubset({0}), "returned index must be within range"


def test_exception_conditions() -> None:
    """Check that invalid inputs raise ValueError with expected condition keywords."""
    __tracebackhide__ = True
    factor = [0.01, 0.02, 0.03, 0.04]

    # Length mismatch
    with pytest.raises(ValueError, match="need at least 3 months and equal lengths"):
        sol.alpha_and_t([0.01, 0.02], factor)

    # T < 3
    with pytest.raises(ValueError, match="need at least 3 months and equal lengths"):
        sol.alpha_and_t([0.01, 0.02], [0.01, 0.02])

    # Constant factor
    with pytest.raises(ValueError, match="the factor must vary"):
        sol.alpha_and_t([0.01, 0.02, 0.03], [0.05, 0.05, 0.05])

    # Zero residuals
    perfect_returns = [0.01 + 2.0 * f for f in factor]
    with pytest.raises(ValueError, match="residuals are zero; the t-statistic is undefined"):
        sol.alpha_and_t(perfect_returns, factor)

    # Invalid bootstrap level
    with pytest.raises(ValueError, match="level must lie strictly between 0 and 1"):
        sol.bootstrap_skilled_set([[0.01, 0.02, 0.03]], [0.01, 0.02, 0.03], level=0.0, n_boot=10, seed=1)

    with pytest.raises(ValueError, match="level must lie strictly between 0 and 1"):
        sol.bootstrap_skilled_set([[0.01, 0.02, 0.03]], [0.01, 0.02, 0.03], level=1.0, n_boot=10, seed=1)

    # Invalid n_boot < 1
    with pytest.raises(ValueError, match="n_boot must be at least 1"):
        sol.bootstrap_skilled_set([[0.01, 0.02, 0.03]], [0.01, 0.02, 0.03], level=0.05, n_boot=0, seed=1)
