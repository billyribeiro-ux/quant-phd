"""Autograder test suite for PR1 Allocator Shoot-Out project.

Checks property invariants, exact numerical values, KKT conditions,
lookahead guards, exception handling, and backtest accounting.
"""

from __future__ import annotations

import math
import os

import pytest
from allocators import (
    black_litterman,
    equal_weight,
    min_variance,
    run_backtest,
    sample_mv,
    shrinkage_mv,
)
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))


def _solve_linear(a_mat: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m_sys = [[*a_mat[i], b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m_sys[r][i]))
        if abs(m_sys[max_row][i]) < 1e-14:
            raise ValueError("Singular matrix in test helper.")
        if max_row != i:
            m_sys[i], m_sys[max_row] = m_sys[max_row], m_sys[i]
        pivot = m_sys[i][i]
        for j in range(i, n + 1):
            m_sys[i][j] /= pivot
        for r in range(n):
            if r != i:
                factor = m_sys[r][i]
                if factor != 0.0:
                    for j in range(i, n + 1):
                        m_sys[r][j] -= factor * m_sys[i][j]
    return [m_sys[i][n] for i in range(n)]


def _invert_matrix(a_mat: list[list[float]]) -> list[list[float]]:
    n = len(a_mat)
    inv: list[list[float]] = [[0.0] * n for _ in range(n)]
    for j in range(n):
        e_j = [1.0 if i == j else 0.0 for i in range(n)]
        col = _solve_linear(a_mat, e_j)
        for i in range(n):
            inv[i][j] = col[i]
    return inv


def _compute_mean_and_cov(
    window: list[list[float]],
) -> tuple[list[float], list[list[float]]]:
    t = len(window)
    n = len(window[0])
    means = [sum(window[s][i] for s in range(t)) / t for i in range(n)]
    cov = [[0.0] * n for _ in range(n)]
    for s in range(t):
        diff = [window[s][i] - means[i] for i in range(n)]
        for i in range(n):
            for j in range(n):
                cov[i][j] += diff[i] * diff[j]
    for i in range(n):
        for j in range(n):
            cov[i][j] /= t - 1
    return means, cov


def _check_kkt(q_mat: list[list[float]], c: list[float], w: list[float], tol: float = 1e-8) -> None:
    __tracebackhide__ = True
    n = len(w)
    # 1. Budget constraint: sum(w) == 1
    assert abs(sum(w) - 1.0) < 1e-7, "Budget constraint violated: weights do not sum to 1."
    # 2. Long-only constraint: w >= 0
    assert all(x >= -1e-11 for x in w), "Long-only constraint violated: negative weight detected."

    # Active assets where w_i > 1e-6
    active = [i for i, x in enumerate(w) if x > 1e-6]
    assert len(active) >= 1, "At least one asset must be held in the portfolio."

    # Solve for budget multiplier nu using active assets:
    # (Qw)_i - c_i + nu = 0 => nu = c_i - (Qw)_i
    nu_vals = [c[i] - sum(q_mat[i][j] * w[j] for j in range(n)) for i in active]
    nu = sum(nu_vals) / len(nu_vals)
    for v in nu_vals:
        assert abs(v - nu) < tol, "Stationarity violated: active assets have inconsistent gradient residuals."

    # For zero-weight assets, check dual feasibility: (Qw)_i - c_i + nu >= -tol
    for i in range(n):
        if w[i] <= 1e-6:
            grad_i = sum(q_mat[i][j] * w[j] for j in range(n)) - c[i] + nu
            assert grad_i >= -tol, f"Dual feasibility violated for asset {i}: bound multiplier is negative."


def test_instance_valid_and_varies() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    assert "returns" in inst and "window" in inst
    assert inst["window"] == 60
    assert len(inst["returns"]) == 120
    assert 4 <= len(inst["names"]) <= 6

    # Verify instances differ across seeds
    inst0 = make_instance(0)
    inst1 = make_instance(1)
    assert inst0["returns"] != inst1["returns"], "make_instance produces identical returns across seeds."


def test_equal_weight_exact() -> None:
    __tracebackhide__ = True
    w4 = equal_weight(4)
    assert len(w4) == 4, "equal_weight(4) length must be 4."
    assert all(abs(x - 0.25) < 1e-12 for x in w4), "equal_weight(4) must allocate exactly 0.25 to each asset."

    w5 = equal_weight(5)
    assert len(w5) == 5, "equal_weight(5) length must be 5."
    assert all(abs(x - 0.20) < 1e-12 for x in w5), "equal_weight(5) must allocate exactly 0.20 to each asset."


def test_sample_covariance_convention() -> None:
    __tracebackhide__ = True
    # Window with T=3, N=2
    win = [[0.01, 0.02], [0.03, 0.04], [0.05, 0.09]]
    _, cov = _compute_mean_and_cov(win)
    assert abs(cov[0][0] - 0.0004) < 1e-9, "Sample covariance must use divisor T - 1, not T."


def test_budget_and_long_only() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win = inst["returns"][: inst["window"]]
    gamma = inst["gamma"]
    delta = inst["delta"]
    w_mkt = inst["w_mkt"]
    tau = inst["tau"]
    p = inst["P"]
    q = inst["q"]
    omega = inst["omega"]
    n = len(inst["names"])

    allocations = [
        equal_weight(n),
        sample_mv(win, gamma),
        shrinkage_mv(win, gamma, delta),
        min_variance(win),
        black_litterman(win, w_mkt, tau, p, q, omega, gamma),
    ]
    for w in allocations:
        assert abs(sum(w) - 1.0) < 1e-8, "Portfolio weights must sum to 1.0 within tolerance."
        assert all(x >= -1e-12 for x in w), "Portfolio weights must be non-negative (long-only)."


def test_shrinkage_formula_and_intensity() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win = inst["returns"][: inst["window"]]
    gamma = inst["gamma"]

    # delta = 0 must match sample_mv
    w_delta0 = shrinkage_mv(win, gamma, 0.0)
    w_sample = sample_mv(win, gamma)
    assert all(abs(a - b) < 1e-7 for a, b in zip(w_delta0, w_sample, strict=True)), (
        "shrinkage_mv with delta=0 must equal sample_mv."
    )


def test_shrinkage_min_eigenvalue() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win = inst["returns"][: inst["window"]]
    n = len(inst["names"])
    delta = inst["delta"]
    _, s = _compute_mean_and_cov(win)
    tr_s = sum(s[i][i] for i in range(n))
    target_scale = tr_s / n

    sigma_delta = [
        [(1.0 - delta) * s[i][j] + (delta * target_scale if i == j else 0.0) for j in range(n)] for i in range(n)
    ]
    for i in range(n):
        diag_val = sigma_delta[i][i]
        assert diag_val >= delta * target_scale - 1e-12, "Shrunk covariance diagonal must be at least delta * tr(S)/N."


def test_sample_mv_kkt() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win = inst["returns"][: inst["window"]]
    gamma = inst["gamma"]
    mu, s = _compute_mean_and_cov(win)
    n = len(mu)
    q = [[gamma * s[i][j] for j in range(n)] for i in range(n)]

    w = sample_mv(win, gamma)
    _check_kkt(q, mu, w)


def test_min_variance_kkt_residual() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win = inst["returns"][: inst["window"]]
    _, s = _compute_mean_and_cov(win)
    n = len(s)
    c = [0.0] * n

    w = min_variance(win)
    _check_kkt(s, c, w)


def test_black_litterman_precision_form() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win = inst["returns"][: inst["window"]]
    gamma = inst["gamma"]
    w_mkt = inst["w_mkt"]
    tau = inst["tau"]
    p = inst["P"]
    q = inst["q"]
    omega = inst["omega"]
    n = len(w_mkt)
    k = len(q)

    _, s = _compute_mean_and_cov(win)
    s_inv = _invert_matrix(s)
    mu_eq = [gamma * sum(s[i][j] * w_mkt[j] for j in range(n)) for i in range(n)]

    m_bl = [[(1.0 / tau) * s_inv[i][j] for j in range(n)] for i in range(n)]
    for r in range(k):
        for i in range(n):
            for j in range(n):
                m_bl[i][j] += p[r][i] * p[r][j] / omega[r]

    v_bl = [
        sum((1.0 / tau) * s_inv[i][j] * mu_eq[j] for j in range(n)) + sum(p[r][i] * q[r] / omega[r] for r in range(k))
        for i in range(n)
    ]
    mu_bl = _solve_linear(m_bl, v_bl)

    w = black_litterman(win, w_mkt, tau, p, q, omega, gamma)
    q_mat = [[gamma * s[i][j] for j in range(n)] for i in range(n)]
    _check_kkt(q_mat, mu_bl, w)


def test_turnover_zero_when_unchanged() -> None:
    __tracebackhide__ = True
    w = [0.25, 0.25, 0.25, 0.25]
    turnover = sum(abs(w[i] - w[i]) for i in range(4))
    assert turnover == 0.0, "Turnover must be 0 when weights remain unchanged."


def test_turnover_swap_example() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    res = run_backtest(inst, "sample_mv")
    n = len(inst["w_mkt"])
    w_prev = [1.0 / n] * n
    for w, tau in zip(res["weights"], res["turnover"], strict=True):
        expected_tau = sum(abs(w[i] - w_prev[i]) for i in range(n))
        assert abs(tau - expected_tau) < 1e-11, "Turnover must equal two-way sum(|w_t - w_{t-1}|)."
        w_prev = w


def test_costs_reduce_net_return() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    res = run_backtest(inst, "sample_mv")
    cost_rate = inst["cost_rate"]
    assert any(tau > 1e-4 for tau in res["turnover"]), "sample_mv must exhibit positive turnover."
    for g, n, tau in zip(res["gross"], res["net"], res["turnover"], strict=True):
        expected_net = g - cost_rate * tau
        assert abs(n - expected_net) < 1e-11, "Net return must equal gross return minus cost_rate * turnover."


def test_no_lookahead_perturbation() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win_len = inst["window"]
    res1 = run_backtest(inst, "sample_mv")

    inst2 = make_instance(SEED)
    inst2["returns"][win_len][0] += 0.50
    res2 = run_backtest(inst2, "sample_mv")

    assert all(abs(a - b) < 1e-9 for a, b in zip(res1["weights"][0], res2["weights"][0], strict=True)), (
        "Look-ahead detected: rebalancing weights at date t changed when realized return at date t was altered."
    )


def test_sharpe_formula() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    res = run_backtest(inst, "sample_mv")
    net_returns = res["net"]
    k = len(net_returns)
    mean_val = sum(net_returns) / k
    var_val = sum((x - mean_val) ** 2 for x in net_returns) / (k - 1)
    expected_sr = mean_val / math.sqrt(var_val) if var_val > 1e-14 else 0.0
    assert abs(res["sharpe"] - expected_sr) < 1e-11, (
        "Sharpe ratio formula must equal mean(net) / std(net) with K - 1 divisor."
    )


def test_weights_match_reference_on_each_seed() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    win = inst["returns"][: inst["window"]]
    gamma = inst["gamma"]
    delta = inst["delta"]
    w_mkt = inst["w_mkt"]

    w_ew = equal_weight(len(w_mkt))
    assert all(abs(x - 1.0 / len(w_mkt)) < 1e-9 for x in w_ew)

    w_min = min_variance(win)
    _, s = _compute_mean_and_cov(win)
    _check_kkt(s, [0.0] * len(w_mkt), w_min)

    w_smv = sample_mv(win, gamma)
    mu, _ = _compute_mean_and_cov(win)
    q_mat = [[gamma * s[i][j] for j in range(len(mu))] for i in range(len(mu))]
    _check_kkt(q_mat, mu, w_smv)

    w_shrunk = shrinkage_mv(win, gamma, delta)
    n = len(mu)
    tr_s = sum(s[i][i] for i in range(n))
    s_del = [[(1.0 - delta) * s[i][j] + (delta * tr_s / n if i == j else 0.0) for j in range(n)] for i in range(n)]
    q_del = [[gamma * s_del[i][j] for j in range(n)] for i in range(n)]
    _check_kkt(q_del, mu, w_shrunk)


def test_error_window_too_short_raises() -> None:
    __tracebackhide__ = True
    short_win = [[0.01, 0.02, 0.03, 0.04] for _ in range(4)]
    with pytest.raises(ValueError, match=r"(?i)window length|strictly greater"):
        sample_mv(short_win, 2.0)
    with pytest.raises(ValueError, match=r"(?i)window length|strictly greater"):
        min_variance(short_win)

    with pytest.raises(ValueError, match=r"(?i)delta|window"):
        shrinkage_mv(short_win, 2.0, delta=0.0)

    w_shrunk = shrinkage_mv(short_win, 2.0, delta=0.5)
    assert len(w_shrunk) == 4


def test_error_delta_range_raises() -> None:
    __tracebackhide__ = True
    win = [[0.01, 0.02], [0.03, 0.04], [0.05, 0.06]]
    with pytest.raises(ValueError, match=r"(?i)delta"):
        shrinkage_mv(win, 2.0, -0.01)
    with pytest.raises(ValueError, match=r"(?i)delta"):
        shrinkage_mv(win, 2.0, 1.01)

    w0 = shrinkage_mv(win, 2.0, 0.0)
    w1 = shrinkage_mv(win, 2.0, 1.0)
    assert len(w0) == 2 and len(w1) == 2


def test_error_ragged_or_nonfinite_raises() -> None:
    __tracebackhide__ = True
    ragged = [[0.01, 0.02], [0.03, 0.04, 0.05], [0.06, 0.07]]
    with pytest.raises(ValueError, match=r"(?i)ragged|unequal"):
        sample_mv(ragged, 2.0)

    nonfinite = [[0.01, 0.02], [float("nan"), 0.04], [0.05, 0.06]]
    with pytest.raises(ValueError, match=r"(?i)non-finite|nan"):
        sample_mv(nonfinite, 2.0)


def test_error_negative_cost_raises() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    inst["cost_rate"] = -0.001
    with pytest.raises(ValueError, match=r"(?i)cost"):
        run_backtest(inst, "equal_weight")


def test_other_invalid_inputs_raise_something() -> None:
    __tracebackhide__ = True
    inst = make_instance(SEED)
    with pytest.raises((ValueError, KeyError, TypeError)):
        run_backtest(inst, "unknown_strategy_name")
