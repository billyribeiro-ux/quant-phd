"""Starter template for the E7 Monetary-Shock Identification project (monetary_shocks.py).

Implement each function according to the specifications in project.html.
Do not modify the declared function signatures.
"""

from __future__ import annotations

from typing import Any


def calculate_fed_funds_surprise(f_post: float, f_pre: float, day: int, days_in_month: int) -> float:
    """Calculate the surprise component of a monetary policy rate decision from Fed funds futures.

    Per Kuttner (2001) and Gürkaynak, Sack, and Swanson (2005):
        Delta i^u = (M / (M - d)) * (f_post - f_pre)
    where M is days in the month and d is the day of the FOMC announcement.
    """
    raise NotImplementedError


def clean_high_frequency_surprises(announcements: list[dict[str, Any]], n_months: int) -> list[float]:
    """Aggregate event-window surprises into a clean monthly time series."""
    raise NotImplementedError


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
    raise NotImplementedError


def compare_monetary_shocks(shock_a: list[float], shock_b: list[float]) -> dict[str, float]:
    """Compute correlation, standard deviation ratio, and regression slope between two shock measures."""
    raise NotImplementedError


def test_information_effect(
    shock: list[float], yield_change: list[float], growth_revision: list[float]
) -> dict[str, float]:
    """Test for the Nakamura & Steinsson (2018) central bank information effect.

    Regresses economic forecast/growth revisions on policy surprises.
    A positive slope indicates that markets infer positive central bank private news about the economy.
    """
    raise NotImplementedError
