"""Starter template for Atlas A19 Systemic-Risk Monitor (`atlas.systemic`).

Students implement the functions and monitor class below to satisfy the contract.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def fit_linear_quantile_regression(
    y: np.ndarray[Any, Any],
    x: np.ndarray[Any, Any],
    q: float = 0.05,
) -> np.ndarray[Any, Any]:
    """Estimate linear quantile regression coefficients beta_q minimizing pinball loss."""
    raise NotImplementedError("fit_linear_quantile_regression is not implemented yet")


def compute_covar(
    r_system: np.ndarray[Any, Any],
    r_institution: np.ndarray[Any, Any],
    state_vars: np.ndarray[Any, Any] | None = None,
    alpha: float = 0.05,
) -> dict[str, float]:
    """Compute CoVaR, median CoVaR, and Delta-CoVaR for an institution."""
    raise NotImplementedError("compute_covar is not implemented yet")


def compute_mes(
    r_system: np.ndarray[Any, Any],
    r_institution: np.ndarray[Any, Any],
    alpha: float = 0.05,
) -> float:
    """Compute non-parametric Marginal Expected Shortfall (MES)."""
    raise NotImplementedError("compute_mes is not implemented yet")


def compute_lrmes(
    r_system: np.ndarray[Any, Any],
    r_institution: np.ndarray[Any, Any],
    alpha: float = 0.05,
    crisis_drop: float = 0.40,
) -> float:
    """Compute Long-Run Marginal Expected Shortfall (LRMES) over a multi-month crisis."""
    raise NotImplementedError("compute_lrmes is not implemented yet")


def compute_srisk(
    equity_value: float,
    debt_value: float,
    lrmes: float,
    prudential_ratio: float = 0.08,
) -> float:
    """Compute individual institution SRISK (conditional capital shortfall)."""
    raise NotImplementedError("compute_srisk is not implemented yet")


def compute_systemic_srisk_panel(
    equities: np.ndarray[Any, Any],
    debts: np.ndarray[Any, Any],
    lrmes_values: np.ndarray[Any, Any],
    prudential_ratio: float = 0.08,
) -> dict[str, Any]:
    """Compute multi-firm SRISK panel, total systemic SRISK, and percentage contributions."""
    raise NotImplementedError("compute_systemic_srisk_panel is not implemented yet")


def compute_network_clearing(
    nominal_liabilities: np.ndarray[Any, Any],
    external_assets: np.ndarray[Any, Any],
    senior_liabilities: np.ndarray[Any, Any] | None = None,
    max_iter: int = 1000,
    tol: float = 1e-10,
) -> dict[str, Any]:
    """Solve Eisenberg-Noe network clearing vectors and cascade propagation."""
    raise NotImplementedError("compute_network_clearing is not implemented yet")


class SystemicRiskMonitor:
    """Enterprise systemic risk monitor with configurable alert thresholds."""

    def __init__(self, thresholds: dict[str, float] | None = None) -> None:
        raise NotImplementedError("SystemicRiskMonitor.__init__ is not implemented yet")

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate systemic indicators against prudential thresholds."""
        raise NotImplementedError("SystemicRiskMonitor.evaluate is not implemented yet")
