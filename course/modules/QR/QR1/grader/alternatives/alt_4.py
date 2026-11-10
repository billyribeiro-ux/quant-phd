"""QR1 Alternative 4: Subqueries using MAX(published) for visible queries."""

from __future__ import annotations

import datetime
import re
import sqlite3

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")

_WALL_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$")
_ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _check_ts(ts: str, name: str) -> None:
    if not isinstance(ts, str) or not _ISO_TIMESTAMP_RE.match(ts):
        raise ValueError(f"{name} must be UTC ISO timestamp ending in Z: {ts!r}")


def _check_date(d: str) -> None:
    if not isinstance(d, str) or not _ISO_DATE_RE.match(d):
        raise ValueError(f"Date must be YYYY-MM-DD: {d!r}")


def et_to_utc(wall: str) -> str:
    m = _WALL_RE.match(wall)
    if not m:
        raise ValueError(f"Malformed Eastern wall timestamp: {wall!r}")
    y, mth, d, h, mn = map(int, m.groups())
    dt = datetime.datetime(y, mth, d, h, mn)

    d_mar1 = datetime.date(y, 3, 1)
    sun2_mar = 1 + (6 - d_mar1.weekday()) % 7 + 7
    spring_date = datetime.date(y, 3, sun2_mar)

    d_nov1 = datetime.date(y, 11, 1)
    sun1_nov = 1 + (6 - d_nov1.weekday()) % 7
    fall_date = datetime.date(y, 11, sun1_nov)

    cdate = dt.date()
    if cdate == spring_date and 2 <= dt.hour < 3:
        raise ValueError("Spring DST gap does not exist")

    is_dst = (
        (spring_date < cdate < fall_date)
        or (cdate == spring_date and dt.hour >= 3)
        or (cdate == fall_date and dt.hour < 2)
    )
    offset = datetime.timedelta(hours=-4 if is_dst else -5)
    return (dt - offset).strftime("%Y-%m-%dT%H:%M:%SZ")


class VintageIndex:
    def __init__(self, path: str) -> None:
        if not path or not path.strip():
            raise ValueError("empty path")
        self.conn = sqlite3.connect(path)
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS vintages (seq INTEGER PRIMARY KEY AUTOINCREMENT, "
                "source TEXT, series TEXT, obs_date TEXT, value TEXT, published TEXT, retrieved TEXT)"
            )
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_v ON vintages(source, series, obs_date, published)")

    def record(self, source: str, series: str, obs_date: str, value: str, published: str, retrieved: str) -> None:
        if source not in SOURCES:
            raise ValueError(f"Unknown source: {source}")
        _check_date(obs_date)
        _check_ts(published, "published")
        _check_ts(retrieved, "retrieved")
        if retrieved < published:
            raise ValueError("retrieved precedes published")

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT value FROM vintages WHERE source=? AND series=? AND obs_date=? AND published=?",
                (source, series, obs_date, published),
            )
            row = cur.fetchone()
            if row is not None:
                if row[0] == value:
                    return
                raise ValueError("conflict")
            self.conn.execute(
                "INSERT INTO vintages(source, series, obs_date, value, published, retrieved) VALUES(?,?,?,?,?,?)",
                (source, series, obs_date, value, published, retrieved),
            )

    def visible(self, source: str, series: str, obs_date: str, t: str) -> str | None:
        _check_ts(t, "t")
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT value FROM vintages
            WHERE source=? AND series=? AND obs_date=? AND published<=?
              AND seq = (
                  SELECT seq FROM vintages
                  WHERE source=? AND series=? AND obs_date=? AND published<=?
                  ORDER BY published DESC, seq DESC LIMIT 1
              )
            """,
            (source, series, obs_date, t, source, series, obs_date, t),
        )
        r = cur.fetchone()
        return r[0] if r else None

    def visible_series(self, source: str, series: str, t: str) -> dict[str, str]:
        _check_ts(t, "t")
        cur = self.conn.cursor()
        # Find all distinct obs_date for source, series
        cur.execute(
            "SELECT DISTINCT obs_date FROM vintages WHERE source=? AND series=? AND published<=? ORDER BY obs_date ASC",
            (source, series, t),
        )
        dates = [r[0] for r in cur.fetchall()]
        res: dict[str, str] = {}
        for d in dates:
            v = self.visible(source, series, d, t)
            if v is not None:
                res[d] = v
        return res

    def close(self) -> None:
        self.conn.close()


def last_trade_at(ticks: list[tuple[str, int, float]], t: str) -> float | None:
    _check_ts(t, "t")
    cand = [tick for tick in ticks if tick[0] <= t]
    if not cand:
        return None
    return max(cand, key=lambda x: (x[0], x[1]))[2]


def adjust_closes(dates: list[str], closes: list[float], events: list[tuple[str, float]]) -> list[float]:
    if len(dates) != len(closes):
        raise ValueError("length mismatch")
    for _, r in events:
        if r <= 0:
            raise ValueError("ratio must be positive")
    res: list[float] = []
    for d, c in zip(dates, closes, strict=True):
        f = 1.0
        for ed, r in events:
            if ed > d:
                f *= r
        res.append(c / f)
    return res
