"""Offline tests for tools/fetch_vendor.py: the lock is honoured byte for byte, and the local pins match Pyodide."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml

import fetch_vendor

ROOT = Path(__file__).resolve().parent.parent


def _entry(path: str, data: bytes) -> dict[str, Any]:
    return {
        "path": path,
        "url": f"https://example.invalid/{path}",
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }


@pytest.fixture
def vendor_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(fetch_vendor, "VENDOR", tmp_path)
    monkeypatch.setattr(fetch_vendor, "LOCK", tmp_path / "LOCK.json")
    return tmp_path


def test_verify_accepts_an_intact_file(vendor_dir: Path) -> None:
    (vendor_dir / "a.js").write_bytes(b"abc")
    assert fetch_vendor.verify(_entry("a.js", b"abc")) is None


def test_verify_reports_a_missing_file(vendor_dir: Path) -> None:
    assert fetch_vendor.verify(_entry("a.js", b"abc")) == "missing a.js"


@pytest.mark.parametrize("on_disk", [b"abd", b"abcd"], ids=["same-size-different-bytes", "different-size"])
def test_verify_reports_an_altered_file(vendor_dir: Path, on_disk: bytes) -> None:
    (vendor_dir / "a.js").write_bytes(on_disk)
    problem = fetch_vendor.verify(_entry("a.js", b"abc"))
    assert problem is not None and problem.startswith("altered a.js")


def test_fetch_writes_a_download_that_matches_the_lock(vendor_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fetch_vendor, "download", lambda url, **_: b"abc")
    assert fetch_vendor.fetch({"files": [_entry("sub/a.js", b"abc")]}) == []
    assert (vendor_dir / "sub" / "a.js").read_bytes() == b"abc"


def test_fetch_refuses_and_does_not_write_a_download_that_differs(
    vendor_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(fetch_vendor, "download", lambda url, **_: b"evil")
    problems = fetch_vendor.fetch({"files": [_entry("a.js", b"abc")]})
    assert len(problems) == 1 and "does not match the lock" in problems[0]
    assert not (vendor_dir / "a.js").exists()


def test_fetch_does_not_download_a_file_that_is_already_intact(
    vendor_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (vendor_dir / "a.js").write_bytes(b"abc")

    def boom(url: str, **_: Any) -> bytes:
        raise AssertionError("downloaded an intact file")

    monkeypatch.setattr(fetch_vendor, "download", boom)
    assert fetch_vendor.fetch({"files": [_entry("a.js", b"abc")]}) == []


def test_check_mode_exit_codes(vendor_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    lock = {"files": [_entry("a.js", b"abc")]}
    (vendor_dir / "LOCK.json").write_text(json.dumps(lock), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["fetch_vendor.py", "--check"])
    assert fetch_vendor.main() == 1  # missing
    (vendor_dir / "a.js").write_bytes(b"abc")
    assert fetch_vendor.main() == 0
    (vendor_dir / "a.js").write_bytes(b"abX")
    assert fetch_vendor.main() == 1  # altered


def test_the_committed_lock_is_well_formed() -> None:
    lock = json.loads((ROOT / "course" / "assets" / "vendor" / "LOCK.json").read_text(encoding="utf-8"))
    paths = [e["path"] for e in lock["files"]]
    assert len(paths) == len(set(paths)), "a file is locked twice"
    for e in lock["files"]:
        assert re.fullmatch(r"[0-9a-f]{64}", e["sha256"]), e["path"]
        assert e["bytes"] > 0 and e["url"].startswith("https://"), e["path"]
        assert ".." not in Path(e["path"]).parts and not Path(e["path"]).is_absolute(), e["path"]


def test_the_lock_matches_the_spec_pins() -> None:
    spec = yaml.safe_load((ROOT / "tools" / "vendor_spec.yaml").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "course" / "assets" / "vendor" / "LOCK.json").read_text(encoding="utf-8"))
    urls = " ".join(e["url"] for e in lock["files"])
    for pkg in spec["npm"]:
        assert f"/{pkg['package']}@{pkg['version']}/" in urls, f"{pkg['package']} {pkg['version']} is not locked"
    assert f"/v{spec['pyodide']['version']}/" in urls, "the locked Pyodide is not the spec's"


def test_the_local_pins_are_the_versions_the_browser_runs() -> None:
    """Labs and graders run in Pyodide and under pytest: the packages must be the same versions."""
    lock_file = ROOT / "course" / "assets" / "vendor" / "pyodide" / "pyodide-lock.json"
    if not lock_file.exists():
        pytest.skip("vendored Pyodide not fetched (tools/fetch_vendor.py)")
    packages = json.loads(lock_file.read_text(encoding="utf-8"))["packages"]
    pins = dict(re.findall(r"^(numpy|scipy|pytest)==([^\s#]+)", (ROOT / "requirements-dev.txt").read_text(), re.M))
    assert set(pins) == {"numpy", "scipy", "pytest"}
    for name, version in pins.items():
        assert packages[name]["version"] == version, (
            f"{name}: pinned {version}, Pyodide ships {packages[name]['version']}"
        )
