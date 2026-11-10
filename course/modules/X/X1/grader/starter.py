"""Starter template for X1 project: Meese-Rogoff re-run (meese_rogoff.py).

Implement rolling_forecast_rw, rolling_forecast_fundamentals, rolling_forecast_uip,
compute_metrics, compute_diebold_mariano, and run_meese_rogoff.
"""

from __future__ import annotations

from typing import Any


def rolling_forecast_rw(s_series: list[float], horizon: int, window_size: int) -> list[float]:
    """Compute out-of-sample driftless random-walk forecasts."""
    raise NotImplementedError("Student implementation required.")


def rolling_forecast_fundamentals(
    s_series: list[float],
    f_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
    """Compute out-of-sample macroeconomic fundamentals regression forecasts."""
    raise NotImplementedError("Student implementation required.")


def rolling_forecast_uip(
    s_series: list[float],
    i_diff_series: list[float],
    horizon: int,
    window_size: int,
) -> list[float]:
    """Compute out-of-sample uncovered interest parity forecasts."""
    raise NotImplementedError("Student implementation required.")


def compute_metrics(actual: list[float], predicted: list[float]) -> dict[str, float]:
    """Compute Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE)."""
    raise NotImplementedError("Student implementation required.")


def compute_diebold_mariano(
    actual: list[float],
    pred_model: list[float],
    pred_bench: list[float],
    horizon: int,
) -> float:
    """Compute the Diebold-Mariano test statistic."""
    raise NotImplementedError("Student implementation required.")


def run_meese_rogoff(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute the complete Meese-Rogoff horse race across all horizons."""
    raise NotImplementedError("Student implementation required.")
