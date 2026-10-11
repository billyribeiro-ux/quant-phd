#!/usr/bin/env python3
"""Vendor the site's third-party runtime assets from the npm registry, verifiably.

Commands::

    python3 tools/vendor.py lock      # resolve SPEC.yaml pins -> LOCK.json (tarball, sha512, publish date)
    python3 tools/vendor.py install   # download, verify sha512, extract mapped files, write INSTALLED.json
    python3 tools/vendor.py check     # offline: installed files match INSTALLED.json and LOCK.json
    python3 tools/vendor.py outdated  # list newer versions that already satisfy the age policy

Guarantees:

* A version younger than ``policy.min_age_days`` is refused at lock time.
* Every tarball is verified against the registry's sha512 ``integrity`` before
  anything is extracted.
* Only files named in SPEC.yaml are extracted. Member paths are checked so a
  tarball cannot write outside the vendor directory.
* ``INSTALLED.json`` records the SHA-256 of every extracted file; ``check``
  re-hashes them, so a modified or partially installed asset fails the build.
"""

from __future__ import annotations

import argparse
import base64
import fnmatch
import hashlib
import io
import json
import os
import ssl
import sys
import tarfile
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "course" / "assets" / "vendor"
SPEC = VENDOR / "SPEC.yaml"
LOCK = VENDOR / "LOCK.json"
INSTALLED = VENDOR / "INSTALLED.json"
REGISTRY = "https://registry.npmjs.org"
_PRERELEASE = ("-", "alpha", "beta", "rc", "dev", "next")


class VendorError(RuntimeError):
    """Raised when a pin, download, integrity check or installed file is wrong."""


@dataclass(frozen=True)
class Pin:
    name: str
    version: str
    license: str
    files: dict[str, str]


def _ssl() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    return ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()


def _get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "quant-phd-vendor/1.0"})
    with urllib.request.urlopen(request, timeout=120, context=_ssl()) as response:
        data: bytes = response.read()
    return data


def _packument(name: str) -> dict[str, Any]:
    payload: dict[str, Any] = json.loads(_get(f"{REGISTRY}/{urllib.parse.quote(name, safe='@')}"))
    return payload


def load_spec() -> tuple[int, list[Pin]]:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    pins = [Pin(p["name"], str(p["version"]), p["license"], dict(p["files"])) for p in spec["packages"]]
    return int(spec["policy"]["min_age_days"]), pins


def _semver_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def _published(packument: dict[str, Any], version: str) -> datetime:
    return datetime.fromisoformat(packument["time"][version].replace("Z", "+00:00"))


def lock(now: datetime) -> int:
    min_age, pins = load_spec()
    entries = []
    for pin in pins:
        doc = _packument(pin.name)
        if pin.version not in doc["versions"]:
            raise VendorError(f"{pin.name}@{pin.version} does not exist on the registry")
        published = _published(doc, pin.version)
        if now - published < timedelta(days=min_age):
            raise VendorError(f"{pin.name}@{pin.version} published {published:%Y-%m-%d}: younger than {min_age} days")
        dist = doc["versions"][pin.version]["dist"]
        if not str(dist.get("integrity", "")).startswith("sha512-"):
            raise VendorError(f"{pin.name}@{pin.version} has no sha512 integrity on the registry")
        entries.append(
            {
                "name": pin.name,
                "version": pin.version,
                "license": pin.license,
                "published": published.date().isoformat(),
                "tarball": dist["tarball"],
                "integrity": dist["integrity"],
            }
        )
        print(f"locked {pin.name}@{pin.version} (published {published:%Y-%m-%d})")
    LOCK.write_text(json.dumps({"lockfile_version": 1, "packages": entries}, indent=2) + "\n", encoding="utf-8")
    return 0


def _verify_integrity(blob: bytes, integrity: str) -> None:
    algorithm, _, expected = integrity.partition("-")
    if algorithm != "sha512":
        raise VendorError(f"unsupported integrity algorithm {algorithm}")
    actual = base64.b64encode(hashlib.sha512(blob).digest()).decode()
    if actual != expected:
        raise VendorError("tarball integrity mismatch")


def _safe_destination(relative: str) -> Path:
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts:
        raise VendorError(f"unsafe destination path {relative!r}")
    return VENDOR / Path(*path.parts)


def _extract(blob: bytes, pin: Pin) -> dict[str, str]:
    written: dict[str, str] = {}
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as archive:
        members = {m.name.removeprefix("package/"): m for m in archive.getmembers() if m.isfile()}
        for source, dest in pin.files.items():
            if "*" in source:
                if not dest.endswith("/"):
                    raise VendorError(f"{pin.name}: glob {source!r} needs a directory destination")
                matched = sorted(name for name in members if fnmatch.fnmatchcase(name, source))
                targets = [(name, f"{dest}{PurePosixPath(name).name}") for name in matched]
            else:
                targets = [(source, dest)]
            if not targets:
                raise VendorError(f"{pin.name}: {source!r} matched nothing")
            for name, target in targets:
                member = members.get(name)
                if member is None:
                    raise VendorError(f"{pin.name}: {name!r} not in tarball")
                handle = archive.extractfile(member)
                if handle is None:
                    raise VendorError(f"{pin.name}: cannot read {name!r}")
                data = handle.read()
                out = _safe_destination(target)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
                written[target] = hashlib.sha256(data).hexdigest()
    return written


def install() -> int:
    _, pins = load_spec()
    locked = {p["name"]: p for p in json.loads(LOCK.read_text(encoding="utf-8"))["packages"]}
    files: dict[str, dict[str, str]] = {}
    for pin in pins:
        entry = locked.get(pin.name)
        if entry is None or entry["version"] != pin.version:
            raise VendorError(f"{pin.name}: LOCK.json is stale; run `vendor.py lock`")
        blob = _get(entry["tarball"])
        _verify_integrity(blob, entry["integrity"])
        written = _extract(blob, pin)
        files.update({path: {"sha256": digest, "package": pin.name} for path, digest in written.items()})
        print(f"installed {pin.name}@{pin.version}: {len(written)} files")
    INSTALLED.write_text(json.dumps({"files": dict(sorted(files.items()))}, indent=2) + "\n", encoding="utf-8")
    return 0


def check() -> int:
    if not INSTALLED.exists():
        print("FAIL vendor assets not installed; run `python3 tools/vendor.py install`")
        return 1
    _, pins = load_spec()
    locked = {p["name"]: p["version"] for p in json.loads(LOCK.read_text(encoding="utf-8"))["packages"]}
    problems = [
        f"{p.name}: spec {p.version} != lock {locked.get(p.name)}" for p in pins if locked.get(p.name) != p.version
    ]
    for relative, meta in json.loads(INSTALLED.read_text(encoding="utf-8"))["files"].items():
        path = _safe_destination(relative)
        if not path.exists():
            problems.append(f"missing {relative}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != meta["sha256"]:
            problems.append(f"modified {relative}")
    for problem in problems:
        print(f"FAIL {problem}")
    print(f"vendor check: {len(problems)} problems")
    return 1 if problems else 0


def outdated(now: datetime) -> int:
    min_age, pins = load_spec()
    for pin in pins:
        doc = _packument(pin.name)
        eligible = [
            v
            for v in doc["versions"]
            if not any(tag in v for tag in _PRERELEASE)
            and v in doc["time"]
            and now - _published(doc, v) >= timedelta(days=min_age)
        ]
        newest = max(eligible, key=_semver_key)
        marker = "up to date" if newest == pin.version else f"-> {newest} available"
        print(f"{pin.name}@{pin.version}: {marker}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("lock", "install", "check", "outdated"))
    args = parser.parse_args()
    now = datetime.now(UTC)
    try:
        if args.command == "lock":
            return lock(now)
        if args.command == "install":
            return install()
        if args.command == "outdated":
            return outdated(now)
        return check()
    except VendorError as exc:
        print(f"vendor: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
