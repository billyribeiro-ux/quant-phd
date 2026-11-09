"""Atlas A5 starter implementation (atlas.curves).

Student skeleton for FI1: Bond Math & Curve Construction.
Implement each function according to the contract in atlas/A5.contract.md.
"""

from __future__ import annotations

import datetime
from fractions import Fraction
from typing import Any

DAY_COUNT_CONVENTIONS: tuple[str, ...] = ("ACT/360", "ACT/365", "30/360")


def day_count_fraction(start: datetime.date, end: datetime.date, convention: str) -> Fraction:
    """Compute the day-count fraction between start and end under the stated convention."""
    raise NotImplementedError


def price_from_yield(face_cents: int, coupon_rate: Fraction, periods: int, yield_per_period: Fraction) -> int:
    """Compute the dirty price in cents on a coupon date from periodic yield."""
    raise NotImplementedError


def yield_to_maturity(dirty_cents: int, face_cents: int, coupon_rate: Fraction, periods: int) -> Fraction:
    """Solve for the internal rate of return (yield per period) by bisection."""
    raise NotImplementedError


def bootstrap_zero_rates(par_bonds: list[dict[str, Any]]) -> dict[int, float]:
    """Extract zero-coupon discount rates per period from a set of coupon bonds."""
    raise NotImplementedError


def ns_yield(tau: float, beta0: float, beta1: float, beta2: float, lam: float) -> float:
    """Compute the continuously compounded zero yield at maturity tau in the Nelson-Siegel model."""
    raise NotImplementedError


def svensson_yield(
    tau: float,
    beta0: float,
    beta1: float,
    beta2: float,
    beta3: float,
    lam1: float,
    lam2: float,
) -> float:
    """Compute the zero yield at maturity tau in the Svensson extension model."""
    raise NotImplementedError


def fit_nelson_siegel(maturities: list[Fraction], yields: list[Fraction]) -> dict[str, float]:
    """Fit Nelson-Siegel parameters by grid search over lambda and linear least squares for betas."""
    raise NotImplementedError


def fit_svensson(maturities: list[Fraction], yields: list[Fraction]) -> dict[str, float]:
    """Fit Svensson parameters by 2D grid search over (lam1, lam2) and linear least squares for betas."""
    raise NotImplementedError
