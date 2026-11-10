"""Starter implementation for Atlas A13 (atlas.term_premium).

Students complete each function according to the specifications in
atlas/A13.contract.md and the FI3 project page.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def fama_bliss_forward_rates(yields: np.ndarray, maturities: np.ndarray) -> np.ndarray:
    """Compute 1-year forward rates from zero-coupon yields."""
    raise NotImplementedError("Implement fama_bliss_forward_rates")


def excess_bond_returns(yields: np.ndarray, maturities: np.ndarray) -> np.ndarray:
    """Compute 1-year holding period excess log returns for annual maturities."""
    raise NotImplementedError("Implement excess_bond_returns")


def cochrane_piazzesi_factor(yields: np.ndarray, maturities: np.ndarray) -> dict[str, Any]:
    """Estimate the single-factor Cochrane-Piazzesi (2005) return predictability model."""
    raise NotImplementedError("Implement cochrane_piazzesi_factor")


def acm_term_premium(yields: np.ndarray, maturities: np.ndarray, num_factors: int = 3) -> dict[str, Any]:
    """Adrian, Crump & Moench (2013) 3-step linear regression affine term-structure model."""
    raise NotImplementedError("Implement acm_term_premium")


def carry_and_roll_down(yield_curve: np.ndarray, maturities: np.ndarray, horizon: float = 1.0) -> dict[str, np.ndarray]:
    """Decompose horizon bond return into carry and roll-down on a static yield curve."""
    raise NotImplementedError("Implement carry_and_roll_down")


def curve_trade_pnl_attribution(
    weights: np.ndarray,
    maturities: np.ndarray,
    yields_t0: np.ndarray,
    yields_t1: np.ndarray,
    dt: float,
    financing_rate: float,
) -> dict[str, float]:
    """Perform relative-value fixed-income P&L attribution for curve portfolios."""
    raise NotImplementedError("Implement curve_trade_pnl_attribution")
