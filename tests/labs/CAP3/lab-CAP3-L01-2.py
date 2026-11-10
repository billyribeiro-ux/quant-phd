"""Lab CAP3-L01-2: Mock Prelim Automated Timing & Scoring Engine.

Simulates a doctoral prelim submission pipeline, checking mathematical proof steps,
numerical tolerance validation, and score aggregation across parts.
"""

from __future__ import annotations

from typing import Any


def evaluate_exam_step(
    candidate_answer: float,
    true_solution: float,
    tolerance: float = 1e-4,
    points_possible: float = 10.0,
) -> tuple[float, str]:
    error = abs(candidate_answer - true_solution)
    if error <= tolerance:
        return points_possible, f"PASS (error = {error:.2e} <= {tolerance:.2e})"
    partial = max(0.0, points_possible * (1.0 - min(1.0, error / (10.0 * tolerance))))
    return partial, f"FAIL (error = {error:.2e} > {tolerance:.2e})"


def main() -> None:
    exam_sections: list[dict[str, Any]] = [
        {"name": "Part A: SDF Variance Bound", "candidate": 0.4815, "truth": 0.48152, "tol": 1e-3, "points": 25.0},
        {"name": "Part B: Merton Fraction", "candidate": 0.5208, "truth": 0.52083, "tol": 1e-4, "points": 25.0},
        {"name": "Part C: Shanken Standard Error", "candidate": 0.0142, "truth": 0.01425, "tol": 1e-4, "points": 25.0},
        {
            "name": "Part D: Taylor Determinacy Metric",
            "candidate": 1.5833,
            "truth": 1.58333,
            "tol": 1e-4,
            "points": 25.0,
        },
    ]

    total_score = 0.0
    max_possible = 0.0

    print("--- Doctoral Prelim Mock Assessment ---")
    for sec in exam_sections:
        score, msg = evaluate_exam_step(sec["candidate"], sec["truth"], sec["tol"], sec["points"])
        total_score += score
        max_possible += sec["points"]
        print(f"{sec['name']}: {score:.1f}/{sec['points']:.1f} pts | {msg}")

    pct = (total_score / max_possible) * 100.0
    status = "QUALIFIED PASS" if pct >= 80.0 else "RETAKE REQUIRED"
    print(f"Final Aggregated Score: {total_score:.1f} / {max_possible:.1f} ({pct:.1f}%) -> {status}")


main()
