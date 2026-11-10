"""CS4 Lesson 2 Inline Lab 1: Golden-master regression testing for quantitative models.

Demonstrates the transformation of unit tests into regression tests by pinning exact golden outputs.
Evaluates a deterministic quantitative risk engine against a recorded baseline fixture.
Injects a deliberate formula regression (population divisor n instead of sample divisor n - 1)
and verifies that the regression assertion catches the defect with an explicit diff.

Data: SIMULATED fixed return series generated with a deterministic pseudo-random seed.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from fractions import Fraction


def compute_portfolio_metrics(returns: Sequence[int | Fraction]) -> dict[str, str]:
    """Compute exact mean and sample variance as reduced fractions, formatted deterministically."""
    n = len(returns)
    if n < 2:
        raise ValueError("At least 2 return observations required")

    total = sum(returns)
    mean_val = Fraction(total, n)

    # Sample variance: sum((x - mean)^2) / (n - 1)
    sum_sq = sum(r * r for r in returns)
    var_val = Fraction(n * sum_sq - total * total, n * (n - 1))

    return {
        "count": str(n),
        "mean": str(mean_val),
        "variance": str(var_val),
    }


def compute_portfolio_metrics_mutant(returns: Sequence[int | Fraction]) -> dict[str, str]:
    """Deliberate bug mutation: uses population variance (divisor n) instead of sample variance (n - 1)."""
    n = len(returns)
    if n < 2:
        raise ValueError("At least 2 return observations required")

    total = sum(returns)
    mean_val = Fraction(total, n)

    # Defect: dividing by n instead of (n - 1)
    sum_sq = sum(r * r for r in returns)
    var_val = Fraction(n * sum_sq - total * total, n * n)

    return {
        "count": str(n),
        "mean": str(mean_val),
        "variance": str(var_val),
    }


def serialize_golden(metrics: dict[str, str]) -> str:
    """Canonical deterministic JSON serialization."""
    return json.dumps(metrics, sort_keys=True, indent=2)


def main() -> None:
    # Deterministic SIMULATED fixed input fixture (returns expressed in basis points: 10, 25, -15, 30, 0)
    fixture_returns: list[int] = [10, 25, -15, 30, 0]

    # Baseline run
    baseline_metrics = compute_portfolio_metrics(fixture_returns)
    golden_master = serialize_golden(baseline_metrics)

    print("SIMULATED quantitative model regression test:")
    print("Golden master baseline recorded:")
    for line in golden_master.splitlines():
        print(f"  {line}")

    # 1. Verify that current reference matches golden master
    current_metrics = compute_portfolio_metrics(fixture_returns)
    current_output = serialize_golden(current_metrics)
    baseline_passed = current_output == golden_master
    print(f"\nBaseline regression test against golden master: {'PASS' if baseline_passed else 'FAIL'}")

    # 2. Inject deliberate formula mutation
    mutant_metrics = compute_portfolio_metrics_mutant(fixture_returns)
    mutant_output = serialize_golden(mutant_metrics)

    print("\nInjected code mutation: sample variance divisor changed from (n - 1) to n.")
    mutant_passed = mutant_output == golden_master
    print(f"Mutant evaluation against golden master: {'PASS' if mutant_passed else 'FAIL (regression caught)'}")

    if not mutant_passed:
        print("Diff analysis:")
        print(f"  Expected variance: {baseline_metrics['variance']}")
        print(f"  Actual variance:   {mutant_metrics['variance']}")
        print("Regression test successfully prevented defect from reaching production.")


main()
