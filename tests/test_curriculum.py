"""Tests for the curriculum validator: the real curriculum passes, and each
structural invariant rejects a deliberately broken copy."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def run_check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "tools" / "render_curriculum.py"), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def sandbox(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "curriculum", tmp_path / "curriculum")
    shutil.copytree(ROOT / "tools", tmp_path / "tools", ignore=shutil.ignore_patterns("__pycache__"))
    return tmp_path


def mutate(root: Path, file: str, old: str, new: str) -> None:
    path = root / "curriculum" / file
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture drift: {old!r} not found in {file}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_real_curriculum_is_valid() -> None:
    result = run_check(ROOT)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("file", "old", "new", "expected"),
    [
        ("01-foundations.yaml", "prereqs: [M1]\n", "prereqs: [M1, M4]\n", "prerequisite cycle"),
        ("01-foundations.yaml", "prereqs: [CS1]\n", "prereqs: [CS1, F5]\n", "cannot sit below its prerequisites"),
        ("01-foundations.yaml", "prereqs: [S2]\n", "prereqs: [S2, ZZ9]\n", "unknown prerequisite ZZ9"),
        ("01-foundations.yaml", "requires: [M7, M8]", "requires: [M7, M8, F5]", "STUDIO-M (tier U) requires F5"),
        ("meta.yaml", "requires: [CAP0, FC1,", "requires: [CAP0, DV4, FC1,", "credential BS-FIN (max tier U) pulls in"),
        (
            "meta.yaml",
            "studios: [STUDIO-FC, STUDIO-AC,",
            "studios: [STUDIO-FC, STUDIO-DV, STUDIO-AC,",
            "STUDIO-DV needs modules outside the closure",
        ),
        (
            "meta.yaml",
            '{topic: "Derivatives", modules: [FC2, DV1]}',
            '{topic: "Derivatives", modules: [FC2, DV9]}',
            "unknown module DV9",
        ),
    ],
)
def test_invariant_rejects_broken_copy(sandbox: Path, file: str, old: str, new: str, expected: str) -> None:
    mutate(sandbox, file, old, new)
    result = run_check(sandbox)
    assert result.returncode == 1
    assert expected in result.stderr
