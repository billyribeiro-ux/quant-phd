"""Lab PR1-project-3: Rung 3 independent project reference benchmark (seed 3).

SIMULATED: generates the reference instance for seed 3 and executes the full
out-of-sample backtest across all five allocation methods under proportional
turnover costs (10 bps). Prints the benchmark allocator shoot-out table
against which the student report is compared.
"""

from __future__ import annotations

import itertools
import math
import random
from typing import Any


def _solve_linear(a_mat: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m_sys = [[*a_mat[i], b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m_sys[r][i]))
        if abs(m_sys[max_row][i]) < 1e-14:
            raise ValueError("Singular matrix encountered.")
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
    raise RuntimeError("No KKT solution found.")


def equal_weight(n: int) -> list[float]:
    return [1.0 / n] * n


def sample_mv(window: list[list[float]], gamma: float) -> list[float]:
    mu, s = _mean_and_cov(window)
    n = len(mu)
    q = [[gamma * s[i][j] for j in range(n)] for i in range(n)]
    return _solve_long_only_qp(q, mu)


def shrinkage_mv(window: list[list[float]], gamma: float, delta: float) -> list[float]:
    mu, s = _mean_and_cov(window)
    n = len(mu)
    tr_s = sum(s[i][i] for i in range(n))
    target_scale = tr_s / n
    sigma_delta = [
        [(1.0 - delta) * s[i][j] + (delta * target_scale if i == j else 0.0) for j in range(n)] for i in range(n)
    ]
    q = [[gamma * sigma_delta[i][j] for j in range(n)] for i in range(n)]
    return _solve_long_only_qp(q, mu)


def min_variance(window: list[list[float]]) -> list[float]:
    _, s = _mean_and_cov(window)
    n = len(s)
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
    n = len(w_mkt)
    k = len(q)
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


def make_instance_seed3() -> dict[str, Any]:
    seed = 3
    rng = random.Random(seed)
    n = 4 + (seed % 3)  # n = 4
    h = 120
    window = 60
    gamma = 2.0 + (seed % 4) * 0.8
    delta = 0.25 + (seed % 5) * 0.12
    tau = 0.03 + (seed % 4) * 0.02
    cost_rates = [0.0005, 0.001, 0.002]
    cost_rate = cost_rates[seed % len(cost_rates)]
    names = [f"Asset_{chr(65 + i)}" for i in range(n)]

    raw_mkt = [1.0 + rng.random() for _ in range(n)]
    tot_mkt = sum(raw_mkt)
    w_mkt = [round(x / tot_mkt, 6) for x in raw_mkt]
    w_mkt[0] += round(1.0 - sum(w_mkt), 6)

    drift = [0.004 + 0.008 * rng.random() for _ in range(n)]
    vol = [0.03 + 0.02 * rng.random() for _ in range(n)]
    beta1 = [0.6 + 0.8 * rng.random() for _ in range(n)]
    beta2 = [-0.3 + 0.6 * rng.random() for _ in range(n)]

    returns: list[list[float]] = []
    for _ in range(h):
        f1 = rng.gauss(0.0, 0.04)
        f2 = rng.gauss(0.0, 0.03)
        row: list[float] = []
        for i in range(n):
            idio = rng.gauss(0.0, vol[i])
            r = drift[i] + beta1[i] * f1 + beta2[i] * f2 + idio
            row.append(round(r, 6))
        returns.append(row)

    # Views for seed 3 (odd seed: 2 views)
    p = [[0.0] * n, [0.0] * n]
    p[0][0] = 1.0
    p[0][1] = -1.0
    p[1][2] = 1.0
    q = [
        round(0.004 + 0.004 * rng.random(), 5),
        round(0.008 + 0.004 * rng.random(), 5),
    ]
    omega = [
        round(0.0003 + 0.0001 * rng.random(), 6),
        round(0.0005 + 0.0002 * rng.random(), 6),
    ]

    return {
        "names": names,
        "returns": returns,
        "window": window,
        "gamma": gamma,
        "delta": delta,
        "tau": tau,
        "w_mkt": w_mkt,
        "P": p,
        "q": q,
        "omega": omega,
        "cost_rate": cost_rate,
    }


def main() -> None:
    inst = make_instance_seed3()
    returns = inst["returns"]
    window_len = inst["window"]
    gamma = inst["gamma"]
    delta = inst["delta"]
    tau = inst["tau"]
    w_mkt = inst["w_mkt"]
    p = inst["P"]
    q = inst["q"]
    omega = inst["omega"]
    cost_rate = inst["cost_rate"]

    n_assets = len(returns[0])
    k_dates = len(returns) - window_len
    methods = [
        "sample_mv",
        "shrinkage_mv",
        "equal_weight",
        "black_litterman",
        "min_variance",
    ]

    results: list[tuple[str, float, float, float, float]] = []

    for m in methods:
        w_prev = [1.0 / n_assets] * n_assets
        gross_list: list[float] = []
        net_list: list[float] = []
        turnover_list: list[float] = []

        for step in range(k_dates):
            t = window_len + step
            win = returns[t - window_len : t]
            if m == "equal_weight":
                w = equal_weight(n_assets)
            elif m == "sample_mv":
                w = sample_mv(win, gamma)
            elif m == "shrinkage_mv":
                w = shrinkage_mv(win, gamma, delta)
            elif m == "black_litterman":
                w = black_litterman(win, w_mkt, tau, p, q, omega, gamma)
            elif m == "min_variance":
                w = min_variance(win)

            turnover = sum(abs(w[i] - w_prev[i]) for i in range(n_assets))
            cost = cost_rate * turnover
            gross = sum(w[i] * returns[t][i] for i in range(n_assets))
            net = gross - cost

            gross_list.append(gross)
            net_list.append(net)
            turnover_list.append(turnover)
            w_prev = w

        mean_net = sum(net_list) / k_dates
        var_net = sum((x - mean_net) ** 2 for x in net_list) / (k_dates - 1)
        sr_net = mean_net / math.sqrt(var_net) if var_net > 1e-14 else 0.0

        mean_gross = sum(gross_list) / k_dates
        var_gross = sum((x - mean_gross) ** 2 for x in gross_list) / (k_dates - 1)
        sr_gross = mean_gross / math.sqrt(var_gross) if var_gross > 1e-14 else 0.0

        mean_turnover = sum(turnover_list) / k_dates
        results.append((m, sr_net, sr_gross, mean_turnover, mean_net))

    results.sort(key=lambda r: r[1], reverse=True)

    print("Rank Method              Net SR      Gross SR    Turnover    Net Return")
    print("-" * 72)
    for rank, (m_name, ns, gs, to, nr) in enumerate(results, 1):
        print(f"{rank:<5}{m_name:<20}{ns:<12.4f}{gs:<12.4f}{to:<12.4f}{nr:<12.4f}")


main()
