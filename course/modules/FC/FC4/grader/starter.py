"""Starter module for FC4 Investments & Equity Security Analysis project."""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction


def gordon_value(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
    """Compute the Gordon growth model value D_1 / (r - g)."""
    raise NotImplementedError


def ddm_value(dividends: Sequence[Fraction], r: Fraction, g: Fraction) -> Fraction:
    """Compute multistage DDM equity value with a terminal Gordon perpetuity."""
    raise NotImplementedError


def fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    """Compute FCFE value per share with a terminal Gordon perpetuity."""
    raise NotImplementedError


def residual_income_value(
    book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
) -> Fraction:
    """Compute finite-horizon residual income equity value under clean surplus."""
    raise NotImplementedError


def scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
    """Compute scenario-weighted price target in integer cents rounded half-up."""
    raise NotImplementedError
