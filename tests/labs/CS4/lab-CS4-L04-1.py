"""CS4 Lesson 4 Inline Lab 1: Modern Python packaging and pyproject.toml validation.

Demonstrates the structure and specification requirements of installable Python packages.
Uses the standard library tomllib module to parse pyproject.toml configuration strings.
Verifies the presence of required [build-system] and [project] tables and fields.
Tests validator behavior across valid and deliberately malformed package specifications.
"""

from __future__ import annotations

import tomllib
from typing import Any


def validate_pyproject_toml(toml_content: str) -> tuple[bool, list[str]]:
    """Validate a pyproject.toml configuration string against standard packaging rules."""
    errors: list[str] = []
    try:
        data = tomllib.loads(toml_content)
    except tomllib.TOMLDecodeError as err:
        return False, [f"Syntax error: {err}"]

    # 1. Validate [build-system]
    if "build-system" not in data or not isinstance(data["build-system"], dict):
        errors.append("Missing required table [build-system]")
    else:
        bs: dict[str, Any] = data["build-system"]
        if "requires" not in bs or not isinstance(bs["requires"], list) or not bs["requires"]:
            errors.append("[build-system] missing non-empty list 'requires'")
        if "build-backend" not in bs or not isinstance(bs["build-backend"], str) or not bs["build-backend"].strip():
            errors.append("[build-system] missing non-empty string 'build-backend'")

    # 2. Validate [project]
    if "project" not in data or not isinstance(data["project"], dict):
        errors.append("Missing required table [project]")
    else:
        proj: dict[str, Any] = data["project"]
        for required_field in ("name", "version", "requires-python"):
            if required_field not in proj or not str(proj[required_field]).strip():
                errors.append(f"[project] missing required field '{required_field}'")

    return len(errors) == 0, errors


def main() -> None:
    # 1. Valid package specification
    valid_toml = """[build-system]
requires = ["setuptools>=68.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "quant-research-core"
version = "1.0.0"
description = "Deterministic quantitative research library"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "numpy>=2.0.0",
]
"""

    # 2. Missing build-system table
    missing_build_sys = """[project]
name = "broken-package"
version = "0.1.0"
requires-python = ">=3.14"
"""

    # 3. Missing project name and version
    missing_fields = """[build-system]
requires = ["flit_core>=3.9.0"]
build-backend = "flit_core.buildapi"

[project]
requires-python = ">=3.14"
"""

    print("Python packaging pyproject.toml validation suite:")

    ok1, errs1 = validate_pyproject_toml(valid_toml)
    print(f"Case 1 (Valid package): {'PASS' if ok1 else 'FAIL'}")
    if errs1:
        for e in errs1:
            print(f"  Error: {e}")

    ok2, errs2 = validate_pyproject_toml(missing_build_sys)
    print(f"\nCase 2 (Missing [build-system]): {'PASS' if ok2 else 'FAIL (caught expected defect)'}")
    for e in errs2:
        print(f"  Reported: {e}")

    ok3, errs3 = validate_pyproject_toml(missing_fields)
    print(f"\nCase 3 (Missing [project] name/version): {'PASS' if ok3 else 'FAIL (caught expected defect)'}")
    for e in errs3:
        print(f"  Reported: {e}")

    print("\nPackaging specification checks completed successfully.")


main()
