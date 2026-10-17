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
        # Concept graph: each concept is defined once, and used only after its definition.
        (
            "01-foundations.yaml",
            '          cscv: "Combinatorially symmetric cross-validation (CSCV)"\n',
            '          cscv: "CSCV"\n          sharpe-ratio: "Sharpe ratio"\n',
            "concept sharpe-ratio is introduced by S1, S7",
        ),
        (
            "01-foundations.yaml",
            "          - kurtosis\n",
            "          - kurtosis\n          - purged-cross-validation\n",
            "S7: uses purged-cross-validation from QR2, which is not in its prerequisite closure",
        ),
        (
            "01-foundations.yaml",
            "          - kurtosis\n",
            "          - kurtosis\n          - cscv\n",
            "which it introduces",
        ),
        (
            "01-foundations.yaml",
            "          - kurtosis\n",
            "          - kurtosis\n          - no-such-concept\n",
            "S7: uses unknown concept no-such-concept",
        ),
        (
            "01-foundations.yaml",
            "          cscv: ",
            "          CSCV: ",
            "concept id 'CSCV' must be lowercase kebab-case",
        ),
        (
            "01-foundations.yaml",
            "        introduces:\n          data-snooping-bias:",
            "        introduced:\n          data-snooping-bias:",
            "S7: introduces must be a non-empty mapping",
        ),
        # A reading scope may replace sources only in capstone modules.
        (
            "01-foundations.yaml",
            "        introduces:\n          data-snooping-bias:",
            '        reading: "all module sources"\n        introduces:\n          data-snooping-bias:',
            "S7: only capstone modules may replace sources with a reading scope",
        ),
    ],
)
def test_invariant_rejects_broken_copy(sandbox: Path, file: str, old: str, new: str, expected: str) -> None:
    mutate(sandbox, file, old, new)
    result = run_check(sandbox)
    assert result.returncode == 1
    assert expected in result.stderr
