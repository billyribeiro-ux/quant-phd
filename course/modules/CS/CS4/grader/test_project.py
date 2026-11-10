"""Pytest test suite for CS4 Reproducibility Audit capstone project.

Validates the full reproducibility audit across repository structure, packaging,
dependency pinning, determinism, test suites, and CI workflows.
"""

from __future__ import annotations

import ast
import os
import random
import re
import tomllib
from pathlib import Path
from typing import Any

import pytest

# Dynamic import: support Pyodide / single-file grader runner / local development
try:
    from repro_audit import materialize_repo, run, summarize  # type: ignore[import-not-found]
except ImportError:
    try:
        from reference import materialize_repo, run, summarize  # type: ignore[import-not-found]
    except ImportError:
        from starter import materialize_repo, run, summarize  # type: ignore[import-not-found]

from instance import make_instance  # type: ignore[import-not-found]


@pytest.fixture(scope="module")
def current_seed() -> int:
    """Read the workspace seed passed via QF_SEED environment variable."""
    return int(os.environ.get("QF_SEED", "0"))


@pytest.fixture(scope="module")
def repo_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Materialize the candidate repository once for the test module."""
    root = tmp_path_factory.mktemp("candidate_repo")
    materialize_repo(root)
    return root


def test_lock_pins_every_requirement_exactly(repo_root: Path) -> None:
    """T1: requirements.lock must pin exact versions with cryptographic sha256 hashes."""
    lock_file = repo_root / "requirements.lock"
    assert lock_file.is_file(), "requirements.lock is missing from repository root"

    lines = [line.strip() for line in lock_file.read_text(encoding="utf-8").splitlines()]
    meaningful_lines = [line for line in lines if line and not line.startswith("#")]
    assert len(meaningful_lines) > 0, "requirements.lock contains no dependency specifications"

    for line in meaningful_lines:
        parts = line.split()
        spec = parts[0]
        hashes = [p for p in parts[1:] if p.startswith("--hash=sha256:")]

        assert "==" in spec, f"Dependency '{spec}' is not pinned to an exact version (use '==')"
        assert not any(op in spec for op in (">=", "<=", "~=", ">", "<", "!=", "^")), (
            f"Dependency '{spec}' contains unpinned comparison operators"
        )
        assert len(hashes) >= 1, f"Dependency '{spec}' lacks required '--hash=sha256:' integrity digests"
        for h in hashes:
            digest = h.removeprefix("--hash=sha256:")
            assert re.fullmatch(r"[a-fA-F0-9]{64}", digest), f"Invalid sha256 hex digest: '{digest}'"


def test_pyproject_declares_build_system_and_project(repo_root: Path) -> None:
    """T2: pyproject.toml must declare standard [build-system] and [project] metadata."""
    pyproject_file = repo_root / "pyproject.toml"
    assert pyproject_file.is_file(), "pyproject.toml is missing from repository root"

    data = tomllib.loads(pyproject_file.read_text(encoding="utf-8"))
    assert "build-system" in data, "pyproject.toml is missing required [build-system] table"

    bs: dict[str, Any] = data["build-system"]
    assert "requires" in bs and isinstance(bs["requires"], list) and len(bs["requires"]) > 0, (
        "[build-system] must specify non-empty 'requires' list"
    )
    assert "build-backend" in bs and isinstance(bs["build-backend"], str) and bs["build-backend"].strip(), (
        "[build-system] must specify non-empty string 'build-backend'"
    )

    assert "project" in data, "pyproject.toml is missing required [project] table"
    proj: dict[str, Any] = data["project"]
    for key in ("name", "version", "requires-python"):
        assert key in proj and str(proj[key]).strip(), f"[project] table missing required field '{key}'"


def test_ci_runs_pytest(repo_root: Path) -> None:
    """T3: Continuous integration workflow must execute pytest in a run step."""
    workflow_dir = repo_root / ".github" / "workflows"
    assert workflow_dir.is_dir(), ".github/workflows/ directory is missing"

    yaml_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    assert len(yaml_files) > 0, "No CI workflow YAML files found in .github/workflows/"

    found_pytest = False
    for wf in yaml_files:
        content = wf.read_text(encoding="utf-8")
        for line in content.splitlines():
            line_str = line.strip()
            if "run:" in line_str and "pytest" in line_str:
                found_pytest = True
                break
        if found_pytest:
            break

    assert found_pytest, "No CI workflow contains a 'run:' step invoking 'pytest'"


def test_tests_exist(repo_root: Path) -> None:
    """T4: tests/ directory must contain test files with at least 3 test functions."""
    tests_dir = repo_root / "tests"
    assert tests_dir.is_dir(), "tests/ directory is missing"

    test_files = list(tests_dir.glob("test_*.py"))
    assert len(test_files) > 0, "tests/ contains no test_*.py files"

    test_fn_count = 0
    for tf in test_files:
        tree = ast.parse(tf.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                test_fn_count += 1

    assert test_fn_count >= 3, f"Expected at least 3 test functions, found {test_fn_count}"


def test_run_matches_exact_text_seeds(current_seed: int) -> None:
    """T5: run(seed) must match the exact expected output text byte-for-byte."""
    inst = make_instance(current_seed)
    actual_output = run(current_seed)
    expected_output = str(inst["expected"])
    assert actual_output == expected_output, "run(seed) output does not match expected canonical JSON"


def test_two_runs_identical(current_seed: int) -> None:
    """T6: Two consecutive runs with the same seed must produce identical output."""
    out1 = run(current_seed)
    out2 = run(current_seed)
    assert out1 == out2, "run(seed) is non-deterministic between consecutive calls"


def test_summarize_is_order_invariant(current_seed: int) -> None:
    """T7: summarize(values) must be completely invariant to input sequence permutation."""
    inst = make_instance(current_seed)
    raw_seq = [int(v) for v in str(inst["sequence"]).split(",")]

    stats1 = summarize(raw_seq)

    # Permute sequence deterministically
    permuted = list(raw_seq)
    random.Random(current_seed + 101).shuffle(permuted)
    stats2 = summarize(permuted)

    assert stats1 == stats2, "summarize() output depends on input ordering"
    assert "first" not in stats1, "summarize() output contains order-dependent key 'first'"


def test_sample_variance_hand_example() -> None:
    """T8: Verify sample variance formula using hand-calculable test vector [1, 2, 4]."""
    # Vector: [1, 2, 4]. Mean = 7/3.
    # Deviations: (1 - 7/3) = -4/3, squared = 16/9.
    #             (2 - 7/3) = -1/3, squared = 1/9.
    #             (4 - 7/3) = 5/3,  squared = 25/9.
    # Sum of squared deviations: (16 + 1 + 25) / 9 = 42/9 = 14/3.
    # Sample variance: (14/3) / (3 - 1) = (14/3) / 2 = 7/3.
    # (Population variance would incorrectly be (14/3) / 3 = 14/9).
    stats = summarize([1, 2, 4])
    assert stats["count"] == 3
    assert stats["mean"] == "7/3"
    assert stats["variance"] == "7/3"
    assert stats["min"] == 1
    assert stats["max"] == 4


def test_seeds_give_materially_different_sequences() -> None:
    """T9: Seeds must yield distinct sequences (guards against seed integer truncation)."""
    out0 = run(0)
    out1 = run(1)
    out2 = run(2)
    assert out0 != out1, "Seeds 0 and 1 produced identical output"
    assert out1 != out2, "Seeds 1 and 2 produced identical output"
    assert out0 != out2, "Seeds 0 and 2 produced identical output"


def test_summarize_rejects_fewer_than_two_values() -> None:
    """T10: summarize() raises ValueError on < 2 values; accepts exactly 2 values."""
    with pytest.raises(ValueError):
        summarize([42])
    with pytest.raises(ValueError):
        summarize([])

    # Exactly 2 values must succeed
    res = summarize([10, 20])
    assert res["count"] == 2
    assert res["mean"] == "15"
    assert res["variance"] == "50"


def test_run_rejects_negative_seed() -> None:
    """T11: run() raises ValueError on negative seed; accepts seed 0."""
    with pytest.raises(ValueError):
        run(-1)
    with pytest.raises(ValueError):
        run(-100)

    # Seed 0 must succeed
    res = run(0)
    assert isinstance(res, str) and len(res) > 0


def test_audit_log_names_every_defect(repo_root: Path) -> None:
    """T12: AUDIT.md must contain an entry for each defect D1-D8 naming an existing file path."""
    audit_file = repo_root / "AUDIT.md"
    assert audit_file.is_file(), "AUDIT.md is missing from repository root"

    audit_text = audit_file.read_text(encoding="utf-8")
    for d_num in range(1, 9):
        defect_id = f"D{d_num}"
        found_line = None
        for line in audit_text.splitlines():
            if defect_id in line:
                found_line = line
                break

        assert found_line is not None, f"AUDIT.md does not document defect {defect_id}"

        # Check that the line references an actual path that exists in the repo
        words = re.findall(r"[A-Za-z0-9_\-\.\/]+", found_line)
        valid_paths = [w for w in words if (repo_root / w).exists() and not (repo_root / w).is_dir()]
        assert len(valid_paths) > 0, (
            f"AUDIT.md row for {defect_id} does not reference an existing repository file: '{found_line}'"
        )
