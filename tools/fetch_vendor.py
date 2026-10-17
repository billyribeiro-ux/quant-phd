#!/usr/bin/env python3
"""Fetch and verify the course site's vendored runtime against its lock file.

``course/assets/vendor/LOCK.json`` lists every vendored file with its source
URL, SHA-256 and size. This tool downloads exactly those files into
``course/assets/vendor/`` and fails if any byte differs. Vendored files are
never committed; the lock file is, so every checkout gets identical bytes.

Usage::

    python3 tools/fetch_vendor.py            # download missing files, verify all
    python3 tools/fetch_vendor.py --check    # verify only; non-zero if anything is missing or altered
    python3 tools/fetch_vendor.py --relock   # architect only: resolve tools/vendor_spec.yaml into LOCK.json

``--relock`` resolves globs against the jsdelivr file listing, computes the
Pyodide package closure from that release's ``pyodide-lock.json``, and
cross-checks every Pyodide wheel against the hash Pyodide itself publishes.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "tools" / "vendor_spec.yaml"
VENDOR = ROOT / "course" / "assets" / "vendor"
LOCK = VENDOR / "LOCK.json"
NPM_CDN = "https://cdn.jsdelivr.net/npm"
LISTING = "https://data.jsdelivr.com/v1/packages/npm"
PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide"
USER_AGENT = "quant-finance-curriculum/0.1 (vendor fetcher; Python urllib)"


class VendorError(RuntimeError):
    """Raised when a vendored file cannot be fetched or does not match the lock."""


def _context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    return ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()


def download(url: str, *, attempts: int = 4) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=120, context=_context()) as response:
                data: bytes = response.read()
                return data
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise VendorError(f"cannot fetch {url}: {exc}") from exc
    raise VendorError(f"cannot fetch {url}")  # pragma: no cover


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_lock() -> dict[str, Any]:
    if not LOCK.exists():
        raise VendorError(f"{LOCK.relative_to(ROOT)} does not exist; run --relock")
    lock: dict[str, Any] = json.loads(LOCK.read_text(encoding="utf-8"))
    return lock


def verify(entry: dict[str, Any]) -> str | None:
    """Problem with one locked file on disk, or ``None`` if it is present and intact."""
    path = VENDOR / entry["path"]
    if not path.exists():
        return f"missing {entry['path']}"
    data = path.read_bytes()
    if len(data) != entry["bytes"] or sha256(data) != entry["sha256"]:
        return f"altered {entry['path']} (sha256 {sha256(data)[:12]}…, lock {entry['sha256'][:12]}…)"
    return None


def fetch(lock: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    for entry in lock["files"]:
        if verify(entry) is None:
            continue
        data = download(entry["url"])
        if len(data) != entry["bytes"] or sha256(data) != entry["sha256"]:
            problems.append(f"{entry['url']} does not match the lock (sha256 {sha256(data)[:12]}…)")
            continue
        path = VENDOR / entry["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return problems


def npm_listing(package: str, version: str) -> list[str]:
    payload = json.loads(download(f"{LISTING}/{package}@{version}?structure=flat"))
    return [str(f["name"]).lstrip("/") for f in payload["files"]]


def relock() -> dict[str, Any]:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    files: list[dict[str, Any]] = []

    def add(path: str, url: str, package: str, license_id: str, expected: str | None = None) -> None:
        data = download(url)
        digest = sha256(data)
        if expected is not None and digest != expected:
            raise VendorError(f"{url}: sha256 {digest} differs from the publisher's {expected}")
        files.append(
            {"path": path, "url": url, "sha256": digest, "bytes": len(data), "package": package, "license": license_id}
        )

    for item in spec["npm"]:
        package, version = item["package"], item["version"]
        available = npm_listing(package, version)
        for pattern in item["files"]:
            matches = sorted(f for f in available if fnmatch.fnmatch(f, pattern))
            if not matches:
                raise VendorError(f"{package}@{version}: no file matches {pattern!r}")
            for name in matches:
                relative = name.removeprefix(item.get("strip", ""))
                add(
                    f"{item['dest']}/{relative}",
                    f"{NPM_CDN}/{package}@{version}/{name}",
                    f"{package}@{version}",
                    item["license"],
                )

    py = spec["pyodide"]
    base = f"{PYODIDE_CDN}/v{py['version']}/full"
    for name in py["core"]:
        add(f"{py['dest']}/{name}", f"{base}/{name}", f"pyodide@{py['version']}", py["license"])
    pyodide_lock = json.loads(download(f"{base}/pyodide-lock.json"))
    packages = pyodide_lock["packages"]
    needed: set[str] = set()
    stack = list(py["packages"])
    while stack:
        name = stack.pop()
        if name in needed:
            continue
        if name not in packages:
            raise VendorError(f"pyodide {py['version']} has no package {name!r}")
        needed.add(name)
        stack.extend(packages[name].get("depends") or [])
    for name in sorted(needed):
        record = packages[name]
        add(
            f"{py['dest']}/{record['file_name']}",
            f"{base}/{record['file_name']}",
            f"{name}@{record['version']} (pyodide {py['version']})",
            py["license"] if name == "pyodide" else "see package metadata",
            expected=record.get("sha256"),
        )

    return {
        "schema": 1,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "spec": str(SPEC.relative_to(ROOT)),
        "pyodide_packages": sorted(needed),
        "total_bytes": sum(f["bytes"] for f in files),
        "files": sorted(files, key=lambda f: f["path"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify files on disk only")
    group.add_argument("--relock", action="store_true", help="regenerate LOCK.json from the spec")
    args = parser.parse_args()

    try:
        if args.relock:
            lock = relock()
            VENDOR.mkdir(parents=True, exist_ok=True)
            LOCK.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
            print(f"locked {len(lock['files'])} files, {lock['total_bytes']:,} bytes")
            return 0
        lock = load_lock()
        problems = [p for p in (verify(e) for e in lock["files"]) if p] if args.check else fetch(lock)
    except VendorError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    print(f"vendor: {len(lock['files'])} files, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
