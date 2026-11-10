"""Starter template for PM1: Private Equity (PME Engine).

Implement the benchmarking functions below to pass the autograder suite:
- compute_irr
- compute_moic
- compute_ks_pme
- compute_direct_alpha
- compute_long_nickels_pme
- evaluate_fund
"""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_irr(times: np.ndarray, cash_flows: np.ndarray) -> float:
    """Compute the annualized internal rate of return (IRR) for irregular cash flows."""
    raise NotImplementedError("compute_irr is not yet implemented")


def compute_moic(calls: np.ndarray, distributions: np.ndarray, nav: float) -> tuple[float, float, float]:
    """Compute Multiple on Invested Capital (MOIC) metrics (DPI, RVPI, TVPI)."""
    raise NotImplementedError("compute_moic is not yet implemented")


def compute_ks_pme(
    times: np.ndarray,
    calls: np.ndarray,
    distributions: np.ndarray,
    nav: float,
    benchmark_prices: np.ndarray,
) -> float:
    """Compute Kaplan & Schoar (2005) Public Market Equivalent (KS-PME)."""
    raise NotImplementedError("compute_ks_pme is not yet implemented")


def compute_direct_alpha(
    times: np.ndarray,
    calls: np.ndarray,
    distributions: np.ndarray,
    nav: float,
    benchmark_prices: np.ndarray,
) -> float:
    """Compute Gredil, Griffiths & Stucke (2014) Direct Alpha."""
    raise NotImplementedError("compute_direct_alpha is not yet implemented")


def compute_long_nickels_pme(
    times: np.ndarray,
    calls: np.ndarray,
    distributions: np.ndarray,
    benchmark_prices: np.ndarray,
) -> tuple[float, np.ndarray, bool]:
    """Compute Long & Nickels (1996) index replication PME."""
    raise NotImplementedError("compute_long_nickels_pme is not yet implemented")


def evaluate_fund(instance: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a complete fund cash flow instance across all private equity benchmarks."""
    raise NotImplementedError("evaluate_fund is not yet implemented")
