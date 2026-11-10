"""Lab X2-project-1: Rung 1 Worked Example for Currency Factor Replication.

Traces complete replication of Lustig et al. (2011) Dollar and HML-FX factors
and Menkhoff et al. (2012) global FX volatility innovations on seed 42.
"""

from __future__ import annotations

import math
import random
from typing import Any


def _solve_linear_system(a_matrix: list[list[float]], b_vector: list[float]) -> list[float]:
    n = len(b_vector)
    aug = [[*row[:], b_vector[i]] for i, row in enumerate(a_matrix)]
    for col in range(n):
        max_row = col
        max_val = abs(aug[col][col])
        for row in range(col + 1, n):
            if abs(aug[row][col]) > max_val:
                max_val = abs(aug[row][col])
                max_row = row
        if max_val < 1e-12:
            raise ValueError("Matrix is singular")
        aug[col], aug[max_row] = aug[max_row], aug[col]
        pivot = aug[col][col]
        for c in range(col, n + 1):
            aug[col][c] /= pivot
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                for c in range(col, n + 1):
                    aug[row][c] -= factor * aug[col][c]
    return [aug[i][n] for i in range(n)]


def _multivariate_ols(
    x_matrix: list[list[float]],
    y_vector: list[float],
    fit_intercept: bool = True,
) -> tuple[list[float], list[float], float]:
    t_obs = len(y_vector)
    p_vars = len(x_matrix[0]) if x_matrix else 0
    if fit_intercept:
        design = [[1.0, *row] for row in x_matrix]
        num_params = p_vars + 1
    else:
        design = [row[:] for row in x_matrix]
        num_params = p_vars

    xt_x = [[0.0] * num_params for _ in range(num_params)]
    xt_y = [0.0] * num_params
    for t in range(t_obs):
        row = design[t]
        y_val = y_vector[t]
        for i in range(num_params):
            xt_y[i] += row[i] * y_val
            for j in range(num_params):
                xt_x[i][j] += row[i] * row[j]

    coeffs = _solve_linear_system(xt_x, xt_y)
    fitted: list[float] = []
    for t in range(t_obs):
        pred = sum(design[t][i] * coeffs[i] for i in range(num_params))
        fitted.append(pred)

    y_mean = sum(y_vector) / t_obs
    ss_tot = sum((y - y_mean) ** 2 for y in y_vector)
    ss_res = sum((y - fitted[t]) ** 2 for t, y in enumerate(y_vector))
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
    return coeffs, fitted, r_squared


def run_worked_example(seed: int = 42) -> dict[str, Any]:
    """Execute complete currency factor replication on seed 42."""
    rng = random.Random(seed)
    n_periods = 120
    n_cur = 10
    n_portfolios = 5

    base_spreads = [0.025, 0.005, -0.020, -0.005, 0.010, -0.035, 0.015, 0.030, 0.008, 0.060]
    initial_spots = [0.70, 0.75, 1.10, 1.15, 1.30, 0.009, 0.11, 0.65, 0.10, 0.065]
    log_spots = [math.log(s) for s in initial_spots]
    days_per_month = 21

    spot_rates: list[list[float]] = []
    forward_rates: list[list[float]] = []
    daily_returns: list[list[float]] = []
    vol_state = 0.006

    for _ in range(n_periods):
        cur_spots = [round(math.exp(ls), 5) for ls in log_spots]
        spot_rates.append(cur_spots)
        month_forwards = [round(cur_spots[j] * math.exp(-base_spreads[j] / 12.0), 5) for j in range(n_cur)]
        forward_rates.append(month_forwards)

        for _ in range(days_per_month):
            vol_state = max(0.003, min(0.025, 0.90 * vol_state + 0.10 * 0.006 + rng.gauss(0.0, 0.0007)))
            dol_shock = rng.gauss(0.0, vol_state)
            vol_shock = vol_state - 0.006
            day_rets: list[float] = []
            for j in range(n_cur):
                vol_loading = -6.0 * base_spreads[j]
                idio = rng.gauss(0.0, 0.0025)
                d_ret = dol_shock + vol_loading * vol_shock + idio
                log_spots[j] += d_ret
                day_rets.append(round(d_ret, 6))
            daily_returns.append(day_rets)

    # 1. Excess returns and forward discounts
    excess_returns: list[list[float]] = []
    forward_discounts: list[list[float]] = []
    for t in range(n_periods - 1):
        rx_row: list[float] = []
        fd_row: list[float] = []
        for j in range(n_cur):
            rx = math.log(spot_rates[t + 1][j]) - math.log(forward_rates[t][j])
            fd = math.log(forward_rates[t][j]) - math.log(spot_rates[t][j])
            rx_row.append(rx)
            fd_row.append(fd)
        excess_returns.append(rx_row)
        forward_discounts.append(fd_row)

    # 2. Sort into 5 carry portfolios
    t_ret = len(excess_returns)
    port_rets: list[list[float]] = []
    for t in range(t_ret):
        fds = forward_discounts[t]
        rxs = excess_returns[t]
        ranked_indices = sorted(range(n_cur), key=lambda j: fds[j], reverse=True)
        p_row = [0.0] * n_portfolios
        p_cnt = [0] * n_portfolios
        for rank_pos, cur_idx in enumerate(ranked_indices):
            bucket = min(int(rank_pos * n_portfolios / n_cur), n_portfolios - 1)
            p_row[bucket] += rxs[cur_idx]
            p_cnt[bucket] += 1
        port_rets.append([p_row[k] / p_cnt[k] for k in range(n_portfolios)])

    # 3. Build factors
    dol_factor = [sum(port_rets[t]) / n_portfolios for t in range(t_ret)]
    hml_factor = [port_rets[t][-1] - port_rets[t][0] for t in range(t_ret)]

    # 4. Volatility innovations
    daily_vol = [sum(abs(r) for r in row) / n_cur for row in daily_returns]
    m_months = len(daily_returns) // days_per_month
    monthly_vol = [
        sum(daily_vol[m * days_per_month : (m + 1) * days_per_month]) / days_per_month for m in range(m_months)
    ]
    y_v = monthly_vol[1:]
    x_v = [[monthly_vol[i]] for i in range(m_months - 1)]
    coeffs_v, fitted_v, _ = _multivariate_ols(x_v, y_v, fit_intercept=True)
    vol_innov = [y_v[i] - fitted_v[i] for i in range(len(y_v))]

    # 5. Lustig 2-factor model: [DOL, HML]
    t_eval = min(t_ret, len(vol_innov))
    x_lustig = [[dol_factor[t], hml_factor[t]] for t in range(t_eval)]
    mean_rets = [sum(port_rets[t][k] for t in range(t_eval)) / t_eval for k in range(n_portfolios)]

    lustig_betas: list[list[float]] = []
    for k in range(n_portfolios):
        yk = [port_rets[t][k] for t in range(t_eval)]
        c_k, _, _ = _multivariate_ols(x_lustig, yk, fit_intercept=True)
        lustig_betas.append([round(c_k[1], 3), round(c_k[2], 3)])

    _cs_lustig, _, r2_lustig = _multivariate_ols(lustig_betas, mean_rets, fit_intercept=False)

    return {
        "n_periods": n_periods,
        "hml_mean_ann": round(sum(hml_factor) / t_ret * 12.0 * 100, 2),
        "dol_mean_ann": round(sum(dol_factor) / t_ret * 12.0 * 100, 2),
        "lustig_betas": lustig_betas,
        "lustig_r2": round(r2_lustig, 3),
        "ar1_rho": round(coeffs_v[1], 3),
    }


def main() -> None:
    res = run_worked_example(seed=42)
    print("=== Rung 1 Worked Example: Currency Factor Replication (Seed 42) ===")
    print(f"Periods: {res['n_periods']} months | Annualized HML-FX Return: {res['hml_mean_ann']}%")
    print(f"Annualized Dollar Factor Return: {res['dol_mean_ann']}% | Vol AR(1) Persistence rho: {res['ar1_rho']}")
    print("Lustig Factor Betas [Beta_DOL, Beta_HML]:")
    for k, b in enumerate(res["lustig_betas"]):
        print(f"  Portfolio {k + 1}: Beta_DOL = {b[0]:>6.3f} | Beta_HML = {b[1]:>6.3f}")
    print(f"Cross-Sectional R^2: {res['lustig_r2']:.3f}")


main()
