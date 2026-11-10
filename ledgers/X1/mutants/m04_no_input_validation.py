"""Mutant: Omits all parameter validation and fails to raise ValueError on non-positive horizons or window sizes."""

from __future__ import annotations

import math
from typing import Any


def rolling_forecast_rw(s_series: list[float], horizon: int, window_size: int) -> list[float]:
    # BUG: No input validation
    n = len(s_series)
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
    # BUG: No input validation
    n = len(s_series)
    forecasts: list[float] = []
    for t in range(window_size, n - horizon):
        s_win = s_series[t - window_size : t]
        f_win = f_series[t - window_size : t]
        mean_s = sum(s_win) / (window_size if window_size > 0 else 1)
        mean_f = sum(f_win) / (window_size if window_size > 0 else 1)
        var_f = sum((f - mean_f) ** 2 for f in f_win)
        cov_sf = sum((f - mean_f) * (s - mean_s) for s, f in zip(s_win, f_win, strict=False))
        beta_hat = cov_sf / var_f if var_f > 1e-12 else 0.0
        alpha_hat = mean_s - beta_hat * mean_f
        pred = alpha_hat + beta_hat * f_series[min(t + horizon, len(f_series) - 1)]
        forecasts.append(round(pred, 6))
    return forecasts


def rolling_forecast_uip(
    s_series: list[float],
    i_diff_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
    # BUG: No input validation
    n = len(s_series)
    forecasts: list[float] = []
    for t in range(window_size, n - horizon):
        pred = s_series[t] + float(horizon) * i_diff_series[min(t, len(i_diff_series) - 1)]
        forecasts.append(round(pred, 6))
    return forecasts


def compute_metrics(actual: list[float], predicted: list[float]) -> dict[str, float]:
    m = len(actual) if actual else 1
    sse = sum((a - p) ** 2 for a, p in zip(actual, predicted, strict=False))
    sae = sum(abs(a - p) for a, p in zip(actual, predicted, strict=False))
    return {"rmse": round(math.sqrt(sse / m), 6), "mae": round(sae / m, 6)}


def compute_diebold_mariano(
    actual: list[float],
    pred_model: list[float],
    pred_bench: list[float],
    horizon: int,
) -> float:
    t_eval = len(actual) if actual else 1
    d = [(a - pm) ** 2 - (a - pb) ** 2 for a, pm, pb in zip(actual, pred_model, pred_bench, strict=False)]
    mean_d = sum(d) / t_eval
    gamma: list[float] = []
    max_lag = max(1, horizon - 1)
    for k in range(max_lag + 1):
        if k == 0:
            g = sum((val - mean_d) ** 2 for val in d) / t_eval
        else:
            g = sum((d[t] - mean_d) * (d[t - k] - mean_d) for t in range(k, t_eval)) / t_eval
        gamma.append(g)
    lr_var = gamma[0]
    if horizon > 1:
        for k in range(1, horizon):
            weight = 1.0 - (k / float(horizon))
            lr_var += 2.0 * weight * gamma[k]
    variance_dbar = lr_var / t_eval
    if variance_dbar <= 1e-12:
        return 0.0
    return round(mean_d / math.sqrt(variance_dbar), 4)


def run_meese_rogoff(instance: dict[str, Any]) -> dict[str, Any]:
    # BUG: No input validation
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
            "fund_theil_u": round(f_metrics["rmse"] / rw_metrics["rmse"], 4) if rw_metrics["rmse"] > 0 else 1.0,
            "fund_dm_stat": compute_diebold_mariano(actual, f_preds, rw_preds, h),
            "uip_rmse": uip_metrics["rmse"],
            "uip_mae": uip_metrics["mae"],
            "uip_theil_u": round(uip_metrics["rmse"] / rw_metrics["rmse"], 4) if rw_metrics["rmse"] > 0 else 1.0,
            "uip_dm_stat": compute_diebold_mariano(actual, uip_preds, rw_preds, h),
        }
    return {
        "seed": int(instance.get("seed", 0)),
        "n_obs": n_obs,
        "window_size": window_size,
        "horizons": horizons,
        "results": results_by_horizon,
    }
