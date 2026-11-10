"""Student error: adds intersection covariance instead of subtracting in two-way clustering (V_A + V_B + V_AB)."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import scipy.stats


def _validate_regression_inputs(x: list[list[float]], y: list[float]) -> tuple[np.ndarray, np.ndarray, int, int]:
    n = len(x)
    if n == 0:
        raise ValueError("Design matrix must not be empty.")
    k = len(x[0])
    if len(y) != n:
        raise ValueError(f"Length mismatch: len(y)={len(y)} != len(x)={n}.")
    if any(len(row) != k for row in x):
        raise ValueError("All rows of design matrix must have identical length.")
    if n <= k:
        raise ValueError(f"Insufficient observations: n={n} must be strictly greater than k={k}.")

    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    rank = int(np.linalg.matrix_rank(x_arr))
    if rank < k:
        raise ValueError(f"Design matrix does not have full column rank: rank={rank} < k={k}.")

    return x_arr, y_arr, n, k


def ols_beta(x: list[list[float]], y: list[float]) -> list[float]:
    x_arr, y_arr, _, _ = _validate_regression_inputs(x, y)
    xtx = x_arr.T @ x_arr
    xty = x_arr.T @ y_arr
    beta_hat = np.linalg.solve(xtx, xty)
    return [float(b) for b in beta_hat]


def se_classical(x: list[list[float]], y: list[float]) -> list[float]:
    x_arr, y_arr, n, k = _validate_regression_inputs(x, y)
    xtx = x_arr.T @ x_arr
    inv_xtx = np.linalg.inv(xtx)
    beta_hat = inv_xtx @ (x_arr.T @ y_arr)
    resid = y_arr - x_arr @ beta_hat
    rss = float(np.sum(resid**2))
    sigma2_hat = rss / (n - k)
    var_beta = sigma2_hat * inv_xtx
    return [float(math.sqrt(max(0.0, var_beta[j, j]))) for j in range(k)]


def se_white(x: list[list[float]], y: list[float]) -> list[float]:
    x_arr, y_arr, n, k = _validate_regression_inputs(x, y)
    xtx = x_arr.T @ x_arr
    inv_xtx = np.linalg.inv(xtx)
    beta_hat = inv_xtx @ (x_arr.T @ y_arr)
    resid = y_arr - x_arr @ beta_hat

    meat = np.zeros((k, k), dtype=float)
    for i in range(n):
        xi = x_arr[i : i + 1, :]
        meat += (resid[i] ** 2) * (xi.T @ xi)

    var_beta = inv_xtx @ meat @ inv_xtx
    return [float(math.sqrt(max(0.0, var_beta[j, j]))) for j in range(k)]


def se_newey_west(x: list[list[float]], y: list[float], lags: int) -> list[float]:
    x_arr, y_arr, n, k = _validate_regression_inputs(x, y)
    if not isinstance(lags, int) or lags < 0 or lags >= n:
        raise ValueError(f"lags must be an integer in [0, n - 1]; got {lags} with n={n}.")

    xtx = x_arr.T @ x_arr
    inv_xtx = np.linalg.inv(xtx)
    beta_hat = inv_xtx @ (x_arr.T @ y_arr)
    resid = y_arr - x_arr @ beta_hat

    omega = np.zeros((k, k), dtype=float)
    for t in range(n):
        xt = x_arr[t : t + 1, :]
        omega += (resid[t] ** 2) * (xt.T @ xt)

    for j in range(1, lags + 1):
        weight = 1.0 - (float(j) / (lags + 1.0))
        gamma_j = np.zeros((k, k), dtype=float)
        for t in range(j, n):
            xt = x_arr[t : t + 1, :]
            xt_prev = x_arr[t - j : t - j + 1, :]
            gamma_j += resid[t] * resid[t - j] * (xt.T @ xt_prev)
        omega += weight * (gamma_j + gamma_j.T)

    var_beta = inv_xtx @ omega @ inv_xtx
    return [float(math.sqrt(max(0.0, var_beta[j, j]))) for j in range(k)]


def _cluster_variance_matrix(
    x_arr: np.ndarray, resid: np.ndarray, inv_xtx: np.ndarray, cluster: list[Any]
) -> np.ndarray:
    k = x_arr.shape[1]
    cluster_scores: dict[Any, np.ndarray] = {}
    for i, g in enumerate(cluster):
        score_i = resid[i] * x_arr[i, :]
        if g not in cluster_scores:
            cluster_scores[g] = np.zeros(k, dtype=float)
        cluster_scores[g] += score_i

    meat = np.zeros((k, k), dtype=float)
    for s_g in cluster_scores.values():
        meat += np.outer(s_g, s_g)

    result: np.ndarray = np.asarray(inv_xtx @ meat @ inv_xtx, dtype=float)
    return result


def se_cluster(x: list[list[float]], y: list[float], cluster: list[Any]) -> list[float]:
    x_arr, y_arr, n, k = _validate_regression_inputs(x, y)
    if len(cluster) != n:
        raise ValueError(f"Cluster length mismatch: len(cluster)={len(cluster)} != n={n}.")

    xtx = x_arr.T @ x_arr
    inv_xtx = np.linalg.inv(xtx)
    beta_hat = inv_xtx @ (x_arr.T @ y_arr)
    resid = y_arr - x_arr @ beta_hat

    var_beta = _cluster_variance_matrix(x_arr, resid, inv_xtx, cluster)
    return [float(math.sqrt(max(0.0, var_beta[j, j]))) for j in range(k)]


def se_two_way(x: list[list[float]], y: list[float], cluster_a: list[Any], cluster_b: list[Any]) -> list[float]:
    x_arr, y_arr, n, k = _validate_regression_inputs(x, y)
    if len(cluster_a) != n or len(cluster_b) != n:
        raise ValueError("Cluster length mismatch with sample size n.")

    xtx = x_arr.T @ x_arr
    inv_xtx = np.linalg.inv(xtx)
    beta_hat = inv_xtx @ (x_arr.T @ y_arr)
    resid = y_arr - x_arr @ beta_hat

    v_a = _cluster_variance_matrix(x_arr, resid, inv_xtx, cluster_a)
    v_b = _cluster_variance_matrix(x_arr, resid, inv_xtx, cluster_b)

    joint_cluster = [(cluster_a[i], cluster_b[i]) for i in range(n)]
    v_ab = _cluster_variance_matrix(x_arr, resid, inv_xtx, joint_cluster)

    # Bug: adds v_ab instead of subtracting
    var_two_way = v_a + v_b + v_ab
    return [float(math.sqrt(max(0.0, var_two_way[j, j]))) for j in range(k)]


def t_critical(df: int) -> float:
    if df <= 0:
        raise ValueError(f"Degrees of freedom must be strictly positive; got {df}.")
    return float(scipy.stats.t.ppf(0.975, df))


def coverage(draws: list[dict[str, Any]], method: str, column: int) -> float:
    if not draws:
        return 0.0

    valid_methods = {"classical", "white", "newey_west", "cluster"}
    if method not in valid_methods:
        raise ValueError(f"Unknown method {method!r}; must be one of {valid_methods}.")

    covered_count = 0
    for draw in draws:
        x_d = draw["X"]
        y_d = draw["y"]
        beta_true = draw["beta_true"]
        n = len(x_d)
        k = len(x_d[0])
        df = n - k

        b_hat = ols_beta(x_d, y_d)
        if method == "classical":
            se = se_classical(x_d, y_d)
        elif method == "white":
            se = se_white(x_d, y_d)
        elif method == "newey_west":
            lags = draw.get("lags", 1)
            se = se_newey_west(x_d, y_d, lags=lags)
        elif method == "cluster":
            cl = draw["cluster_a"]
            se = se_cluster(x_d, y_d, cluster=cl)
        else:
            raise ValueError(f"Unknown method {method}")

        crit = t_critical(df)
        margin = crit * se[column]
        ci_lower = b_hat[column] - margin
        ci_upper = b_hat[column] + margin

        target = beta_true[column]
        if ci_lower <= target <= ci_upper:
            covered_count += 1

    return float(covered_count / len(draws))
