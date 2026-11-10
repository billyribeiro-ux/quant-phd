"""Starter implementation for FI6 Swaption-Cube Engine.

Provides skeleton signatures for multi-curve discounting, Black-76, Bachelier,
SABR calibration, surface interpolation, and swaption pricing.
Students complete the missing methods to satisfy the project requirements.
"""

from __future__ import annotations

from typing import Any


class MultiCurveDiscounting:
    """Multi-curve discount and projection curve framework (Starter Skeleton)."""

    def __init__(
        self,
        tenors: list[float],
        ois_zero_rates: list[float],
        proj_zero_rates: list[float],
    ) -> None:
        self.tenors = list(tenors)
        self.ois_zero_rates = list(ois_zero_rates)
        self.proj_zero_rates = list(proj_zero_rates)

    def discount_factor(self, t: float) -> float:
        """OIS discount factor P_D(0, t)."""
        raise NotImplementedError

    def projection_factor(self, t: float) -> float:
        """Projection curve factor P_F(0, t)."""
        raise NotImplementedError

    def forward_rate(self, t_start: float, t_end: float) -> float:
        """Simple forward rate on projection curve for [t_start, t_end]."""
        raise NotImplementedError

    def swap_annuity(self, texp: float, tenor: float, tau: float = 0.5) -> float:
        """Multi-curve swap annuity A(0)."""
        raise NotImplementedError

    def forward_swap_rate(self, texp: float, tenor: float, tau: float = 0.5) -> float:
        """Multi-curve forward swap rate S(0)."""
        raise NotImplementedError


def black76_swaption(
    fwd: float,
    strike: float,
    annuity: float,
    texp: float,
    vol_black: float,
    is_payer: bool = True,
) -> float:
    """European swaption under Black-76 lognormal model."""
    raise NotImplementedError


def bachelier_swaption(
    fwd: float,
    strike: float,
    annuity: float,
    texp: float,
    vol_normal: float,
    is_payer: bool = True,
) -> float:
    """European swaption under Bachelier normal model."""
    raise NotImplementedError


def sabr_black_vol(
    fwd: float,
    strike: float,
    texp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. (2002) asymptotic Black implied volatility expansion."""
    raise NotImplementedError


def calibrate_sabr_slice(
    fwd: float,
    texp: float,
    strikes: list[float],
    market_vols: list[float],
    beta: float = 0.5,
) -> tuple[float, float, float]:
    """Calibrate (alpha, rho, nu) to market implied volatilities on a single slice."""
    raise NotImplementedError


class SwaptionCubeEngine:
    """3D Swaption Volatility Cube Engine (Starter Skeleton)."""

    def __init__(
        self,
        curve: MultiCurveDiscounting,
        grid_expiries: list[float],
        grid_tenors: list[float],
        beta: float = 0.5,
    ) -> None:
        self.curve = curve
        self.grid_expiries = sorted(grid_expiries)
        self.grid_tenors = sorted(grid_tenors)
        self.beta = beta
        self.calibrated_params: dict[tuple[float, float], tuple[float, float, float]] = {}

    def calibrate_cube(self, market_grid: dict[str, Any]) -> None:
        """Calibrate SABR parameters on all grid nodes."""
        raise NotImplementedError

    def interpolate_sabr_params(self, texp: float, tenor: float) -> tuple[float, float, float]:
        """2D bilinear interpolation of SABR parameters (alpha, rho, nu)."""
        raise NotImplementedError

    def check_arbitrage(self, texp: float, tenor: float, strikes: list[float]) -> dict[str, Any]:
        """Verify absence of butterfly/strike arbitrage."""
        raise NotImplementedError

    def price_swaption(
        self,
        texp: float,
        tenor: float,
        strike: float,
        is_payer: bool = True,
        model: str = "bachelier",
    ) -> dict[str, float]:
        """Price an off-grid European swaption and compute risk sensitivities."""
        raise NotImplementedError
