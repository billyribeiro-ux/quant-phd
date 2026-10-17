"""Runs the browser modules' unit tests (tests/js/*.test.mjs) under Node's built-in test runner."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SUITES = sorted((ROOT / "tests" / "js").glob("*.test.mjs"))


@pytest.mark.parametrize("suite", SUITES, ids=lambda p: p.name)
def test_js_suite(suite: Path) -> None:
    node = shutil.which("node")
    assert node, "Node.js is required for the browser-module tests (CI installs it)"
    result = subprocess.run([node, "--test", str(suite)], capture_output=True, text=True, check=False, cwd=ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
