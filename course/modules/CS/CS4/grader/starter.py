"""CS4 Autograder Starter: Deliberately broken repository implementation.

This module represents the flawed baseline repository prior to remediation.
Contains defects D1 through D8:
- Unpinned dependencies and missing cryptographic hashes
- Missing [build-system] table in pyproject.toml
- Non-deterministic wall-clock timestamp in run()
- Order-dependent 'first' key in summarize()
- Missing automated test suite
- Missing CI workflow
- Floating-point arithmetic in summary statistics
"""

from __future__ import annotations

import datetime
import json
from collections.abc import Sequence
from pathlib import Path

# Defect D1 & D2: Unpinned requirements with no hashes
BROKEN_REQUIREMENTS = """# Broken unpinned requirements
pytest>=7.0.0
numpy
"""

# Defect D6: Missing [build-system] table
BROKEN_PYPROJECT = """[project]
name = "flawed-study"
version = "0.1.0"
requires-python = ">=3.14"
"""

# Defect D3, D4, D8: Broken core module
BROKEN_CORE = '''"""Broken study implementation."""

import datetime
import json


def run(seed: int) -> str:
    # Defect D3: Wall-clock timestamp injected into output
    return json.dumps({
        "timestamp": datetime.datetime.now().isoformat(),
        "seed": seed,
    })
'''

# Defect D7: CI workflow does not invoke pytest
BROKEN_CI = """name: Lint
on: [push]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Syntax check
        run: python -m compileall .
"""

BROKEN_REPO_FILES: dict[str, str] = {
    "requirements.lock": BROKEN_REQUIREMENTS,
    "pyproject.toml": BROKEN_PYPROJECT,
    "study/__init__.py": "",
    "study/core.py": BROKEN_CORE,
    ".github/workflows/ci.yml": BROKEN_CI,
    "AUDIT.md": "# Audit in progress\\n",
}


def generate_sequence(seed: int, n: int = 200) -> list[int]:
    """Flawed sequence generator without input validation."""
    return [(seed + i) for i in range(n)]


def summarize(values: Sequence[int]) -> dict[str, object]:
    """Flawed summary statistics with float arithmetic and order-dependent key."""
    # Defect D4: Order-dependent 'first' key
    # Defect D8: Float arithmetic
    n = len(values)
    mean_val = float(sum(values)) / n if n > 0 else 0.0
    var_val = float(sum((v - mean_val) ** 2 for v in values)) / n if n > 0 else 0.0
    return {
        "count": n,
        "first": values[0] if values else 0,
        "max": max(values) if values else 0,
        "mean": f"{mean_val:.4f}",
        "min": min(values) if values else 0,
        "variance": f"{var_val:.4f}",
    }


def run(seed: int) -> str:
    """Flawed run injecting wall-clock timestamp and float stats."""
    values = generate_sequence(seed)
    stats = summarize(values)
    payload = dict(stats)
    # Defect D3: Wall-clock timestamp
    payload["timestamp"] = datetime.datetime.now(datetime.UTC).isoformat()
    return json.dumps(payload, sort_keys=True, indent=2) + "\n"


def materialize_repo(target_dir: Path | str) -> Path:
    """Materialize the flawed repository tree."""
    root = Path(target_dir)
    for rel_path, content in BROKEN_REPO_FILES.items():
        file_path = root / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    return root
