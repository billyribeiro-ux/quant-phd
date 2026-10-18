#!/usr/bin/env python3
"""Build and verify the course's embedded market-data snapshots.

``tools/data_sources.yaml`` lists every dataset a lab may read: where it comes
from, the issuer's own statement that it may be redistributed (quoted, with the
URL that states it), and the transform from the published file to a small tidy
CSV. This tool writes those CSVs to ``course/assets/data/market/`` and records
each one in ``course/assets/data/market/MANIFEST.json`` with its source, licence,
retrieval date, the SHA-256 of the raw download and of the snapshot, its rows,
columns and date range, and the transform. Snapshots are committed, so labs and
tests never touch the network; a lab names the files it reads in its section's
``data-files`` attribute and opens them as ``data/<file>``.

Only sources whose terms permit redistribution are embedded. Sources that were
checked and rejected stay in the spec under ``rejected``, with the evidence.

Usage::

    python3 tools/fetch_data.py                   # same as --check: offline, verify every snapshot against MANIFEST
    python3 tools/fetch_data.py --fetch           # download every source, rebuild the snapshots and MANIFEST
    python3 tools/fetch_data.py --fetch --only fx_daily
    python3 tools/fetch_data.py --fetch --raw-dir DIR     # build from raw files saved earlier (DIR/<id>.raw)
    python3 tools/fetch_data.py --fetch --keep-raw DIR    # also save each raw download as DIR/<id>.raw

Requests carry a descriptive User-Agent and no personal data.
"""

from __future__ import annotations

import argparse
import calendar
import csv
import hashlib
import io
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "tools" / "data_sources.yaml"
MARKET = ROOT / "course" / "assets" / "data" / "market"
MANIFEST = MARKET / "MANIFEST.json"
USER_AGENT = "quant-finance-curriculum/0.1 (data fetcher; Python urllib)"
REQUIRED = ("id", "title", "issuer", "url", "licence", "licence_url", "citation", "transform")


class DataError(RuntimeError):
    """Raised when a source cannot be fetched or parsed, or a snapshot does not match MANIFEST."""


# ---------------------------------------------------------------- spec and download


@dataclass(frozen=True)
class Dataset:
    id: str
    title: str
    issuer: str
    url: str
    licence: str
    licence_url: str
    citation: str
    transform: dict[str, Any]
    note: str = ""

    @property
    def file(self) -> Path:
        return MARKET / f"{self.id}.csv"


def load_spec(path: Path = SPEC) -> list[Dataset]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    datasets: list[Dataset] = []
    seen: set[str] = set()
    for item in raw.get("datasets") or []:
        missing = [k for k in REQUIRED if not item.get(k)]
        if missing:
            raise DataError(f"{path.name}: dataset {item.get('id')!r} is missing {missing}")
        if item["id"] in seen:
            raise DataError(f"{path.name}: duplicate dataset id {item['id']!r}")
        seen.add(item["id"])
        if item["transform"].get("kind") not in TRANSFORMS:
            raise DataError(f"{path.name}: {item['id']}: unknown transform {item['transform'].get('kind')!r}")
        datasets.append(Dataset(**{k: item[k] for k in (*REQUIRED, "note") if k in item}))
    return datasets


def _context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    return ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()


def download(url: str, *, attempts: int = 4) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=300, context=_context()) as response:
                body: bytes = response.read()
                return body
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise DataError(f"{url}: {exc}") from exc
    raise DataError(f"{url}: no response")


# ---------------------------------------------------------------- transforms


@dataclass(frozen=True)
class Table:
    """A tidy snapshot: a key column (dates or months) and named value columns, values kept as text."""

    key: str
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]  # (key, value, ...) with "" for a missing value

    def csv_bytes(self) -> bytes:
        out = io.StringIO()
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow([self.key, *self.columns])
        writer.writerows(self.rows)
        return out.getvalue().encode("utf-8")


def _sdmx_series(raw: bytes, member: str, wanted: set[str]) -> dict[str, dict[str, str]]:
    """{series name: {date: published value}} for the wanted series of a Federal Reserve DDP SDMX zip.

    Only observations with OBS_STATUS "A" (available) are kept; holidays and gaps ("ND") are dropped.
    """
    found: dict[str, dict[str, str]] = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive, archive.open(member) as stream:
        for _, element in ET.iterparse(stream, events=("end",)):
            if not element.tag.endswith("}Series"):
                continue
            name = element.get("SERIES_NAME") or ""
            if name in wanted:
                found[name] = {
                    obs.get("TIME_PERIOD") or "": obs.get("OBS_VALUE") or ""
                    for obs in element
                    if obs.tag.endswith("}Obs") and obs.get("OBS_STATUS") == "A"
                }
            element.clear()
    missing = sorted(wanted - found.keys())
    if missing:
        raise DataError(f"{member}: series not found: {missing}")
    return found


def _invert(value: str) -> str:
    """1 / value to eight significant digits, in plain decimal notation."""
    inverse = 1.0 / float(value)
    digits = 8 - 1 - int(f"{inverse:e}".split("e")[1])
    return f"{inverse:.{max(digits, 0)}f}"


def fed_sdmx(raw: bytes, spec: dict[str, Any]) -> Table:
    """Selected series of a Federal Reserve DDP release, daily or sampled at month end.

    spec: member (XML file in the zip), series ({column: SERIES_NAME}), invert (columns quoted per USD, shown
    as USD per unit by taking 1/x to eight significant digits), start and end (ISO dates, inclusive),
    sample ("daily": every date with at least one value; "month_end": each column's last value in each month).
    """
    series: dict[str, str] = spec["series"]
    invert = set(spec.get("invert") or [])
    start, end = str(spec["start"]), str(spec["end"])
    data = _sdmx_series(raw, spec["member"], set(series.values()))
    columns = tuple(series)
    by_column = {
        col: {d: (_invert(v) if col in invert else v) for d, v in data[name].items() if start <= d <= end}
        for col, name in series.items()
    }
    if spec.get("sample", "daily") == "daily":
        dates = sorted(set().union(*(values.keys() for values in by_column.values())))
        rows = tuple((d, *(by_column[c].get(d, "") for c in columns)) for d in dates)
        return Table("date", columns, rows)
    if spec["sample"] != "month_end":
        raise DataError(f"unknown sample {spec['sample']!r}")
    months: dict[str, dict[str, str]] = {}
    for col in columns:
        for d in sorted(by_column[col]):
            months.setdefault(d[:7], {})[col] = by_column[col][d]  # later dates overwrite: the month's last value
    last_month = end[:7]
    end_day = date.fromisoformat(end)
    if end_day.day != calendar.monthrange(end_day.year, end_day.month)[1]:
        months.pop(last_month, None)  # an incomplete final month would carry a mid-month value
    rows = tuple((m, *(months[m].get(c, "") for c in columns)) for m in sorted(months))
    return Table("month", columns, rows)


TRANSFORMS: dict[str, Callable[[bytes, dict[str, Any]], Table]] = {"fed_sdmx": fed_sdmx}


def describe(spec: dict[str, Any]) -> str:
    """A one-line, human-readable statement of a transform, recorded in MANIFEST."""
    if spec["kind"] == "fed_sdmx":
        sample = "month-end (each column's last value in the month)" if spec.get("sample") == "month_end" else "daily"
        invert = ", ".join(spec.get("invert") or [])
        inverted = f"; {invert} inverted to USD per unit (1/x, 8 significant digits)" if invert else ""
        series = ", ".join(f"{col}={name}" for col, name in spec["series"].items())
        return (
            f"{spec['member']} observations with OBS_STATUS A, {spec['start']} to {spec['end']}, {sample}{inverted}; "
            f"published values kept as text otherwise; series {series}"
        )
    raise DataError(f"unknown transform {spec['kind']!r}")


# ---------------------------------------------------------------- build and check


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _shown(path: Path) -> Path:
    return path.relative_to(ROOT) if path.is_relative_to(ROOT) else path


def build(dataset: Dataset, raw: bytes, retrieved: str) -> dict[str, Any]:
    """Write the dataset's snapshot and return its MANIFEST entry."""
    table = TRANSFORMS[dataset.transform["kind"]](raw, dataset.transform)
    if not table.rows:
        raise DataError(f"{dataset.id}: the transform produced no rows")
    blob = table.csv_bytes()
    dataset.file.parent.mkdir(parents=True, exist_ok=True)
    dataset.file.write_bytes(blob)
    return {
        "id": dataset.id,
        "file": dataset.file.name,
        "title": dataset.title,
        "issuer": dataset.issuer,
        "source_url": dataset.url,
        "licence": dataset.licence,
        "licence_url": dataset.licence_url,
        "citation": dataset.citation,
        "retrieved": retrieved,
        "raw_sha256": sha256(raw),
        "sha256": sha256(blob),
        "bytes": len(blob),
        "rows": len(table.rows),
        "key": table.key,
        "columns": list(table.columns),
        "first": table.rows[0][0],
        "last": table.rows[-1][0],
        "transform": describe(dataset.transform),
    }


# Paths default to the module's MARKET and MANIFEST at call time, so a test that points them elsewhere never
# touches the committed snapshots.


def load_manifest(path: Path | None = None) -> dict[str, dict[str, Any]]:
    path = path or MANIFEST
    if not path.exists():
        return {}
    entries: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))["datasets"]
    return {e["id"]: e for e in entries}


def save_manifest(entries: dict[str, dict[str, Any]], path: Path | None = None) -> None:
    path = path or MANIFEST
    payload = {"schema": 1, "datasets": [entries[k] for k in sorted(entries)]}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check(datasets: list[Dataset], manifest: dict[str, dict[str, Any]]) -> list[str]:
    """Offline: every dataset has a MANIFEST entry and a snapshot whose bytes and shape match it."""
    problems: list[str] = []
    ids = {d.id for d in datasets}
    for extra in sorted(manifest.keys() - ids):
        problems.append(f"MANIFEST lists {extra!r}, which tools/data_sources.yaml does not")
    listed = {MANIFEST.name} | {d.file.name for d in datasets}
    if MARKET.is_dir():
        for stray in sorted(p.name for p in MARKET.iterdir() if p.name not in listed):
            problems.append(f"{stray}: in {_shown(MARKET)} but not a dataset of tools/data_sources.yaml")
    for dataset in datasets:
        entry = manifest.get(dataset.id)
        if entry is None:
            problems.append(f"{dataset.id}: no MANIFEST entry (run --fetch)")
            continue
        if not dataset.file.exists():
            problems.append(f"{dataset.id}: snapshot {_shown(dataset.file)} is missing")
            continue
        blob = dataset.file.read_bytes()
        if sha256(blob) != entry["sha256"]:
            problems.append(f"{dataset.id}: snapshot SHA-256 differs from MANIFEST (edited by hand?)")
        rows = list(csv.reader(io.StringIO(blob.decode("utf-8")))) or [[]]
        if entry.get("file") != dataset.file.name:
            problems.append(f"{dataset.id}: MANIFEST file is {entry.get('file')!r}, expected {dataset.file.name!r}")
        if rows[0] != [entry["key"], *entry["columns"]]:
            problems.append(f"{dataset.id}: header {rows[0]} differs from MANIFEST")
        if len(rows) - 1 != entry["rows"]:
            problems.append(f"{dataset.id}: {len(rows) - 1} rows, MANIFEST says {entry['rows']}")
        for field, value in (
            ("licence", dataset.licence),
            ("licence_url", dataset.licence_url),
            ("source_url", dataset.url),
            ("transform", describe(dataset.transform)),
        ):
            if entry.get(field) != value:
                problems.append(f"{dataset.id}: MANIFEST {field} differs from tools/data_sources.yaml (re-run --fetch)")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="offline: verify snapshots against MANIFEST (default)")
    mode.add_argument("--fetch", action="store_true", help="download the sources and rebuild snapshots and MANIFEST")
    parser.add_argument("--only", nargs="+", metavar="ID", help="with --fetch: only these datasets")
    parser.add_argument("--raw-dir", type=Path, help="with --fetch: read DIR/<id>.raw instead of downloading")
    parser.add_argument("--keep-raw", type=Path, help="with --fetch: also save each download as DIR/<id>.raw")
    args = parser.parse_args()

    datasets = load_spec()
    manifest = load_manifest()
    if args.fetch:
        chosen = [d for d in datasets if not args.only or d.id in args.only]
        unknown = sorted(set(args.only or []) - {d.id for d in datasets})
        if unknown:
            raise SystemExit(f"unknown dataset ids: {unknown}")
        retrieved = datetime.now(UTC).date().isoformat()
        downloads: dict[str, bytes] = {}  # several datasets can come from one release file
        for dataset in chosen:
            if args.raw_dir:
                raw = (args.raw_dir / f"{dataset.id}.raw").read_bytes()
            else:
                if dataset.url not in downloads:
                    downloads[dataset.url] = download(dataset.url)
                raw = downloads[dataset.url]
            if args.keep_raw:
                args.keep_raw.mkdir(parents=True, exist_ok=True)
                (args.keep_raw / f"{dataset.id}.raw").write_bytes(raw)
            entry = manifest[dataset.id] = build(dataset, raw, retrieved)
            span = f"{entry['first']} to {entry['last']}"
            print(f"built {dataset.id}: {entry['rows']} rows, {entry['bytes']} bytes, {span}")
        manifest = {k: v for k, v in manifest.items() if k in {d.id for d in datasets}}
        save_manifest(manifest)
    problems = check(datasets, manifest)
    for problem in problems:
        print(f"FAIL {problem}")
    print(f"fetch_data: {len(datasets)} datasets, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
