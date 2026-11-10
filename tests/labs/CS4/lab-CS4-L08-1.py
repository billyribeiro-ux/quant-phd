"""CS4 Lesson 8 Inline Lab 1: Continuous integration pipeline gating and early-exit semantics.

Demonstrates continuous integration pipeline architectures and sequential verification gates.
Executes an automated verification pipeline comprising formatting, typing, unit testing,
and regression checks with deterministic early-exit semantics on failure.
Compares pipeline behavior and diagnostic reporting across clean and defective branch states.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import NamedTuple


class PipelineStep(NamedTuple):
    name: str
    check: Callable[[], tuple[bool, str]]


def run_pipeline(steps: list[PipelineStep]) -> tuple[bool, list[str]]:
    """Execute pipeline steps sequentially; halt execution immediately on first failure."""
    logs: list[str] = []
    for step in steps:
        passed, msg = step.check()
        if passed:
            logs.append(f"  Step [{step.name}]: PASS - {msg}")
        else:
            logs.append(f"  Step [{step.name}]: FAIL - {msg}")
            logs.append(f"Pipeline halted early: '{step.name}' failed. Subsequent steps skipped.")
            return False, logs
    logs.append("All pipeline gates passed successfully.")
    return True, logs


def main() -> None:
    print("Continuous integration pipeline gate evaluation:")

    # Clean branch checks
    clean_steps: list[PipelineStep] = [
        PipelineStep("format-check", lambda: (True, "Ruff formatting verified")),
        PipelineStep("type-check", lambda: (True, "Mypy strict passed 0 errors")),
        PipelineStep("unit-tests", lambda: (True, "Pytest 42 passed in 0.12s")),
        PipelineStep("regression-tests", lambda: (True, "Golden outputs match 100%")),
    ]

    print("\nExecuting CI pipeline on clean feature branch:")
    clean_ok, clean_logs = run_pipeline(clean_steps)
    for log in clean_logs:
        print(log)
    print(f"Clean branch CI pipeline verdict: {'SUCCESS' if clean_ok else 'FAILED'}")

    # Defective branch checks (typing failure at step 2)
    defective_steps: list[PipelineStep] = [
        PipelineStep("format-check", lambda: (True, "Ruff formatting verified")),
        PipelineStep("type-check", lambda: (False, "Incompatible return type 'float' expected 'Fraction'")),
        PipelineStep("unit-tests", lambda: (True, "Pytest 42 passed")),
        PipelineStep("regression-tests", lambda: (True, "Golden outputs match")),
    ]

    print("\nExecuting CI pipeline on defective feature branch:")
    defective_ok, defective_logs = run_pipeline(defective_steps)
    for log in defective_logs:
        print(log)
    print(f"Defective branch CI pipeline verdict: {'SUCCESS' if defective_ok else 'FAILED'}")

    print("\nConclusion: CI gates protect branch integrity by blocking unverified changes.")


main()
