"""Lab 8: Allocator ranking across random seeds: 1/N benchmark vs sample MV.

SIMULATED: 30 independent synthetic market simulations (seeds 0 through 29).
Computes out-of-sample net Sharpe ratios for 1/N equal weighting versus
unconstrained/long-only sample mean-variance optimization under realistic
turnover costs (10 bps). Evaluates empirical win rates across market environments.
"""

from __future__ import annotations

import itertools
import math
import random


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


def sample_mv(win: list[list[float]], gamma: float = 3.0) -> list[float]:
    t = len(win)
    n = len(win[0])
    means = [sum(win[s][i] for s in range(t)) / t for i in range(n)]
    cov = [[0.0] * n for _ in range(n)]
    for s in range(t):
        diff = [win[s][i] - means[i] for i in range(n)]
        for i in range(n):
            for j in range(n):
                cov[i][j] += diff[i] * diff[j]
    for i in range(n):
        for j in range(n):
            cov[i][j] /= t - 1
    q = [[gamma * cov[i][j] for j in range(n)] for i in range(n)]
    return _solve_long_only_qp(q, means)


def main() -> None:
    num_seeds = 30
    n_assets = 4
    h_periods = 120
    t_window = 60
    k_dates = h_periods - t_window
    cost_rate = 0.001

    ew_beats_mv = 0
    ew_sharpes: list[float] = []
    mv_sharpes: list[float] = []

    for seed in range(num_seeds):
        rng = random.Random(seed)
        returns = [[rng.gauss(0.006, 0.04) for _ in range(n_assets)] for _ in range(h_periods)]

        # 1. 1/N strategy
        w_ew = [1.0 / n_assets] * n_assets
        net_ew: list[float] = []
        for k in range(k_dates):
            t = t_window + k
            g = sum(w_ew[i] * returns[t][i] for i in range(n_assets))
            net_ew.append(g)
        m_ew = sum(net_ew) / k_dates
        v_ew = sum((x - m_ew) ** 2 for x in net_ew) / (k_dates - 1)
        sr_ew = m_ew / math.sqrt(v_ew)
        ew_sharpes.append(sr_ew)

        # 2. Sample MV strategy
        w_prev = [1.0 / n_assets] * n_assets
        net_mv: list[float] = []
        for k in range(k_dates):
            t = t_window + k
            win = returns[t - t_window : t]
            w = sample_mv(win)
            turnover = sum(abs(w[i] - w_prev[i]) for i in range(n_assets))
            g = sum(w[i] * returns[t][i] for i in range(n_assets))
            net_mv.append(g - cost_rate * turnover)
            w_prev = w
        m_mv = sum(net_mv) / k_dates
        v_mv = sum((x - m_mv) ** 2 for x in net_mv) / (k_dates - 1)
        sr_mv = m_mv / math.sqrt(v_mv)
        mv_sharpes.append(sr_mv)

        if sr_ew > sr_mv:
            ew_beats_mv += 1

    print(f"Seeds where 1/N beats sample MV: {ew_beats_mv} / {num_seeds}")
    print(f"Mean 1/N Sharpe: {sum(ew_sharpes) / num_seeds:.4f}")
    print(f"Mean MV Sharpe:  {sum(mv_sharpes) / num_seeds:.4f}")


main()
