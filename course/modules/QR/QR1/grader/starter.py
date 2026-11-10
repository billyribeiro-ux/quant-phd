"""Starter template for QR1 research data engineering project (vintages.py).

Implement et_to_utc, VintageIndex, last_trade_at, and adjust_closes
strictly adhering to the project specification in project.html.
"""

from __future__ import annotations

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")


def et_to_utc(wall: str) -> str:
    """Convert Eastern wall-clock time 'YYYY-MM-DD HH:MM' to ISO 8601 UTC 'YYYY-MM-DDTHH:MM:SSZ'."""
    raise NotImplementedError("et_to_utc is not implemented")


class VintageIndex:
    """Point-in-time data vintage index backed by SQLite."""

    def __init__(self, path: str) -> None:
        raise NotImplementedError("VintageIndex.__init__ is not implemented")

    def record(
        self,
        source: str,
        series: str,
        obs_date: str,
        value: str,
        published: str,
        retrieved: str,
    ) -> None:
        """Record an observed data vintage with publication and retrieval timestamps."""
        raise NotImplementedError("VintageIndex.record is not implemented")

    def visible(self, source: str, series: str, obs_date: str, t: str) -> str | None:
        """Return visible value of (source, series, obs_date) at cut-off instant t."""
        raise NotImplementedError("VintageIndex.visible is not implemented")

    def visible_series(self, source: str, series: str, t: str) -> dict[str, str]:
        """Return mapping of obs_date to visible value for (source, series) at cut-off instant t."""
        raise NotImplementedError("VintageIndex.visible_series is not implemented")

    def close(self) -> None:
        """Close SQLite database connection."""
        raise NotImplementedError("VintageIndex.close is not implemented")


def last_trade_at(ticks: list[tuple[str, int, float]], t: str) -> float | None:
    """Return price of tick with greatest (timestamp, seq) whose timestamp <= t."""
    raise NotImplementedError("last_trade_at is not implemented")


def adjust_closes(
    dates: list[str],
    closes: list[float],
    events: list[tuple[str, float]],
) -> list[float]:
    """Compute backward-adjusted closes: raw close divided by product of subsequent split ratios."""
    raise NotImplementedError("adjust_closes is not implemented")
