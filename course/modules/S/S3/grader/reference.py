"""Reference implementation for S3 project: Pairs-trading audit.

Implements econometric time series estimators using Python standard library:
- adf_t: Augmented Dickey-Fuller t-statistic with intercept
- alpha_beta: OLS regression of y on x with intercept
- trading_spread: out-of-sample trading spread using formation hedge ratio
- eg_t: Engle-Granger residual ADF test with no intercept
- half_life: mean-reversion half-life from AR(1) spread regression
- survives: cointegration survival verdict
"""

from __future__ import annotations

import math


def _validate_finite_list(vals: list[float], name: str = "series") -> None:
    if not vals:
        raise ValueError(f"{name} cannot be empty")
    for v in vals:
        if not math.isfinite(v):
            raise ValueError(f"Non-finite value {v} encountered in {name}")


def alpha_beta(y: list[float], x: list[float]) -> tuple[float, float]:
    """Estimate y = alpha + beta * x + e by ordinary least squares with intercept.

    Returns (alpha, beta).
    Raises ValueError if lengths differ or non-finite values are present.
    """
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
    """Solve A * x = b via Gaussian elimination with partial pivoting."""
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
    """Compute matrix inverse via Gauss-Jordan elimination."""
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
    """Compute the Augmented Dickey-Fuller t-statistic with an intercept:

    Delta y_t = alpha + gamma * y_{t-1} + sum_{j=1}^{lags} delta_j * Delta y_{t-j} + e_t.

    Returns the t-statistic of gamma: hat(gamma) / SE(hat(gamma)).
    Raises ValueError for negative lags or non-finite inputs.
    """
    if lags < 0:
        raise ValueError(f"lags must be non-negative, got {lags}")
    _validate_finite_list(series, "series")
    m = len(series)
    min_needed = lags + 3
    if m < min_needed:
        raise ValueError(f"Series length {m} too short for lags={lags} (needs at least {min_needed})")

    dy = [series[i] - series[i - 1] for i in range(1, m)]
    # Regression rows t from lags + 1 to m - 1
    # Y_t = dy[t-1]
    # Regressors: [1.0, series[t-1], dy[t-2], ..., dy[t-1-lags]]
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
    """Calculate the out-of-sample spread on the trading window [split, len(y)).

    Hedge ratio (alpha, beta) is estimated on the formation window [0, split).
    Returns [y[t] - alpha - beta * x[t] for t in range(split, len(y))].
    """
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
    """Compute the Engle-Granger cointegration test statistic:

    1. Fit formation regression y_t = alpha + beta * x_t + u_t for t in [0, split).
    2. Run ADF regression on formation residuals u_t with NO INTERCEPT:
       Delta u_t = gamma * u_{t-1} + sum_{j=1}^{lags} delta_j * Delta u_{t-j} + e_t.

    Returns the t-statistic of gamma: hat(gamma) / SE(hat(gamma)).
    """
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
        row = [u[t - 1]]
        for j in range(1, lags + 1):
            row.append(du[t - 1 - j])
        x_rows.append(row)

    n_obs = len(y_dep)
    k_vars = 1 + lags
    if n_obs <= k_vars:
        raise ValueError(f"Not enough observations ({n_obs}) for {k_vars} parameters")

    xtx = [[sum(x_rows[r][i] * x_rows[r][j] for r in range(n_obs)) for j in range(k_vars)] for i in range(k_vars)]
    xty = [sum(x_rows[r][i] * y_dep[r] for r in range(n_obs)) for i in range(k_vars)]

    beta_vec = _solve_symmetric_system(xtx, xty)
    inv_xtx = _matrix_inverse(xtx)

    residuals = [y_dep[r] - sum(x_rows[r][j] * beta_vec[j] for j in range(k_vars)) for r in range(n_obs)]
    rss = sum(res * res for res in residuals)
    sigma2 = rss / (n_obs - k_vars)
    var_gamma = sigma2 * inv_xtx[0][0]
    if var_gamma <= 0.0:
        raise ValueError("Estimated variance of gamma is non-positive")
    se_gamma = math.sqrt(var_gamma)
    return beta_vec[0] / se_gamma


def half_life(spread: list[float]) -> float:
    """Calculate the half-life of mean reversion from an AR(1) fit:

    s_t = c + phi * s_{t-1} + e_t.

    Returns:
    - ln(2) / (-ln(hat(phi))) for 0 < hat(phi) < 1 (in business days)
    - math.inf for hat(phi) >= 1 (unit root or explosive)
    Raises ValueError for hat(phi) <= 0 or non-finite inputs.
    """
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
    """Determine whether a pairs-trading candidate survives the econometric audit:

    Survives iff:
    1. eg_stat < eg_critical (rejects null of no cointegration at nominal level)
    2. math.isfinite(half_life_value) (trading spread is strictly mean-reverting)
    """
    return bool(eg_stat < eg_critical and math.isfinite(half_life_value))
