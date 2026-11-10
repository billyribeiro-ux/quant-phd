"""Starter implementation for M8 robust implied-volatility solver."""

from __future__ import annotations


def implied_vol(price: float, spot: float, strike: float, tau: float, rate: float, kind: str) -> float:
    """Invert Black-Scholes formula for implied volatility."""
    raise NotImplementedError


def region(price: float, spot: float, strike: float, tau: float, rate: float, kind: str) -> str:
    """Classify the conditioning region of an inversion problem."""
    raise NotImplementedError


def last_evaluations() -> int:
    """Return the number of evaluations in the last inversion."""
    raise NotImplementedError
