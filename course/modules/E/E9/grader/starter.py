"""Starter skeleton for E9 Sovereign DSA and Fan Chart Engine.

Students implement the functions below adhering strictly to the specifications.
Standard library only.
"""

from __future__ import annotations


def debt_dynamics_step(b_prev: float, r: float, g: float, s: float) -> float:
    """Compute one-period exact discrete-time debt-to-GDP ratio."""
    raise NotImplementedError("Implement debt_dynamics_step")


def primary_gap(b_target: float, r: float, g: float, s_actual: float) -> float:
    """Compute primary gap s* - s required to stabilize debt at b_target."""
    raise NotImplementedError("Implement primary_gap")


def simulate_trajectory(
    b0: float,
    r_path: list[float],
    g_path: list[float],
    s_path: list[float],
) -> list[float]:
    """Deterministically simulate debt-to-GDP trajectory from t=0 to t=H."""
    raise NotImplementedError("Implement simulate_trajectory")


def compute_fan_chart(
    trajectories: list[list[float]],
    percentiles: list[float],
) -> dict[float, list[float]]:
    """Compute percentile curves across simulated paths for each period t in 0..H."""
    raise NotImplementedError("Implement compute_fan_chart")


def breach_probability(trajectories: list[list[float]], debt_ceiling: float) -> float:
    """Compute empirical probability of exceeding debt_ceiling at any point across horizon."""
    raise NotImplementedError("Implement breach_probability")


def dsa_summary(instance_data: dict[str, object]) -> dict[str, object]:
    """Execute complete DSA pipeline on instance dictionary."""
    raise NotImplementedError("Implement dsa_summary")
