"""Reference solution for E7 Monetary-Shock Identification project."""

from __future__ import annotations

import math
from typing import Any


def calculate_fed_funds_surprise(f_post: float, f_pre: float, day: int, days_in_month: int) -> float:
    """Calculate the surprise component of a monetary policy rate decision from Fed funds futures.

    Per Kuttner (2001) and Gürkaynak, Sack, and Swanson (2005):
        Delta i^u = (M / (M - d)) * (f_post - f_pre)
    where M is days in the month and d is the day of the FOMC announcement.
    """
    if day < 1 or day > days_in_month:
        raise ValueError(f"Invalid meeting day {day} for month with {days_in_month} days")
    if day >= days_in_month:
        raise ValueError("Cannot scale current-month contract on or after the last day of the month")

    scale = days_in_month / float(days_in_month - day)
    return scale * (f_post - f_pre)


def clean_high_frequency_surprises(announcements: list[dict[str, Any]], n_months: int) -> list[float]:
    """Aggregate event-window surprises into a clean monthly time series."""
    monthly = [0.0] * n_months
    for item in announcements:
        m = int(item["month_index"])
        if 0 <= m < n_months:
            d = int(item["day"])
            days_in_month = int(item["days_in_month"])
            f_post = float(item["f_post"])
            f_pre = float(item["f_pre"])
            surp = calculate_fed_funds_surprise(f_post, f_pre, d, days_in_month)
            monthly[m] += surp
    return monthly


def _ols_with_newey_west(y: list[float], x: list[list[float]], max_lags: int) -> tuple[list[float], list[float]]:
    """Compute OLS coefficients and Newey-West (HAC) standard errors.

    y: vector of length t_obs
    x: t_obs x k_vars design matrix
    max_lags: bandwidth for Bartlett kernel
    """
    t_obs = len(y)
    k_vars = len(x[0])

    # Compute (X'X) and (X'y)
    xtx = [[0.0] * k_vars for _ in range(k_vars)]
    xty = [0.0] * k_vars

    for t in range(t_obs):
        for i in range(k_vars):
            xty[i] += x[t][i] * y[t]
            for j in range(k_vars):
                xtx[i][j] += x[t][i] * x[t][j]

    # Invert xtx using Gauss-Jordan elimination
    # Augmented matrix [xtx | I]
    aug = [[xtx[i][j] for j in range(k_vars)] + [1.0 if i == j else 0.0 for j in range(k_vars)] for i in range(k_vars)]
    for col in range(k_vars):
        pivot = col
        max_val = abs(aug[col][col])
        for row in range(col + 1, k_vars):
            if abs(aug[row][col]) > max_val:
                max_val = abs(aug[row][col])
                pivot = row
        if max_val < 1e-12:
            raise ValueError("Singular matrix in OLS design")
        aug[col], aug[pivot] = aug[pivot], aug[col]

        pivot_val = aug[col][col]
        for j in range(2 * k_vars):
            aug[col][j] /= pivot_val

        for row in range(k_vars):
            if row != col:
                factor = aug[row][col]
                for j in range(2 * k_vars):
                    aug[row][j] -= factor * aug[col][j]

    inv_xtx = [[aug[i][k_vars + j] for j in range(k_vars)] for i in range(k_vars)]

    # beta = inv(X'X) * X'y
    beta = [sum(inv_xtx[i][j] * xty[j] for j in range(k_vars)) for i in range(k_vars)]

    # Compute residuals e_t = y_t - X_t * beta
    residuals = [y[t] - sum(x[t][j] * beta[j] for j in range(k_vars)) for t in range(t_obs)]

    # Newey-West covariance matrix:
    # V = inv(X'X) * S * inv(X'X)
    # S = Gamma_0 + sum_{l=1}^L w_l (Gamma_l + Gamma_l')
    # Gamma_l = sum_{t=l+1}^T (e_t X_t') * (e_{t-l} X_{t-l})

    s_mat = [[0.0] * k_vars for _ in range(k_vars)]
    for t in range(t_obs):
        e_t = residuals[t]
        for i in range(k_vars):
            for j in range(k_vars):
                s_mat[i][j] += e_t * e_t * x[t][i] * x[t][j]

    for lag in range(1, max_lags + 1):
        weight = 1.0 - (lag / float(max_lags + 1))  # Bartlett kernel
        for t in range(lag, t_obs):
            e_t = residuals[t]
            e_lag = residuals[t - lag]
            for i in range(k_vars):
                for j in range(k_vars):
                    term = e_t * e_lag * x[t][i] * x[t - lag][j]
                    s_mat[i][j] += weight * (term + term if i == j else term)
                    if i != j:
                        s_mat[j][i] += weight * term

    # V = inv_xtx * s_mat * inv_xtx
    temp = [[sum(inv_xtx[i][k] * s_mat[k][j] for k in range(k_vars)) for j in range(k_vars)] for i in range(k_vars)]
    cov_matrix = [
        [sum(temp[i][k] * inv_xtx[k][j] for k in range(k_vars)) for j in range(k_vars)] for i in range(k_vars)
    ]

    se = [math.sqrt(max(1e-12, cov_matrix[i][i])) for i in range(k_vars)]
    return beta, se


def estimate_local_projection(
    y: list[float],
    shock: list[float],
    controls: list[list[float]] | None,
    horizon: int,
    lags: int,
) -> tuple[list[float], list[float]]:
    """Estimate Jordà (2005) local projections for impulse responses over horizons h = 0 .. H.

    Model:
        y_{t+h} - y_{t-1} = alpha^(h) + beta^(h) * shock_t + sum_{p=1}^lags gamma_p^(h) * y_{t-p} + controls + u_{t+h}
    """
    if horizon < 0:
        raise ValueError("Horizon must be non-negative")
    if lags < 1:
        raise ValueError("Lags must be at least 1")
    if len(y) != len(shock):
        raise ValueError("y and shock series must have equal length")

    n = len(y)
    start_t = lags
    end_t = n - horizon

    if end_t <= start_t:
        raise ValueError("Series length insufficient for given lags and horizon")

    betas: list[float] = []
    ses: list[float] = []

    for h in range(horizon + 1):
        # Target: y_{t+h} - y_{t-1}
        target: list[float] = []
        design: list[list[float]] = []

        for t in range(start_t, end_t):
            target_val = y[t + h] - y[t - 1]
            target.append(target_val)

            # Regressors: [1.0 (constant), shock_t, y_{t-1}, ..., y_{t-lags}]
            row = [1.0, shock[t]]
            for p in range(1, lags + 1):
                row.append(y[t - p])

            if controls is not None:
                for c_series in controls:
                    row.append(c_series[t])

            design.append(row)

        nw_lags = h + 1
        b_vec, se_vec = _ols_with_newey_west(target, design, max_lags=nw_lags)
        betas.append(b_vec[1])  # shock coefficient
        ses.append(se_vec[1])  # shock standard error

    return betas, ses


def compare_monetary_shocks(shock_a: list[float], shock_b: list[float]) -> dict[str, float]:
    """Compute correlation, standard deviation ratio, and regression slope between two shock measures."""
    if len(shock_a) != len(shock_b):
        raise ValueError("Shock series must have identical length")
    n = len(shock_a)
    if n < 2:
        raise ValueError("Shock series must contain at least 2 points")

    mean_a = sum(shock_a) / n
    mean_b = sum(shock_b) / n

    cov = sum((shock_a[i] - mean_a) * (shock_b[i] - mean_b) for i in range(n)) / (n - 1)
    var_a = sum((shock_a[i] - mean_a) ** 2 for i in range(n)) / (n - 1)
    var_b = sum((shock_b[i] - mean_b) ** 2 for i in range(n)) / (n - 1)

    std_a = math.sqrt(var_a) if var_a > 1e-12 else 1e-6
    std_b = math.sqrt(var_b) if var_b > 1e-12 else 1e-6

    corr = cov / (std_a * std_b)
    ratio = std_a / std_b
    slope = cov / var_b if var_b > 1e-12 else 0.0

    return {
        "correlation": corr,
        "std_a": std_a,
        "std_b": std_b,
        "ratio_a_to_b": ratio,
        "slope_a_on_b": slope,
    }


def test_information_effect(
    shock: list[float], yield_change: list[float], growth_revision: list[float]
) -> dict[str, float]:
    """Test for the Nakamura & Steinsson (2018) central bank information effect.

    Regresses economic forecast/growth revisions on policy surprises.
    A positive slope indicates that markets infer positive central bank private news about the economy.
    """
    if len(shock) != len(yield_change) or len(shock) != len(growth_revision):
        raise ValueError("All input series must have equal length")

    n = len(shock)
    mean_s = sum(shock) / n
    mean_g = sum(growth_revision) / n

    cov_sg = sum((shock[i] - mean_s) * (growth_revision[i] - mean_g) for i in range(n)) / (n - 1)
    var_s = sum((shock[i] - mean_s) ** 2 for i in range(n)) / (n - 1)

    slope = cov_sg / var_s if var_s > 1e-12 else 0.0
    is_info = 1.0 if slope > 0.0 else 0.0

    return {
        "information_slope": slope,
        "has_positive_information_effect": is_info,
    }
