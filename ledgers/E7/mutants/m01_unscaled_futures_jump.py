"""Mutant m01: Omits the month-scaling factor M / (M - d) in calculate_fed_funds_surprise.

Returns raw futures price jump (f_post - f_pre) without scaling for the timing of the announcement.
"""

from __future__ import annotations

import math
from typing import Any


def calculate_fed_funds_surprise(f_post: float, f_pre: float, day: int, days_in_month: int) -> float:
    if day < 1 or day > days_in_month:
        raise ValueError(f"Invalid meeting day {day} for month with {days_in_month} days")
    if day >= days_in_month:
        raise ValueError("Cannot scale current-month contract on or after the last day of the month")

    # BUG: Omit M / (M - d) scaling
    return f_post - f_pre


def clean_high_frequency_surprises(announcements: list[dict[str, Any]], n_months: int) -> list[float]:
    monthly = [0.0] * n_months
    for item in announcements:
        m = int(item["month_index"])
        if 0 <= m < n_months:
            d = int(item["day"])
            M = int(item["days_in_month"])
            f_post = float(item["f_post"])
            f_pre = float(item["f_pre"])
            surp = calculate_fed_funds_surprise(f_post, f_pre, d, M)
            monthly[m] += surp
    return monthly


def _ols_with_newey_west(
    y: list[float], X: list[list[float]], max_lags: int
) -> tuple[list[float], list[float]]:
    T = len(y)
    K = len(X[0])
    XtX = [[0.0] * K for _ in range(K)]
    Xty = [0.0] * K
    for t in range(T):
        for i in range(K):
            Xty[i] += X[t][i] * y[t]
            for j in range(K):
                XtX[i][j] += X[t][i] * X[t][j]

    aug = [[XtX[i][j] for j in range(K)] + [1.0 if i == j else 0.0 for j in range(K)] for i in range(K)]
    for col in range(K):
        pivot = col
        max_val = abs(aug[col][col])
        for row in range(col + 1, K):
            if abs(aug[row][col]) > max_val:
                max_val = abs(aug[row][col])
                pivot = row
        if max_val < 1e-12:
            raise ValueError("Singular matrix in OLS design")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        pivot_val = aug[col][col]
        for j in range(2 * K):
            aug[col][j] /= pivot_val
        for row in range(K):
            if row != col:
                factor = aug[row][col]
                for j in range(2 * K):
                    aug[row][j] -= factor * aug[col][j]

    invXtX = [[aug[i][K + j] for j in range(K)] for i in range(K)]
    beta = [sum(invXtX[i][j] * Xty[j] for j in range(K)) for i in range(K)]
    residuals = [y[t] - sum(X[t][j] * beta[j] for j in range(K)) for t in range(T)]

    S = [[0.0] * K for _ in range(K)]
    for t in range(T):
        e_t = residuals[t]
        for i in range(K):
            for j in range(K):
                S[i][j] += e_t * e_t * X[t][i] * X[t][j]

    for lag in range(1, max_lags + 1):
        weight = 1.0 - (lag / float(max_lags + 1))
        for t in range(lag, T):
            e_t = residuals[t]
            e_lag = residuals[t - lag]
            for i in range(K):
                for j in range(K):
                    term = e_t * e_lag * X[t][i] * X[t - lag][j]
                    S[i][j] += weight * (term + term if i == j else term)
                    if i != j:
                        S[j][i] += weight * term

    temp = [[sum(invXtX[i][k] * S[k][j] for k in range(K)) for j in range(K)] for i in range(K)]
    cov_matrix = [[sum(temp[i][k] * invXtX[k][j] for k in range(K)) for j in range(K)] for i in range(K)]
    se = [math.sqrt(max(1e-12, cov_matrix[i][i])) for i in range(K)]
    return beta, se


def estimate_local_projection(
    y: list[float],
    shock: list[float],
    controls: list[list[float]] | None,
    horizon: int,
    lags: int,
) -> tuple[list[float], list[float]]:
    if horizon < 0 or lags < 1 or len(y) != len(shock):
        raise ValueError("Invalid parameters")
    n = len(y)
    start_t = lags
    end_t = n - horizon
    betas: list[float] = []
    ses: list[float] = []
    for h in range(horizon + 1):
        target = [y[t + h] - y[t - 1] for t in range(start_t, end_t)]
        design = []
        for t in range(start_t, end_t):
            row = [1.0, shock[t]] + [y[t - p] for p in range(1, lags + 1)]
            if controls is not None:
                for c_series in controls:
                    row.append(c_series[t])
            design.append(row)
        b_vec, se_vec = _ols_with_newey_west(target, design, max_lags=h + 1)
        betas.append(b_vec[1])
        ses.append(se_vec[1])
    return betas, ses


def compare_monetary_shocks(shock_a: list[float], shock_b: list[float]) -> dict[str, float]:
    n = len(shock_a)
    mean_a = sum(shock_a) / n
    mean_b = sum(shock_b) / n
    cov = sum((shock_a[i] - mean_a) * (shock_b[i] - mean_b) for i in range(n)) / (n - 1)
    var_a = sum((shock_a[i] - mean_a) ** 2 for i in range(n)) / (n - 1)
    var_b = sum((shock_b[i] - mean_b) ** 2 for i in range(n)) / (n - 1)
    std_a = math.sqrt(var_a) if var_a > 1e-12 else 1e-6
    std_b = math.sqrt(var_b) if var_b > 1e-12 else 1e-6
    return {
        "correlation": cov / (std_a * std_b),
        "std_a": std_a,
        "std_b": std_b,
        "ratio_a_to_b": std_a / std_b,
        "slope_a_on_b": cov / var_b if var_b > 1e-12 else 0.0,
    }


def test_information_effect(
    shock: list[float], yield_change: list[float], growth_revision: list[float]
) -> dict[str, float]:
    n = len(shock)
    mean_s = sum(shock) / n
    mean_g = sum(growth_revision) / n
    cov_sg = sum((shock[i] - mean_s) * (growth_revision[i] - mean_g) for i in range(n)) / (n - 1)
    var_s = sum((shock[i] - mean_s) ** 2 for i in range(n)) / (n - 1)
    slope = cov_sg / var_s if var_s > 1e-12 else 0.0
    return {"information_slope": slope, "has_positive_information_effect": 1.0 if slope > 0.0 else 0.0}
