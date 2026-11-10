"""Lab X1-project-2: Rung 2 completion problem for forecast evaluation metrics.

SIMULATED: generates sample actual and predicted series.
On the project page, the RMSE and Theil's U lines are blanked:
rmse_model = ___
rmse_bench = ___
theil_u = ___
The twin contains the complete solution.
"""

from __future__ import annotations

import math


def compute_metrics_and_theil_u(
    actual: list[float],
    pred_model: list[float],
    pred_bench: list[float],
) -> dict[str, float]:
    """Calculate RMSE, MAE, and Theil's U inequality coefficient."""
    m = len(actual)

    # 1. Compute RMSE for model and benchmark
    sse_model = sum((a - p) ** 2 for a, p in zip(actual, pred_model, strict=True))
    sse_bench = sum((a - p) ** 2 for a, p in zip(actual, pred_bench, strict=True))

    rmse_model = math.sqrt(sse_model / m)
    rmse_bench = math.sqrt(sse_bench / m)

    # 2. Compute Theil's U = RMSE_model / RMSE_benchmark
    theil_u = rmse_model / rmse_bench

    # 3. Compute MAE
    mae_model = sum(abs(a - p) for a, p in zip(actual, pred_model, strict=True)) / m
    mae_bench = sum(abs(a - p) for a, p in zip(actual, pred_bench, strict=True)) / m

    return {
        "rmse_model": round(rmse_model, 6),
        "rmse_bench": round(rmse_bench, 6),
        "theil_u": round(theil_u, 4),
        "mae_model": round(mae_model, 6),
        "mae_bench": round(mae_bench, 6),
    }


def main() -> None:
    print("Lab X1-project-2 | Forecast Evaluation Metrics (Rung 2 Completion Problem)")
    print("--------------------------------------------------------------------------")

    # Sample evaluation vectors (10 observations)
    actual = [1.0850, 1.0920, 1.0880, 1.1010, 1.0950, 1.0890, 1.0970, 1.1050, 1.0990, 1.1020]
    pred_rw = [1.0820, 1.0850, 1.0920, 1.0880, 1.1010, 1.0950, 1.0890, 1.0970, 1.1050, 1.0990]
    pred_fund = [1.0790, 1.0810, 1.0990, 1.0820, 1.1080, 1.1020, 1.0810, 1.1120, 1.0910, 1.1110]

    res = compute_metrics_and_theil_u(actual, pred_fund, pred_rw)

    print(f"Random Walk Benchmark RMSE:       {res['rmse_bench']:.6f}")
    print(f"Fundamentals Model RMSE:          {res['rmse_model']:.6f}")
    print(f"Theil's U (Model RMSE / RW RMSE): {res['theil_u']:.4f}")
    print(f"Random Walk Benchmark MAE:        {res['mae_bench']:.6f}")
    print(f"Fundamentals Model MAE:           {res['mae_model']:.6f}")
    print(f"Random Walk Outperforms Model:    {res['theil_u'] > 1.0}")


main()
