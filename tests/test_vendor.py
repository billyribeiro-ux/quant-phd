"""Offline tests for tools/vendor.py: integrity, extraction safety, glob mapping."""

from __future__ import annotations

import base64
import hashlib
import io
import tarfile
from pathlib import Path

import pytest

import vendor


def tarball(files: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for name, data in files.items():
            info = tarfile.TarInfo(f"package/{name}")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def integrity(blob: bytes) -> str:
    return "sha512-" + base64.b64encode(hashlib.sha512(blob).digest()).decode()


@pytest.fixture
def vendor_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(vendor, "VENDOR", tmp_path)
    return tmp_path


def test_integrity_accepts_matching_and_rejects_tampered_tarball() -> None:
    blob = tarball({"a.js": b"ok"})
    vendor._verify_integrity(blob, integrity(blob))
    with pytest.raises(vendor.VendorError, match="integrity mismatch"):
        vendor._verify_integrity(blob + b"x", integrity(blob))
    with pytest.raises(vendor.VendorError, match="unsupported"):
        vendor._verify_integrity(blob, "sha1-abc")


def test_extract_maps_files_and_globs(vendor_dir: Path) -> None:
    blob = tarball({"dist/a.min.js": b"A", "dist/fonts/x.woff2": b"X", "dist/fonts/x.ttf": b"T", "LICENSE": b"L"})
    pin = vendor.Pin("pkg", "1.0.0", "MIT", {"dist/a.min.js": "pkg/a.js", "dist/fonts/*.woff2": "pkg/fonts/"})
    written = vendor._extract(blob, pin)
    assert sorted(written) == ["pkg/a.js", "pkg/fonts/x.woff2"]
    assert (vendor_dir / "pkg" / "fonts" / "x.woff2").read_bytes() == b"X"
    assert not (vendor_dir / "pkg" / "fonts" / "x.ttf").exists()
    assert written["pkg/a.js"] == hashlib.sha256(b"A").hexdigest()


@pytest.mark.parametrize("dest", ["../escape.js", "/abs/escape.js", "pkg/../../escape.js"])
def test_extract_refuses_paths_outside_vendor(vendor_dir: Path, dest: str) -> None:
    pin = vendor.Pin("pkg", "1.0.0", "MIT", {"a.js": dest})
    with pytest.raises(vendor.VendorError, match="unsafe destination"):
        vendor._extract(tarball({"a.js": b"A"}), pin)


def test_extract_fails_closed_on_missing_file(vendor_dir: Path) -> None:
    # Real case: @duckdb/duckdb-wasm ships no LICENSE file.
    pin = vendor.Pin("pkg", "1.0.0", "MIT", {"LICENSE": "pkg/LICENSE"})
    with pytest.raises(vendor.VendorError, match="not in tarball"):
        vendor._extract(tarball({"a.js": b"A"}), pin)


def test_glob_requires_directory_destination(vendor_dir: Path) -> None:
    pin = vendor.Pin("pkg", "1.0.0", "MIT", {"*.js": "pkg/file.js"})
    with pytest.raises(vendor.VendorError, match="directory destination"):
        vendor._extract(tarball({"a.js": b"A"}), pin)


def test_semver_ordering_is_numeric() -> None:
    # Pyodide moved from 0.29.x to 314.x: string ordering would pick the wrong release.
    assert max(["0.29.5", "314.0.7", "0.27.8"], key=vendor._semver_key) == "314.0.7"
    assert max(["7.10.0", "7.9.0"], key=vendor._semver_key) == "7.10.0"
