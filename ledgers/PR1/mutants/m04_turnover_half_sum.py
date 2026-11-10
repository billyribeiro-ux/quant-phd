"""run_backtest calculates turnover as 0.5 * sum(|w - w_prev|) instead of full sum"""

from __future__ import annotations

import itertools
import math
from typing import Any


def _validate_window(window: list[list[float]]) -> tuple[int, int]:
    if not window or not window[0]:
        raise ValueError("Window must not be empty.")
    t = len(window)
    n = len(window[0])
    for row in window:
        if len(row) != n:
            raise ValueError("Ragged window: rows have unequal lengths.")
        for val in row:
            if not math.isfinite(val):
                raise ValueError("Window contains non-finite values.")
    return t, n


def _solve_linear(a_mat: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m_sys = [[*a_mat[i], b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m_sys[r][i]))
        if abs(m_sys[max_row][i]) < 1e-14:
            raise ValueError("Singular matrix encountered in linear solver.")
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


def _mean_and_cov(window: list[list[float]]) -> tuple[list[float], list[list[float]]]:
    t = len(window)
    n = len(window[0])
    means = [0.0] * n
    for row in window:
        for j in range(n):
            means[j] += row[j]
    means = [m / t for m in means]

    cov = [[0.0] * n for _ in range(n)]
    for row in window:
        diff = [row[j] - means[j] for j in range(n)]
        for i in range(n):
            for j in range(n):
                cov[i][j] += diff[i] * diff[j]

    denom = t - 1
    for i in range(n):
        for j in range(n):
            cov[i][j] /= denom
    return means, cov


def _solve_long_only_qp(q_mat: list[list[float]], c: list[float]) -> list[float]:
    n = len(c)
    for k in range(n):
        for z in itertools.combinations(range(n), k):
            z_set = set(z)
            a = [i for i in range(n) if i not in z_set]
            m = len(a)

            sys_a = [[0.0] * (m + 1) for _ in range(m + 1)]
            sys_b = [0.0] * (m + 1)
            for i_idx, i in enumerate(a):
                for j_idx, j in enumerate(a):
                    sys_a[i_idx][j_idx] = q_mat[i][j]
                sys_a[i_idx][m] = 1.0
                sys_b[i_idx] = c[i]
            for j_idx in range(m):
                sys_a[m][j_idx] = 1.0
            sys_b[m] = 1.0

            try:
                sol = _solve_linear(sys_a, sys_b)
            except ValueError:
                continue

            w_a = sol[:m]
            nu = sol[m]

            if any(x < -1e-9 for x in w_a):
                continue

            w = [0.0] * n
            for idx, i in enumerate(a):
                w[i] = max(w_a[idx], 0.0)
            tot = sum(w)
            if tot <= 1e-12:
                continue
            w = [x / tot for x in w]

            dual_ok = True
            for i in z:
                grad_i = sum(q_mat[i][j] * w[j] for j in range(n)) - c[i] + nu
                if grad_i < -1e-8:
                    dual_ok = False
                    break

            if dual_ok:
                return w

    raise RuntimeError("No KKT solution found for quadratic program.")


def equal_weight(n: int) -> list[float]:
    if n <= 0:
        raise ValueError("n must be positive.")
    return [1.0 / n] * n


def sample_mv(window: list[list[float]], gamma: float) -> list[float]:
    t, n = _validate_window(window)
    if t <= n:
        raise ValueError(f"Window length {t} must be strictly greater than N {n}.")
    if gamma <= 0.0:
        raise ValueError("Risk aversion gamma must be strictly positive.")

    mu, s = _mean_and_cov(window)
    q = [[gamma * s[i][j] for j in range(n)] for i in range(n)]
    return _solve_long_only_qp(q, mu)


def shrinkage_mv(window: list[list[float]], gamma: float, delta: float) -> list[float]:
    t, n = _validate_window(window)
    if delta < 0.0 or delta > 1.0:
        raise ValueError("Shrinkage intensity delta must lie in [0, 1].")
    if delta == 0.0 and t <= n:
        raise ValueError(f"Window length {t} must be greater than N {n} when delta=0.")
    if gamma <= 0.0:
        raise ValueError("Risk aversion gamma must be strictly positive.")

    mu, s = _mean_and_cov(window)
    tr_s = sum(s[i][i] for i in range(n))
    target_scale = tr_s / n
    sigma_delta = [
        [(1.0 - delta) * s[i][j] + (delta * target_scale if i == j else 0.0) for j in range(n)] for i in range(n)
    ]
    q = [[gamma * sigma_delta[i][j] for j in range(n)] for i in range(n)]
    return _solve_long_only_qp(q, mu)


def min_variance(window: list[list[float]]) -> list[float]:
    t, n = _validate_window(window)
    if t <= n:
        raise ValueError(f"Window length {t} must be strictly greater than N {n}.")

    _, s = _mean_and_cov(window)
    c = [0.0] * n
    return _solve_long_only_qp(s, c)


def black_litterman(
    window: list[list[float]],
    w_mkt: list[float],
    tau: float,
    p: list[list[float]],
    q: list[float],
    omega: list[float],
    gamma: float,
) -> list[float]:
    t, n = _validate_window(window)
    if t <= n:
        raise ValueError(f"Window length {t} must be strictly greater than N {n}.")
    if tau <= 0.0:
        raise ValueError("tau must be strictly positive.")
    if gamma <= 0.0:
        raise ValueError("Risk aversion gamma must be strictly positive.")
    if len(w_mkt) != n:
        raise ValueError("w_mkt length must match asset count N.")
    k = len(q)
    if len(p) != k or any(len(row) != n for row in p) or len(omega) != k:
        raise ValueError("View dimensions (P, q, omega) are inconsistent.")

    _, s = _mean_and_cov(window)
    s_inv = _invert_matrix(s)

    mu_eq = [gamma * sum(s[i][j] * w_mkt[j] for j in range(n)) for i in range(n)]
    tau_inv = 1.0 / tau
    m_bl = [[tau_inv * s_inv[i][j] for j in range(n)] for i in range(n)]

    for r in range(k):
        inv_om = 1.0 / omega[r]
        for i in range(n):
            for j in range(n):
                m_bl[i][j] += p[r][i] * p[r][j] * inv_om

    v_bl = [0.0] * n
    for i in range(n):
        v_bl[i] = sum(tau_inv * s_inv[i][j] * mu_eq[j] for j in range(n))
        for r in range(k):
            v_bl[i] += p[r][i] * q[r] / omega[r]

    mu_bl = _solve_linear(m_bl, v_bl)
    q_mat = [[gamma * s[i][j] for j in range(n)] for i in range(n)]
    return _solve_long_only_qp(q_mat, mu_bl)


def run_backtest(instance: dict[str, Any], method: str) -> dict[str, Any]:
    allowed = {
        "equal_weight",
        "sample_mv",
        "shrinkage_mv",
        "black_litterman",
        "min_variance",
    }
    if method not in allowed:
        raise ValueError(f"Unknown allocation method: {method}")

    returns: list[list[float]] = instance["returns"]
    window_len: int = instance["window"]
    gamma: float = instance["gamma"]
    delta: float = instance["delta"]
    tau: float = instance["tau"]
    w_mkt: list[float] = instance["w_mkt"]
    p: list[list[float]] = instance["P"]
    q: list[float] = instance["q"]
    omega: list[float] = instance["omega"]
    cost_rate: float = instance["cost_rate"]

    if cost_rate < 0.0:
        raise ValueError("Cost rate must be non-negative.")

    h = len(returns)
    n = len(returns[0])
    k_dates = h - window_len

    weights: list[list[float]] = []
    turnovers: list[float] = []
    gross_returns: list[float] = []
    net_returns: list[float] = []

    w_prev = [1.0 / n] * n

    for step in range(k_dates):
        t = window_len + step
        win = returns[t - window_len : t]

        if method == "equal_weight":
            w = equal_weight(n)
        elif method == "sample_mv":
            w = sample_mv(win, gamma)
        elif method == "shrinkage_mv":
            w = shrinkage_mv(win, gamma, delta)
        elif method == "black_litterman":
            w = black_litterman(win, w_mkt, tau, p, q, omega, gamma)
        elif method == "min_variance":
            w = min_variance(win)

        # BUG: one-way turnover 0.5 * sum(|w - w_prev|) instead of two-way gross turnover
        turnover = 0.5 * sum(abs(w[i] - w_prev[i]) for i in range(n))
        cost = cost_rate * turnover
        gross = sum(w[i] * returns[t][i] for i in range(n))
        net = gross - cost

        weights.append(w)
        turnovers.append(turnover)
        gross_returns.append(gross)
        net_returns.append(net)
        w_prev = w

    mean_net = sum(net_returns) / k_dates
    var_net = sum((r - mean_net) ** 2 for r in net_returns) / (k_dates - 1)
    sd_net = math.sqrt(var_net)
    sharpe = mean_net / sd_net if sd_net > 1e-14 else 0.0

    return {
        "weights": weights,
        "turnover": turnovers,
        "gross": gross_returns,
        "net": net_returns,
        "sharpe": sharpe,
    }
