"""Lab 1 (L01): Placement diagnostic testing, mastery thresholds, and test-out recommendation engine.

Standard library only. Simulates a diagnostic placement examination across curriculum foundation
modules. Evaluates student item responses under a logistic item-response model, computes diagnostic
mastery scores against candidate mastery thresholds theta in [0.60, 0.90], analyzes Type I (false-pass)
and Type II (false-fail) classification errors, and generates an automated test-out recommendation
path across the curriculum prerequisite DAG.
"""

from __future__ import annotations

import math
import random

# Synthetic foundation modules available for placement testing
MODULES: list[str] = ["P0.1", "M1", "M2", "CS1"]

# Prerequisites within the diagnostic subset
PREREQS: dict[str, list[str]] = {
    "P0.1": [],
    "M1": ["P0.1"],
    "M2": ["M1"],
    "CS1": ["P0.1"],
}

# Number of diagnostic items per module
ITEMS_PER_MODULE: int = 10

# True competence threshold on latent ability scale (theta >= 1.0 implies mastery)
TRUE_MASTERY_ABILITY: float = 1.0


def simulate_item_difficulties(seed: int) -> dict[str, list[float]]:
    """Generate fixed item difficulties for each module diagnostic."""
    rng = random.Random(seed)
    difficulties: dict[str, list[float]] = {}
    for mod in MODULES:
        # Items range from easy (b = -0.5) to discriminating (b = 1.5)
        difficulties[mod] = [round(rng.uniform(-0.5, 1.5), 2) for _ in range(ITEMS_PER_MODULE)]
    return difficulties


def rasch_probability(ability: float, difficulty: float) -> float:
    """Logistic item response probability P(correct | theta, b)."""
    return 1.0 / (1.0 + math.exp(-(ability - difficulty)))


def simulate_student_test(
    abilities: dict[str, float],
    difficulties: dict[str, list[float]],
    rng: random.Random,
) -> dict[str, float]:
    """Simulate item responses and compute fraction of correct answers per module."""
    scores: dict[str, float] = {}
    for mod in MODULES:
        theta = abilities[mod]
        correct = 0
        for b in difficulties[mod]:
            prob = rasch_probability(theta, b)
            if rng.random() < prob:
                correct += 1
        scores[mod] = correct / ITEMS_PER_MODULE
    return scores


def evaluate_cohort(
    difficulties: dict[str, list[float]],
    n_students: int = 500,
    seed: int = 42,
) -> dict[float, tuple[float, float]]:
    """Evaluate Type I (false-pass) and Type II (false-fail) rates across candidate mastery thresholds."""
    rng = random.Random(seed)
    thresholds: list[float] = [0.60, 0.70, 0.80, 0.85, 0.90]
    results: dict[float, tuple[float, float]] = {}

    # Pre-generate student latent abilities: mixture of novices (theta ~ N(0, 0.5)) and experts (theta ~ N(1.8, 0.5))
    students: list[dict[str, float]] = []
    for _ in range(n_students):
        # 40% are competent in a given module, 60% are novices
        student_ability = {}
        for mod in MODULES:
            if rng.random() < 0.40:
                student_ability[mod] = rng.gauss(1.8, 0.4)
            else:
                student_ability[mod] = rng.gauss(0.0, 0.5)
        students.append(student_ability)

    for thresh in thresholds:
        false_passes = 0
        false_fails = 0
        total_incompetent = 0
        total_competent = 0

        # Reset RNG seed for identical response draws per threshold
        eval_rng = random.Random(seed + 100)
        for abilities in students:
            scores = simulate_student_test(abilities, difficulties, eval_rng)
            for mod in MODULES:
                true_competent = abilities[mod] >= TRUE_MASTERY_ABILITY
                passed = scores[mod] >= thresh

                if true_competent:
                    total_competent += 1
                    if not passed:
                        false_fails += 1
                else:
                    total_incompetent += 1
                    if passed:
                        false_passes += 1

        fp_rate = false_passes / total_incompetent if total_incompetent > 0 else 0.0
        ff_rate = false_fails / total_competent if total_competent > 0 else 0.0
        results[thresh] = (fp_rate, ff_rate)

    return results


def recommend_learning_path(
    scores: dict[str, float],
    mastery_threshold: float = 0.80,
) -> tuple[list[str], list[str]]:
    """Determine unlocked exemptions and required modules enforcing prerequisite DAG constraints."""
    exemptions: list[str] = []
    required: list[str] = []

    for mod in MODULES:
        score = scores[mod]
        prereqs_satisfied = all(p in exemptions for p in PREREQS[mod])
        if score >= mastery_threshold and prereqs_satisfied:
            exemptions.append(mod)
        else:
            required.append(mod)

    return exemptions, required


def main() -> None:
    print("SIMULATED Diagnostic Placement & Mastery Gating Evaluation")
    print(f"Foundation modules evaluated: {MODULES}")
    print(f"Items per module diagnostic: {ITEMS_PER_MODULE}")

    seed = 42
    difficulties = simulate_item_difficulties(seed)

    print("\n--- Cohort Error Rates by Mastery Threshold (N = 500 learners) ---")
    error_rates = evaluate_cohort(difficulties, n_students=500, seed=seed)
    print(f"{'Threshold':>10} | {'False-Pass (Type I)':>20} | {'False-Fail (Type II)':>20} | {'Joint Risk':>12}")
    print("-" * 72)
    for thresh, (fp, ff) in error_rates.items():
        # False-pass penalty is weighted 3x higher because premature advancement breaks downstream prerequisites
        risk = 3.0 * fp + 1.0 * ff
        print(f"{thresh:10.2f} | {fp:20.4f} | {ff:20.4f} | {risk:12.4f}")

    print("\n--- Illustrative Student Placement Diagnostic ---")
    # Illustrative incoming learner: strong in linear algebra and coding, novice in multivariable calculus
    student_profile: dict[str, float] = {
        "P0.1": 2.2,  # Fluent in methodology
        "M1": 2.0,  # Fluent in linear algebra
        "M2": 0.2,  # Novice in vector calculus
        "CS1": 1.9,  # Fluent in Python systems
    }

    test_rng = random.Random(123)
    student_scores = simulate_student_test(student_profile, difficulties, test_rng)

    print("Student Diagnostic Test Results:")
    for mod in MODULES:
        score = student_scores[mod]
        latent = student_profile[mod]
        print(f"  Module {mod:>4}: Score = {score:.1%} (True ability theta = {latent:+.2f})")

    exempt, req = recommend_learning_path(student_scores, mastery_threshold=0.80)
    print("\nMastery threshold applied: 80.0%")
    print(f"Test-out exemptions granted: {exempt}")
    print(f"Required study sequence:     {req}")


main()
