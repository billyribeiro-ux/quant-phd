"""Lab CAP3-L05-2: Multi-Field Qualifying Examination Comprehensive Diagnostic.

Executes a joint multi-field mock prelim evaluation across Asset Pricing,
Econometrics, and Macro/Monetary Economics.
"""

from __future__ import annotations

from typing import Any


def main() -> None:
    # Summary results across the three mock field prelims
    prelim_results: list[dict[str, Any]] = [
        {"field": "Asset Pricing (AP)", "weight": 0.35, "proof_score": 92.0, "empirical_score": 88.0},
        {"field": "Econometrics (EC)", "weight": 0.35, "proof_score": 86.0, "empirical_score": 90.0},
        {"field": "Macro & Monetary (MM)", "weight": 0.30, "proof_score": 85.0, "empirical_score": 84.0},
    ]

    print("--- Doctoral Qualifying Examination Multi-Field Synthesis ---")
    composite_score = 0.0
    all_fields_passed = True

    for item in prelim_results:
        f_score = 0.5 * (item["proof_score"] + item["empirical_score"])
        field_pass = f_score >= 80.0
        if not field_pass:
            all_fields_passed = False
        weighted = f_score * item["weight"]
        composite_score += weighted
        status = "PASS" if field_pass else "FAIL"
        print(
            f"{item['field']}: Proof={item['proof_score']:.1f}, Empirical={item['empirical_score']:.1f} -> "
            f"Mean={f_score:.1f}% (Weight={item['weight']:.2f}) [{status}]"
        )

    verdict = "QUALIFIED PASS (ALL FIELDS)" if (all_fields_passed and composite_score >= 80.0) else "RETAKE REQUIRED"
    print(f"Overall Composite Qualifying Score: {composite_score:.2f}% -> Verdict: {verdict}")


main()
