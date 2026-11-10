"""Starter skeleton for E8 CIP-basis monitor project.

Students complete the function implementations according to the specification.
"""

from __future__ import annotations


def implied_usd_rate(
    spot: float,
    forward: float,
    foreign_rate: float,
    tau_usd: float,
    tau_foreign: float,
) -> float:
    """Compute the annual dollar rate implied by the spot, forward, and foreign interest rate."""
    raise NotImplementedError("Implement implied_usd_rate")


def cross_currency_basis_bp(
    spot: float,
    forward: float,
    usd_rate: float,
    foreign_rate: float,
    tau_usd: float,
    tau_foreign: float,
) -> float:
    """Compute the cross-currency basis in basis points."""
    raise NotImplementedError("Implement cross_currency_basis_bp")


def is_quarter_end(date_iso: str) -> bool:
    """Return True if date_iso is the last weekday of a calendar quarter."""
    raise NotImplementedError("Implement is_quarter_end")


def monitor_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Generate monitor records for a sequence of daily quote rows."""
    raise NotImplementedError("Implement monitor_table")
