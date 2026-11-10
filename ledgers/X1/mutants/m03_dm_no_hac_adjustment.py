"""Mutant: Diebold-Mariano test ignores Bartlett HAC autocovariance adjustments for horizons h > 1."""

from __future__ import annotations

import math
from typing import Any


def rolling_forecast_rw(s_series: list[float], horizon: int, window_size: int) -> list[float]:
    if horizon <= 0:
        raise ValueError("horizon must be positive integer")
    if window_size < 10:
        raise ValueError("window_size must be at least 10")
    n = len(s_series)
    if n <= window_size + horizon:
        raise ValueError("insufficient observations for rolling forecast")

    forecasts: list[float] = []
    for t in range(window_size, n - horizon):
        forecasts.append(round(s_series[t], 6))
    return forecasts


def rolling_forecast_fundamentals(
    s_series: list[float],
    f_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
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
        s_win = s_series[t - window_size : t]
        f_win = f_series[t - window_size : t]
        mean_s = sum(s_win) / window_size
        mean_f = sum(f_win) / window_size
        var_f = sum((f - mean_f) ** 2 for f in f_win)
        cov_sf = sum((f - mean_f) * (s - mean_s) for s, f in zip(s_win, f_win, strict=True))
        beta_hat = cov_sf / var_f if var_f > 1e-12 else 0.0
        alpha_hat = mean_s - beta_hat * mean_f
        pred = alpha_hat + beta_hat * f_series[t + horizon]
        forecasts.append(round(pred, 6))
    return forecasts


def rolling_forecast_uip(
    s_series: list[float],
    i_diff_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
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
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted series must have equal length")
    if not actual:
        raise ValueError("series cannot be empty")
    m = len(actual)
    sse = sum((a - p) ** 2 for a, p in zip(actual, predicted, strict=True))
    sae = sum(abs(a - p) for a, p in zip(actual, predicted, strict=True))
    return {"rmse": round(math.sqrt(sse / m), 6), "mae": round(sae / m, 6)}


def compute_diebold_mariano(
    actual: list[float],
    pred_model: list[float],
    pred_bench: list[float],
    horizon: int,
) -> float:
    if len(actual) != len(pred_model) or len(actual) != len(pred_bench):
        raise ValueError("series lengths must match")
    t_eval = len(actual)
    if t_eval < 5:
        raise ValueError("insufficient evaluation observations for DM test")
    d = [(a - pm) ** 2 - (a - pb) ** 2 for a, pm, pb in zip(actual, pred_model, pred_bench, strict=True)]
    mean_d = sum(d) / t_eval
    # BUG: uses gamma_0 only, ignores autocovariance / HAC adjustments for h > 1
    gamma_0 = sum((val - mean_d) ** 2 for val in d) / t_eval
    variance_dbar = gamma_0 / t_eval
    if variance_dbar <= 1e-12:
        return 0.0
    return round(mean_d / math.sqrt(variance_dbar), 4)


def run_meese_rogoff(instance: dict[str, Any]) -> dict[str, Any]:
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
        actual = [s_series[t + h] for t in range(window_size, n_obs - h)]
        rw_preds = rolling_forecast_rw(s_series, h, window_size)
        f_preds = rolling_forecast_fundamentals(s_series, f_series, h, window_size)
        uip_preds = rolling_forecast_uip(s_series, i_diff_series, h, window_size)
        rw_metrics = compute_metrics(actual, rw_preds)
        f_metrics = compute_metrics(actual, f_preds)
        uip_metrics = compute_metrics(actual, uip_preds)
        results_by_horizon[h] = {
            "eval_count": len(actual),
            "rw_rmse": rw_metrics["rmse"],
            "rw_mae": rw_metrics["mae"],
            "fund_rmse": f_metrics["rmse"],
            "fund_mae": f_metrics["mae"],
            "fund_theil_u": round(f_metrics["rmse"] / rw_metrics["rmse"], 4),
            "fund_dm_stat": compute_diebold_mariano(actual, f_preds, rw_preds, h),
            "uip_rmse": uip_metrics["rmse"],
            "uip_mae": uip_metrics["mae"],
            "uip_theil_u": round(uip_metrics["rmse"] / rw_metrics["rmse"], 4),
            "uip_dm_stat": compute_diebold_mariano(actual, uip_preds, rw_preds, h),
        }
    return {
        "seed": int(instance["seed"]),
        "n_obs": n_obs,
        "window_size": window_size,
        "horizons": horizons,
        "results": results_by_horizon,
    }
