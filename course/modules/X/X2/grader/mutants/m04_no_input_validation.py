"""Mutant: Omits all parameter validation and fails to raise ValueError on invalid dimensions or arguments."""

from __future__ import annotations

import math
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
        aug[col], aug[max_row] = aug[max_row], aug[col]
        pivot = aug[col][col] if abs(aug[col][col]) > 1e-12 else 1.0
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

    y_mean = sum(y_vector) / t_obs if t_obs else 0.0
    ss_tot = sum((y - y_mean) ** 2 for y in y_vector)
    ss_res = sum((y - fitted[t]) ** 2 for t, y in enumerate(y_vector))
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
    return coeffs, fitted, r_squared


def compute_excess_returns(
    spot_rates: list[list[float]],
    forward_rates: list[list[float]],
) -> list[list[float]]:
    # BUG: No input validation
    if not spot_rates or not forward_rates:
        return []
    t_obs = min(len(spot_rates), len(forward_rates))
    n_cur = len(spot_rates[0]) if spot_rates else 0
    excess_returns: list[list[float]] = []
    for t in range(t_obs - 1):
        month_rx: list[float] = []
        for j in range(n_cur):
            s_next = spot_rates[t + 1][j]
            f_curr = forward_rates[t][j]
            rx = math.log(max(1e-6, s_next)) - math.log(max(1e-6, f_curr))
            month_rx.append(round(rx, 6))
        excess_returns.append(month_rx)
    return excess_returns


def compute_forward_discounts(
    spot_rates: list[list[float]],
    forward_rates: list[list[float]],
) -> list[list[float]]:
    # BUG: No input validation
    if not spot_rates or not forward_rates:
        return []
    t_obs = min(len(spot_rates), len(forward_rates))
    n_cur = len(spot_rates[0]) if spot_rates else 0
    forward_discounts: list[list[float]] = []
    for t in range(t_obs - 1):
        month_fd: list[float] = []
        for j in range(n_cur):
            s_curr = spot_rates[t][j]
            f_curr = forward_rates[t][j]
            fd = math.log(max(1e-6, f_curr)) - math.log(max(1e-6, s_curr))
            month_fd.append(round(fd, 6))
        forward_discounts.append(month_fd)
    return forward_discounts


def sort_carry_portfolios(
    excess_returns: list[list[float]],
    forward_discounts: list[list[float]],
    n_portfolios: int = 5,
) -> dict[str, Any]:
    # BUG: No input validation
    t_ret = len(excess_returns)
    n_cur = len(excess_returns[0]) if excess_returns else 0

    portfolio_returns: list[list[float]] = []
    for t in range(t_ret):
        fds = forward_discounts[t]
        rxs = excess_returns[t]
        ranked_indices = sorted(range(n_cur), key=lambda j: fds[j], reverse=True)
        p_rets: list[float] = [0.0] * n_portfolios
        p_counts: list[int] = [0] * n_portfolios
        for rank_pos, cur_idx in enumerate(ranked_indices):
            bucket = min(int(rank_pos * n_portfolios / max(1, n_cur)), n_portfolios - 1)
            p_rets[bucket] += rxs[cur_idx]
            p_counts[bucket] += 1
        month_p = [round(p_rets[k] / max(1, p_counts[k]), 6) for k in range(n_portfolios)]
        portfolio_returns.append(month_p)

    mean_returns: list[float] = []
    std_returns: list[float] = []
    sharpe_ratios: list[float] = []
    for k in range(n_portfolios):
        k_rets = [portfolio_returns[t][k] for t in range(t_ret)]
        m_ret = sum(k_rets) / max(1, t_ret)
        var_ret = sum((r - m_ret) ** 2 for r in k_rets) / max(1, t_ret - 1) if t_ret > 1 else 0.0
        s_ret = math.sqrt(max(0.0, var_ret))
        ann_mean = m_ret * 12.0
        ann_std = s_ret * math.sqrt(12.0)
        ann_sr = (ann_mean / ann_std) if ann_std > 1e-8 else 0.0
        mean_returns.append(round(ann_mean, 5))
        std_returns.append(round(ann_std, 5))
        sharpe_ratios.append(round(ann_sr, 4))

    return {
        "portfolio_returns": portfolio_returns,
        "mean_returns": mean_returns,
        "std_returns": std_returns,
        "sharpe_ratios": sharpe_ratios,
    }


def build_factors(portfolio_returns: list[list[float]]) -> dict[str, list[float]]:
    # BUG: No input validation
    if not portfolio_returns:
        return {"dollar_factor": [], "hml_fx": []}
    t_obs = len(portfolio_returns)
    k_ports = len(portfolio_returns[0])
    dollar_factor: list[float] = []
    hml_fx: list[float] = []
    for t in range(t_obs):
        p_row = portfolio_returns[t]
        dol_val = sum(p_row) / max(1, k_ports)
        hml_val = p_row[-1] - p_row[0]
        dollar_factor.append(round(dol_val, 6))
        hml_fx.append(round(hml_val, 6))
    return {"dollar_factor": dollar_factor, "hml_fx": hml_fx}


def estimate_volatility_innovations(
    daily_returns: list[list[float]],
    days_per_month: int = 21,
) -> dict[str, Any]:
    # BUG: No input validation
    if not daily_returns:
        return {"monthly_vol": [], "ar1_rho": 0.0, "ar1_const": 0.0, "vol_innovations": []}
    total_days = len(daily_returns)
    n_cur = len(daily_returns[0])
    m_months = total_days // max(1, days_per_month)
    if m_months < 2:
        return {"monthly_vol": [], "ar1_rho": 0.0, "ar1_const": 0.0, "vol_innovations": []}
    daily_vol: list[float] = []
    for day_row in daily_returns:
        mean_abs = sum(abs(r) for r in day_row) / max(1, n_cur)
        daily_vol.append(mean_abs)
    monthly_vol: list[float] = []
    for m in range(m_months):
        start_d = m * days_per_month
        end_d = start_d + days_per_month
        m_vol = sum(daily_vol[start_d:end_d]) / max(1, days_per_month)
        monthly_vol.append(round(m_vol, 6))
    y_vec = monthly_vol[1:]
    x_mat = [[monthly_vol[i]] for i in range(m_months - 1)]
    coeffs, fitted, _ = _multivariate_ols(x_mat, y_vec, fit_intercept=True)
    ar1_const = round(coeffs[0], 6)
    ar1_rho = round(coeffs[1], 5)
    vol_innovations: list[float] = []
    for i in range(len(y_vec)):
        innov = y_vec[i] - fitted[i]
        vol_innovations.append(round(innov, 6))
    return {
        "monthly_vol": monthly_vol,
        "ar1_rho": ar1_rho,
        "ar1_const": ar1_const,
        "vol_innovations": vol_innovations,
    }


def fama_macbeth_twostep(
    portfolio_returns: list[list[float]],
    factor_matrix: list[list[float]],
    factor_names: list[str],
) -> dict[str, Any]:
    # BUG: No input validation
    t_obs = len(portfolio_returns)
    k_ports = len(portfolio_returns[0]) if portfolio_returns else 0
    len(factor_matrix[0]) if factor_matrix else 0
    betas: list[list[float]] = []
    mean_excess_returns: list[float] = []
    for k in range(k_ports):
        y_k = [portfolio_returns[t][k] for t in range(t_obs)]
        mean_excess_returns.append(sum(y_k) / max(1, t_obs))
        coeffs, _, _ = _multivariate_ols(factor_matrix, y_k, fit_intercept=True)
        k_betas = [round(c, 5) for c in coeffs[1:]]
        betas.append(k_betas)
    cs_coeffs, fitted_mean, r_squared = _multivariate_ols(betas, mean_excess_returns, fit_intercept=False)
    lambda_premia = [round(c, 6) for c in cs_coeffs]
    pricing_errors: list[float] = []
    for k in range(k_ports):
        alpha_k = mean_excess_returns[k] - fitted_mean[k]
        pricing_errors.append(round(alpha_k, 6))
    mape = round(sum(abs(a) for a in pricing_errors) / max(1, k_ports), 6)
    return {
        "factor_names": factor_names,
        "betas": betas,
        "lambda_premia": lambda_premia,
        "pricing_errors": pricing_errors,
        "r_squared": round(r_squared, 4),
        "mape": mape,
    }


def run_currency_factor_replication(instance: dict[str, Any]) -> dict[str, Any]:
    # BUG: No input validation
    spot_rates = instance.get("spot_rates", [[1.0, 1.0], [1.0, 1.0]])
    forward_rates = instance.get("forward_rates", [[1.0, 1.0], [1.0, 1.0]])
    daily_returns = instance.get("daily_returns", [[0.0, 0.0]] * 50)
    n_portfolios = instance.get("n_portfolios", 5)
    rx = compute_excess_returns(spot_rates, forward_rates)
    fd = compute_forward_discounts(spot_rates, forward_rates)
    carry_info = sort_carry_portfolios(rx, fd, n_portfolios=n_portfolios)
    port_rets = carry_info["portfolio_returns"]
    factors = build_factors(port_rets)
    dol = factors["dollar_factor"]
    hml = factors["hml_fx"]
    vol_info = estimate_volatility_innovations(daily_returns, days_per_month=21)
    vol_innov = vol_info["vol_innovations"]
    t_eval = min(len(port_rets), len(vol_innov)) if vol_innov else len(port_rets)
    eval_port_rets = port_rets[:t_eval]
    eval_dol = dol[:t_eval]
    eval_hml = hml[:t_eval]
    eval_vol_innov = vol_innov[:t_eval]
    x_lustig = [[eval_dol[t], eval_hml[t]] for t in range(t_eval)]
    lustig_pricing = fama_macbeth_twostep(eval_port_rets, x_lustig, factor_names=["DOL", "HML_FX"])
    x_menkhoff = [[eval_dol[t], eval_vol_innov[t]] for t in range(t_eval)]
    menkhoff_pricing = fama_macbeth_twostep(eval_port_rets, x_menkhoff, factor_names=["DOL", "VOL_INNOV"])
    return {
        "n_periods": len(spot_rates),
        "n_currencies": len(spot_rates[0]) if spot_rates else 0,
        "n_portfolios": n_portfolios,
        "carry_portfolios": carry_info,
        "factors": {
            "dollar_factor": dol,
            "hml_fx": hml,
            "monthly_vol": vol_info["monthly_vol"],
            "vol_innovations": vol_innov,
            "ar1_rho": vol_info["ar1_rho"],
            "ar1_const": vol_info["ar1_const"],
        },
        "lustig_model": lustig_pricing,
        "menkhoff_model": menkhoff_pricing,
    }
