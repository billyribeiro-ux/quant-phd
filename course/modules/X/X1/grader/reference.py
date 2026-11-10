"""Reference solution for X1 project: Meese-Rogoff re-run (meese_rogoff.py).

Implements rolling out-of-sample exchange rate forecasting models, Theil's U statistics,
and Diebold-Mariano predictive accuracy tests comparing Random Walk against
macroeconomic fundamentals and UIP benchmarks.
"""

from __future__ import annotations

import math
from typing import Any


def rolling_forecast_rw(s_series: list[float], horizon: int, window_size: int) -> list[float]:
    """Compute out-of-sample driftless random-walk forecasts.

    For each evaluation period t from window_size to N - horizon, the forecast
    for s_{t+horizon} made at time t is s_t.

    Args:
        s_series: Log exchange rate time series s_t = ln(S_t).
        horizon: Forecast horizon h in months (>= 1).
        window_size: Rolling estimation window size W (>= 10).

    Returns:
        List of forecasted log exchange rates of length N - window_size - horizon + 1.
    """
    if horizon <= 0:
        raise ValueError("horizon must be positive integer")
    if window_size < 10:
        raise ValueError("window_size must be at least 10")
    n = len(s_series)
    if n <= window_size + horizon:
        raise ValueError("insufficient observations for rolling forecast")

    forecasts: list[float] = []
    for t in range(window_size, n - horizon):
        # Driftless random walk forecast: E_t[s_{t+h}] = s_t
        # Note: at index t, s_t is s_series[t]
        forecasts.append(round(s_series[t], 6))
    return forecasts


def rolling_forecast_fundamentals(
    s_series: list[float],
    f_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
    """Compute out-of-sample macroeconomic fundamentals regression forecasts.

    On each rolling window [t - window_size, t), fits OLS:
        s_tau = alpha + beta * f_tau + epsilon_tau
    and generates forecast for target t + horizon using realized fundamentals:
        s_hat_{t+horizon|t} = alpha_hat_t + beta_hat_t * f_{t+horizon}

    Args:
        s_series: Log exchange rate series.
        f_series: Fundamental variable series (money supply / output differential).
        horizon: Forecast horizon h in months (>= 1).
        window_size: Rolling window size W (>= 10).

    Returns:
        List of forecasts of length N - window_size - horizon + 1.
    """
    if horizon <= 0:
        raise ValueError("horizon must be positive integer")
    if window_size < 10:
        raise ValueError("window_size must be at least 10")
    if len(s_series) != len(f_series):
        raise ValueError("series lengths must match")
    n = len(s_series)
    if n <= window_size + horizon:
        raise ValueError("insufficient observations for rolling forecast")

    forecasts: list[float] = []
    for t in range(window_size, n - horizon):
        # Window observations: [t - window_size, t)
        s_win = s_series[t - window_size : t]
        f_win = f_series[t - window_size : t]

        mean_s = sum(s_win) / window_size
        mean_f = sum(f_win) / window_size

        var_f = sum((f - mean_f) ** 2 for f in f_win)
        cov_sf = sum((f - mean_f) * (s - mean_s) for s, f in zip(s_win, f_win, strict=True))

        beta_hat = cov_sf / var_f if var_f > 1e-12 else 0.0
        alpha_hat = mean_s - beta_hat * mean_f

        # Meese-Rogoff formulation: forecast using realized fundamental at t + horizon
        pred = alpha_hat + beta_hat * f_series[t + horizon]
        forecasts.append(round(pred, 6))

    return forecasts


def rolling_forecast_uip(
    s_series: list[float],
    i_diff_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
    """Compute out-of-sample uncovered interest parity (forward rate) forecasts.

    Under UIP, E_t[s_{t+h}] = s_t + h * (i_t - i_t^*).

    Args:
        s_series: Log exchange rate series.
        i_diff_series: Interest rate differential series (i_t - i_t^*) per period.
        horizon: Forecast horizon h in months (>= 1).
        window_size: Rolling window size W (>= 10).

    Returns:
        List of forecasts of length N - window_size - horizon + 1.
    """
    if horizon <= 0:
        raise ValueError("horizon must be positive integer")
    if window_size < 10:
        raise ValueError("window_size must be at least 10")
    if len(s_series) != len(i_diff_series):
        raise ValueError("series lengths must match")
    n = len(s_series)
    if n <= window_size + horizon:
        raise ValueError("insufficient observations for rolling forecast")

    forecasts: list[float] = []
    for t in range(window_size, n - horizon):
        pred = s_series[t] + float(horizon) * i_diff_series[t]
        forecasts.append(round(pred, 6))
    return forecasts


def compute_metrics(actual: list[float], predicted: list[float]) -> dict[str, float]:
    """Compute Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE).

    Args:
        actual: Realized actual values.
        predicted: Model predicted values.

    Returns:
        dict with keys 'rmse' and 'mae'.
    """
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted series must have equal length")
    if not actual:
        raise ValueError("series cannot be empty")

    m = len(actual)
    sse = sum((a - p) ** 2 for a, p in zip(actual, predicted, strict=True))
    sae = sum(abs(a - p) for a, p in zip(actual, predicted, strict=True))

    rmse = math.sqrt(sse / m)
    mae = sae / m
    return {"rmse": round(rmse, 6), "mae": round(mae, 6)}


def compute_diebold_mariano(
    actual: list[float],
    pred_model: list[float],
    pred_bench: list[float],
    horizon: int,
) -> float:
    """Compute the Diebold-Mariano test statistic for squared error loss differential.

    Loss differential:
        d_t = (y_t - y_hat_model,t)^2 - (y_t - y_hat_bench,t)^2
    Positive DM statistic indicates benchmark has lower loss (model performs worse).

    Args:
        actual: Realized actual values.
        pred_model: Model forecasts.
        pred_bench: Benchmark (e.g. Random Walk) forecasts.
        horizon: Forecast horizon h for HAC Bartlett lag weighting.

    Returns:
        DM test statistic (t-ratio).
    """
    if len(actual) != len(pred_model) or len(actual) != len(pred_bench):
        raise ValueError("series lengths must match")
    t_eval = len(actual)
    if t_eval < 5:
        raise ValueError("insufficient evaluation observations for DM test")

    d = [(a - pm) ** 2 - (a - pb) ** 2 for a, pm, pb in zip(actual, pred_model, pred_bench, strict=True)]
    mean_d = sum(d) / t_eval

    # Sample autocovariance gamma_k
    gamma: list[float] = []
    max_lag = max(1, horizon - 1)
    for k in range(max_lag + 1):
        if k == 0:
            g = sum((val - mean_d) ** 2 for val in d) / t_eval
        else:
            g = sum((d[t] - mean_d) * (d[t - k] - mean_d) for t in range(k, t_eval)) / t_eval
        gamma.append(g)

    # Long-run variance using Bartlett triangular kernel:
    # f_hat = gamma_0 + 2 * sum_{k=1}^{h-1} (1 - k / h) * gamma_k
    lr_var = gamma[0]
    if horizon > 1:
        for k in range(1, horizon):
            weight = 1.0 - (k / float(horizon))
            lr_var += 2.0 * weight * gamma[k]

    variance_dbar = lr_var / t_eval
    if variance_dbar <= 1e-12:
        return 0.0

    dm_stat = mean_d / math.sqrt(variance_dbar)
    return round(dm_stat, 4)


def run_meese_rogoff(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute the complete Meese-Rogoff horse race across all horizons.

    Args:
        instance: dict generated by make_instance(seed).

    Returns:
        dict containing metrics, Theil's U, and DM statistics for each horizon.
    """
    initial_price = float(instance.get("initial_price", 0.0))
    if initial_price <= 0.0:
        raise ValueError("initial_price must be positive")

    s_series = [float(x) for x in instance["s_series"]]
    f_series = [float(x) for x in instance["f_series"]]
    i_diff_series = [float(x) for x in instance["i_diff_series"]]
    window_size = int(instance["window_size"])
    horizons = [int(h) for h in instance["horizons"]]
    n_obs = len(s_series)

    results_by_horizon: dict[int, dict[str, Any]] = {}

    for h in horizons:
        # Ground truth realized values at evaluation points
        # For evaluation point t from window_size to n_obs - h: target is s_series[t + h]
        actual = [s_series[t + h] for t in range(window_size, n_obs - h)]

        rw_preds = rolling_forecast_rw(s_series, h, window_size)
        f_preds = rolling_forecast_fundamentals(s_series, f_series, h, window_size)
        uip_preds = rolling_forecast_uip(s_series, i_diff_series, h, window_size)

        rw_metrics = compute_metrics(actual, rw_preds)
        f_metrics = compute_metrics(actual, f_preds)
        uip_metrics = compute_metrics(actual, uip_preds)

        # Theil's U = RMSE_model / RMSE_RW
        u_fund = round(f_metrics["rmse"] / rw_metrics["rmse"], 4)
        u_uip = round(uip_metrics["rmse"] / rw_metrics["rmse"], 4)

        # DM test vs RW benchmark
        dm_fund = compute_diebold_mariano(actual, f_preds, rw_preds, h)
        dm_uip = compute_diebold_mariano(actual, uip_preds, rw_preds, h)

        results_by_horizon[h] = {
            "eval_count": len(actual),
            "rw_rmse": rw_metrics["rmse"],
            "rw_mae": rw_metrics["mae"],
            "fund_rmse": f_metrics["rmse"],
            "fund_mae": f_metrics["mae"],
            "fund_theil_u": u_fund,
            "fund_dm_stat": dm_fund,
            "uip_rmse": uip_metrics["rmse"],
            "uip_mae": uip_metrics["mae"],
            "uip_theil_u": u_uip,
            "uip_dm_stat": dm_uip,
        }

    return {
        "seed": int(instance["seed"]),
        "n_obs": n_obs,
        "window_size": window_size,
        "horizons": horizons,
        "results": results_by_horizon,
    }
