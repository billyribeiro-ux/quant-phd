"""QR1 Reference Solution: Vintage-aware ingestion engine and research data layer.

Implements point-in-time vintage indexing, UTC timestamp normalization,
prevailing tick resolution, and corporate action backward-adjustment factors.
Data: SIMULATED research data store records.
"""

from __future__ import annotations

import datetime
import re
import sqlite3

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")

_WALL_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$")
_ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_iso_timestamp(ts: str, field_name: str) -> None:
    if not isinstance(ts, str) or not _ISO_TIMESTAMP_RE.match(ts):
        raise ValueError(f"Field '{field_name}' must be an ISO 8601 UTC timestamp ending in 'Z', got: {ts!r}")
    # Check valid date/time components
    base_ts = ts.rstrip("Z")
    if "." in base_ts:
        base_ts, _ = base_ts.split(".", 1)
    try:
        datetime.datetime.strptime(base_ts, "%Y-%m-%dT%H:%M:%S")
    except ValueError as exc:
        raise ValueError(f"Field '{field_name}' contains invalid date/time: {ts!r}") from exc


def _validate_iso_date(date_str: str) -> None:
    if not isinstance(date_str, str) or not _ISO_DATE_RE.match(date_str):
        raise ValueError(f"Observation date must be ISO 8601 'YYYY-MM-DD', got: {date_str!r}")
    try:
        datetime.date.fromisoformat(date_str)
    except ValueError as exc:
        raise ValueError(f"Observation date is invalid: {date_str!r}") from exc


def et_to_utc(wall: str) -> str:
    """Convert Eastern wall-clock time 'YYYY-MM-DD HH:MM' to ISO 8601 UTC 'YYYY-MM-DDTHH:MM:SSZ'."""
    m = _WALL_RE.match(wall)
    if not m:
        raise ValueError(f"Malformed Eastern wall timestamp: {wall!r}")
    year, month, day, hour, minute = map(int, m.groups())
    try:
        dt = datetime.datetime(year, month, day, hour, minute)
    except ValueError as exc:
        raise ValueError(f"Invalid date or time: {wall!r}") from exc

    # US DST rule: Second Sunday of March to First Sunday of November
    d_mar1 = datetime.date(year, 3, 1)
    sun2_mar = 1 + (6 - d_mar1.weekday()) % 7 + 7
    spring_date = datetime.date(year, 3, sun2_mar)

    d_nov1 = datetime.date(year, 11, 1)
    sun1_nov = 1 + (6 - d_nov1.weekday()) % 7
    fall_date = datetime.date(year, 11, sun1_nov)

    curr_date = dt.date()
    if curr_date == spring_date and 2 <= dt.hour < 3:
        raise ValueError(f"Wall time in spring DST gap does not exist: {wall!r}")

    is_dst = False
    if spring_date < curr_date < fall_date or (curr_date == spring_date and dt.hour >= 3):
        is_dst = True
    elif curr_date == fall_date and dt.hour < 2:
        # Fall overlap 01:00-01:59 takes earlier instant (daylight time UTC-4)
        is_dst = True

    offset_hours = -4 if is_dst else -5
    utc_dt = dt - datetime.timedelta(hours=offset_hours)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class VintageIndex:
    """Point-in-time data vintage index backed by SQLite."""

    def __init__(self, path: str) -> None:
        if not isinstance(path, str) or not path.strip():
            raise ValueError("path cannot be empty")
        self._path = path
        self._conn = sqlite3.connect(path)
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS vintages (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    series TEXT NOT NULL,
                    obs_date TEXT NOT NULL,
                    value TEXT NOT NULL,
                    published TEXT NOT NULL,
                    retrieved TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_vintages_lookup ON vintages(source, series, obs_date, published, seq)"
            )

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
        if source not in SOURCES:
            raise ValueError(f"Unknown source '{source}'. Must be one of {SOURCES}")
        _validate_iso_date(obs_date)
        _validate_iso_timestamp(published, "published")
        _validate_iso_timestamp(retrieved, "retrieved")

        if retrieved < published:
            raise ValueError(f"retrieved timestamp ({retrieved}) cannot precede publication timestamp ({published})")

        with self._conn:
            cur = self._conn.cursor()
            cur.execute(
                """
                SELECT value FROM vintages
                WHERE source = ? AND series = ? AND obs_date = ? AND published = ?
                """,
                (source, series, obs_date, published),
            )
            existing = cur.fetchone()
            if existing is not None:
                if existing[0] == value:
                    return  # Idempotent re-recording
                raise ValueError(
                    f"Conflicting value for {source} {series} on {obs_date} at {published}: "
                    f"existing {existing[0]!r} vs new {value!r}"
                )

            self._conn.execute(
                """
                INSERT INTO vintages (source, series, obs_date, value, published, retrieved)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (source, series, obs_date, value, published, retrieved),
            )

    def visible(self, source: str, series: str, obs_date: str, t: str) -> str | None:
        """Return visible value of (source, series, obs_date) at cut-off instant t."""
        _validate_iso_timestamp(t, "t")
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT value FROM vintages
            WHERE source = ? AND series = ? AND obs_date = ? AND published <= ?
            ORDER BY published DESC, seq DESC LIMIT 1
            """,
            (source, series, obs_date, t),
        )
        row = cur.fetchone()
        return row[0] if row else None

    def visible_series(self, source: str, series: str, t: str) -> dict[str, str]:
        """Return mapping of obs_date to visible value for (source, series) at cut-off instant t."""
        _validate_iso_timestamp(t, "t")
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT obs_date, value FROM vintages
            WHERE source = ? AND series = ? AND published <= ?
            ORDER BY published ASC, seq ASC
            """,
            (source, series, t),
        )
        series_map: dict[str, str] = {}
        for d, v in cur.fetchall():
            series_map[d] = v
        return series_map

    def close(self) -> None:
        """Close SQLite database connection."""
        self._conn.close()


def last_trade_at(ticks: list[tuple[str, int, float]], t: str) -> float | None:
    """Return price of tick with greatest (timestamp, seq) whose timestamp <= t."""
    _validate_iso_timestamp(t, "t")
    eligible = [tick for tick in ticks if tick[0] <= t]
    if not eligible:
        return None
    best = max(eligible, key=lambda tick: (tick[0], tick[1]))
    return best[2]


def adjust_closes(
    dates: list[str],
    closes: list[float],
    events: list[tuple[str, float]],
) -> list[float]:
    """Compute backward-adjusted closes: raw close divided by product of subsequent split ratios."""
    if len(dates) != len(closes):
        raise ValueError(f"Length mismatch: {len(dates)} dates vs {len(closes)} closes")
    for _ex_date, ratio in events:
        if ratio <= 0:
            raise ValueError(f"Split ratio must be strictly positive, got {ratio}")

    adjusted: list[float] = []
    for d, c in zip(dates, closes, strict=True):
        factor = 1.0
        for ex_date, ratio in events:
            if ex_date > d:
                factor *= ratio
        adjusted.append(c / factor)
    return adjusted
