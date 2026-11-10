"""Lab X1-project-1: Rung 1 worked example for Meese-Rogoff re-run.

Replays the out-of-sample forecasting horse race comparing a driftless random walk
against macroeconomic fundamentals and UIP models across 1, 3, and 12-month horizons.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic problem instance for the X1 project."""
    rng = random.Random(seed)
    n_obs = 120 + (seed * 11) % 41
    initial_price = round(1.10 + ((seed * 7) % 30) * 0.01, 4)
    log_s0 = math.log(initial_price)
    window_size = 36
    horizons = [1, 3, 12]

    rho_f = round(0.92 + (seed % 6) * 0.01, 3)
    sigma_f = 0.02
    f_series: list[float] = [round(rng.gauss(0.0, 0.05), 4)]
    for _ in range(1, n_obs):
        f_next = rho_f * f_series[-1] + rng.gauss(0.0, sigma_f)
        f_series.append(round(f_next, 4))

    i_diff_series: list[float] = []
    for t in range(n_obs):
        diff = round(0.0015 * f_series[t] + rng.gauss(0.001, 0.0008), 5)
        i_diff_series.append(diff)

    beta_true = round(0.12 + (seed % 5) * 0.03, 3)
    sigma_s = 0.03
    s_series: list[float] = [round(log_s0, 4)]
    for t in range(1, n_obs):
        shock = rng.gauss(0.0, sigma_s)
        f_delta = f_series[t] - f_series[t - 1]
        ds = beta_true * f_delta + shock
        s_next = s_series[-1] + ds
        s_series.append(round(s_next, 4))

    return {
        "seed": seed,
        "n_obs": n_obs,
        "initial_price": initial_price,
        "window_size": window_size,
        "horizons": horizons,
        "s_series": s_series,
        "f_series": f_series,
        "i_diff_series": i_diff_series,
    }


def rolling_forecast_rw(s_series: list[float], horizon: int, window_size: int) -> list[float]:
    """Compute out-of-sample driftless random walk forecasts E_t[s_{t+h}] = s_t."""
    n = len(s_series)
    return [round(s_series[t], 6) for t in range(window_size, n - horizon)]


def rolling_forecast_fundamentals(
    s_series: list[float],
    f_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
    """Compute rolling OLS monetary fundamentals forecasts using realized fundamentals."""
    n = len(s_series)
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
    """Compute out-of-sample UIP forecasts E_t[s_{t+h}] = s_t + h * (i_t - i*_t)."""
    n = len(s_series)
    return [round(s_series[t] + float(horizon) * i_diff_series[t], 6) for t in range(window_size, n - horizon)]


def compute_metrics(actual: list[float], predicted: list[float]) -> dict[str, float]:
    """Compute RMSE and MAE."""
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
    """Compute Diebold-Mariano test statistic with Bartlett HAC adjustment."""
    t_eval = len(actual)
    d = [(a - pm) ** 2 - (a - pb) ** 2 for a, pm, pb in zip(actual, pred_model, pred_bench, strict=True)]
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
    """Execute the complete Meese-Rogoff horse race across all horizons."""
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

        u_fund = round(f_metrics["rmse"] / rw_metrics["rmse"], 4)
        u_uip = round(uip_metrics["rmse"] / rw_metrics["rmse"], 4)
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


def run_worked_example() -> None:
    print("Step 1 | Generating problem instance (seed 42, N=130 observations)")
    inst = make_instance(42)
    s_series = inst["s_series"]
    f_series = inst["f_series"]
    horizons = inst["horizons"]
    window = inst["window_size"]

    print(
        f"Step 1 | Time series generated: S_0 = {inst['initial_price']:.4f}, W = {window} months, Horizons = {horizons}"
    )
    print(f"       | Series length: {len(s_series)} months, Fundamentals length: {len(f_series)} months")

    # Step 2: Execute full horse race
    res = run_meese_rogoff(inst)
    results = res["results"]

    print("\nStep 2 | Out-of-Sample Forecasting Horse Race Results:")
    print("Horizon | Eval Obs | RW RMSE | Fund RMSE | Fund Theil's U | Fund DM Stat | UIP Theil's U")
    print("-----------------------------------------------------------------------------------------")

    for h in horizons:
        hr = results[h]
        print(
            f"{h:>2d} mo   | {hr['eval_count']:>8d} | {hr['rw_rmse']:>7.4f} | {hr['fund_rmse']:>9.4f} | "
            f"{hr['fund_theil_u']:>14.4f} | {hr['fund_dm_stat']:>12.2f} | {hr['uip_theil_u']:>13.4f}"
        )

    print("\nStep 3 | Synthesis and Meese-Rogoff Verification:")
    h1 = results[1]
    h12 = results[12]
    u1 = h1["fund_theil_u"]
    u12 = h12["fund_theil_u"]
    rw_wins_1m = u1 > 1.0
    rw_wins_12m = u12 > 1.0
    print(f"       | 1-Month Horizon: Random Walk Beats Fundamentals (Theil's U = {u1:.4f} > 1.0): {rw_wins_1m}")
    print(f"       | 12-Month Horizon: Random Walk Beats Fundamentals (Theil's U = {u12:.4f} > 1.0): {rw_wins_12m}")


def main() -> None:
    run_worked_example()


main()
