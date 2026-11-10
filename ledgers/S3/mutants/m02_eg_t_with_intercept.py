"""eg_t erroneously includes an intercept in the residual ADF auxiliary regression"""

from __future__ import annotations

import math


def _validate_finite_list(vals: list[float], name: str = "series") -> None:
    if not vals:
        raise ValueError(f"{name} cannot be empty")
    for v in vals:
        if not math.isfinite(v):
            raise ValueError(f"Non-finite value {v} encountered in {name}")


def alpha_beta(y: list[float], x: list[float]) -> tuple[float, float]:
    if len(y) != len(x):
        raise ValueError(f"Length mismatch: len(y)={len(y)} != len(x)={len(x)}")
    _validate_finite_list(y, "y")
    _validate_finite_list(x, "x")
    m = len(y)
    if m < 2:
        raise ValueError("At least 2 observations required for OLS")
    mean_x = sum(x) / m
    mean_y = sum(y) / m
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(m))
    var_x = sum((x[i] - mean_x) ** 2 for i in range(m))
    if var_x == 0.0:
        raise ValueError("Variance of x is zero; cannot compute slope")
    beta = cov / var_x
    alpha = mean_y - beta * mean_x
    return alpha, beta


def _solve_symmetric_system(a_mat: list[list[float]], b_vec: list[float]) -> list[float]:
    k = len(b_vec)
    aug = [[*a_mat[i], b_vec[i]] for i in range(k)]
    for i in range(k):
        pivot = i
        max_val = abs(aug[i][i])
        for r in range(i + 1, k):
            if abs(aug[r][i]) > max_val:
                max_val = abs(aug[r][i])
                pivot = r
        if max_val == 0.0:
            raise ValueError("Singular matrix in normal equations")
        if pivot != i:
            aug[i], aug[pivot] = aug[pivot], aug[i]
        pivot_val = aug[i][i]
        for col in range(i, k + 1):
            aug[i][col] /= pivot_val
        for r in range(k):
            if r != i:
                factor = aug[r][i]
                for col in range(i, k + 1):
                    aug[r][col] -= factor * aug[i][col]
    return [aug[i][k] for i in range(k)]


def _matrix_inverse(a_mat: list[list[float]]) -> list[list[float]]:
    k = len(a_mat)
    aug = [[*a_mat[i], *(1.0 if i == j else 0.0 for j in range(k))] for i in range(k)]
    for i in range(k):
        pivot = i
        max_val = abs(aug[i][i])
        for r in range(i + 1, k):
            if abs(aug[r][i]) > max_val:
                max_val = abs(aug[r][i])
                pivot = r
        if max_val == 0.0:
            raise ValueError("Singular matrix in matrix inverse")
        if pivot != i:
            aug[i], aug[pivot] = aug[pivot], aug[i]
        pivot_val = aug[i][i]
        for col in range(i, 2 * k):
            aug[i][col] /= pivot_val
        for r in range(k):
            if r != i:
                factor = aug[r][i]
                for col in range(i, 2 * k):
                    aug[r][col] -= factor * aug[i][col]
    return [[aug[i][k + j] for j in range(k)] for i in range(k)]


def adf_t(series: list[float], lags: int) -> float:
    if lags < 0:
        raise ValueError(f"lags must be non-negative, got {lags}")
    _validate_finite_list(series, "series")
    m = len(series)
    min_needed = lags + 3
    if m < min_needed:
        raise ValueError(f"Series length {m} too short for lags={lags} (needs at least {min_needed})")

    dy = [series[i] - series[i - 1] for i in range(1, m)]
    y_dep: list[float] = []
    x_rows: list[list[float]] = []
    for t in range(lags + 1, m):
        y_dep.append(dy[t - 1])
        row = [1.0, series[t - 1]]
        for j in range(1, lags + 1):
            row.append(dy[t - 1 - j])
        x_rows.append(row)

    n_obs = len(y_dep)
    k_vars = 2 + lags
    if n_obs <= k_vars:
        raise ValueError(f"Not enough observations ({n_obs}) for {k_vars} parameters")

    xtx = [[sum(x_rows[r][i] * x_rows[r][j] for r in range(n_obs)) for j in range(k_vars)] for i in range(k_vars)]
    xty = [sum(x_rows[r][i] * y_dep[r] for r in range(n_obs)) for i in range(k_vars)]

    beta = _solve_symmetric_system(xtx, xty)
    inv_xtx = _matrix_inverse(xtx)

    residuals = [y_dep[r] - sum(x_rows[r][j] * beta[j] for j in range(k_vars)) for r in range(n_obs)]
    rss = sum(res * res for res in residuals)
    sigma2 = rss / (n_obs - k_vars)
    var_gamma = sigma2 * inv_xtx[1][1]
    if var_gamma <= 0.0:
        raise ValueError("Estimated variance of gamma is non-positive")
    se_gamma = math.sqrt(var_gamma)
    return beta[1] / se_gamma


def trading_spread(y: list[float], x: list[float], split: int) -> list[float]:
    if len(y) != len(x):
        raise ValueError(f"Length mismatch: len(y)={len(y)} != len(x)={len(x)}")
    _validate_finite_list(y, "y")
    _validate_finite_list(x, "x")
    n = len(y)
    min_obs = 30
    if split < min_obs or split > n - min_obs:
        raise ValueError(f"split={split} out of valid range [{min_obs}, {n - min_obs}]")

    alpha, beta = alpha_beta(y[:split], x[:split])
    return [y[t] - alpha - beta * x[t] for t in range(split, n)]


def eg_t(y: list[float], x: list[float], split: int, lags: int) -> float:
    if len(y) != len(x):
        raise ValueError(f"Length mismatch: len(y)={len(y)} != len(x)={len(x)}")
    if lags < 0:
        raise ValueError(f"lags must be non-negative, got {lags}")
    _validate_finite_list(y, "y")
    _validate_finite_list(x, "x")
    n = len(y)
    min_obs = 30
    if split < min_obs or split > n - min_obs:
        raise ValueError(f"split={split} out of valid range [{min_obs}, {n - min_obs}]")

    alpha, beta = alpha_beta(y[:split], x[:split])
    u = [y[t] - alpha - beta * x[t] for t in range(split)]
    m = len(u)
    du = [u[i] - u[i - 1] for i in range(1, m)]

    y_dep: list[float] = []
    x_rows: list[list[float]] = []
    for t in range(lags + 1, m):
        y_dep.append(du[t - 1])
        # BUG: includes an intercept in residual ADF regression
        row = [1.0, u[t - 1]]
        for j in range(1, lags + 1):
            row.append(du[t - 1 - j])
        x_rows.append(row)

    n_obs = len(y_dep)
    k_vars = 2 + lags
    if n_obs <= k_vars:
        raise ValueError(f"Not enough observations ({n_obs}) for {k_vars} parameters")

    xtx = [[sum(x_rows[r][i] * x_rows[r][j] for r in range(n_obs)) for j in range(k_vars)] for i in range(k_vars)]
    xty = [sum(x_rows[r][i] * y_dep[r] for r in range(n_obs)) for i in range(k_vars)]

    beta_vec = _solve_symmetric_system(xtx, xty)
    inv_xtx = _matrix_inverse(xtx)

    residuals = [y_dep[r] - sum(x_rows[r][j] * beta_vec[j] for j in range(k_vars)) for r in range(n_obs)]
    rss = sum(res * res for res in residuals)
    sigma2 = rss / (n_obs - k_vars)
    var_gamma = sigma2 * inv_xtx[1][1]
    if var_gamma <= 0.0:
        raise ValueError("Estimated variance of gamma is non-positive")
    se_gamma = math.sqrt(var_gamma)
    return beta_vec[1] / se_gamma


def half_life(spread: list[float]) -> float:
    _validate_finite_list(spread, "spread")
    m = len(spread)
    if m < 3:
        raise ValueError(f"Spread length {m} too short to estimate AR(1)")

    y = spread[1:]
    x = spread[:-1]
    _, phi = alpha_beta(y, x)

    if phi <= 0.0:
        raise ValueError(f"Estimated phi={phi} <= 0; half-life is undefined")
    if phi >= 1.0:
        return math.inf
    return math.log(2.0) / (-math.log(phi))


def survives(eg_stat: float, eg_critical: float, half_life_value: float) -> bool:
    return bool(eg_stat < eg_critical and math.isfinite(half_life_value))
