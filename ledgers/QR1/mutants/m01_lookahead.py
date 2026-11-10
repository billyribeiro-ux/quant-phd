"""Student error: ignores cutoff parameter t in visible(), introducing look-ahead contamination."""

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
    m = _WALL_RE.match(wall)
    if not m:
        raise ValueError(f"Malformed Eastern wall timestamp: {wall!r}")
    year, month, day, hour, minute = map(int, m.groups())
    dt = datetime.datetime(year, month, day, hour, minute)

    d_mar1 = datetime.date(year, 3, 1)
    sun2_mar = 1 + (6 - d_mar1.weekday()) % 7 + 7
    spring_date = datetime.date(year, 3, sun2_mar)

    d_nov1 = datetime.date(year, 11, 1)
    sun1_nov = 1 + (6 - d_nov1.weekday()) % 7
    fall_date = datetime.date(year, 11, sun1_nov)

    curr_date = dt.date()
    if curr_date == spring_date and 2 <= dt.hour < 3:
        raise ValueError(f"Spring forward clock jump: {wall!r} does not exist in Eastern time")

    is_dst = False
    if spring_date < curr_date < fall_date or (curr_date == spring_date and dt.hour >= 3):
        is_dst = True
    elif curr_date == fall_date and dt.hour < 2:
        is_dst = True

    offset_hours = -4 if is_dst else -5
    tz = datetime.timezone(datetime.timedelta(hours=offset_hours))
    dt_local = dt.replace(tzinfo=tz)
    dt_utc = dt_local.astimezone(datetime.timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")


class VintageIndex:
    def __init__(self, db_path: str) -> None:
        self._conn = sqlite3.connect(db_path)
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

    def record(self, source: str, series: str, obs_date: str, value: str, published: str, retrieved: str) -> None:
        if source not in SOURCES:
            raise ValueError(f"Invalid source: {source!r}")
        _validate_iso_date(obs_date)
        _validate_iso_timestamp(published, "published")
        _validate_iso_timestamp(retrieved, "retrieved")
        if retrieved < published:
            raise ValueError("retrieved cannot precede published")

        with self._conn:
            cur = self._conn.cursor()
            cur.execute(
                "SELECT value FROM vintages WHERE source = ? AND series = ? AND obs_date = ? AND published = ?",
                (source, series, obs_date, published),
            )
            existing = cur.fetchone()
            if existing is not None:
                if existing[0] == value:
                    return
                raise ValueError("Conflicting value")
            self._conn.execute(
                "INSERT INTO vintages (source, series, obs_date, value, published, retrieved) VALUES (?, ?, ?, ?, ?, ?)",
                (source, series, obs_date, value, published, retrieved),
            )

    def visible(self, source: str, series: str, obs_date: str, t: str) -> str | None:
        _validate_iso_timestamp(t, "t")
        cur = self._conn.cursor()
        # MUTANT ERROR: forgets published <= t, returns absolute latest vintage
        cur.execute(
            "SELECT value FROM vintages WHERE source = ? AND series = ? AND obs_date = ? ORDER BY published DESC, seq DESC LIMIT 1",
            (source, series, obs_date),
        )
        row = cur.fetchone()
        return row[0] if row else None

    def visible_series(self, source: str, series: str, t: str) -> dict[str, str]:
        _validate_iso_timestamp(t, "t")
        cur = self._conn.cursor()
        cur.execute(
            "SELECT obs_date, value FROM vintages WHERE source = ? AND series = ? AND published <= ? ORDER BY published ASC, seq ASC",
            (source, series, t),
        )
        return {d: v for d, v in cur.fetchall()}

    def close(self) -> None:
        self._conn.close()


def last_trade_at(ticks: list[tuple[str, int, float]], t: str) -> float | None:
    _validate_iso_timestamp(t, "t")
    eligible = [tick for tick in ticks if tick[0] <= t]
    if not eligible:
        return None
    best = max(eligible, key=lambda tick: (tick[0], tick[1]))
    return best[2]


def adjust_closes(dates: list[str], closes: list[float], events: list[tuple[str, float]]) -> list[float]:
    if len(dates) != len(closes):
        raise ValueError("Length mismatch")
    for _ex_date, ratio in events:
        if ratio <= 0:
            raise ValueError("Split ratio must be strictly positive")
    adjusted: list[float] = []
    for d, c in zip(dates, closes, strict=True):
        factor = 1.0
        for ex_date, ratio in events:
            if ex_date > d:
                factor *= ratio
        adjusted.append(c / factor)
    return adjusted
