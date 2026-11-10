"""Starter template for AP4 Model Horse Race project."""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_twelve_moments(data: dict[str, np.ndarray]) -> dict[str, float]:
    """Compute the 12 canonical macro-finance data moments from simulation time series."""
    raise NotImplementedError("compute_twelve_moments not implemented")


def simulate_campbell_cochrane(params: dict[str, float], t_len: int, seed: int) -> dict[str, np.ndarray]:
    """Simulate the Campbell-Cochrane (1999) external habit model."""
    raise NotImplementedError("simulate_campbell_cochrane not implemented")


def simulate_bansal_yaron(params: dict[str, float], t_len: int, seed: int) -> dict[str, np.ndarray]:
    """Simulate the Bansal-Yaron (2004) long-run risks model."""
    raise NotImplementedError("simulate_bansal_yaron not implemented")


def simulate_barro_rietz(params: dict[str, float], t_len: int, seed: int) -> dict[str, np.ndarray]:
    """Simulate the Barro-Rietz (1988, 2006) rare disasters model."""
    raise NotImplementedError("simulate_barro_rietz not implemented")


def evaluate_model_scorecard(
    sim_moments: dict[str, float],
    target_moments: dict[str, float],
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Evaluate simulated moments against empirical target moments, computing scorecard metrics."""
    raise NotImplementedError("evaluate_model_scorecard not implemented")


def run_horse_race(instance: dict[str, Any]) -> dict[str, Any]:
    """Run full horse race comparing Campbell-Cochrane, Bansal-Yaron, and Barro-Rietz on 12 moments."""
    raise NotImplementedError("run_horse_race not implemented")
