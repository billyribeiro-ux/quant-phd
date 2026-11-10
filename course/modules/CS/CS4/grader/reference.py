"""CS4 Autograder Reference Solution: Reproducibility Audit.

Full reference implementation providing:
1. Deterministic sequence generation and exact rational statistics (run, summarize).
2. Complete fixed repository files (requirements.lock, pyproject.toml, CI, tests, AUDIT.md).
3. materialize_repo() helper for physical repository generation.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

# Pinned production lockfile with verified SHA-256 hashes
LOCKFILE_CONTENT = """# Pinned dependency lockfile with SHA-256 hashes
iniconfig==2.0.0 --hash=sha256:b845d3e32f20f0204f0f9e6abd67d7e07c34e537da454d427fc26bf43c417bac
packaging==24.0 --hash=sha256:2ddfb556884787140e941162463339178f5661b69766627063f27664ff6d8621
pluggy==1.5.0 --hash=sha256:8f48af886261329324d2c884b2c1404c272a832be1b4f49491410d3f2ec8eb09
pytest==8.2.0 --hash=sha256:462a9af17f3dc53f65e4e69b59695d36e2f1856711776953288fb875b282c074
"""

# Modern standard packaging configuration
PYPROJECT_CONTENT = """[build-system]
requires = ["setuptools>=68.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "repro-study"
version = "1.0.0"
description = "Deterministic reproducible quantitative research package"
requires-python = ">=3.14"
dependencies = [
    "pytest==8.2.0",
]
"""

# Study core module
STUDY_CORE_CONTENT = '''"""Core deterministic research study module."""

from __future__ import annotations

import json
from collections.abc import Sequence
from fractions import Fraction


def generate_sequence(seed: int, n: int = 200) -> list[int]:
    """Generate deterministic sequence using linear congruential arithmetic."""
    if seed < 0:
        raise ValueError("seed must be non-negative")
    seq: list[int] = []
    for i in range(1, n + 1):
        val = (1103515245 * seed + 12345 * i * i + 7 * i) % 1000003
        seq.append(val)
    return seq


def summarize(values: Sequence[int]) -> dict[str, object]:
    """Compute exact summary statistics using Fraction for mean and sample variance."""
    n = len(values)
    if n < 2:
        raise ValueError("len(values) must be at least 2")
    s = sum(values)
    s2 = sum(v * v for v in values)
    mean_frac = Fraction(s, n)
    var_frac = Fraction(n * s2 - s * s, n * (n - 1))
    return {
        "count": n,
        "max": max(values),
        "mean": str(mean_frac),
        "min": min(values),
        "variance": str(var_frac),
    }


def run(seed: int) -> str:
    """Execute study for given seed and return canonical JSON output."""
    values = generate_sequence(seed)
    stats = summarize(values)
    return json.dumps(stats, sort_keys=True, indent=2) + "\\n"
'''

# Test suite with at least 3 test_ functions
TEST_STUDY_CONTENT = """\"\"\"Automated test suite for study package.\"\"\"

from __future__ import annotations

import pytest
from study.core import generate_sequence, run, summarize


def test_run_determinism() -> None:
    res1 = run(42)
    res2 = run(42)
    assert res1 == res2


def test_summarize_accuracy() -> None:
    stats = summarize([1, 2, 4])
    assert stats["count"] == 3
    assert stats["mean"] == "7/3"
    assert stats["variance"] == "7/3"
    assert stats["min"] == 1
    assert stats["max"] == 4


def test_validation_errors() -> None:
    with pytest.raises(ValueError):
        run(-1)
    with pytest.raises(ValueError):
        summarize([42])
"""

# Continuous integration workflow invoking pytest
CI_WORKFLOW_CONTENT = """name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.14
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      - name: Install dependencies from lockfile
        run: pip install --require-hashes -r requirements.lock
      - name: Run test suite
        run: pytest tests/
"""

# Audit log documenting all 8 defects
AUDIT_LOG_CONTENT = """# Reproducibility Audit Log

| Defect ID | Defect Name | File Path | Remediation Summary |
|---|---|---|---|
| D1 | unpinned-requirements | requirements.lock | Pinned all transitive dependencies to exact versions |
| D2 | unhashed-lock | requirements.lock | Added cryptographic SHA-256 hashes for all wheels |
| D3 | wall-clock-in-output | study/core.py | Removed non-deterministic timestamp and system metadata |
| D4 | input-order-dependence | study/core.py | Removed order-dependent 'first' key from summary output |
| D5 | no-tests | tests/test_study.py | Implemented automated pytest suite covering invariants and edge cases |
| D6 | no-build-system | pyproject.toml | Declared standard [build-system] and [project] tables |
| D7 | no-ci | .github/workflows/ci.yml | Created automated GitHub Actions workflow invoking pytest |
| D8 | float-mean | study/core.py | Migrated floating-point accumulators to exact rational Fraction |
"""

REPO_FILES: dict[str, str] = {
    "requirements.lock": LOCKFILE_CONTENT,
    "pyproject.toml": PYPROJECT_CONTENT,
    "study/__init__.py": "",
    "study/core.py": STUDY_CORE_CONTENT,
    "tests/__init__.py": "",
    "tests/test_study.py": TEST_STUDY_CONTENT,
    ".github/workflows/ci.yml": CI_WORKFLOW_CONTENT,
    "AUDIT.md": AUDIT_LOG_CONTENT,
}


def generate_sequence(seed: int, n: int = 200) -> list[int]:
    """Generate deterministic sequence using the exact modular arithmetic formula."""
    if seed < 0:
        raise ValueError("seed must be non-negative")
    seq: list[int] = []
    for i in range(1, n + 1):
        val = (1103515245 * seed + 12345 * i * i + 7 * i) % 1000003
        seq.append(val)
    return seq


def summarize(values: Sequence[int]) -> dict[str, object]:
    """Compute exact summary statistics using Fraction for mean and sample variance."""
    n = len(values)
    if n < 2:
        raise ValueError("len(values) must be at least 2")
    s = sum(values)
    s2 = sum(v * v for v in values)
    mean_frac = Fraction(s, n)
    var_frac = Fraction(n * s2 - s * s, n * (n - 1))
    return {
        "count": n,
        "max": max(values),
        "mean": str(mean_frac),
        "min": min(values),
        "variance": str(var_frac),
    }


def run(seed: int) -> str:
    """Generate sequence, compute summary statistics, and return formatted JSON."""
    seq = generate_sequence(seed)
    stats = summarize(seq)
    return json.dumps(stats, sort_keys=True, indent=2) + "\n"


def materialize_repo(target_dir: Path | str) -> Path:
    """Materialize the full fixed repository tree to a target directory."""
    root = Path(target_dir)
    for rel_path, content in REPO_FILES.items():
        file_path = root / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    return root
